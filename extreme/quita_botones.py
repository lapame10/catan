#!/usr/bin/env python3
"""Quita los botones de zoom (Pam: "solo quitame los botones de zoom").

Pero NO se queda sin zoom: el zoom pasa a hacerlo con DOS DEDOS (pellizcar),
que es lo natural en un movil y no ocupa nada en pantalla. El arrastre con un
dedo se queda, y la rueda del raton en la compu tambien.

Los botones tapaban el tablero justo en la esquina donde esta el panel de
recursos, y para colocar la primera pieza molestaban mas que ayudaban.
"""
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


# 1) fuera el HTML de los botones
rep("""    <div class="mapa" id="mapaBox"><svg id="tablero" viewBox="0 0 466 500"></svg>
      <div class="zoomMando">
        <button id="zMas" title="Agrandar">+</button>
        <button id="zMenos" title="Encoger">−</button>
        <button id="zReset" title="Ver todo">⟲</button>
      </div>
    </div>""",
    """    <div class="mapa" id="mapaBox"><svg id="tablero" viewBox="0 0 466 500"></svg></div>""")

# 2) fuera el CSS de los botones
rep("""  /* el mando para mover y agrandar el tablero (peticion de Pam) */
  .zoomMando{position:absolute;right:6px;top:6px;display:flex;flex-direction:column;
    gap:6px;z-index:6}
  .zoomMando button{width:38px;height:38px;border-radius:10px;border:1.5px solid #c9a558;
    background:rgba(26,18,11,.85);color:#f0d899;font-size:20px;font-weight:800;
    cursor:pointer;display:flex;align-items:center;justify-content:center;
    font-family:inherit;padding:0;line-height:1;touch-action:manipulation}
  .zoomMando button:active{background:rgba(201,165,88,.35)}
  .mapa.arrastrando svg{cursor:grabbing}
  .mapa svg{cursor:grab}""",
    """  .mapa.arrastrando svg{cursor:grabbing}
  .mapa svg{cursor:grab}""")

# 3) el motor: sin botones, y con pellizco de dos dedos
rep("""(function motorTablero(){
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
})();""",
    """/* la distancia entre dos dedos, y su punto medio */
function dosDedos(){
  const ids = Object.keys(punterosVb);
  if (ids.length < 2) return null;
  const a = punterosVb[ids[0]], b = punterosVb[ids[1]];
  return { d: Math.hypot(a.x - b.x, a.y - b.y), mx: (a.x + b.x) / 2, my: (a.y + b.y) / 2 };
}

(function motorTablero(){
  const svg = $('tablero'), caja = $('mapaBox');
  if (!svg || !caja) return;

  /* la rueda del raton, para la compu */
  caja.addEventListener('wheel', e => {
    e.preventDefault();
    zoomTab(e.deltaY < 0 ? 1.12 : 1 / 1.12);
  }, { passive: false });

  caja.addEventListener('pointerdown', e => {
    punterosVb[e.pointerId] = { x: e.clientX, y: e.clientY };
    const n = Object.keys(punterosVb).length;
    if (n === 1){
      const v0 = vb || cogeVb();
      arrastrando = v0 ? { x: e.clientX, y: e.clientY, vb0: v0.slice() } : null;
      huboArrastre = false;
    } else {
      /* DOS DEDOS = pellizcar para agrandar. Dejo de arrastrar y guardo el
         tamaño de partida, para medir cuanto han abierto o cerrado. */
      arrastrando = null;
      huboArrastre = true;                  /* que el toque no coloque pieza */
      const v0 = vb || cogeVb();
      if (v0) pinch0 = { d: (dosDedos() || {}).d || 0, vb: v0.slice() };
    }
  });

  caja.addEventListener('pointermove', e => {
    if (!punterosVb[e.pointerId]) return;
    punterosVb[e.pointerId] = { x: e.clientX, y: e.clientY };

    /* --- con dos dedos: pellizcar --- */
    if (Object.keys(punterosVb).length >= 2){
      const p = dosDedos();
      if (!pinch0 || !pinch0.d) return;
      const f = p.d / pinch0.d;
      const nw = Math.max(vbBase[2] * 0.3, Math.min(vbBase[2], pinch0.vb[2] / f));
      const nh = nw * (vbBase[3] / vbBase[2]);
      const cx = pinch0.vb[0] + pinch0.vb[2] / 2;
      const cy = pinch0.vb[1] + pinch0.vb[3] / 2;
      vb = [cx - nw / 2, cy - nh / 2, nw, nh];
      ponVb();
      return;
    }

    /* --- con un dedo: arrastrar --- */
    if (!arrastrando) return;
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
    /* si quedan dos dedos (soltaste uno de tres), vuelvo a medir */
    if (Object.keys(punterosVb).length >= 2){
      const v0 = vb || cogeVb();
      if (v0) pinch0 = { d: (dosDedos() || {}).d || 0, vb: v0.slice() };
    } else {
      pinch0 = null;
    }
    arrastrando = null;
    caja.classList.remove('arrastrando');
    /* el onclick llega DESPUES del pointerup: doy un momento antes de limpiar */
    setTimeout(() => { huboArrastre = false; }, 120);
  };
  caja.addEventListener('pointerup', suelta);
  caja.addEventListener('pointercancel', suelta);
  caja.addEventListener('pointerleave', suelta);
})();""")

# 4) la variable del pellizco
rep("""let vbBase = null, vb = null, arrastrando = null, huboArrastre = false;""",
    """let vbBase = null, vb = null, arrastrando = null, huboArrastre = false, pinch0 = null;""")

open(RUTA, 'w', encoding='utf-8').write(s)
print()
print('  cambios:', toc)
print('  archivo:', len(s), 'bytes')
