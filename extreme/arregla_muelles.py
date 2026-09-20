#!/usr/bin/env python3
"""EXTREME: el basecamp no se ve cuando cae en un muelle.

Pam: 'si alguien pone basecamp en los muelles, no se ve el basecamp'.

Eran DOS problemas, y los dos hacian falta:

1) EL ORDEN DE PINTADO. Las capas se añadian asi:
     capaPiezas   (basecamps, hubs, rutas)
     capaTocar    (los puntos donde tocas)
     capaOutposts (LOS MUELLES)   <- AL FINAL = ENCIMA DE TODO
   Los muelles se pintaban los ultimos, o sea por encima. Un muelle tiene r=11
   y relleno oscuro #2a1d12: si el basecamp caia ahi, lo tapaba entero.
   Ahora los muelles van al FONDO y las piezas encima. El muelle se sigue
   viendo (es mas grande que el basecamp), pero ya no se come nada.

2) EL TAMAÑO. El basecamp era r=8, el mas pequeño de TODO el tablero:
     basecamp  r=8
     hub       r=11
     muelle    r=11
     punto de toque r=13
   Un circulo de 8 de radio en un hexagono de 92 de ancho es un puntito: Pam lo
   llamaba "el puntito rojo". Ahora el basecamp es r=12 y el hub r=16, y los
   dos llevan un punto claro en el centro para que se lean como fichas.
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


# ==========================================================================
# 1) EL BASECAMP Y EL HUB, MAS GRANDES Y LEGIBLES
# ==========================================================================
rep("""    (pp.base||[]).forEach(b => {
      const [x,y] = b.k.split('#').slice(1);
      h += `<circle cx="${x}" cy="${y}" r="8" fill="${col.c}" stroke="#1a1009" stroke-width="2.4"/>`;
    });
    (pp.hub||[]).forEach(b => {
      const [x,y] = b.k.split('#').slice(1);
      h += `<circle cx="${x}" cy="${y}" r="11" fill="${col.c}" stroke="#f0d899" stroke-width="2.6"/>`;
    });""",
    """    /* EL BASECAMP: r=8 era el circulo mas pequeño del tablero (el muelle tiene
       11 y el punto de toque 13). En un hexagono de 92 de ancho eso es un
       puntito. Ahora r=12, con contorno oscuro grueso y un punto claro dentro,
       para que se lea como una ficha y no como una mota. */
    (pp.base||[]).forEach(b => {
      const [x,y] = b.k.split('#').slice(1);
      h += `<g class="fichaBase">
        <circle cx="${x}" cy="${y}" r="12" fill="${col.c}" stroke="#1a1009" stroke-width="3"/>
        <circle cx="${x}" cy="${y}" r="4.5" fill="#fff" opacity=".93"/>
      </g>`;
    });
    (pp.hub||[]).forEach(b => {
      const [x,y] = b.k.split('#').slice(1);
      h += `<g class="fichaHub">
        <circle cx="${x}" cy="${y}" r="16" fill="${col.c}" stroke="#1a1009" stroke-width="3.2"/>
        <circle cx="${x}" cy="${y}" r="9.5" fill="none" stroke="#f0d899" stroke-width="2.4"/>
        <circle cx="${x}" cy="${y}" r="3.5" fill="#fff" opacity=".93"/>
      </g>`;
    });""")

# ==========================================================================
# 2) LOS MUELLES, AL FONDO
# ==========================================================================
# primero: saco el bloque de los outposts de donde esta
BLOQUE = """  h += '<g class="capaOutposts">';
  OUTPOSTS.forEach(o => {
    const col = o.r ? (RECURSOS.find(x => x.id === o.r) || {}) : {};
    /* Los puertos estaban con r=15 encima de los cruces, y los puntos donde
       tocas son r=13: el puerto se los comia y no dejaba tocar el vertice.
       Ahora son mas pequeños, y ademas se ATENUAN cuando estas colocando, para
       que el circulo verde del cruce se vea por encima. */
    const atenuado = modo ? ' opacity=".32"' : '';
    h += `<g class="outpost"${atenuado}>
      <circle cx="${o.x.toFixed(1)}" cy="${o.y.toFixed(1)}" r="11"
        fill="#2a1d12" stroke="#c9a558" stroke-width="1.8"
        style="filter:drop-shadow(0 2px 5px rgba(0,0,0,.85))"/>
      <text x="${o.x.toFixed(1)}" y="${(o.y-0.5).toFixed(1)}" text-anchor="middle"
        style="font-family:Anton,sans-serif;font-size:9.5px;fill:#f0d899">${o.t}</text>
      ${o.r ? `<text x="${o.x.toFixed(1)}" y="${(o.y+9.5).toFixed(1)}" text-anchor="middle"
        style="font-family:Anton,sans-serif;font-size:7.5px;fill:#fff">${(col.n||'').slice(0,4)}</text>` : ''}
    </g>`;
  });
  h += '</g>';
"""

NUEVO = """  /* ===== LOS MUELLES, AL FONDO =====
     Pam: "si alguien pone basecamp en los muelles, no se ve el basecamp".
     Pasaba porque esta capa se añadia la ULTIMA, o sea que se pintaba ENCIMA
     de las piezas: un muelle tiene r=11 con relleno oscuro, y un basecamp que
     cayera ahi quedaba enterrado debajo. Ahora los muelles son el FONDO del
     tablero y las piezas van encima. El muelle se sigue viendo perfectamente
     (es una pieza del tablero, no un adorno), pero ya no se come nada. */
  h += '<g class="capaOutposts">';
  OUTPOSTS.forEach(o => {
    const col = o.r ? (RECURSOS.find(x => x.id === o.r) || {}) : {};
    /* y se ATENUAN cuando estas colocando, para que se vea el cruce */
    const atenuado = modo ? ' opacity=".38"' : '';
    h += `<g class="outpost"${atenuado}>
      <circle cx="${o.x.toFixed(1)}" cy="${o.y.toFixed(1)}" r="10"
        fill="#2a1d12" stroke="#c9a558" stroke-width="1.8"
        style="filter:drop-shadow(0 2px 5px rgba(0,0,0,.85))"/>
      <text x="${o.x.toFixed(1)}" y="${(o.y-0.5).toFixed(1)}" text-anchor="middle"
        style="font-family:Anton,sans-serif;font-size:9px;fill:#f0d899">${o.t}</text>
      ${o.r ? `<text x="${o.x.toFixed(1)}" y="${(o.y+8.5).toFixed(1)}" text-anchor="middle"
        style="font-family:Anton,sans-serif;font-size:7px;fill:#fff">${(col.n||'').slice(0,4)}</text>` : ''}
    </g>`;
  });
  h += '</g>';
"""

# lo quito de su sitio
if BLOQUE in s:
    s = s.replace(BLOQUE, "", 1)
    toc += 1
    print('  bloque de muelles extraido')
else:
    print('  NO ENCUENTRO el bloque de muelles para extraerlo')

# y lo pongo AL PRINCIPIO, antes de la capa de piezas
rep("""  let h = '<g class="capaPiezas">';""",
    NUEVO + """  /* ===== Y LAS PIEZAS, ENCIMA DE LOS MUELLES ===== */
  let h = '<g class="capaPiezas">';""")

open(RUTA, 'w', encoding='utf-8').write(s)
print()
print('  cambios:', toc)
print('  archivo:', len(s), 'bytes')
