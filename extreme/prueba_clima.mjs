/* La geometria del tablero, copiada del juego, para probar tocaHex */
const R = 46, RX = 1.5*R, RY = Math.sqrt(3)*R;
const COLS = [3,4,5,4,3];
const CX = 260, CY = 250;
const POS = {};
COLS.forEach((cuantos, c) => {
  const cx = CX + (c - (COLS.length-1)/2)*RX, y0 = CY - ((cuantos-1)*RY)/2;
  for (let i=0;i<cuantos;i++) POS[c*10+i] = { cx, cy: y0+i*RY };
});
const HEXES = [];
COLS.forEach((cuantos, c) => { for (let i=0;i<cuantos;i++) HEXES.push({ c, i }); });
const posHex = (c, i) => POS[c*10 + i];

function hexesDelCruce(k){
  const p = String(k).replace(/^v#/, '').split('#').map(Number);
  if (!isFinite(p[0]) || !isFinite(p[1])) return [];
  const out = [];
  HEXES.forEach((h, i) => {
    const pos = posHex(h.c, h.i);
    if (pos && Math.hypot(pos.cx - p[0], pos.cy - p[1]) < R * 1.08) out.push(i);
  });
  return out;
}
function tocaHex(pz, i){
  let n = 0;
  ((pz && pz.base) || []).forEach(b => { if (hexesDelCruce(b.k).includes(i)) n += 1; });
  ((pz && pz.hub)  || []).forEach(b => { if (hexesDelCruce(b.k).includes(i)) n += 2; });
  return n;
}

console.log('  hexagonos: %d\n', HEXES.length);

/* Un cruce: el punto medio entre dos centros de hexagono vecinos. Es donde se
   puede poner un Basecamp de verdad. */
const centro = (idx) => { const h = HEXES[idx]; return posHex(h.c, h.i); };
const cruce = (i, j) => {
  const a = centro(i), b = centro(j);
  return `v#${((a.cx+b.cx)/2).toFixed(1)}#${((a.cy+b.cy)/2).toFixed(1)}`;
};

let malos = 0, probados = 0;
// cojo cada hexagono y todos sus vecinos: el cruce entre ellos debe tocar AMBOS
HEXES.forEach((h, idx) => {
  HEXES.forEach((h2, idx2) => {
    if (idx === idx2) return;
    const a = centro(idx), b = centro(idx2);
    const d = Math.hypot(a.cx-b.cx, a.cy-b.cy);
    if (Math.abs(d - RY) > 1) return;        // no son vecinos
    const k = cruce(idx, idx2);
    const toca = hexesDelCruce(k);
    probados++;
    if (!toca.includes(idx) || !toca.includes(idx2)) {
      if (malos < 6) console.log('  ✗ cruce entre %d y %d -> toca [%s]', idx, idx2, toca.join(','));
      malos++;
    }
  });
});
console.log('  cruces probados: %d   con fallo: %d', probados, malos);
console.log('  %s\n', malos ? '✗ tocaHex FALLA' : '✓ tocaHex esta bien');

/* Y ahora el caso que reporta Pam: alguien tiene un Basecamp y muevo el clima
   a ese hexagono */
const k0 = cruce(6, 7);
const pz = { base: [{ k: k0, hex: 6 }], camino: [] };
console.log('  --- el caso de Pam ---');
for (const i of [6, 7, 8, 0, 1]) {
  console.log('   clima en el hexagono %d -> tocaHex dice %d %s', i, tocaHex(pz, i),
              tocaHex(pz, i) ? '(hay alguien)' : '(no hay nadie)');
}
