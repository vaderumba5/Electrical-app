const assert = require('node:assert/strict');
const fs = require('node:fs');
const vm = require('node:vm');

const html = fs.readFileSync('index.html', 'utf8');
const match = html.match(/\/\/ ===== Safety library infrastructure =====([\s\S]*?)\/\/ ===== End safety library infrastructure =====/);
assert.ok(match, 'No se encontró el modelo de librerías de seguridad');

const context = {};
vm.createContext(context);
vm.runInContext(match[1], context);

assert.equal(context.detectSafetyLibraryFormat('Pilz.SLB'), 'sistema_slb');
assert.equal(context.detectSafetyLibraryFormat('vendor.xml', '<vdma:library xmlns:vdma="urn:vdma:66413">'), 'vdma_66413');
assert.equal(context.detectSafetyLibraryFormat('vendor.xml', '<SISTEMALibrary version="1"/>'), 'sistema_xml');
assert.equal(context.detectSafetyLibraryFormat('notes.txt', ''), null);
assert.equal(context.detectSafetyLibraryFormat('generic.xml', '<catalog/>'), null);
assert.throws(() => context.createSafetyLibrary({ fileName: 'generic.xml', content: '<catalog/>' }), /Formato no reconocido/);

const slb = context.createSafetyLibrary({ fileName: 'pilz.slb', name: 'Pilz Safety', manufacturer: 'Pilz', importedAt: '2026-08-23T10:00:00.000Z' });
assert.equal(slb.format, 'sistema_slb');
assert.equal(slb.status, 'detected_not_interpreted');
assert.equal(slb.components.length, 0, 'Un SLB no debe interpretarse sin esquema verificado');
assert.match(slb.warnings[0], /Firebird/);

const component = context.normalizeSafetyLibraryComponent({ source: { fileName: 'vendor.xml', objectId: 'original-1' } }, slb.id);
for (const field of ['PL', 'PFHd', 'MTTFd', 'B10d', 'DCavg', 'category', 'missionTime']) {
  assert.equal(component.safetyData[field], null, `${field} no debe inventarse`);
}
assert.equal(component.source.fileName, 'vendor.xml');
assert.equal(component.source.objectId, 'original-1');

const repository = { safetyLibraries: [slb] };
const persisted = JSON.parse(JSON.stringify(repository));
persisted.safetyLibraries = persisted.safetyLibraries.map(context.normalizeSafetyLibrary);
assert.equal(persisted.safetyLibraries[0].sourceFileName, 'pilz.slb');
assert.equal(persisted.safetyLibraries[0].manufacturer, 'Pilz');
context.removeSafetyLibrary(persisted, slb.id);
assert.equal(persisted.safetyLibraries.length, 0);

console.log('SISTEMA library infrastructure tests: OK');
