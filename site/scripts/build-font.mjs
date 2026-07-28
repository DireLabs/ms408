// Build the MS408 dingbat font — a small set of manuscript ORNAMENTS (fleuron, quatrefoil,
// rosette-ring, sprig, six-point star, lozenge, sun, bullet) as filled glyph outlines. These are
// decorative dingbats, NOT Voynich glyphs and NOT a transliteration. Output: an OpenType font +
// a specimen JSON, written into ../theme-kit/font/. Run: `node scripts/build-font.mjs` from site/.
import opentype from 'opentype.js';
import { writeFileSync, mkdirSync } from 'node:fs';
import { dirname, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';

const OUT = resolve(dirname(fileURLToPath(import.meta.url)), '..', '..', 'theme-kit', 'font');
mkdirSync(OUT, { recursive: true });

const EM = 1000, CX = 400, CY = 350, AW = 800;
const K = 0.5522847498; // circle bezier constant

function circle(p, cx, cy, r, ccw = false) {
  const k = r * K;
  p.moveTo(cx + r, cy);
  if (!ccw) {
    p.curveTo(cx + r, cy + k, cx + k, cy + r, cx, cy + r);
    p.curveTo(cx - k, cy + r, cx - r, cy + k, cx - r, cy);
    p.curveTo(cx - r, cy - k, cx - k, cy - r, cx, cy - r);
    p.curveTo(cx + k, cy - r, cx + r, cy - k, cx + r, cy);
  } else {
    p.curveTo(cx + r, cy - k, cx + k, cy - r, cx, cy - r);
    p.curveTo(cx - k, cy - r, cx - r, cy - k, cx - r, cy);
    p.curveTo(cx - r, cy + k, cx - k, cy + r, cx, cy + r);
    p.curveTo(cx + k, cy + r, cx + r, cy + k, cx + r, cy);
  }
  p.close();
}
function poly(p, pts) { pts.forEach(([x, y], i) => (i ? p.lineTo(x, y) : p.moveTo(x, y))); p.close(); }
function star(p, cx, cy, points, R, r, rot = -Math.PI / 2) {
  const v = [];
  for (let i = 0; i < points * 2; i++) {
    const rad = i % 2 ? r : R, a = rot + (Math.PI * i) / points;
    v.push([cx + rad * Math.cos(a), cy + rad * Math.sin(a)]);
  }
  poly(p, v);
}

// each: [names, unicodes(array), draw(path)]
const DINGBATS = [
  ['fleuron', ['a', 0xE000], (p) => { // a leaf/fleuron
    p.moveTo(CX, CY + 250); p.quadTo(CX + 190, CY + 20, CX, CY - 250);
    p.quadTo(CX - 190, CY + 20, CX, CY + 250); p.close();
  }],
  ['quatrefoil', ['b', 0xE001], (p) => { // four-lobed flower
    circle(p, CX, CY + 175, 130); circle(p, CX, CY - 175, 130);
    circle(p, CX - 175, CY, 130); circle(p, CX + 175, CY, 130);
    circle(p, CX, CY, 110);
  }],
  ['rosette', ['c', 0xE002], (p) => { // ring with a center dot
    circle(p, CX, CY, 250, false); circle(p, CX, CY, 150, true); circle(p, CX, CY, 55, false);
  }],
  ['sprig', ['d', 0xE003], (p) => { // stem + two leaves
    poly(p, [[CX - 18, CY - 250], [CX + 18, CY - 250], [CX + 18, CY + 210], [CX - 18, CY + 210]]);
    p.moveTo(CX, CY + 20); p.quadTo(CX - 170, CY + 60, CX - 210, CY + 200);
    p.quadTo(CX - 60, CY + 130, CX, CY + 60); p.close();
    p.moveTo(CX, CY + 20); p.quadTo(CX + 170, CY + 60, CX + 210, CY + 200);
    p.quadTo(CX + 60, CY + 130, CX, CY + 60); p.close();
  }],
  ['star', ['e', 0xE004], (p) => star(p, CX, CY, 6, 250, 105)],
  ['lozenge', ['f', 0xE005], (p) => poly(p,
    [[CX, CY + 250], [CX + 165, CY], [CX, CY - 250], [CX - 165, CY]])],
  ['sun', ['g', 0xE006], (p) => { // disc + 8 rays
    for (let i = 0; i < 8; i++) {
      const a = (Math.PI * i) / 4, c = Math.cos(a), s = Math.sin(a), n = a + Math.PI / 2;
      poly(p, [
        [CX + 250 * c, CY + 250 * s],
        [CX + 155 * c + 34 * Math.cos(n), CY + 155 * s + 34 * Math.sin(n)],
        [CX + 155 * c - 34 * Math.cos(n), CY + 155 * s - 34 * Math.sin(n)],
      ]);
    }
    circle(p, CX, CY, 150);
  }],
  ['bullet', ['h', 0xE007], (p) => circle(p, CX, CY, 120)],
];

const glyphs = [new opentype.Glyph({ name: '.notdef', advanceWidth: 0, path: new opentype.Path() })];
glyphs.push(new opentype.Glyph({
  name: 'space', unicode: 0x20, advanceWidth: 400, path: new opentype.Path(),
}));
const specimen = [];
for (const [name, codes, draw] of DINGBATS) {
  const path = new opentype.Path();
  draw(path);
  const unicodes = codes.map((c) => (typeof c === 'string' ? c.charCodeAt(0) : c));
  glyphs.push(new opentype.Glyph({ name, unicodes, advanceWidth: AW, path }));
  specimen.push({ name, char: codes[0], pua: '0x' + codes[1].toString(16).toUpperCase() });
}

const font = new opentype.Font({
  familyName: 'MS408 Dingbats', styleName: 'Regular',
  unitsPerEm: EM, ascender: 760, descender: -240, glyphs,
});
const buf = Buffer.from(font.toArrayBuffer());
writeFileSync(resolve(OUT, 'ms408-dingbats.otf'), buf);
writeFileSync(resolve(OUT, 'specimen.json'), JSON.stringify(specimen, null, 2) + '\n');

// round-trip validate
const reparsed = opentype.parse(buf.buffer.slice(buf.byteOffset, buf.byteOffset + buf.byteLength));
console.log(`Wrote ms408-dingbats.otf (${buf.length} bytes), ${reparsed.glyphs.length} glyphs.`);
console.log('Specimen:', specimen.map((s) => `${s.char}=${s.name}`).join('  '));
