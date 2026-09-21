#!/usr/bin/env python3
"""Las dos funciones del panel de elegir recursos, que faltaban.

Se quedaron sin escribir en el script anterior (el ancla del 'rep' no coincidia
y el fallo paso desapercibido). Y como ya se estaban LLAMANDO desde
pintaPartida y desde window., la app entera reventaba con ReferenceError.

MORALEJA: un 'rep' que no encuentra su ancla imprime un aviso y sigue. Hay que
LEER los avisos y comprobar que las funciones que se llaman EXISTEN.
"""
RUTA = '/Users/lapame10/.hermes/workspace/catan/extreme/index.html'
s = open(RUTA, encoding='utf-8').read()

FUNCIONES = """/* ==========================================================================
   ELEGIR RECURSOS — la carta "Condiciones perfectas"
   --------------------------------------------------------------------------
   Pam: "cuando me sale las dos cartas de recurso me deberia dejar escoger las 2
   cartas que yo quiera". Antes daba dos recursos AL AZAR.
   Ahora la sala guarda eligeRec = { id, cuantos, cogidas } y sale este panel.
   ========================================================================== */
function pintaEligeRec(s){
  const el = $('eligeRec');
  if (!el) return;
  const e = s.eligeRec;
  if (!e || e.id !== yo.id){ el.classList.remove('on'); return; }
  const cogidas = e.cogidas || {};
  const llevo = Object.values(cogidas).reduce((a, b) => a + b, 0);
  el.classList.add('on');
  el.innerHTML =
    '<div class="panelTit">🌤️ Condiciones perfectas</div>' +
    '<div class="panelSub">Elige <b>' + e.cuantos + '</b> cartas de recurso. ' +
      'Llevas <b>' + llevo + ' de ' + e.cuantos + '</b>.</div>' +
    '<div class="eligeFila">' +
      RECURSOS.map(c => {
        const n = cogidas[c.id] || 0;
        return '<button class="eligeBtn' + (n ? ' on' : '') + '"' +
          ' onclick="eligeRecurso(\\'' + c.id + '\\')">' +
          '<img src="' + c.mini + '" alt="' + c.n + '">' +
          '<em style="color:' + c.col + '">' + c.n + '</em>' +
          (n ? '<b>' + n + '</b>' : '') +
          '</button>';
      }).join('') +
    '</div>';
}

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
    /* ya estan las dos: las sumo de verdad y cierro la eleccion */
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

function pintaDescarte(s){"""

v = "function pintaDescarte(s){"
if v in s and 'function pintaEligeRec' not in s:
    s = s.replace(v, FUNCIONES, 1)
    open(RUTA, 'w', encoding='utf-8').write(s)
    print('  las dos funciones añadidas')
else:
    print('  NO encontrado o ya estaban')
