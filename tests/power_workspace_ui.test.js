const assert = require('node:assert/strict');
const fs = require('node:fs');

const html = fs.readFileSync('index.html', 'utf8');

for (const [id, label] of [
  ['receivers', 'Receptores'],
  ['circuits', 'Circuitos'],
  ['distribution', 'Distribución'],
  ['dc', 'Auxiliares DC'],
  ['report', 'Informe'],
]) {
  assert.ok(html.includes(`data-power-tab="${id}"`), `Falta la pestaña ${label}`);
  assert.ok(html.includes(`data-power-page="${id}"`), `Falta la página ${label}`);
}

for (const id of [
  'powerKpis', 'powerLoads', 'powerCircuitProposal', 'powerArchitecture', 'powerGeneral',
  'powerRcd', 'powerDcGroups', 'powerReport', 'powerManualAnalysis',
  'powerProtectionCandidates', 'addPower', 'analyzePower',
]) {
  const count = (html.match(new RegExp(`id="${id}"`, 'g')) || []).length;
  assert.equal(count, 1, `${id} debe existir exactamente una vez`);
}

assert.match(html, /let powerUiTab='receivers'/, 'Receptores debe ser la vista inicial');
assert.match(html, /powerSearch.*powerTypeFilter.*powerStatusFilter.*powerSupplyFilter.*powerSort/s);
assert.match(html, /openPowerDrawer\('\$\{e\.id\}'\)/);
assert.match(html, /Pendiente de cálculo/);
assert.match(html, /Potencia simultánea[\s\S]*Dato requerido/);
assert.match(html, /Caída de tensión[\s\S]*Pendiente de cálculo/);
assert.match(html, /Cortocircuito[\s\S]*Dato requerido/);

console.log('Power workspace UI tests: OK');
