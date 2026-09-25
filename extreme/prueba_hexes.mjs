/* La logica nueva de tocaHex, probada con los datos REALES de las partidas. */
const R = 46, RX = 1.5*R, RY = Math.sqrt(3)*R;
const COLS = [3,4,5,4,3];
function geo(CX, CY){
  const POS = {};
  COLS.forEach((cuantos,c) => {
    const cx = CX + (c-(COLS.length-1)/2)*RX, y0 = CY - ((cuantos-1)*RY)/2;
    for (let i=0;i<cuantos;i++) POS[c*10+i] = { cx, cy: y0+i*RY };
  });
  const HEXES = [];
  COLS.forEach((cuantos,c) => { for (let i=0;i<cuantos;i++) HEXES.push({c,i}); });
  return {POS, HEXES};
}
let g = geo(230, 250);
function hexesDelCruce(k){
  const p = String(k).replace(/^v#/,'').split('#').map(Number);
  const out = [];
  if (!isFinite(p[0]) || !isFinite(p[1])) return out;
  g.HEXES.forEach((h,i) => {
    const q = g.POS[h.c*10+h.i];
    if (q && Math.hypot(q.cx-p[0], q.cy-p[1]) < R*1.08) out.push(i);
  });
  return out;
}
/* la version ARREGLADA */
function suyosNuevo(b){
  if (!b) return [];
  if (Array.isArray(b.hexes) && b.hexes.length) return b.hexes;
  const calc = hexesDelCruce(b.k);
  const guardado = (b.hex != null) ? [b.hex] : [];
  return [...new Set([...calc, ...guardado])];
}
/* la version de antes */
function suyosViejo(b){ return b ? hexesDelCruce(b.k) : []; }
function tocaHex(pz, i, f){ return ((pz.base||[]).filter(b=>f(b).includes(i)).length)
  + 2*((pz.hub||[]).filter(b=>f(b).includes(i)).length); }

console.log('  === piezas REALES de una partida (sala TBYB, Maria) ===\n');
const pz = { base: [
  { k:'v#276.0#278.9', hex:14 },
  { k:'v#207.0#318.7', hex:10 },
], hub: [] };

console.log('  le muevo el clima a cada hexagono y veo si lo detecta:');
let fallosViejos = 0, fallosNuevos = 0;
for (let i = 0; i < 19; i++) {
  const v = tocaHex(pz, i, suyosViejo);
  const n = tocaHex(pz, i, suyosNuevo);
  if (v !== n) console.log('   hex %2d: antes %d   AHORA %d  <- cambia', i, v, n);
  if (v === 0 && i === 14) fallosViejos++;
}
console.log();
console.log('  === y el caso exacto del bug: el calculo no encuentra el hexagono ===');
const pz2 = { base: [{ k:'v#92.0#119.5', hex:0 }], hub: [] };
for (const cx of [200, 230, 260, 350]) {
  g = geo(cx, 250);
  const v = tocaHex(pz2, 0, suyosViejo);
  const n = tocaHex(pz2, 0, suyosNuevo);
  console.log('   con CX=%d -> antes %d %s   AHORA %d %s', cx, v, v?'✓':'✗ "no hay nadie"', n, n?'✓':'✗');
}
console.log();
console.log('  === y una pieza NUEVA (con hexes grabados) no depende del ancho ===');
const pz3 = { base: [{ k:'v#92.0#119.5', hex:0, hexes:[0,1] }], hub: [] };
for (const cx of [200, 230, 260, 350]) {
  g = geo(cx, 250);
  console.log('   con CX=%d -> %d %s', cx, tocaHex(pz3, 0, suyosNuevo), tocaHex(pz3, 0, suyosNuevo)?'✓':'✗');
}
