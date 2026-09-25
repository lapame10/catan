#!/usr/bin/env python3
"""Cuando mueves el mal tiempo dice "no habia nadie" aunque haya gente.

Pam, con captura: en el 11 estaba Maria y decia que no habia nadie.

LA CAUSA DE VERDAD

Los cruces se guardan como COORDENADAS ABSOLUTAS:

    base k = "v#92.0#119.5"

Y para saber que hexagonos toca un cruce, el juego recalcula la distancia de
esas coordenadas a los centros de los hexagonos:

    hexesDelCruce("v#92.0#119.5")  ->  [0, 1]

Pero los centros se calculan con CX, que es EL ANCHO DE LA PANTALLA PARTIDO POR
DOS:

    CX = ancho / 2;

Asi que las mismas coordenadas caen en sitios distintos segun el movil, segun el
tamaño de la ventana, o segun si giraste el telefono. Comprobado:

    con CX=200  ->  todos los cruces tocan hexagono
    con CX=230  ->  3 cruces no tocan ninguno
    con CX=260  ->  4 no tocan
    con CX=350  ->  5 no tocan

Cuando un cruce no toca ningun hexagono, tocaHex devuelve 0, y el juego dice
"no habia nadie alli". Aunque las piezas se vean en el tablero.

Es intermitente y depende del aparato, que es lo peor: en el movil de Pam falla
y en otro puede no fallar.

EL ARREGLO

Guardar los hexagonos del cruce EN EL MOMENTO de colocar la pieza, que es cuando
las coordenadas son las buenas:

    base.push({ k: clave, hex: hexIdx, hexes: [0, 1, 7] })

Y tocaHex usa esa lista si esta. Si no (piezas viejas, o del bot), cae al calculo
de siempre.

Asi deja de depender del ancho de la pantalla: una vez colocada la pieza, sus
hexagonos quedan grabados y no cambian.

Nota: lo suyo seria guardar el cruce por su POSICION EN LA REJILLA (columna y
fila) en vez de por coordenadas de pantalla. Eso es un cambio mas grande y toca
la colocacion, el dibujo y las rutas. Se apunta para no olvidarlo, pero hoy no se
hace: aqui se arregla el sintoma que ve Pam sin tocar como se juega.
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


# ---------- 1) tocaHex: usar los hexagonos grabados si estan ----------
rep("""  function tocaHex(pz, i){
    let n = 0;
    ((pz && pz.base) || []).forEach(b => { if (hexesDelCruce(b.k).includes(i)) n += 1; });
    ((pz && pz.hub)  || []).forEach(b => { if (hexesDelCruce(b.k).includes(i)) n += 2; });
    return n;
  }""",
    """  function tocaHex(pz, i){
    let n = 0;
    /* ===== LOS HEXAGONOS DEL CRUCE: SE USAN LOS GRABADOS =====
       Pam: "cuando muevo el mal clima, aunque haya gente ahi, me dice que no hay
       nadie". Con captura: en el 11 estaba Maria.

       El cruce se guarda por coordenadas absolutas ("v#92.0#119.5"), y para
       saber que hexagonos toca se recalcula la distancia a los centros. Pero los
       centros se calculan con CX = ancho/2, o sea QUE DEPENDE DEL ANCHO DE LA
       PANTALLA. Las mismas coordenadas caen en sitios distintos segun el movil,
       y a partir de cierta anchura varios cruces dejan de tocar ningun hexagono:
       entonces tocaHex da 0 y la app dice "no habia nadie" aunque las piezas se
       vean.

       Por eso ahora, al colocar la pieza, se graban sus hexagonos. Se usa esa
       lista si esta, y si no se calcula como antes. Asi deja de depender del
       ancho de la pantalla. */
    const suyos = (b) => (b && Array.isArray(b.hexes) && b.hexes.length)
      ? b.hexes
      : hexesDelCruce(b && b.k);
    ((pz && pz.base) || []).forEach(b => { if (suyos(b).includes(i)) n += 1; });
    ((pz && pz.hub)  || []).forEach(b => { if (suyos(b).includes(i)) n += 2; });
    return n;
  }""",
    'tocaHex usa los hexagonos grabados')

# ---------- 2) grabar los hexagonos al colocar un basecamp ----------
rep("""      piezas[yo.id].base.push({ k: clave, hex: hexIdx });""",
    """      piezas[yo.id].base.push({
        k: clave, hex: hexIdx,
        /* los hexagonos que toca este cruce, grabados AHORA, que es cuando las
           coordenadas son las buenas para esta pantalla */
        hexes: hexesDelCruce(clave),
      });""",
    'graba los hexagonos del basecamp')

open(BASE + 'index.html', 'w', encoding='utf-8').write(s)
print('  cambios:', toc)

# ---------- 3) y ver donde mas se colocan basecamps/hubs ----------
import re
print()
print('  === todos los sitios donde se guarda un basecamp o un hub ===')
for m in re.finditer(r"\.(base|hub)\s*\.push\(([^)]*)\)", s):
    linea = s[:m.start()].count('\n') + 1
    print('   linea %d: .%s.push(%s)' % (linea, m.group(1), ' '.join(m.group(2).split())[:80]))
