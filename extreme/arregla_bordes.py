#!/usr/bin/env python3
"""EXTREME: el bug de los bordes del tablero + los bordes de color.

Pam:
 1) "a la hora de poner las primeras casas, no me deja poner en los bordes del
    tablero y deberia dejarme"
 2) "quiero poner los bordes de cada hexagono del color de la carta que dan,
    para que ayude visualmente"

BUG 1, medido con datos:
  El filtro "if (x.n < 2) return;" esconde los cruces que tocan UN SOLO
  hexagono. En el tablero de 19 hay 54 cruces: 18 de n=1, 12 de n=2 y 24 de
  n=3. O sea que estaba escondiendo 18 cruces, UN TERCIO DEL TABLERO, y son
  justo los del perimetro exterior. En el Catan de verdad los 54 son validos.
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
    print('  NO ENCUENTRO:', v[:72].replace('\n', ' | '))
    return False


# ==========================================================================
# BUG 1: los cruces del borde
# ==========================================================================
# la capa donde tocas para poner (el que ve Pam)
rep("""      Object.entries(V).forEach(([k, x]) => {
        if (x.n < 2) return;
        if (!libres(k)) return;                    /* ya hay una pieza ahi */""",
    """      Object.entries(V).forEach(([k, x]) => {
        /* ===== OJO CON ESTE FILTRO =====
           Antes ponia "if (x.n < 2) return;", que esconde los cruces que tocan
           UN SOLO hexagono. Medido: en el tablero de 19 hay 54 cruces (18 de
           n=1, 12 de n=2, 24 de n=3). O sea que se estaban escondiendo 18
           cruces, UN TERCIO DEL TABLERO, y son justo los del perimetro
           exterior. Pam: "no me deja poner en los bordes y deberia dejarme".
           En el Catan de verdad los 54 cruces son validos. */
        if (x.n < 1) return;
        if (!libres(k)) return;                    /* ya hay una pieza ahi */""")

# la capa de los huecos dorados (cuando no hay ninguno a mano)
rep("""        Object.entries(V).forEach(([k, x]) => {
          if (x.n < 2) return;
          if (!libres(k)) return;
          huecos++;""",
    """        Object.entries(V).forEach(([k, x]) => {
          if (x.n < 1) return;
          if (!libres(k)) return;
          huecos++;""")

# y el bot, que tenia el mismo filtro: tambien se estaba perdiendo el borde
rep("""        const libres = Object.keys(V).filter(k => V[k].n >= 2
          && !camps.includes(k)""",
    """        const libres = Object.keys(V).filter(k => V[k].n >= 1
          && !camps.includes(k)""")

# ==========================================================================
# 2) LOS BORDES DE COLOR
# ==========================================================================
rep("""    /* la junta: ahora DORADA y fina, como en el tablero de Pam. Ya no es un borde negro. */
    h += `<path d="${pathHex(x.cx,x.cy)}" fill="none" stroke="#1a1009" stroke-width="2.2" stroke-linejoin="round"/>`;""",
    """    /* ===== EL BORDE, DEL COLOR DEL RECURSO QUE DA (idea de Pam) =====
       Se pintan DOS trazos, en este orden:
         1) el ARO del color, grueso — asi cada hexagono dice de un vistazo que
            carta da, sin tener que reconocer la foto del terreno.
         2) la junta oscura, fina, ENCIMA — mantiene la separacion entre
            hexagonos, para que el tablero no se vea como una mancha de color.
       El orden importa: si la junta va antes, el aro la tapa y todo se mezcla. */
    const colRec = (RECURSOS.find(r => r.id === x.rec) || {}).col || '#5f584e';
    h += `<path d="${pathHex(x.cx,x.cy)}" fill="none" stroke="${colRec}"
           stroke-width="7" stroke-linejoin="round" opacity=".95"/>`;
    h += `<path d="${pathHex(x.cx,x.cy)}" fill="none" stroke="#1a1009" stroke-width="2.2" stroke-linejoin="round"/>`;""")

open(RUTA, 'w', encoding='utf-8').write(s)
print('  cambios:', toc)
print('  archivo:', len(s), 'bytes')
