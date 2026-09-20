#!/usr/bin/env python3
"""EXTREME: los 4 arreglos que pide Pam.

Pam:
 1) "los colores no quedaron correctamente"  -> los hexagonos COMPARTEN bordes,
    asi que un aro centrado en el trazo pisa al vecino y la frontera es del
    color del ultimo pintado. Cada hexagono no tiene "su" borde. Se arregla
    RECORTANDO el aro con el clipPath del propio hexagono: asi queda por dentro
    y no invade al vecino.
 2) "me gustaria tener como movilidad en el tablero, que lo pueda manipular
    sobre la pantalla, hacer grande, chico"  -> zoom + arrastre.
    CLAVE: se hace moviendo el viewBox del SVG, NO con transform: scale(). Con
    viewBox el navegador recalcula solo la posicion de los clics, asi que
    seguir tocando los cruces funciona. Con transform:scale() los toques se
    descolocan y no habria forma de poner nada.
 3) "que los puertos no tapen el vertice"  -> eran circulos de r=15 justo
    encima de los cruces, y los puntos donde tocas son de r=13: el puerto se
    los comia. Ahora son mas pequeños y se atenuan cuando estas colocando.
 4) y el tablero "no se ve" -> con max-height:62vh en un movil queda pequeñisimo.
    Con el zoom ya se puede agrandar, y ademas le doy mas alto.
"""
RUTA = '/Users/lapame10/.hermes/workspace/catan/extreme/index.html'
s = open(RUTA, encoding='utf-8').read()
toc = 0


def rep(v, n, todas=False):
    global s, toc
    if v in s:
        s = s.replace(v, n) if todas else s.replace(v, n, 1)
        toc += 1
        return True
    print('  NO ENCUENTRO:', v[:70].replace('\n', ' | '))
    return False


# ==========================================================================
# 1) EL ARO DEL COLOR, RECORTADO AL HEXAGONO
# ==========================================================================
rep("""    const colRec = (RECURSOS.find(r => r.id === x.rec) || {}).col || '#5f584e';
    h += `<path d="${pathHex(x.cx,x.cy)}" fill="none" stroke="${colRec}"
           stroke-width="7" stroke-linejoin="round" opacity=".95"/>`;
    h += `<path d="${pathHex(x.cx,x.cy)}" fill="none" stroke="#1a1009" stroke-width="2.2" stroke-linejoin="round"/>`;""",
    """    /* ===== EL BORDE, DEL COLOR DEL RECURSO QUE DA =====
       Los hexagonos COMPARTEN los bordes. Un aro centrado en el trazo se mete
       en el vecino y gana el ultimo que se pinta: por eso la frontera entre un
       hexagono morado y uno azul salia de un color u otro al azar, y parecia
       que "los colores no quedaron bien".
       Solucion: recortar el aro con el clipPath del PROPIO hexagono. Asi el
       aro queda por DENTRO y cada hexagono tiene su borde limpio, sin pisar
       al de al lado. El clipPath ya existe (se define mas arriba). */
    const colRec = (RECURSOS.find(r => r.id === x.rec) || {}).col || '#5f584e';
    h += `<path d="${pathHex(x.cx,x.cy)}" fill="none" stroke="${colRec}"
           stroke-width="10" stroke-linejoin="round"
           clip-path="url(#c${x.id})"/>`;
    /* y la junta oscura, encima y mas fina, para que se vea donde acaba cada uno */
    h += `<path d="${pathHex(x.cx,x.cy)}" fill="none" stroke="#1a1009" stroke-width="2" stroke-linejoin="round"/>`;""")

# ==========================================================================
# 2) LOS PUERTOS MAS PEQUEÑOS Y ATENUADOS AL COLOCAR
# ==========================================================================
rep("""    h += `<g class="outpost">
      <circle cx="${o.x.toFixed(1)}" cy="${o.y.toFixed(1)}" r="15"
        fill="#2a1d12" stroke="#c9a558" stroke-width="2.2"
        style="filter:drop-shadow(0 2px 5px rgba(0,0,0,.85))"/>""",
    """    /* Los puertos estaban con r=15 encima de los cruces, y los puntos donde
       tocas son r=13: el puerto se los comia y no dejaba tocar el vertice.
       Ahora son mas pequeños, y ademas se ATENUAN cuando estas colocando, para
       que el circulo verde del cruce se vea por encima. */
    const atenuado = modo ? ' opacity=".32"' : '';
    h += `<g class="outpost"${atenuado}>
      <circle cx="${o.x.toFixed(1)}" cy="${o.y.toFixed(1)}" r="11"
        fill="#2a1d12" stroke="#c9a558" stroke-width="1.8"
        style="filter:drop-shadow(0 2px 5px rgba(0,0,0,.85))"/>""")

rep("""      <text x="${o.x.toFixed(1)}" y="${(o.y-1).toFixed(1)}" text-anchor="middle"
        style="font-family:Anton,sans-serif;font-size:11px;fill:#f0d899">${o.t}</text>""",
    """      <text x="${o.x.toFixed(1)}" y="${(o.y-0.5).toFixed(1)}" text-anchor="middle"
        style="font-family:Anton,sans-serif;font-size:9.5px;fill:#f0d899">${o.t}</text>""")

# ==========================================================================
# 3) EL MAPA: mas alto, y con el mando de zoom
# ==========================================================================
rep("""  .mapa{width:100%;display:block;position:relative;margin:2px 0 0}
  .mapa svg{width:100%;display:block;max-height:62vh}""",
    """  .mapa{width:100%;display:block;position:relative;margin:2px 0 0;touch-action:none}
  .mapa svg{width:100%;display:block;max-height:74vh}
  /* el mando para mover y agrandar el tablero (peticion de Pam) */
  .zoomMando{position:absolute;right:6px;top:6px;display:flex;flex-direction:column;
    gap:6px;z-index:6}
  .zoomMando button{width:38px;height:38px;border-radius:10px;border:1.5px solid #c9a558;
    background:rgba(26,18,11,.85);color:#f0d899;font-size:20px;font-weight:800;
    cursor:pointer;display:flex;align-items:center;justify-content:center;
    font-family:inherit;padding:0;line-height:1;touch-action:manipulation}
  .zoomMando button:active{background:rgba(201,165,88,.35)}
  .mapa.arrastrando svg{cursor:grabbing}
  .mapa svg{cursor:grab}""")

rep("""    <div class="mapa"><svg id="tablero" viewBox="0 0 466 500"></svg></div>""",
    """    <div class="mapa" id="mapaBox"><svg id="tablero" viewBox="0 0 466 500"></svg>
      <div class="zoomMando">
        <button id="zMas" title="Agrandar">+</button>
        <button id="zMenos" title="Encoger">−</button>
        <button id="zReset" title="Ver todo">⟲</button>
      </div>
    </div>""")

# ==========================================================================
# 4) EL MOTOR DEL ZOOM Y EL ARRASTRE
# ==========================================================================
rep("""    svg.onclick = (e) => {
      const todos = [...svg.querySelectorAll('.toque')];
      if (!todos.length) return;""",
    """    /* los puertos se atenuan mientras colocas, asi que hay que repintar al
       cambiar de modo. Eso ya lo hace ponModo() llamando a pintaPartida(). */

    svg.onclick = (e) => {
      /* si acabas de ARRASTRAR el tablero, el toque no cuenta: si no, cada vez
         que mueves el mapa colocarias una pieza sin querer */
      if (huboArrastre) return;
      const todos = [...svg.querySelectorAll('.toque')];
      if (!todos.length) return;""")

rep("""/* ---------- el archivo IGC ---------- */""",
    """/* ==========================================================================
   MOVER Y AGRANDAR EL TABLERO (peticion de Pam)
   --------------------------------------------------------------------------
   Se hace moviendo el viewBox del SVG, NO con transform: scale().

   El motivo importa: los clics se resuelven con createSVGPoint() +
   getScreenCTM().inverse(), que traduce la posicion del dedo a coordenadas del
   SVG. Si escalo con transform:scale(), el navegador NO tiene eso en cuenta y
   los toques se descolocan: no habria forma de acertar a un cruce. Con el
   viewBox, el propio navegador recalcula, y todo sigue cuadrando.
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
    if (!e.ctrlKey && Math.abs(e.deltaY) < 2) return;
    e.preventDefault();
    zoomTab(e.deltaY < 0 ? 1.12 : 1 / 1.12);
  }, { passive: false });

  caja.addEventListener('pointerdown', e => {
    punterosVb[e.pointerId] = { x: e.clientX, y: e.clientY };
    if (Object.keys(punterosVb).length === 1){
      arrastrando = { x: e.clientX, y: e.clientY, vb0: (vb || cogeVb() || []).slice() };
      huboArrastre = false;
    }
  });
  caja.addEventListener('pointermove', e => {
    if (!punterosVb[e.pointerId] || !arrastrando) return;
    punterosVb[e.pointerId] = { x: e.clientX, y: e.clientY };
    if (Object.keys(punterosVb).length >= 2) return;      /* dos dedos: lo dejo */
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

/* ---------- el archivo IGC ---------- */""")

open(RUTA, 'w', encoding='utf-8').write(s)
print()
print('  cambios:', toc)
print('  archivo:', len(s), 'bytes')
