from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
from pathlib import Path
from urllib.parse import urlparse, parse_qs, quote, unquote
import json, re, io, os

try:
    import requests
    from bs4 import BeautifulSoup
    from pypdf import PdfReader
except Exception as e:
    print("Dependencia opcional no disponible:", e)

ROOT = Path(__file__).resolve().parent
SEED = json.loads((ROOT/'catalog_seed.json').read_text(encoding='utf-8')) if (ROOT/'catalog_seed.json').exists() else []
EPLAN = json.loads((ROOT/'eplan_catalog.json').read_text(encoding='utf-8')) if (ROOT/'eplan_catalog.json').exists() else []

MANUFACTURER_DOMAINS = {
    'balluff':['balluff.com'], 'ifm':['ifm.com'], 'ifm electronic':['ifm.com'],
    'siemens':['siemens.com'], 'festo':['festo.com'], 'pilz':['pilz.com'],
    'phoenix contact':['phoenixcontact.com'], 'sick':['sick.com'],
    'schneider':['se.com','schneider-electric.com'], 'schneider electric':['se.com','schneider-electric.com'],
    'omron':['omron.eu','automation.omron.com'], 'sew':['sew-eurodrive.com'],
    'abb':['abb.com'], 'lovato':['lovatoelectric.com'], 'lovato electric':['lovatoelectric.com'],
    'circutor':['circutor.com'], 'eaton':['eaton.com'], 'allen-bradley':['rockwellautomation.com'],
    'allen bradley':['rockwellautomation.com'], 'a-b':['rockwellautomation.com'], 'rockwell':['rockwellautomation.com'],
    'chint':['chintglobal.com'], 'legrand':['legrand.com'], 'ide':['ide.es']
}
REPUTABLE = ['rs-online.com','tme.eu','mouser.com','digikey.com','farnell.com','newark.com']
UA = {'User-Agent':'Mozilla/5.0 (ElectricalEngineeringCatalog/0.7; technical-documentation-check)'}

S210_PROTECTION_URL = 'https://cache.industry.siemens.com/dl/files/356/109815356/att_1354258/v1/Protective_Devices_S210_0126_A5E52740053A_AB.pdf'
S210_OPERATING_URL = 'https://support.industry.siemens.com/cs/attachments/109827474/S210_S-1FK2_S-1FT2_op_instr_0424_es-ES.pdf'
S210_RULES = [
    {'match':'6SL5310-1BE10-4DF','kw':.4,'inputA':1.6,'msp':{'a':3.2,'ref':'3RV2011-1DA..'},'cb':{'a':3,'ref':'5SY7303-7','curve':'C'}},
    {'match':'6SL5310-1BE10-8DF','kw':.75,'inputA':2.8,'msp':{'a':5,'ref':'3RV2011-1FA..'},'cb':{'a':6,'ref':'5SY7306-7','curve':'C'}},
    {'match':'6SL5310-1BE11-0DF','kw':1,'inputA':3.8,'msp':{'a':8,'ref':'3RV2011-1HA..'},'cb':{'a':8,'ref':'5SY7308-7','curve':'C'}},
    {'match':'6SL5310-1BE11-5DF','kw':1.5,'inputA':6,'msp':{'a':10,'ref':'3RV2011-1JA..'},'cb':{'a':10,'ref':'5SY7310-7','curve':'C'}},
    {'match':'6SL5310-1BE12-0DF','kw':2,'inputA':7.5,'msp':{'a':16,'ref':'3RV2011-4AA..'},'cb':{'a':16,'ref':'5SY7316-7','curve':'C'}},
    {'match':'6SL5310-1BE13-5DF','kw':3.5,'inputA':12.5,'msp':{'a':25,'ref':'3RV2021-4DA..'},'cb':{'a':25,'ref':'5SY7325-7','curve':'C'}},
    {'match':'6SL5310-1BE15-0DF','kw':5,'inputA':15,'msp':{'a':28,'ref':'3RV2021-4NA..'},'cb':{'a':32,'ref':'5SY7332-7','curve':'C'}},
    {'match':'6SL5310-1BE17-0DF','kw':7,'inputA':17.9,'msp':{'a':32,'ref':'3RV2021-4EA..'},'cb':{'a':32,'ref':'5SY7332-7','curve':'C'}},
]

def clean(s):
    return re.sub(r'\s+',' ', str(s or '')).strip()

def clean_ref(s):
    s = clean(s).upper()
    # EPLAN internal prefix (SIE., ABB., etc.) is not part of the manufacturer order number
    if '.' in s and not s.startswith(('3RV','5SY','6SL','1S','2C','P1R','P17')):
        s = s.split('.',1)[1]
    return re.sub(r'\s+','',s)

def manufacturer_domains(manufacturer):
    m = clean(manufacturer).lower()
    direct = MANUFACTURER_DOMAINS.get(m, [])
    if direct: return direct
    for k,v in MANUFACTURER_DOMAINS.items():
        if k in m or m in k: return v
    return []

def eplan_exact(reference, manufacturer=''):
    ref = clean_ref(reference)
    m = clean(manufacturer).lower()
    hits=[]
    for a in EPLAN:
        ar = clean_ref(a.get('order') or a.get('id'))
        if ar != ref: continue
        am = clean(a.get('manufacturer')).lower()
        score = 2 if m and (m in am or am in m) else 1
        hits.append((score,a))
    return max(hits,key=lambda x:x[0])[1] if hits else None

def eplan_pattern(pattern, category='', manufacturer=''):
    p = clean_ref(pattern).replace('..','').rstrip('*')
    m = clean(manufacturer).lower()
    rows=[]
    for a in EPLAN:
        if category and a.get('category') != category: continue
        if m:
            am=clean(a.get('manufacturer')).lower()
            if not (m in am or am in m): continue
        if clean_ref(a.get('order') or a.get('id')).startswith(p): rows.append(a)
    return rows[:25]

def s210_rule(reference):
    u=clean_ref(reference)
    return next((r for r in S210_RULES if r['match'] in u), None)

def extract(text):
    t=clean(text); d={}
    m=re.search(r'(?:operating voltage|supply voltage|tensi[oó]n(?: de servicio| de alimentaci[oó]n)?)[^\d]{0,30}(\d+(?:[.,]\d+)?)\s*(?:\.\.\.|→|[-–])\s*(\d+(?:[.,]\d+)?)\s*V\s*(DC|dc|VDC|AC|ac)?',t,re.I)
    if m:
        d['voltage']=f"{m.group(1)}...{m.group(2)} V{(' '+m.group(3).upper()) if m.group(3) else ''}"
    currents=[]
    for pat in [r'(?:no-load current|current consumption|consumo de corriente)[^\d]{0,35}(?:<|≤|max\.?|:)?\s*(\d+(?:[.,]\d+)?)\s*mA']:
        currents += [float(x.replace(',','.')) for x in re.findall(pat,t,re.I)]
    if currents:
        d['currentA']=max(currents)/1000; d['currentLabel']=f"≤ {max(currents):g} mA (extraído)"
    mi=re.search(r'(?:rated input current|input current|corriente (?:nominal )?de entrada)[^\d]{0,45}(\d+(?:[.,]\d+)?)\s*A\b',t,re.I)
    if mi: d['inputCurrentA']=float(mi.group(1).replace(',','.'))
    mo=re.search(r'(?:rated output current|output current|corriente (?:nominal )?de salida)[^\d]{0,45}(\d+(?:[.,]\d+)?)\s*A\b',t,re.I)
    if mo: d['outputCurrentA']=float(mo.group(1).replace(',','.'))
    m=re.search(r'((?:M8|M12|M08|M23)x?1?[^.;]{0,60}?(?:3|4|5|8)[ -]?(?:pin|pole|polos|poles|polo))',t,re.I)
    if m: d['connection']=clean(m.group(1))
    m=re.search(r'\b(PNP|NPN)\b[^.;]{0,50}\b(normally open|normally closed|NO|NC|NA|NF)(?:/|\s)*(NC|NO)?',t,re.I)
    if m: d['output']=clean(' '.join(x for x in m.groups() if x))
    m=re.search(r'\bIP\s?(6[56789]|[0-9]{2})\b',t,re.I)
    if m: d['ip']='IP'+m.group(1)
    return d

def extract_power_constraints(text):
    """Heuristic extraction. Results stay 'pending' unless a known rule validates them."""
    t=clean(text); d={'protections':[],'rcd':{},'warnings':[]}
    # Common IEC device references
    refs=list(dict.fromkeys(re.findall(r'\b(?:3RV\d{4}-[A-Z0-9.\-]+|5SY\d{4}-\d|5SL\d{4}-\d|[A-Z0-9]{2,}-[A-Z0-9\-]{4,})\b',t,re.I)))
    for ref in refs[:12]: d['protections'].append({'reference':ref.upper()})
    # RCD type and residual current
    mt=re.search(r'(?:RCCB|RCD|differential|diferencial)[^.;]{0,150}\btype\s*([A-FB]+)\b',t,re.I)
    if not mt: mt=re.search(r'\btipo\s*([ABF])\b[^.;]{0,120}(?:RCCB|RCD|diferencial)',t,re.I)
    if mt: d['rcd']['type']=mt.group(1).upper()
    mm=re.search(r'(?:residual current|corriente diferencial|rated residual current)[^\d]{0,50}(\d{2,4})\s*mA',t,re.I)
    if mm: d['rcd']['sensitivitymA']=int(mm.group(1))
    if re.search(r'(short[- ]time delayed|short delay|super[- ]?resistant|retardo breve|superresistente)',t,re.I): d['rcd']['shortDelay']=True
    # Circuit-breaker curve phrases
    mc=re.search(r'(?:characteristic|curve|curva)\s*([BCD KZ])\b',t,re.I)
    if mc: d['curve']=mc.group(1).strip().upper()
    return d

def decode_ddg(href):
    # DuckDuckGo HTML results may wrap the target in uddg=
    try:
        q=parse_qs(urlparse(href).query)
        if 'uddg' in q: return unquote(q['uddg'][0])
    except Exception: pass
    if href.startswith('//'): return 'https:'+href
    return href

def search_web(manufacturer, reference, extra='datasheet manual'):
    q=quote(f'"{manufacturer}" "{reference}" {extra}')
    url='https://html.duckduckgo.com/html/?q='+q
    r=requests.get(url,headers=UA,timeout=12); r.raise_for_status(); soup=BeautifulSoup(r.text,'html.parser')
    links=[]
    for a in soup.select('.result__a')[:14]:
        href=decode_ddg(a.get('href',''))
        if href: links.append(href)
    domains=manufacturer_domains(manufacturer)
    def score(u):
        h=urlparse(u).netloc.lower()
        if any(d in h for d in domains): return 100
        if any(d in h for d in REPUTABLE): return 60
        return 10
    return sorted(dict.fromkeys(links),key=score,reverse=True)

def fetch_text(url, max_pages=15):
    r=requests.get(url,headers=UA,timeout=18); r.raise_for_status(); c=(r.headers.get('content-type') or '').lower()
    if 'pdf' in c or url.lower().split('?')[0].endswith('.pdf'):
        reader=PdfReader(io.BytesIO(r.content)); return '\n'.join((p.extract_text() or '') for p in reader.pages[:max_pages])
    return BeautifulSoup(r.text,'html.parser').get_text(' ',strip=True)

def enrich(manufacturer,reference):
    for a in SEED:
        if clean_ref(a.get('reference'))==clean_ref(reference) and (not manufacturer or clean(manufacturer).lower() in clean(a.get('manufacturer')).lower() or clean(a.get('manufacturer')).lower() in clean(manufacturer).lower()):
            return dict(a)
    local=eplan_exact(reference,manufacturer)
    if local:
        # Local catalog is identity/inventory evidence only.
        return {'key':(manufacturer+'|'+reference).upper(),'manufacturer':local.get('manufacturer') or manufacturer,'reference':local.get('order') or reference,'name':local.get('d1') or local.get('d2') or reference,'type':local.get('d3') or '', 'status':'found','confidence':'media','sourceType':'Base EPLAN XML (inventario)','sourceUrl':(local.get('docs') or [''])[0], 'notes':'Identificado en la base EPLAN. Los datos críticos deben contrastarse con documentación oficial.'}
    for u in search_web(manufacturer,reference)[:6]:
        try:
            text=fetch_text(u)
            if clean_ref(reference).lower() not in clean(text).replace(' ','').lower(): continue
            data=extract(text)
            host=urlparse(u).netloc.lower(); official=any(d in host for d in manufacturer_domains(manufacturer))
            data.update({'key':(manufacturer+'|'+reference).upper(),'manufacturer':manufacturer,'reference':reference,'name':reference,'type':'','status':'found','confidence':'alta' if official else 'media','sourceType':'Web oficial / datasheet' if official else 'Fuente técnica externa','sourceUrl':u,'datasheetUrl':u,'notes':'Datos extraídos automáticamente. Requiere validación antes de usarlos como definitivos.'})
            return data
        except Exception:
            pass
    return None

def analyze_reference(manufacturer, reference):
    local=eplan_exact(reference,manufacturer)
    rule=s210_rule(reference)
    if rule:
        live=False; live_error=''
        try:
            # This is deliberately a live request: it lets the UI state whether the manufacturer document was reachable now.
            rr=requests.get(S210_PROTECTION_URL,headers=UA,timeout=10)
            live=rr.ok and len(rr.content)>10000
        except Exception as e:
            live_error=str(e)
        return {
            'found':True,'status':'manufacturer','family':'SINAMICS S210 6SL5','manufacturer':'Siemens','reference':reference,
            'catalogArticle':local,'liveVerified':live,'liveError':live_error,
            'inputA':rule['inputA'],'powerKw':rule['kw'],
            'requirements':[
                {'category':'motor_protector','referencePattern':rule['msp']['ref'],'ratingA':rule['msp']['a'],'preferred':True,'source':S210_PROTECTION_URL},
                {'category':'mcb','referencePattern':rule['cb']['ref'],'ratingA':rule['cb']['a'],'curve':rule['cb'].get('curve','C'),'preferred':False,'source':S210_PROTECTION_URL},
            ],
            'rcd':{'type':'B','sensitivitymA':300,'shortDelay':True,'note':'Si se utiliza RCCB en 3 AC: tipo B superresistente/retardo breve, 300 mA. Un RCCB aguas arriba también debe ser tipo B.','source':S210_OPERATING_URL},
            'sources':[S210_PROTECTION_URL,S210_OPERATING_URL]
        }
    # Generic: first try official documentation links already in EPLAN, then manufacturer web search.
    urls=[]
    if local:
        urls.extend([u for u in (local.get('docs') or []) if u])
    urls.extend(search_web(manufacturer,reference,'datasheet manual protection circuit breaker'))
    seen=set()
    for u in urls[:8]:
        if u in seen: continue
        seen.add(u)
        try:
            host=urlparse(u).netloc.lower(); official=any(d in host for d in manufacturer_domains(manufacturer))
            if not official and local and u in (local.get('docs') or []):
                # EPLAN may contain stale/wrong URLs; never mark as official unless host matches the manufacturer.
                pass
            text=fetch_text(u)
            if clean_ref(reference).lower() not in re.sub(r'\s+','',text).lower() and clean(reference).lower() not in text.lower():
                continue
            technical=extract(text); constraints=extract_power_constraints(text)
            return {'found':True,'status':'manufacturer' if official else 'technical','manufacturer':manufacturer,'reference':reference,'catalogArticle':local,'liveVerified':True,'technical':technical,'constraints':constraints,'source':u,'official':official,'note':'Extracción automática del documento. Las restricciones críticas deben validarse en la interfaz antes de aprobar la selección.'}
        except Exception:
            continue
    return {'found':bool(local),'status':'catalog-only' if local else 'not-found','manufacturer':manufacturer,'reference':reference,'catalogArticle':local,'liveVerified':False,'note':'Artículo identificado en EPLAN, pero no se ha podido validar todavía un manual oficial.' if local else 'No se ha identificado una fuente técnica fiable.'}

def search_protection(req):
    category=clean(req.get('category'))
    manufacturer=clean(req.get('manufacturer'))
    pattern=clean(req.get('exactPattern') or req.get('referencePattern'))
    local=eplan_pattern(pattern,category,manufacturer) if pattern else []
    if local:
        return {'found':True,'source':'eplan','reference':local[0].get('order') or local[0].get('id'),'article':local[0],'candidates':local[:8]}
    # If manufacturer gave an exact family/reference but it is missing locally, search ONLY manufacturer domains first.
    query_ref=pattern.replace('..','') if pattern else clean(req.get('required'))
    links=[]
    try: links=search_web(manufacturer or 'Siemens',query_ref,'product technical data')
    except Exception: links=[]
    official=[u for u in links if any(d in urlparse(u).netloc.lower() for d in manufacturer_domains(manufacturer or 'Siemens'))]
    if official:
        return {'found':True,'source':'manufacturer-web','reference':query_ref,'url':official[0],'candidates':[{'reference':query_ref,'url':u} for u in official[:5]]}
    return {'found':False,'source':'none','reference':query_ref,'candidates':[]}

class Handler(SimpleHTTPRequestHandler):
    def translate_path(self,path):
        rel=urlparse(path).path.lstrip('/') or 'index.html'; return str(ROOT/rel)
    def json_response(self,obj,status=200):
        b=json.dumps(obj,ensure_ascii=False).encode(); self.send_response(status); self.send_header('Content-Type','application/json; charset=utf-8'); self.send_header('Content-Length',str(len(b))); self.end_headers(); self.wfile.write(b)
    def read_json(self):
        n=int(self.headers.get('Content-Length','0')); return json.loads(self.rfile.read(n) or b'{}')
    def do_GET(self):
        p=urlparse(self.path)
        if p.path=='/api/health': return self.json_response({'ok':True,'internet_enrichment':True,'sql_eplan':bool(os.getenv('EPLAN_SQL_DSN')),'eplan_xml_articles':len(EPLAN),'version':'0.7'})
        if p.path=='/api/sql/status': return self.json_response({'configured':bool(os.getenv('EPLAN_SQL_DSN')),'message':'La conexión SQL requiere DSN/credenciales y mapeo del esquema real de EPLAN.'})
        return super().do_GET()
    def do_POST(self):
        path=urlparse(self.path).path
        try:
            data=self.read_json()
            if path=='/api/enrich':
                man=clean(data.get('manufacturer')); ref=clean(data.get('reference'))
                if not ref: return self.json_response({'error':'reference required'},400)
                a=enrich(man,ref); return self.json_response({'article':a,'found':bool(a)})
            if path=='/api/power/reference':
                man=clean(data.get('manufacturer')); ref=clean(data.get('reference'))
                if not ref: return self.json_response({'error':'reference required'},400)
                return self.json_response(analyze_reference(man,ref))
            if path=='/api/power/search-protection':
                return self.json_response(search_protection(data))
            return self.json_response({'error':'not found'},404)
        except Exception as e:
            return self.json_response({'error':str(e)},500)

if __name__=='__main__':
    port=int(os.getenv('PORT','8765'))
    print(f'Electrical app v0.7: http://127.0.0.1:{port}')
    print(f'Catalogo EPLAN XML normalizado: {len(EPLAN)} articulos')
    ThreadingHTTPServer(('127.0.0.1',port),Handler).serve_forever()
