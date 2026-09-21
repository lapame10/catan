#!/usr/bin/env python3
"""EXTREME: las dos cartas de aventura que no funcionan.

Pam:
 a) "cuando me salen dos rutas gratis, no me deja usarlas, solo me quita la
    card pero no las puedo usar"
 b) "cuando me sale las dos cartas de recurso me deberia dejar escoger las 2
    cartas que yo quiera"

LO QUE ENCONTRE:

 a) El mecanismo de gratis SI existe: al jugar la carta se pone g[yo.id] += 2, y
    al colocar una Ruta se mira 'esGratis' para no cobrarla. El problema es que
    DESPUES de jugar la carta NO se activa el modo ruta: no salen los circulos
    donde tocar, asi que parece que la carta se ha perdido. Hay que llamar a
    ponModo('camino') al jugarla.

 b) La carta 'perfectas' da DOS RECURSOS AL AZAR:
        const r = ids[Math.floor(Math.random()*ids.length)];
    Pam quiere elegir cuales. Se cambia por un panel donde toca los dos que
    quiera.
"""
RUTA = '/Users/lapame10/.hermes/workspace/catan/extreme/index.html'
s = open(RUTA, encoding='utf-8').read()
toc = 0


def rep(v, n):
    global s, toc
    if v in s:
        s = s.replace(v, n, 1); toc += 1
        return True
    print('  NO ENCUENTRO:', v[:72].replace('\n', ' | '))
    return False


# ==========================================================================
# a) LAS DOS RUTAS GRATIS: activar el modo ruta al jugar la carta
# ==========================================================================
rep("""    if (tipo === 'rutas'){
      const g = Object.assign({}, s.gratis || {});
      g[yo.id] = (g[yo.id] || 0) + 2; upd.gratis = g;
    }""",
    """    if (tipo === 'rutas'){
      const g = Object.assign({}, s.gratis || {});
      g[yo.id] = (g[yo.id] || 0) + 2; upd.gratis = g;
    }""")

# el aviso que se enseña al jugarla
rep("""    aviso(CARTA_AV[tipo].ic + ' ' + CARTA_AV[tipo].n,
          tipo === 'heli' ? 'Toca un terreno para llevar allí el Mal Tiempo.' : 'Hecho.', 4200);""",
    """    aviso(CARTA_AV[tipo].ic + ' ' + CARTA_AV[tipo].n,
          tipo === 'heli' ? 'Toca un terreno para llevar allí el Mal Tiempo.'
        : tipo === 'rutas' ? 'Se activa el modo RUTA. Toca el tablero para ponerlas — no te costarán nada.'
        : tipo === 'perfectas' ? 'Elige las 2 cartas que quieras.'
        : 'Hecho.', 4200);""")

# y el modo, despues de guardar
rep("""    di('ha jugado ' + CARTA_AV[tipo].ic + ' ' + CARTA_AV[tipo].n);
    revisaLogros(await leerSala(salaCod));""",
    """    di('ha jugado ' + CARTA_AV[tipo].ic + ' ' + CARTA_AV[tipo].n);
    /* ===== DOS RUTAS GRATIS: hay que PONER EL MODO =====
       Pam: "no me deja usarlas, solo me quita la card". El descuento del precio
       ya funcionaba, pero al no activar el modo 'camino' no salian los circulos
       donde tocar, asi que la carta parecia perdida. */
    if (tipo === 'rutas' && typeof ponModo === 'function') ponModo('camino');
    revisaLogros(await leerSala(salaCod));""")

# ==========================================================================
# b) CONDICIONES PERFECTAS: elegir los 2 recursos
# ==========================================================================
rep("""    if (tipo === 'perfectas'){
      for (let k = 0; k < 2; k++){
        const r = ids[Math.floor(Math.random()*ids.length)];
        rec[yo.id][r] = (rec[yo.id][r] || 0) + 1;
      }
      upd.recursos = rec;
    }""",
    """    if (tipo === 'perfectas'){
      /* ANTES: dos recursos al AZAR (Math.random). Pam: "me deberia dejar
         escoger las 2 cartas que yo quiera". Ahora se guarda la eleccion
         pendiente y sale un panel para que toque las dos. */
      upd.eligeRec = { id: yo.id, cuantos: 2, cogidas: {} };
    }""")

# ==========================================================================
# EL PANEL PARA ELEGIR LOS RECURSOS + el motor
# ==========================================================================
rep("""/* los botones del panel son HTML con onclick=, y esta funcion vive dentro de un
   modulo: hay que exponerla en window o el navegador no la encuentra. */
window.eligeRecurso = eligeRecurso;

/* ==========================================================================
   MOVER Y AGRANDAR EL TABLERO (peticion de Pam)""",
    """/* ==========================================================================
   ELEGIR RECURSOS ("Condiciones perfectas": 2 cartas de recurso a elegir)
   --------------------------------------------------------------------------
   Antes la carta daba 2 recursos AL AZAR. Pam quiere elegirlos. Mientras hay
   una eleccion pendiente, sale un panel con los 5 recursos y lo que ya llevas.
   ========================================================================== */
async function eligeRecurso(rid){
  const s = await leerSala(salaCod);
  if (!s || !s.eligeRec || s.eligeRec.id !== yo.id) return;
  const e = JSON.parse(JSON.stringify(s.eligeRec));
  e.cogidas = e.cogidas || {};
  const llevo = Object.values(e.cogidas).reduce((a, b) => a + b, 0);
  if (llevo >= e.cuantos) return;
  e.cogidas[rid] = (e.cogidas[rid] || 0) + 1;
  const ya = Object.values(e.cogidas).reduce((a, b) => a + b, 0);
  if (ya >= e.cuantos){
    /* ya estan las dos: las sumo y cierro la eleccion */
    const rec = JSON.parse(JSON.stringify(s.recursos || {}));
    rec[yo.id] = rec[yo.id] || {};
    Object.entries(e.cogidas).forEach(([k, v]) => { rec[yo.id][k] = (rec[yo.id][k] || 0) + v; });
    await update(ref(db,'extreme/salas/'+salaCod), { recursos: rec, eligeRec: null });
    aviso('🌤️ Condiciones perfectas',
      'Te llevas: ' + Object.entries(e.cogidas).map(([k, v]) => v + ' ' + k.toUpperCase()).join(', '), 4200);
  } else {
    await update(ref(db,'extreme/salas/'+salaCod), { eligeRec: e });
  }
}

/* ==========================================================================
   MOVER Y AGRANDAR EL TABLERO (peticion de Pam)""")

# el pintado del panel, dentro de pintaPartida
rep("""  pintaOfertas(s);
  const svg = $('tablero');""",
    """  pintaOfertas(s);
  pintaEligeRec(s);
  const svg = $('tablero');""")

# y la funcion que lo pinta
rep("""async function eligeRecurso(rid){""",
    """function pintaEligeRec(s){
  const el = $('eligeRec');
  if (!el) return;
  const e = s.eligeRec;
  if (!e || e.id !== yo.id){ el.classList.remove('on'); return; }
  const cogidas = e.cogidas || {};
  const llevo = Object.values(cogidas).reduce((a, b) => a + b, 0);
  el.classList.add('on');
  el.innerHTML =
    '<div class="panelTit">🌤️ Condiciones perfectas</div>' +
    '<div class="panelSub">Elige <b>' + e.cuantos + '</b> cartas de recurso. Llevas <b>' +
      llevo + ' de ' + e.cuantos + '</b>.</div>' +
    '<div class="eligeFila">' +
      RECURSOS.map(c => {
        const n = cogidas[c.id] || 0;
        return '<button class="eligeBtn' + (n ? ' on' : '') + '" onclick="eligeRecurso(\\'' + c.id + '\\')">' +
          '<img src="' + c.mini + '" alt="' + c.n + '">' +
          '<em style="color:' + c.col + '">' + c.n + '</em>' +
          (n ? '<b>' + n + '</b>' : '') + '</button>';
      }).join('') +
    '</div>';

}

async function eligeRecurso(rid){""")

# el HTML del panel
rep("""    <div class="mapa" id="mapaBox"><svg id="tablero" viewBox="0 0 466 500"></svg></div>""",
    """    <div class="eligerec" id="eligeRec" style="position:fixed;left:0;right:0;bottom:0;z-index:40"></div>

    <div class="mapa" id="mapaBox"><svg id="tablero" viewBox="0 0 466 500"></svg></div>""")

# el CSS
rep("""  .mapa.arrastrando svg{cursor:grabbing}""",
    """  /* el panel para elegir recursos */
  .eligerec{display:none;background:rgba(20,14,8,.97);border-top:2px solid #c9a558;
    padding:12px 12px calc(12px + env(safe-area-inset-bottom));text-align:center;
    box-shadow:0 -8px 30px rgba(0,0,0,.7)}
  .eligerec.on{display:block}
  .panelTit{font-family:Anton,sans-serif;font-size:17px;color:#f0d899;letter-spacing:.5px}
  .panelSub{font-size:12.5px;color:#e8dcc0;margin:5px 0 11px;line-height:1.5}
  .panelSub b{color:#f0d899}
  .eligeFila{display:flex;gap:8px;justify-content:center;flex-wrap:wrap}
  .eligeBtn{position:relative;background:rgba(255,255,255,.05);border:2px solid #3a2b1c;
    border-radius:12px;padding:7px 9px 5px;cursor:pointer;display:flex;flex-direction:column;
    align-items:center;gap:3px;font-family:inherit;min-width:62px}
  .eligeBtn.on{border-color:#5df08a;background:rgba(93,240,138,.15)}
  .eligeBtn img{width:30px;height:30px;border-radius:50%;display:block}
  .eligeBtn em{font-style:normal;font-family:Anton,sans-serif;font-size:9.5px;letter-spacing:.3px}
  .eligeBtn b{position:absolute;top:-6px;right:-6px;background:#5df08a;color:#10240f;
    font-size:12px;width:19px;height:19px;border-radius:50%;display:flex;
    align-items:center;justify-content:center}
  .mapa.arrastrando svg{cursor:grabbing}""")

open(RUTA, 'w', encoding='utf-8').write(s)
print()
print('  cambios:', toc)
print('  archivo:', len(s), 'bytes')
