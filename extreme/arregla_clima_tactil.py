#!/usr/bin/env python3
"""El Mal Tiempo no se dejaba mover. Por que.

Pam: "cuando sale 7 el mal tiempo no lo puedo mover".

Lo que pasaba:

El tablero tiene UN solo manejador de toques para todo. Cuando tocas, coge el
punto de los que se pueden tocar que este MAS CERCA de tu dedo, y solo lo acepta
si esta a 34 pixeles o menos.

    if (mejor && mejorD <= 34){ ... }

34 pixeles vale para los cruces y las aristas, que son puntos y lineas finas.
Pero para mover el Mal Tiempo hay que tocar el CENTRO de un hexagono, y un
hexagono tiene 46 pixeles de radio. O sea:

    tocas el centro        -> distancia 0    -> vale
    tocas a media altura   -> distancia 23   -> vale
    tocas cerca del borde  -> distancia 41   -> NO VALE

Y el borde es la mitad del hexagono. Pam tocaba el terreno, no el centro exacto,
y la app se quedaba como si no hubiera tocado nada. No salia ningun aviso,
ningun error: simplemente no pasaba nada. Eso es lo peor, porque parece que el
juego esta roto.

ARREGLO

Cuando hay puntos para mover el Mal Tiempo, se miran PRIMERO y con un radio que
es el del hexagono entero. Si estas moviendo el clima, cualquier toque dentro
del hexagono vale. Ademas tienen prioridad sobre los cruces: si estas moviendo
el clima, no estas construyendo.

Y si tocas fuera de todo, ahora se dice, en vez de quedarse callado.
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


VIEJO = """    if (e.clientX || e.clientY){
      const pt = svg.createSVGPoint();
      pt.x = e.clientX; pt.y = e.clientY;
      let p;
      try { p = pt.matrixTransform(svg.getScreenCTM().inverse()); } catch(err){ p = null; }
      if (p){
        let mejor = null, mejorD = Infinity;
        todos.forEach(el => {
          let d;
          if (el.tagName === 'line'){
            d = distPuntoSegmento(p.x, p.y, +el.getAttribute('x1'), +el.getAttribute('y1'),
                                                +el.getAttribute('x2'), +el.getAttribute('y2'));
          } else {
            d = Math.hypot(p.x - +el.getAttribute('cx'), p.y - +el.getAttribute('cy'));
          }
          if (d < mejorD){ mejorD = d; mejor = el; }
        });
        if (mejor && mejorD <= 34){ coloca(mejor.dataset.t, mejor.dataset.k, +mejor.dataset.h); return; }
      }
    }"""

NUEVO = """    if (e.clientX || e.clientY){
      const pt = svg.createSVGPoint();
      pt.x = e.clientX; pt.y = e.clientY;
      let p;
      try { p = pt.matrixTransform(svg.getScreenCTM().inverse()); } catch(err){ p = null; }
      if (p){
        const distancia = (el) => {
          if (el.tagName === 'line'){
            return distPuntoSegmento(p.x, p.y, +el.getAttribute('x1'), +el.getAttribute('y1'),
                                                 +el.getAttribute('x2'), +el.getAttribute('y2'));
          }
          return Math.hypot(p.x - +el.getAttribute('cx'), p.y - +el.getAttribute('cy'));
        };

        /* ===== MOVER EL MAL TIEMPO VA PRIMERO, Y CON RADIO DE HEXAGONO =====
           Pam: "cuando sale 7 el mal tiempo no lo puedo mover".
           El limite de 34 px vale para cruces y aristas, que son puntos y lineas
           finas. Pero para el clima hay que tocar el CENTRO de un hexagono, y el
           hexagono tiene 46 de radio: tocando cerca del borde, la distancia al
           centro pasa de 34 y la app se quedaba como si no hubieras tocado nada.
           Sin aviso y sin error, que es lo peor: parece que el juego esta roto.

           Ahora, si estas moviendo el clima, se mira SOLO entre los puntos de
           clima, y vale cualquier toque DENTRO del hexagono. Y tienen prioridad
           sobre los cruces: si mueves el clima, no estas construyendo. */
        const deClima = todos.filter(el => el.dataset.t === 'clima');
        if (deClima.length){
          let mejor = null, mejorD = Infinity;
          deClima.forEach(el => {
            const d = distancia(el);
            if (d < mejorD){ mejorD = d; mejor = el; }
          });
          /* el radio del hexagono, y un poco mas de margen por si el dedo cae
             justo fuera de la linea */
          if (mejor && mejorD <= R * 1.05){
            coloca(mejor.dataset.t, mejor.dataset.k, +mejor.dataset.h);
            return;
          }
        }

        let mejor = null, mejorD = Infinity;
        todos.forEach(el => {
          const d = distancia(el);
          if (d < mejorD){ mejorD = d; mejor = el; }
        });
        if (mejor && mejorD <= 34){
          coloca(mejor.dataset.t, mejor.dataset.k, +mejor.dataset.h);
          return;
        }

        /* ===== Y SI NO SE COGIO NADA, SE DICE =====
           Antes esto era un silencio. Si estas moviendo el clima y tocas donde
           no hay nada, la persona se queda pensando que el juego no responde. */
        if (deClima.length){
          aviso('Toca un terreno', 'Pulsa en el centro de cualquiera de los terrenos marcados.', 3200);
        }
      }
    }"""

rep(VIEJO, NUEVO, 'el toque para mover el Mal Tiempo')

open(BASE + 'index.html', 'w', encoding='utf-8').write(s)
print('  cambios:', toc)
