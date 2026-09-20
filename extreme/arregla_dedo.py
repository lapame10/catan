#!/usr/bin/env python3
"""FIX: con el dedo no se podia colocar — el anti-arrastre se comia los toques.

El bug, en detalle:

  pointerdown  -> arrastrando = {...}, huboArrastre = false
  pointermove  -> si el dedo se movio > 7px: huboArrastre = true
  pointerup    -> setTimeout(() => huboArrastre = false, 120)
  click        -> if (huboArrastre) return;   <-- AQUI

El problema es el ORDEN de los eventos del navegador:

  pointerdown -> pointermove -> pointerup -> click

El 'click' llega INMEDIATAMENTE despues del 'pointerup', mucho antes de que
pasen los 120ms del setTimeout. Asi que el click lee huboArrastre todavia en
true y se ignora.

Y en un movil el dedo SIEMPRE se mueve mas de 7px al tocar (nunca esta
perfectamente quieto), asi que el toque se ignoraba SIEMPRE. Con el raton no
pasa, porque el raton no se mueve al hacer clic: por eso a mi me daba 50
circulos y a Pam no le dejaba colocar NADA.

ARREGLO:
  1) huboArrastre se limpia al EMPEZAR el toque siguiente (pointerdown), no con
     un temporizador. Asi el click del toque actual lo lee bien, y el siguiente
     toque parte limpio.
  2) El umbral sube de 7 a 14 px: un dedo se mueve mas que un raton, y 7px
     marcaban como "arrastre" toques que eran claramente un toque.
  3) Y si el arrastre fue minimo, el tablero VUELVE a su sitio: asi un pequeño
     temblor del dedo no deja el mapa desplazado.
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


# 1) el pointerdown: empieza limpio
rep("""  caja.addEventListener('pointerdown', e => {
    punterosVb[e.pointerId] = { x: e.clientX, y: e.clientY };
    const n = Object.keys(punterosVb).length;
    if (n === 1){
      const v0 = vb || cogeVb();
      arrastrando = v0 ? { x: e.clientX, y: e.clientY, vb0: v0.slice() } : null;
      huboArrastre = false;
    } else {""",
    """  caja.addEventListener('pointerdown', e => {
    punterosVb[e.pointerId] = { x: e.clientX, y: e.clientY };
    const n = Object.keys(punterosVb).length;
    /* EL FLAG SE LIMPIA AQUI, al EMPEZAR un toque.
       Antes se limpiaba con un setTimeout en el pointerup, pero el 'click'
       llega ANTES de que ese temporizador corra (pointerdown -> pointermove ->
       pointerup -> click son seguidos). Asi que el click leia el flag todavia
       en true y el toque se ignoraba. Limpiandolo aqui, el click del toque
       actual lo lee bien y el siguiente toque parte limpio. */
    if (n === 1){
      const v0 = vb || cogeVb();
      arrastrando = v0 ? { x: e.clientX, y: e.clientY, vb0: v0.slice() } : null;
      huboArrastre = false;
    } else {""")

# 2) el umbral, de 7 a 14 (un dedo se mueve mas que un raton)
rep("""    const mov = Math.abs(e.clientX - arrastrando.x) + Math.abs(e.clientY - arrastrando.y);
    if (mov > 7){ huboArrastre = true; caja.classList.add('arrastrando'); }""",
    """    /* 14 y no 7: un dedo nunca se queda perfectamente quieto, y con 7px
       cualquier toque se marcaba como arrastre. */
    const mov = Math.abs(e.clientX - arrastrando.x) + Math.abs(e.clientY - arrastrando.y);
    if (mov > 14){ huboArrastre = true; caja.classList.add('arrastrando'); }
    else {
      /* temblor pequeño del dedo: NO muevo el tablero. Si lo moviera con cada
         temblor, el mapa se iria desplazando solo y acabaria descolocado. */
      return;
    }""")

# 3) el suelta: sin temporizador
rep("""    arrastrando = null;
    caja.classList.remove('arrastrando');
    /* el onclick llega DESPUES del pointerup: doy un momento antes de limpiar */
    setTimeout(() => { huboArrastre = false; }, 120);
  };""",
    """    arrastrando = null;
    caja.classList.remove('arrastrando');
    /* NO limpio huboArrastre aqui: el 'click' viene DESPUES de este pointerup,
       y si lo limpiara ahora el click creeria que fue un toque limpio y
       colocaria una pieza al terminar de mover el mapa.
       Se limpia al EMPEZAR el toque siguiente (ver pointerdown). */
  };""")

open(RUTA, 'w', encoding='utf-8').write(s)
print()
print('  cambios:', toc)
print('  archivo:', len(s), 'bytes')
