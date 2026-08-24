const assert = require('node:assert/strict');
const fs = require('node:fs');
const vm = require('node:vm');

const html = fs.readFileSync('index.html', 'utf8');
const match = html.match(/\/\/ ===== Adaptive power receiver model =====([\s\S]*?)\/\/ ===== End adaptive power receiver model =====/);
assert.ok(match, 'No se encontró el modelo de receptores');
const context = {
  num: value => Number.isFinite(Number(value)) ? Number(value) : 0,
  isDC: value => /V?DC/i.test(String(value || '')),
};
vm.createContext(context);
vm.runInContext(match[1], context);

const close = (actual, expected, tolerance = 1e-9) => assert.ok(Math.abs(actual - expected) < tolerance, `${actual} != ${expected}`);
const receiver = (kind, values = {}) => context.normalizePowerReceiverElement({
  block: 'power', tag: 'R1', name: 'Receptor', currentA: null,
  receiver: { kind, supplyType: 'ac', dataOrigins: {}, ...values.receiver },
  ...values,
});

const motor = receiver('direct_motor', { voltage: '400VAC', phases: 3, powerKw: 11, cosPhi: 0.85, efficiency: 0.9 });
close(motor.receiver.calculations.designCurrent.value, 11000 / (Math.sqrt(3) * 400 * 0.85 * 0.9));
assert.equal(motor.receiver.calculations.designCurrent.formula, 'P / (√3 · U · cosφ · η)');

const single = receiver('single_phase_load', { voltage: '230VAC', phases: 1, powerKw: 2.3, cosPhi: 0.92, efficiency: 0.95 });
close(single.receiver.calculations.designCurrent.value, 2300 / (230 * 0.92 * 0.95));

const apparent = receiver('three_phase_load', { voltage: '400VAC', phases: 3, cosPhi: null, efficiency: null, receiver: { kind: 'three_phase_load', supplyType: 'ac', apparentPowerKva: 10, dataOrigins: {} } });
close(apparent.receiver.calculations.designCurrent.value, 10000 / (Math.sqrt(3) * 400));
assert.equal(apparent.receiver.calculations.designCurrent.formula, 'S / (√3 · U)');

const dc = receiver('single_phase_load', { voltage: '24VDC', phases: 1, powerKw: 0.24, receiver: { kind: 'single_phase_load', supplyType: 'dc', dataOrigins: {} } });
close(dc.receiver.calculations.designCurrent.value, 10);
assert.equal(dc.receiver.calculations.designCurrent.formula, 'P / U');

const heater = receiver('heater', { voltage: '230VAC', phases: 1, powerKw: 3, cosPhi: null, efficiency: null });
close(heater.receiver.calculations.designCurrent.value, 3000 / 230);

const transformer = receiver('transformer', { voltage: '400VAC', phases: 3, receiver: { kind: 'transformer', supplyType: 'ac', apparentPowerVa: 20000, dataOrigins: {} } });
close(transformer.receiver.calculations.designCurrent.value, 20000 / (Math.sqrt(3) * 400));

const plate = receiver('direct_motor', { voltage: '400VAC', phases: 3, powerKw: 5.5, currentA: 12.4, cosPhi: 0.82, efficiency: 0.88, receiver: { kind: 'direct_motor', supplyType: 'ac', simultaneity: 0.75, startingCurrentA: 70, dataOrigins: { currentA: 'imported' } } });
assert.equal(plate.receiver.calculations.designCurrent.status, 'plate');
assert.equal(plate.receiver.calculations.designCurrent.value, 12.4);
assert.equal(plate.receiver.calculations.calculatedCurrent.status, 'calculated');
close(plate.receiver.calculations.demandCurrent.value, 9.3);
assert.equal(plate.receiver.calculations.startingCurrent.excludedFromIb, true);

const insufficient = receiver('direct_motor', { voltage: '', phases: '', powerKw: 2.2, cosPhi: null, efficiency: null });
assert.equal(insufficient.receiver.calculations.designCurrent.status, 'pending');
assert.ok(insufficient.receiver.calculations.designCurrent.missing.includes('tensión válida'));
assert.ok(insufficient.receiver.calculations.designCurrent.missing.includes('número de fases (1 o 3)'));

for (const invalidPower of [0, -1, 'abc']) {
  const invalid = receiver('heater', { voltage: '230VAC', phases: 1, powerKw: invalidPower });
  assert.equal(invalid.receiver.calculations.designCurrent.status, 'pending');
  assert.ok(invalid.receiver.calculations.designCurrent.missing.some(item => item.includes('potencia válida')));
}
for (const invalidVoltage of [0, -230, 'abc']) {
  const invalid = receiver('heater', { voltage: invalidVoltage, phases: 1, powerKw: 1 });
  assert.equal(invalid.receiver.calculations.designCurrent.status, 'pending');
  assert.ok(invalid.receiver.calculations.designCurrent.missing.includes('tensión válida'));
}

console.log('Power Ib calculation tests: OK');
