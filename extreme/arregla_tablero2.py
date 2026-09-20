#!/usr/bin/env python3
"""El motor del zoom, con las anclas correctas (2 espacios de indentacion)."""
RUTA = '/Users/lapame10/.hermes/workspace/catan/extreme/index.html'
s = open(RUTA, encoding='utf-8').read()
toc = 0


def rep(v, n):
    global s, toc
    if v in s:
        s = s.replace(v, n, 1); toc += 1
        return True
    print('  NO ENCUENTRO:', v[:70].replace('\n', ' | '))
    return False


# 1) el check de arrastre en el onclick (2 espacios, no 4)
rep("""  svg.onclick = (e) => {
      const todos = [...svg.querySelectorAll('.toque')];""",
    """  svg.onclick = (e) => {
      /* si acabas de ARRASTRAR el tablero, el toque no cuenta: si no, cada vez
         que mueves el mapa colocarias una pieza sin querer */
      if (huboArrastre) return;
      const todos = [...svg.querySelectorAll('.toque')];""")

# 2) el motor, antes de pintaPartida
MOTOR = """/* ==========================================================================
   MOVER Y AGRANDAR EL TABLERO (peticion de Pam: "que lo pueda manipular sobre
   la pantalla, hacer grande, chico")
   --------------------------------------------------------------------------
   Se hace moviendo el viewBox del SVG, NO con transform: scale().

   El motivo importa: los clics del tablero se resuelven con createSVGPoint() +
   getScreenCTM().inverse(), que traduce la posicion del dedo a coordenadas del
   SVG. Si escalo con transform:scale(), el navegador NO tiene eso en cuenta y
   los toques se descolocan: no habria forma de acertar a un cruce. Con el
   viewBox lo recalcula el propio navegador y todo sigue cuadrando.
   ========================================================================== */
let vbBase = null, vb = null, arrastrando = null, huboArrastre = false;
const punterosVb = {};

function cogeVb(){
  const svg = $('tablero');
  if (!svg) return null;
  const v = (svg.getAttribute('viewBox') || '0 0 466 500').split(/\\s+/).map(Number);
  if (!vbBase || Math.abs(vbBase[2] - v[2]) > 0.5){ vbBase = v.slice(); vb = v.slice(); }
  return v;
}
function ponVb(){
  const svg = $('tablero');
  if (svg && vb) svg.setAttribute('viewBox', vb.map(n => n.toFixed(2)).join(' '));
}
function zoomTab(f){
  if (!vb) cogeVb();
  if (!vbBase) return;
  const nw = Math.max(vbBase[2] * 0.3, Math.min(vbBase[2], vb[2] / f));
  const nh = nw * (vbBase[3] / vbBase[2]);
  const mx = vb[0] + vb[2] / 2, my = vb[1] + vb[3] / 2;
  vb = [mx - nw / 2, my - nh / 2, nw, nh];
  ponVb();
}
function resetTab(){ if (!vbBase) cogeVb(); if (vbBase) vb = vbBase.slice(); ponVb(); }

(function motorTablero(){
  const svg = $('tablero'), caja = $('mapaBox');
  if (!svg || !caja) return;
  if ($('zMas')){
    $('zMas').onclick   = e => { e.stopPropagation(); zoomTab(1.4); };
    $('zMenos').onclick = e => { e.stopPropagation(); zoomTab(1 / 1.4); };
    $('zReset').onclick = e => { e.stopPropagation(); resetTab(); };
  }
  /* la rueda del raton, para la compu */
  caja.addEventListener('wheel', e => {
    e.preventDefault();
    zoomTab(e.deltaY < 0 ? 1.12 : 1 / 1.12);
  }, { passive: false });

  caja.addEventListener('pointerdown', e => {
    punterosVb[e.pointerId] = { x: e.clientX, y: e.clientY };
    if (Object.keys(punterosVb).length === 1){
      const v0 = vb || cogeVb();
      arrastrando = v0 ? { x: e.clientX, y: e.clientY, vb0: v0.slice() } : null;
      huboArrastre = false;
    }
  });
  caja.addEventListener('pointermove', e => {
    if (!punterosVb[e.pointerId] || !arrastrando) return;
    punterosVb[e.pointerId] = { x: e.clientX, y: e.clientY };
    if (Object.keys(punterosVb).length >= 2) return;      /* con dos dedos, quieto */
    const r = svg.getBoundingClientRect();
    if (!r.width || !arrastrando.vb0.length) return;
    const mov = Math.abs(e.clientX - arrastrando.x) + Math.abs(e.clientY - arrastrando.y);
    if (mov > 7){ huboArrastre = true; caja.classList.add('arrastrando'); }
    const dx = (e.clientX - arrastrando.x) * arrastrando.vb0[2] / r.width;
    const dy = (e.clientY - arrastrando.y) * arrastrando.vb0[3] / r.height;
    vb = [arrastrando.vb0[0] - dx, arrastrando.vb0[1] - dy, arrastrando.vb0[2], arrastrando.vb0[3]];
    ponVb();
  });
  const suelta = e => {
    delete punterosVb[e.pointerId];
    arrastrando = null;
    caja.classList.remove('arrastrando');
    /* el onclick llega DESPUES del pointerup: doy un momento antes de limpiar */
    setTimeout(() => { huboArrastre = false; }, 120);
  };
  caja.addEventListener('pointerup', suelta);
  caja.addEventListener('pointercancel', suelta);
  caja.addEventListener('pointerleave', suelta);
})();

function pintaPartida(s){"""

rep("function pintaPartida(s){", MOTOR)

open(RUTA, 'w', encoding='utf-8').write(s)
print()
print('  cambios:', toc)
print('  archivo:', len(s), 'bytes')
