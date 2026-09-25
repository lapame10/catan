#!/usr/bin/env python3
"""Comprabas una carta y se te bloqueaban TODAS las demas.

Pam: "si compro una carta de aventura que no puedo usar ese turno, tampoco me
deja usar las otras que ya tenia antes".

LA CAUSA

Al comprar se apuntaba esto:

    ahora[yo.id] = true;

O sea: "Pam ha comprado una carta". Pero no CUAL. Y al jugar:

    if ((s.compradaAhora || {})[yo.id]){ bloquear; }

Ese 'true' valia para cualquier carta tuya. Asi que comprabas una y se te
apagaban todas las que ya tenias de antes. Y la regla solo dice que la recien
comprada no se juega ese turno.

EL ARREGLO

Ahora se apunta CUANTAS de cada tipo se compraron este turno:

    ahora[yo.id] = { rutas: 1 }

Y al jugar una carta de tipo X se mira si te quedan de ese tipo que NO sean de
este turno. Si todas las que tienes de X son de este turno, se bloquea. Si
tienes una vieja, se juega la vieja.

El caso raro: tienes 2 cartas del mismo tipo, una vieja y una comprada ahora. Con
'cuantas' en vez de 'cual' se resuelve solo: tienes 2 y de este turno hay 1,
asi que una se puede jugar. Da igual cual de las dos, porque el efecto es el
mismo: es la misma carta duplicada.
"""
BASE = '/Users/lapame10/.hermes/workspace/catan/extreme/'
toc = 0
s = open(BASE + 'index.html', encoding='utf-8').read()


def rep(v, n, q):
    global s, toc
    if v in s:
        s = s.replace(v, n, 1); toc += 1; print('  ok:', q)
    else:
        print('  ✗ NO COINCIDIO:', q)


# ---------- 1) al comprar: apuntar CUANTAS de cada tipo ----------
rep("""  const ahora = Object.assign({}, s.compradaAhora || {});
  ahora[yo.id] = true;""",
    """  const ahora = Object.assign({}, s.compradaAhora || {});
  /* Se apunta CUANTAS de cada tipo se compraron este turno, no solo que
     compraste. Antes era 'ahora[yo.id] = true' y ese true valia para cualquier
     carta tuya: comprabas una y se te apagaban TODAS, incluidas las de antes. */
  ahora[yo.id] = Object.assign({}, ahora[yo.id] || {});
  ahora[yo.id][tipo] = (ahora[yo.id][tipo] || 0) + 1;""",
    'al comprar, se apunta cual')

# ---------- 2) al jugar: solo se bloquea si no te queda ninguna vieja ----------
rep("""  /* ===== REGLA: la comprada ESTE turno no se puede jugar todavia ===== */
  if ((s.compradaAhora || {})[yo.id]){
    aviso('Todavía no', 'La carta se compra en un turno y <b>se juega en el siguiente</b>.<br>Pasa el turno y ya está.', 4600);
    return;
  }""",
    """  /* ===== REGLA: la comprada ESTE turno no se puede jugar todavía =====
     Pero SOLO esa. Las que ya tenías de antes sí.
     Pam: "si compro una carta de aventura que no puedo usar ese turno, tampoco
     me deja usar las otras que ya tenía antes". */
  const deAhora = ((s.compradaAhora || {})[yo.id] || {});
  {
    const tipoPedido = ((s.cartas || {})[yo.id] || [])[i];
    const compradasDeEsteTipo = deAhora[tipoPedido] || 0;
    const tengoDeEsteTipo = ((s.cartas || {})[yo.id] || []).filter(x => x === tipoPedido).length;
    /* si de este tipo tengo más que las compradas ahora, al menos una es vieja */
    if (compradasDeEsteTipo > 0 && tengoDeEsteTipo <= compradasDeEsteTipo){
      aviso('Todavía no', 'Esa la acabas de comprar. Se compra en un turno y <b>se juega en el siguiente</b>.<br>' +
        (tengoDeEsteTipo > 1 ? 'Ojo: tienes ' + tengoDeEsteTipo + ' iguales y son todas de este turno.' : 'Pasa el turno y ya está.'), 4600);
      return;
    }
  }""",
    'al jugar, solo se bloquea la recien comprada')

open(BASE + 'index.html', 'w', encoding='utf-8').write(s)
print('  cambios:', toc)

# ---------- 3) y comprobar que al pasar el turno se limpia bien ----------
import re
k = s.find('const ah = Object.assign({}, s.compradaAhora')
print()
print('  === al pasar el turno ===')
print('  ' + ' '.join(s[k-200:k+260].split())[:420])
