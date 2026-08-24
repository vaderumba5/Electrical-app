const assert = require('node:assert/strict');
const fs = require('node:fs');
const vm = require('node:vm');

const html = fs.readFileSync('index.html', 'utf8');
const powerModel = html.match(/\/\/ ===== Adaptive power receiver model =====([\s\S]*?)\/\/ ===== End adaptive power receiver model =====/);
const match = html.match(/\/\/ ===== Functional safety Phase 1: model =====([\s\S]*?)\/\/ ===== End functional safety Phase 1 model =====/);
assert.ok(powerModel, 'No se encontró el modelo adaptativo de receptores');
assert.ok(match, 'No se encontró el bloque de modelo Safety Phase 1 en index.html');

const context = {
  INITIAL_SETTINGS: {
    projectCode: 'TEST',
    ioReservePct: 20,
    source24Ratings: [2.5, 5, 10],
  },
  clone: value => JSON.parse(JSON.stringify(value)),
  num: value => Number.isFinite(Number(value)) ? Number(value) : 0,
  isDC: value => /V?DC/i.test(String(value || '')),
};
vm.createContext(context);
vm.runInContext(powerModel[1], context);
vm.runInContext(match[1], context);

const legacyElements = [
  { id: 'el-power', block: 'power', tag: 'M1', name: 'Motor' },
  { id: 'el-control', block: 'control', tag: 'CAM1', name: 'Cámara' },
  { id: 'el-plc', block: 'plc', tag: 'PLC1', name: 'PLC' },
];
const legacyCircuits = [{ id: 'c-1', elementId: 'el-power', name: 'Rama M1' }];
const legacy = {
  id: 'legacy-v07',
  code: 'V07',
  name: 'Proyecto v0.7',
  elements: legacyElements,
  circuits: legacyCircuits,
  settings: { projectCode: 'V07', ioReservePct: 20 },
};

const migrated = context.makeProject(legacy);
for (const original of legacyElements) {
  const current = migrated.elements.find(element => element.id === original.id);
  for (const [key, value] of Object.entries(original)) assert.deepEqual(current[key], value, `La migración debe conservar elements.${original.id}.${key}`);
}
assert.deepEqual(migrated.circuits, legacyCircuits, 'La migración debe conservar circuits');
for (const [key, value] of Object.entries(legacy.settings)) {
  assert.deepEqual(migrated.settings[key], value, `La migración debe conservar settings.${key}`);
}
assert.equal(migrated.safetyFunctions.length, 0, 'Un proyecto v0.7 debe migrar con safetyFunctions vacío');
assert.equal(migrated.safetyFunctionNextNumber, 1, 'La migración v0.7 debe inicializar el contador');

const sf1 = context.addSafetyFunction(migrated, context.createSafetyFunction(migrated));
assert.equal(sf1.code, 'SF-001');
sf1.name = 'Parada de emergencia';
sf1.requiredPL = 'd';
sf1.stages.input = [{ elementId: 'el-plc' }];
assert.equal(migrated.elements.length, 3, 'Vincular una etapa no debe duplicar elementos');
assert.equal(migrated.safetyFunctions[0].stages.input[0].elementId, 'el-plc');
assert.equal(migrated.safetyFunctions[0].requiredPL, 'd');

const sf2 = context.addSafetyFunction(migrated, context.createSafetyFunction(migrated));
assert.equal(sf2.code, 'SF-002');
migrated.safetyFunctions = migrated.safetyFunctions.filter(sf => sf.id !== sf2.id);
const sf3 = context.addSafetyFunction(migrated, context.createSafetyFunction(migrated));
assert.equal(sf3.code, 'SF-003', 'Un código eliminado no debe reutilizarse');

const reloaded = context.makeProject(JSON.parse(JSON.stringify(migrated)));
assert.equal(reloaded.safetyFunctions.length, 2, 'Las funciones deben persistir tras serializar y recargar');
assert.equal(reloaded.safetyFunctions[0].code, 'SF-001');
assert.equal(reloaded.safetyFunctions[1].code, 'SF-003');
assert.equal(reloaded.safetyFunctionNextNumber, 4, 'El contador debe persistir tras recargar');
assert.equal(context.createSafetyFunction(reloaded).code, 'SF-004');
assert.equal(reloaded.safetyFunctions[0].stages.input[0].elementId, 'el-plc');
assert.equal(reloaded.elements.length, 3, 'La recarga no debe duplicar elementos');
assert.deepEqual(Array.from(reloaded.elements, e => e.block), ['power', 'control', 'plc'], 'Los bloques existentes deben conservarse');
assert.equal(reloaded.safetyFunctions[0].calculation.achievedPL, null, 'No debe inventarse PL alcanzado');
assert.ok(['not_calculated', 'missing_data'].includes(reloaded.safetyFunctions[0].calculation.status));

const elementsBeforeSafetyDelete = JSON.stringify(reloaded.elements);
reloaded.safetyFunctions = reloaded.safetyFunctions.filter(sf => sf.id !== sf1.id);
assert.equal(JSON.stringify(reloaded.elements), elementsBeforeSafetyDelete, 'Eliminar una función no debe eliminar elementos enlazados');

const unresolvedProject = context.makeProject(JSON.parse(JSON.stringify(migrated)));
unresolvedProject.elements = unresolvedProject.elements.filter(e => e.id !== 'el-plc');
const unresolvedReloaded = context.makeProject(JSON.parse(JSON.stringify(unresolvedProject)));
assert.equal(unresolvedReloaded.safetyFunctions[0].stages.input[0].elementId, 'el-plc', 'Una referencia debe mantenerse aunque desaparezca el elemento enlazado');

const invalid = context.normalizeSafetyFunction({ requiredPL: 'z', calculation: { status: 'calculated', achievedPL: 'e' } });
assert.equal(invalid.requiredPL, '', 'Un PLr inválido debe quedar pendiente');
assert.equal(invalid.calculation.status, 'not_calculated');
assert.equal(invalid.calculation.achievedPL, null, 'La fase 1 debe descartar un PL alcanzado no permitido');

console.log('Safety Phase 1 model tests: OK');
