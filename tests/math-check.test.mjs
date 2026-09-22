import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
import {spawnSync} from 'node:child_process';
const script = new URL('../skills/stem-study-vault/scripts/katex_check.mjs', import.meta.url);
function run(files) {
 const dir=fs.mkdtempSync(path.join(os.tmpdir(),'vault-math-'));
 try {
  for (const [name,text] of Object.entries(files)) { const p=path.join(dir,name);fs.mkdirSync(path.dirname(p),{recursive:true});fs.writeFileSync(p,text); }
  const r=spawnSync(process.execPath,[fileURLToPath(script),dir],{encoding:'utf8'});
  return {status:r.status,...JSON.parse(r.stdout)};
 } finally {fs.rmSync(dir,{recursive:true,force:true});}
}
test('accepts valid math and ignores fenced/inline code',()=>{
 const r=run({'lesson.md':'$x^2$\n```tex\n\\frac\n```\n`\\sum`\n'});
 assert.equal(r.status,0);assert.equal(r.formulas,1);assert.equal(r.errors.length,0);
});
test('flags malformed formula and unmatched delimiter',()=>{
 const r=run({'a.md':'$\\notarealcommand{x}$','b.md':'$$x'});
 assert.equal(r.status,1);assert.equal(r.errors.length,2);
});
test('does not scan source originals, hidden folders or dependencies',()=>{
 const r=run({'lesson.md':'$x$','Sources/Original/a.md':'$$bad','.private/a.md':'$$bad','node_modules/a.md':'$$bad'});
 assert.equal(r.status,0);assert.equal(r.files,1);
});
test('flags bare commands outside math',()=>{
 const r=run({'lesson.md':'A bare \\frac{1}{2} command'});
 assert.equal(r.status,1);assert.equal(r.errors.length,1);
});
