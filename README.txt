APP ELÉCTRICA · v0.7 · POTENCIA BASADA EN RECEPTORES

OBJETIVO DE ESTA VERSIÓN
Potencia ya no se gestiona como una mezcla de cargas, protecciones y distribuidores. El usuario introduce únicamente los receptores reales de la máquina y la app construye después la propuesta de ingeniería.

FLUJO
1. Receptores
   - Servoaccionamientos / variadores
   - Motores trifásicos y monofásicos
   - Cargas mono/trifásicas
   - Tomas de corriente
   - Fuentes DC
   - Transformadores / UPS / otros receptores

2. Datos de red
   - 400/230 V o 230 V
   - TN-S / TT / IT / TN-C-S
   - Ik disponible
   - Iz de la acometida
   - criterio normativo

3. Manuales y restricciones
   - identifica fabricante + referencia
   - consulta reglas verificadas y, con backend, documentación online
   - la documentación del fabricante prevalece sobre reglas genéricas

4. Circuitos sugeridos
   - cada receptor físico se convierte en una rama
   - 3 S210 = 3 ramas, no una rama equivalente de 8,4 A
   - las cargas monofásicas se equilibran entre L1/L2/L3 si no se fija fase

5. Protección general y diferencial
   - corriente máxima por fase
   - calibre mínimo preliminar
   - validación In <= Iz
   - Icn/Icu condicionado por Ik
   - la curva general no se inventa: queda pendiente de coordinación/selectividad
   - restricciones diferenciales de fabricante se propagan a la arquitectura

6. Selección de artículos
   - primero filtra el catálogo derivado del XML EPLAN
   - después busca en Internet solo cuando no existe una coincidencia técnica suficiente
   - una coincidencia de catálogo no se considera automáticamente válida: el manual oficial manda

BASE EPLAN XML
El archivo basado en el XML adjunto contiene 6.133 nodos <part> normalizados. El atributo count del export original declara 6.580, por lo que la app informa del número de registros realmente normalizados y utilizables.

DATOS IMPORTANTES DEL CATÁLOGO
Se preservan referencia, referencia de pedido, fabricante, descripción, categoría, tensión/corriente cuando su semántica es clara, polos, curva, sensibilidad, tipo diferencial, poder de corte y enlaces externos.

ATENCIÓN CON FUENTES DC
En una fuente 24 VDC de 10 A, esos 10 A son capacidad de SALIDA y no se utilizan como corriente de entrada AC. La corriente de entrada se obtiene del manual o se deja pendiente.

SINAMICS S210
Para los S210 6SL5... se incluyen reglas verificadas de protección IEC basadas en la documentación Siemens 01/2026. La app distingue:
- protector de motor recomendado/permitido por tabla del fabricante,
- alternativa magnetotérmica indicada por Siemens,
- requisito diferencial para conexión 3 AC si se emplea RCCB,
- artículo disponible o no disponible en vuestro EPLAN.

ARRANQUE
Windows: ejecutar start_windows.bat.
- Con Python/backend: búsqueda online de manuales y artículos.
- Modo local: catálogo EPLAN normalizado + reglas verificadas precargadas, sin búsqueda web en tiempo real.

IMPORTANTE
Es una herramienta de ingeniería asistida. No se aprueba una protección general si faltan datos críticos como corriente de entrada de receptores, Iz o Ik. La selección final debe respetar documentación vigente del fabricante, sistema de red, normas aplicables, cortocircuito, sección/capacidad de conductor, selectividad, agrupamiento, temperatura y condiciones de instalación.
