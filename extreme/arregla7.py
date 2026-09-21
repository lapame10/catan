#!/usr/bin/env python3
"""EXTREME: terminar lo que falta. Los 4 problemas de Pam.

Ya aplicado antes: ponModo('camino') al jugar la carta de rutas, y el panel
eligeRec. Falta:
  1) el cambio de 'perfectas' (la indentacion real son 2 espacios, no 4)
  2) exponer eligeRecurso en window (vive en un modulo y los onclick son HTML)
  3) el aviso que le dice a Pam que se activo el modo ruta
  4) EL 7: el descarte de la mitad, eligiendo TU cuales devuelves
  5) EL 7: elegir a QUIEN le robas (antes robaba a todos)
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
# 1) CONDICIONES PERFECTAS — con la indentacion REAL (2 espacios)
# ==========================================================================
rep("""  if (tipo === 'perfectas'){
    for (let k = 0; k < 2; k++){
      const r = ids[Math.floor(Math.random()*ids.length)];
      rec[yo.id][r] = (rec[yo.id][r] || 0) + 1;
    }
    upd.recursos = rec;
  }""",
    """  if (tipo === 'perfectas'){
    /* ANTES: dos recursos al AZAR (Math.random). Pam: "me deberia dejar escoger
       las 2 cartas que yo quiera". Ahora queda la eleccion pendiente y sale un
       panel para que toque las dos. */
    upd.eligeRec = { id: yo.id, cuantos: 2, cogidas: {} };
  }""")

# ==========================================================================
# 2) exponer eligeRecurso en window
# ==========================================================================
rep("""  pintaOfertas(s);
  pintaEligeRec(s);""",
    """  pintaOfertas(s);
  pintaEligeRec(s);
  pintaDescarte(s);""")

rep("""/* ==========================================================================
   MOVER Y AGRANDAR EL TABLERO (peticion de Pam)""",
    """/* los botones que genero son HTML con onclick=, y estas funciones viven dentro
   de un modulo: hay que exponerlas en window o el navegador no las encuentra. */
window.eligeRecurso = eligeRecurso;
window.descElegir = descElegir;
window.descEntregar = descEntregar;
window.robaA = robaA;

/* ==========================================================================
   MOVER Y AGRANDAR EL TABLERO (peticion de Pam)""")

# ==========================================================================
# 3) el aviso al jugar la carta de rutas
# ==========================================================================
rep("""  aviso(CARTA_AV[tipo].ic + ' ' + CARTA_AV[tipo].n, 'Te ha tocado: ' + CARTA_AV[tipo].d, 4200);""",
    """  aviso(CARTA_AV[tipo].ic + ' ' + CARTA_AV[tipo].n, 'Te ha tocado: ' + CARTA_AV[tipo].d, 4200);""")

# ==========================================================================
# 4) EL 7: EL DESCARTE
# ==========================================================================
rep("""  if (total === 7){
    await update(ref(db,'extreme/salas/'+salaCod), { dados: { d1, d2, total }, mueveElClima: yo.id });
    aviso('🌩️ 7 — ¡MAL TIEMPO!', 'Nadie cobra. <b>Toca un terreno</b> para llevar allí el Mal Tiempo.', 5200);
    return;
  }""",
    """  if (total === 7){
    /* ===== EL DESCARTE DEL 7 (peticion de Pam) =====
       "quien tenga mas de 7 cartas tiene que regresar la mitad al banco, y si es
       numero par es menos uno, por ejemplo si tienes 11 regresas 5".
       Eso es exactamente la regla oficial: la mitad REDONDEANDO HACIA ABAJO.
       Y Pam añadio: "que tu puedas elegir" y "que puedas ver cuantos [tienes
       de] cada cosa". Asi que no se descarta solo: se guarda quien debe y
       cuanto, y sale un panel para que cada uno elija. */
    const desc = {};
    let totalCartas = 0;
    Object.entries(rec).forEach(([id, r]) => {
      const n = Object.values(r || {}).reduce((a, b) => a + b, 0);
      totalCartas += n;
      if (n > 7) desc[id] = Math.floor(n / 2);
    });
    const deben = Object.keys(desc);
    /* el Mal Tiempo solo se puede mover cuando todos hayan entregado */
    await update(ref(db,'extreme/salas/'+salaCod), {
      dados: { d1, d2, total },
      descarte: desc,
      descarteHecho: {},
      mueveElClima: deben.length ? null : yo.id
    });
    aviso('🌩️ 7 — ¡MAL TIEMPO!',
      deben.length
        ? (deben.length === 1 ? 'Uno tiene' : deben.length + ' tienen') +
          ' más de 7 cartas y devuelven la mitad al banco.'
        : 'Nadie tiene más de 7 cartas. <b>Toca un terreno</b> para llevar allí el Mal Tiempo.',
      5200);
    return;
  }""")

# ==========================================================================
# 5) EL 7: ELEGIR A QUIEN LE ROBAS
# ==========================================================================
rep("""  const rec = JSON.parse(JSON.stringify(s.recursos || {}));
  rec[yo.id] = rec[yo.id] || {};
  const robadas = [];
  Object.keys(s.jugadores || {}).forEach(id => {
    if (id === yo.id) return;
    if (!tocaHex((s.piezas || {})[id], idx)) return;
    rec[id] = Object.assign({}, rec[id] || {});
    const tengo = Object.entries(rec[id]).filter(([k, v]) => v > 0);
    if (!tengo.length) return;
    const [rk] = tengo[Math.floor(Math.random()*tengo.length)];
    rec[id][rk] -= 1;
    rec[yo.id][rk] = (rec[yo.id][rk] || 0) + 1;
    robadas.push(((s.jugadores || {})[id] || {}).nombre + ': 1 ' + rk.toUpperCase());
  });
  await update(ref(db,'extreme/salas/'+salaCod), { clima: idx, mueveElClima: null, recursos: rec });
  aviso('🌩️ Mal Tiempo movido',
        (s.hexes && s.hexes[idx] ? 'Ahora está en <b>' + (TERR[(s.hexes[idx] || {}).rec] || '') + '</b>.' : '') +
        (robadas.length ? '<br>Le robaste: ' + robadas.join(' · ') : '<br>No había nadie allí.'), 4600);""",
    """  /* ===== A QUIEN LE ROBAS (peticion de Pam) =====
     "cuando toca 7 si hay mas de un basecamp, solo le puedes quitar a una
     persona un recurso, puedes elegir a quien".
     Antes el codigo recorria TODOS los que tuvieran pieza alli y le robaba a
     cada uno. En el Catan de verdad robas UNA carta a UN jugador, y el que
     mueve el Mal Tiempo ELIGE a cual. Asi que ahora: si hay uno solo, se roba
     directo; si hay dos o mas, sale un panel para elegir. */
  const candidatos = Object.keys(s.jugadores || {}).filter(id => {
    if (id === yo.id) return false;
    if (!tocaHex((s.piezas || {})[id], idx)) return false;
    const r = (s.recursos || {})[id] || {};
    return Object.values(r).reduce((a, b) => a + b, 0) > 0;
  });

  if (candidatos.length === 0){
    await update(ref(db,'extreme/salas/'+salaCod), { clima: idx, mueveElClima: null });
    aviso('🌩️ Mal Tiempo movido',
          (s.hexes && s.hexes[idx] ? 'Ahora está en <b>' + (TERR[(s.hexes[idx] || {}).rec] || '') + '</b>.' : '') +
          '<br>No había nadie allí.', 4600);
    return;
  }
  if (candidatos.length === 1){
    await robaA(candidatos[0], idx);
    return;
  }
  /* dos o mas: que elija */
  await update(ref(db,'extreme/salas/'+salaCod), { clima: idx, robaDe: { id: yo.id, hex: idx, quienes: candidatos } });
  aviso('🌩️ ¿A quién le robas?', 'Hay más de uno ahí. <b>Elige abajo</b>.', 4600);""")

# y la funcion que roba a uno
rep("""/* ===== LOS LOGROS Y EL GANADOR =====""",
    """/* roba UNA carta a UN jugador concreto (el que Pam haya elegido) */
async function robaA(victima, idx){
  const s = await leerSala(salaCod);
  if (!s || s.mueveElClima !== yo.id) return;
  const rec = JSON.parse(JSON.stringify(s.recursos || {}));
  rec[yo.id] = rec[yo.id] || {};
  rec[victima] = Object.assign({}, rec[victima] || {});
  const tengo = Object.entries(rec[victima]).filter(([k, v]) => v > 0);
  let robada = null;
  if (tengo.length){
    const [rk] = tengo[Math.floor(Math.random()*tengo.length)];
    rec[victima][rk] -= 1;
    rec[yo.id][rk] = (rec[yo.id][rk] || 0) + 1;
    robada = rk;
  }
  await update(ref(db,'extreme/salas/'+salaCod),
    { mueveElClima: null, robaDe: null, recursos: rec });
  const nom = ((s.jugadores || {})[victima] || {}).nombre || '?';
  aviso('🌩️ Mal Tiempo movido',
        'Ahora está en <b>' + (TERR[((s.hexes || {})[idx] || {}).rec] || '') + '</b>.<br>' +
        (robada ? 'Le robaste <b>1 ' + robada.toUpperCase() + '</b> a ' + nom : nom + ' no tenía cartas.'), 4600);
}

/* ===== EL DESCARTE DEL 7: el panel para elegir =====
   Pam: "que tu puedas elegir" y "que puedas ver cuantos [tienes de] cada cosa".
   Cada fila enseña el recurso, cuantas TIENES y cuantas vas a devolver, con
   botones - y +. El boton de entregar se activa solo cuando cuadra. */
const descLlevo = {};

function pintaDescarte(s){
  const el = $('descarte');
  if (!el) return;
  const debo = ((s.descarte || {})[yo.id]) || 0;
  const hecho = (s.descarteHecho || {})[yo.id];
  if (!debo || hecho){ el.classList.remove('on'); descLlevo.total = 0; return; }
  const mis = (s.recursos || {})[yo.id] || {};
  /* al abrir, empiezo de cero */
  if (descLlevo.para !== debo){ descLlevo.para = debo; descLlevo.pick = {}; }
  const pick = descLlevo.pick || (descLlevo.pick = {});
  const llevo = Object.values(pick).reduce((a, b) => a + b, 0);
  const listo = llevo === debo;
  el.classList.add('on');
  el.innerHTML =
    '<div class="panelTit">🌩️ 7 — devuelve ' + debo + ' al banco</div>' +
    '<div class="panelSub">Tienes <b>' + Object.values(mis).reduce((a,b)=>a+b,0) +
      '</b> cartas. Toca para elegir cuáles devuelves. Llevas <b>' + llevo + ' de ' + debo + '</b>.</div>' +
    '<div class="descFila">' +
      RECURSOS.map(c => {
        const tienes = mis[c.id] || 0;
        const n = pick[c.id] || 0;
        return '<div class="descItem' + (tienes ? '' : ' vacio') + '">' +
          '<img src="' + c.mini + '" alt="' + c.n + '">' +
          '<em style="color:' + c.col + '">' + c.n + '</em>' +
          '<span class="descTienes">tienes ' + tienes + '</span>' +
          '<div class="descBot">' +
            '<button onclick="descElegir(\\'' + c.id + '\\',-1)"' + (n ? '' : ' disabled') + '>−</button>' +
            '<b>' + n + '</b>' +
            '<button onclick="descElegir(\\'' + c.id + '\\',1)"' +
              (n < tienes && llevo < debo ? '' : ' disabled') + '>+</button>' +
          '</div></div>';
      }).join('') +
    '</div>' +
    '<button class="descOk" id="descOk"' + (listo ? '' : ' disabled') +
      ' onclick="descEntregar()">' + (listo ? 'ENTREGAR' : 'Faltan ' + (debo - llevo)) + '</button>';
}

function descElegir(rid, d){
  const pick = descLlevo.pick || (descLlevo.pick = {});
  const debo = descLlevo.para || 0;
  const llevo = Object.values(pick).reduce((a, b) => a + b, 0);
  const n = pick[rid] || 0;
  if (d > 0 && llevo >= debo) return;
  if (d < 0 && n <= 0) return;
  pick[rid] = n + d;
  if (pick[rid] <= 0) delete pick[rid];
  /* repinto con los datos de la sala, para no perder nada */
  leerSala(salaCod).then(s2 => { if (s2) pintaDescarte(s2); });
}

async function descEntregar(){
  const s = await leerSala(salaCod);
  if (!s) return;
  const debo = ((s.descarte || {})[yo.id]) || 0;
  const pick = descLlevo.pick || {};
  const llevo = Object.values(pick).reduce((a, b) => a + b, 0);
  if (llevo !== debo){ aviso('Todavía no', 'Tienes que devolver exactamente <b>' + debo + '</b>.'); return; }
  const rec = JSON.parse(JSON.stringify(s.recursos || {}));
  rec[yo.id] = rec[yo.id] || {};
  Object.entries(pick).forEach(([k, v]) => { rec[yo.id][k] = Math.max(0, (rec[yo.id][k] || 0) - v); });
  descLlevo.pick = {}; descLlevo.para = null;
  await update(ref(db,'extreme/salas/'+salaCod), { recursos: rec });
  await marcDescarte(s, rec);
  aviso('✅ Entregado', 'Devolviste ' + llevo + ' cartas al banco.', 3200);
}

/* marca que ya entregue, y si ya estamos todos, deja mover el Mal Tiempo */
async function marcDescarte(s, rec){
  const hecho = Object.assign({}, s.descarteHecho || {});
  hecho[yo.id] = true;
  const upd = { descarteHecho: hecho };
  const todos = Object.keys(s.descarte || {});
  if (todos.every(id => hecho[id])){
    /* el que tiro los dados es quien mueve el Mal Tiempo */
    upd.mueveElClima = s.tirador7 || s.turno;
  }
  await update(ref(db,'extreme/salas/'+salaCod), upd);
}

/* los bots descartan solos, o el juego se queda esperando para siempre */
async function botsDescartan(s){
  if (!s || !s.descarte) return;
  for (const id of Object.keys(s.descarte)){
    if ((s.descarteHecho || {})[id]) continue;
    const j = (s.jugadores || {})[id] || {};
    if (!j.esBot) continue;
    const debo = s.descarte[id];
    const rec = JSON.parse(JSON.stringify(s.recursos || {}));
    rec[id] = rec[id] || {};
    /* el bot devuelve de lo que MAS tiene, que es lo sensato */
    let falta = debo;
    const orden = Object.entries(rec[id]).sort((a, b) => b[1] - a[1]);
    for (const [k, v] of orden){
      if (falta <= 0) break;
      const quit = Math.min(v, falta);
      rec[id][k] = v - quit;
      falta -= quit;
    }
    const hecho = Object.assign({}, s.descarteHecho || {});
    hecho[id] = true;
    const upd = { recursos: rec, descarteHecho: hecho };
    const todos = Object.keys(s.descarte);
    if (todos.every(x => hecho[x])) upd.mueveElClima = s.tirador7 || s.turno;
    await update(ref(db,'extreme/salas/'+salaCod), upd);
    s.descarteHecho = hecho;
  }
}

/* ===== LOS LOGROS Y EL GANADOR =====""")

# ==========================================================================
# el HTML y el CSS de los dos paneles
# ==========================================================================
rep("""<div class="eligerec" id="eligeRec" style="position:fixed;left:0;right:0;bottom:0;z-index:40"></div>""",
    """<div class="eligerec" id="eligeRec" style="position:fixed;left:0;right:0;bottom:0;z-index:40"></div>
<div class="eligerec" id="descarte" style="position:fixed;left:0;right:0;bottom:0;z-index:42"></div>
<div class="eligerec" id="robaDe" style="position:fixed;left:0;right:0;bottom:0;z-index:44"></div>""")

rep("""  .mapa.arrastrando svg{cursor:grabbing}""",
    """  /* las filas del descarte del 7 */
  .descFila{display:flex;flex-direction:column;gap:6px;margin-bottom:11px}
  .descItem{display:flex;align-items:center;gap:8px;background:rgba(255,255,255,.05);
    border:1.5px solid #3a2b1c;border-radius:10px;padding:5px 8px}
  .descItem.vacio{opacity:.35}
  .descItem img{width:24px;height:24px;border-radius:50%;display:block}
  .descItem em{font-style:normal;font-family:Anton,sans-serif;font-size:10.5px;
    letter-spacing:.3px;min-width:44px;text-align:left}
  .descTienes{font-size:11px;color:#a89880;flex:1;text-align:left}
  .descBot{display:flex;align-items:center;gap:7px}
  .descBot button{width:30px;height:30px;border-radius:8px;border:1.5px solid #c9a558;
    background:rgba(201,165,88,.14);color:#f0d899;font-size:17px;font-weight:800;
    cursor:pointer;font-family:inherit;padding:0;line-height:1}
  .descBot button:disabled{opacity:.25;cursor:default}
  .descBot b{min-width:16px;text-align:center;color:#fff;font-size:14px}
  .descOk{width:100%;padding:11px;border-radius:11px;border:none;font-family:Anton,sans-serif;
    font-size:15px;letter-spacing:.6px;background:#5df08a;color:#10240f;cursor:pointer}
  .descOk:disabled{background:#3a2b1c;color:#7a6a50;cursor:default}
  .robaBtn{display:block;width:100%;margin:5px 0;padding:11px;border-radius:10px;
    border:1.5px solid #c9a558;background:rgba(201,165,88,.12);color:#f0d899;
    font-family:inherit;font-size:14px;font-weight:700;cursor:pointer}
  .mapa.arrastrando svg{cursor:grabbing}""")

# ==========================================================================
# el pintado del panel de robar, y los bots
# ==========================================================================
rep("""  pintaOfertas(s);
  pintaEligeRec(s);
  pintaDescarte(s);""",
    """  pintaOfertas(s);
  pintaEligeRec(s);
  pintaDescarte(s);
  pintaRobaDe(s);
  botsDescartan(s);""")

rep("""window.robaA = robaA;""",
    """window.robaA = robaA;

/* el panel para elegir a quien le robas (cuando hay mas de uno en el terreno) */
function pintaRobaDe(s){
  const el = $('robaDe');
  if (!el) return;
  const r = s.robaDe;
  if (!r || r.id !== yo.id){ el.classList.remove('on'); return; }
  el.classList.add('on');
  el.innerHTML =
    '<div class="panelTit">🌩️ ¿A quién le robas?</div>' +
    '<div class="panelSub">Hay más de uno en ese terreno. Elige a uno.</div>' +
    (r.quienes || []).map(id => {
      const j = (s.jugadores || {})[id] || {};
      const n = Object.values((s.recursos || {})[id] || {}).reduce((a,b)=>a+b,0);
      return '<button class="robaBtn" onclick="robaA(\\'' + id + '\\',' + r.hex + ')">' +
        (j.nombre || '?') + ' · ' + n + (n === 1 ? ' carta' : ' cartas') + '</button>';
    }).join('');""")

open(RUTA, 'w', encoding='utf-8').write(s)
print()
print('  cambios:', toc)
print('  archivo:', len(s), 'bytes')
