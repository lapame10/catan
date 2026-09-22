#!/usr/bin/env python3
"""Buzon de avisos del comercio.

Pam: "que cuando te acepten o declinen la oferta te diga quien".

Antes: el que ACEPTABA veia 'Trato hecho' y el que RECHAZABA veia 'Rechazada'.
Pero el que habia HECHO la oferta no se enteraba de quien: la oferta
desaparecia y ya, o seguia ahi y te quedabas esperando.

Ahora: cuando alguien acepta o rechaza TU oferta, se te deja un aviso con su
NOMBRE en un buzon, y sale en pantalla una sola vez.
"""
RUTA = '/Users/lapame10/.hermes/workspace/catan/extreme/index.html'
s = open(RUTA, encoding='utf-8').read()
toc = 0


def rep(v, n, quien):
    global s, toc
    if v in s:
        s = s.replace(v, n, 1); toc += 1; print('  ok:', quien)
        return True
    print('  NO ENCONTRE:', quien)
    return False


# ============================================================
# 1) AL ACEPTAR: avisar AL QUE LA HIZO de quien acepto
# ============================================================
rep("""    delete ofertas[oid];
    await update(ref(db,'extreme/salas/'+salaCod), { recursos: rec, ofertas });
    aviso('✔ Trato hecho', 'Se ha hecho el cambio');
    di('ha cerrado un trato con ' + (((s.jugadores || {})[o.de] || {}).nombre || '?'));""",
    """    delete ofertas[oid];
    /* ===== QUE EL QUE LA HIZO SEPA QUIEN ACEPTO =====
       Pam: "que cuando te acepten o declinen la oferta te diga quien". Antes el
       que aceptaba veia 'Trato hecho', pero el que habia hecho la oferta no se
       enteraba de NADA: la oferta desaparecia y ya. Ahora se le deja un aviso
       en su buzon con el nombre de quien acepto. */
    const buzon = Object.assign({}, s.buzon || {});
    buzon[o.de] = {
      t: '<b>' + (yo.nombre || 'Alguien') + '</b> aceptó tu oferta. ¡Trato hecho!',
      ts: Date.now()
    };
    await update(ref(db,'extreme/salas/'+salaCod), { recursos: rec, ofertas, buzon });
    aviso('✔ Trato hecho',
      'Se ha hecho el cambio con <b>' + (((s.jugadores || {})[o.de] || {}).nombre || '?') + '</b>');
    di('ha cerrado un trato con ' + (((s.jugadores || {})[o.de] || {}).nombre || '?'));""",
    'el que ofrecio sabe quien acepto')

# ============================================================
# 2) AL RECHAZAR: aviso en el buzon tambien
# ============================================================
rep("""    aviso('🚫 Rechazada', 'No te la volveremos a ofrecer. Sigue en la mesa para los demás.', 3200);
  }""",
    """    /* y al que la hizo le dejo el aviso, con el NOMBRE de quien dijo que no */
    ofertas[oid].buzon = Object.assign({}, ofertas[oid].buzon || {});
    ofertas[oid].buzon[o.de] = {
      t: '<b>' + (yo.nombre || 'Alguien') + '</b> dijo que <b>no</b> a tu oferta.',
      ts: Date.now()
    };
    aviso('🚫 Rechazada', 'No te la volveremos a ofrecer. Sigue en la mesa para los demás.', 3200);
  }""",
    'el que ofrecio sabe quien rechazo')

# el buzon del rechazo vive DENTRO de la oferta: hay que sacarlo al pintar
rep("""/* Pam: "cuando te rechazan la oferta estaria bueno saber que la rechazaron".""",
    """/* ===== EL BUZON DE AVISOS DEL COMERCIO =====
   Cuando alguien acepta o rechaza TU oferta, se te deja un aviso con su NOMBRE
   y sale en pantalla una sola vez. Pam: "que cuando te acepten o declinen la
   oferta te diga quien". */
let _buzonVisto = 0;
function leeBuzon(s){
  let b = (s.buzon || {})[yo.id];
  /* el del rechazo viaja dentro de la oferta, porque la oferta sigue viva */
  Object.values(s.ofertas || {}).forEach(o => {
    const x = o && o.buzon && o.buzon[yo.id];
    if (x && (!b || x.ts > b.ts)) b = x;
  });
  if (!b || !b.ts) return;
  if (_buzonVisto === b.ts) return;
  _buzonVisto = b.ts;
  aviso('🔄 Comercio', b.t, 6400);
  try { update(ref(db,'extreme/salas/'+salaCod), { ['buzon/' + yo.id]: null }); } catch(e){}
}

/* Pam: "cuando te rechazan la oferta estaria bueno saber que la rechazaron".""",
    'leeBuzon (el buzon)')

rep("""  pintaOfertas(s);
  avisaRechazos(s);""",
    """  pintaOfertas(s);
  leeBuzon(s);
  avisaRechazos(s);""",
    'leeBuzon se llama en pintaPartida')

rep("""    cartas:{}, gratis:{}, helis:{}, logros:{}, ganador:null, mueveElClima:null""",
    """    cartas:{}, gratis:{}, helis:{}, logros:{}, ganador:null, mueveElClima:null,
    buzon:{}, compradaAhora:{}""",
    'buzon y compradaAhora al crear la partida')

open(RUTA, 'w', encoding='utf-8').write(s)
print()
print('  cambios:', toc)
print('  archivo:', len(s), 'bytes')
