import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import ts from 'typescript';

const source = fs.readFileSync(new URL('../src/imageLab.ts', import.meta.url), 'utf8');
const js = ts.transpileModule(source, {compilerOptions: {module: ts.ModuleKind.ESNext, target: ts.ScriptTarget.ES2022}}).outputText;
const lab = await import('data:text/javascript;base64,' + Buffer.from(js).toString('base64'));
const close = (a, b) => assert.ok(Math.abs(a - b) < 1e-12, `${a} != ${b}`);

test('filter preserves constants and zero passes preserves the exact input', () => {
  const flat = new Float64Array(16 * 16).fill(.37);
  for (const v of lab.smoothImage(flat, 8, 16)) close(v, .37);
  const input = lab.makeImage('scene');
  assert.deepEqual(lab.smoothImage(input, 0), input);
  assert.notEqual(lab.smoothImage(input, 0), input);
});

test('two-dimensional periodic sinusoid obeys measured separable frequency gain', () => {
  const size = 24, fx = 1 / 6, fy = 1 / 4;
  const input = Float64Array.from({length:size * size}, (_, i) => .5 + .2 * Math.cos(2 * Math.PI * (fx * (i % size) + fy * Math.floor(i / size))));
  for (const passes of [1, 2, 5]) {
    const actual = lab.smoothImage(input, passes, size);
    // Analytic gain at 1/6 is 3/4; at 1/4 it is 1/2.
    const gain = Math.pow(.75 * .5, passes);
    actual.forEach((v, i) => close(v, .5 + gain * (input[i] - .5)));
  }
});

test('periodic smoothing conserves total intensity and treats wrapped neighbours correctly', () => {
  const input = new Float64Array(8 * 8); input[0] = 1;
  const output = lab.smoothImage(input, 1, 8);
  close(output.reduce((a, b) => a + b, 0), 1);
  close(output[0], .25); close(output[7], .125); close(output[56], .125);
  close(output[63], .0625);
});

test('alternating texture and flat field become indistinguishable after filtering', () => {
  const input = Float64Array.from({length:16 * 16}, (_, i) => .5 + .2 * (-1) ** (i % 16));
  for (const v of lab.smoothImage(input, 1, 16)) close(v, .5);
});

test('noise is reproducible, clipped and does not mutate the reference image', () => {
  const input = lab.makeImage('scene'), saved = input.slice();
  assert.deepEqual(lab.addNoise(input, .35), lab.addNoise(input, .35));
  assert.deepEqual(lab.addNoise(input, 0), input);
  assert.deepEqual(input, saved);
  assert.ok(lab.addNoise(input, .35).every(v => v >= 0 && v <= 1));
});

test('row profiles use the exact corresponding displayed image samples', () => {
  const output = lab.smoothImage(lab.addNoise(lab.makeImage('stripes'), .12), 3);
  for (const row of [0, 48, 95]) {
    assert.deepEqual(lab.imageRow(output, row), Array.from(output.slice(row * 96, (row + 1) * 96)));
  }
  close(lab.response(0), 1); close(lab.response(.25), .5); close(lab.response(.5), 0);
  close(lab.response(.25, 2), .25);
});
