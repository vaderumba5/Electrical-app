const assert = require('node:assert/strict');
const fs = require('node:fs');
const vm = require('node:vm');

const html = fs.readFileSync('index.html', 'utf8');
const match = html.match(/\/\/ ===== Adaptive power receiver model =====([\s\S]*?)\/\/ ===== End adaptive power receiver model =====/);
assert.ok(match, 'No se encontró el modelo adaptativo de receptores');

const context = {
  num: value => Number.isFinite(Number(value)) ? Number(value) : 0,
  isDC: value => /V?DC/i.test(String(value || '')),
};
vm.createContext(context);
vm.runInContext(match[1], context);

assert.deepEqual(
  Object.keys(context.POWER_RECEIVER_KINDS || vm.runInContext('POWER_RECEIVER_KINDS', context)),
  ['direct_motor', 'vfd_motor', 'servo_drive', 'single_phase_load', 'three_phase_load', 'ac_dc_supply', 'socket', 'transformer', 'heater'],
);

const legacy = { id: 'legacy-m1', block: 'power', type: 'Motor trifásico', tag: 'M1', name: 'Motor antiguo', voltage: '400VAC', phases: 3, powerKw: 2.2, currentA: 4.8, cosPhi: 0.9, efficiency: 0.9 };
const migrated = context.normalizePowerReceiverElement(legacy);
for (const [key, value] of Object.entries(legacy)) assert.deepEqual(migrated[key], value, `Debe conservar ${key}`);
assert.equal(migrated.receiver.kind, 'direct_motor');
assert.equal(migrated.receiver.supplyType, 'ac');
assert.equal(migrated.receiver.dataOrigins.cosPhi, 'assumed');

const supply = context.normalizePowerReceiverElement({ id: 'ps1', block: 'power', type: 'Fuente AC/DC', tag: 'PS1', name: 'Fuente', voltage: '230VAC', phases: 1, dcOutputVoltage: 24, dcOutputA: 10, receiver: { kind: 'ac_dc_supply', dataOrigins: { dcOutputA: 'imported' } } });
assert.equal(supply.receiver.kind, 'ac_dc_supply');
assert.equal(supply.receiver.dataOrigins.dcOutputA, 'imported');

const switched = context.normalizePowerReceiverElement({ ...supply, receiver: { ...supply.receiver, kind: 'socket' } });
context.clearNonApplicablePowerData(switched);
assert.equal(switched.dcOutputVoltage, null, 'Un campo no aplicable debe quedar neutralizado');
assert.equal(switched.dcOutputA, null, 'La salida DC no debe intervenir tras cambiar a toma');

assert.deepEqual(Array.from(context.validatePowerReceiver(migrated)), []);
assert.ok(context.validatePowerReceiver(context.normalizePowerReceiverElement({ block: 'power', receiver: { kind: 'direct_motor' }, cosPhi: 1.2 })).some(error => error.includes('cosPhi')));
assert.ok(context.validatePowerReceiver(context.normalizePowerReceiverElement({ block: 'power', tag: '', name: '', receiver: { kind: 'direct_motor' } })).length >= 2);

const reloaded = context.normalizePowerReceiverElement(JSON.parse(JSON.stringify(supply)));
assert.equal(reloaded.receiver.kind, 'ac_dc_supply');
assert.equal(reloaded.dcOutputA, 10);
assert.equal(reloaded.receiver.dataOrigins.dcOutputA, 'imported');

console.log('Adaptive power receiver model tests: OK');
