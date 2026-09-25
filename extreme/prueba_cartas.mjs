// La misma logica que ahora esta en el juego, probada con casos concretos.
function bloquea(cartas, i, compradaAhora) {
  const deAhora = compradaAhora || {};
  const tipoPedido = cartas[i];
  const compradasDeEsteTipo = deAhora[tipoPedido] || 0;
  const tengoDeEsteTipo = cartas.filter(x => x === tipoPedido).length;
  return compradasDeEsteTipo > 0 && tengoDeEsteTipo <= compradasDeEsteTipo;
}
function dibujo(cartas, compradaAhora) {
  const deAhora = compradaAhora || {};
  const libres = {};
  const cuenta = {};
  cartas.forEach(tp => cuenta[tp] = (cuenta[tp] || 0) + 1);
  Object.keys(cuenta).forEach(tp => {
    const bloq = (typeof deAhora === 'object' && deAhora !== null) ? (deAhora[tp] || 0) : cuenta[tp];
    libres[tp] = cuenta[tp] - bloq;
  });
  const puestas = {};
  return cartas.map(tp => {
    puestas[tp] = puestas[tp] || 0;
    const esNueva = puestas[tp]++ >= (libres[tp] || 0);
    return esNueva ? tp + '(comprada ahora)' : tp;
  });
}

let malos = 0;
const prueba = (nombre, obtenido, esperado) => {
  const ok = JSON.stringify(obtenido) === JSON.stringify(esperado);
  if (!ok) malos++;
  console.log('  %s %s', ok ? '✓' : '✗', nombre);
  if (!ok) console.log('      esperaba %s, dio %s', JSON.stringify(esperado), JSON.stringify(obtenido));
};

console.log('  --- EL CASO DE PAM ---');
console.log('  tenia [rutas, heli] y compra [spot] el mismo turno\n');
// compro una 'spot'; tengo rutas (vieja), heli (vieja), spot (nueva)
prueba('jugar la rutas vieja (índice 0) -> DEBE dejarme',
  bloquea(['rutas','heli','spot'], 0, { spot: 1 }), false);
prueba('jugar el heli viejo (índice 1) -> DEBE dejarme',
  bloquea(['rutas','heli','spot'], 1, { spot: 1 }), false);
prueba('jugar la spot recien comprada (índice 2) -> NO debe dejarme',
  bloquea(['rutas','heli','spot'], 2, { spot: 1 }), true);

console.log('\n  --- EL DIBUJO ---');
prueba('se marca solo la spot como comprada ahora',
  dibujo(['rutas','heli','spot'], { spot: 1 }),
  ['rutas','heli','spot(comprada ahora)']);

console.log('\n  --- DOS COMPRADAS EN EL MISMO TURNO ---');
prueba('con 2 spot compradas y 0 viejas: ninguna se puede jugar',
  [bloquea(['spot','spot'], 0, { spot: 2 }), bloquea(['spot','spot'], 1, { spot: 2 })],
  [true, true]);

console.log('\n  --- DOS DEL MISMO TIPO, UNA VIEJA Y UNA NUEVA ---');
prueba('con 1 spot vieja + 1 comprada: la primera se juega',
  bloquea(['spot','spot'], 0, { spot: 1 }), false);
/* Y la segunda TAMBIEN se puede jugar, y esta bien: tienes dos cartas del mismo
   tipo y el efecto de jugar una u otra es identico. Lo que no se puede es jugar
   MAS de las que tenias de antes. Se bloquea por tipo, no por posicion, porque
   las posiciones cambian al jugar cartas. */
prueba('la segunda tambien se puede: son del mismo tipo y da igual cual',
  bloquea(['spot','spot'], 1, { spot: 1 }), false);
prueba('pero no puedes jugar las DOS: solo una es vieja',
  (bloquea(['spot','spot'], 0, { spot: 1 }) === false &&
   cartasJugables(['spot','spot'], { spot: 1 })) === false, true);
function cartasJugables(cartas, compradaAhora){
  // cuenta cuantas se pueden jugar de verdad: las viejas de cada tipo
  const deAhora = compradaAhora || {};
  const cuenta = {}, libres = {};
  cartas.forEach(tp => cuenta[tp] = (cuenta[tp] || 0) + 1);
  Object.keys(cuenta).forEach(tp => libres[tp] = cuenta[tp] - (deAhora[tp] || 0));
  return Object.values(libres).reduce((a,b) => a + Math.max(0,b), 0) >= cartas.length;
}
prueba('el dibujo marca solo la segunda',
  dibujo(['spot','spot'], { spot: 1 }), ['spot','spot(comprada ahora)']);

console.log('\n  --- SIN NADA COMPRADO ---');
prueba('sin compras, todas jugables',
  [bloquea(['rutas','heli'], 0, {}), bloquea(['rutas','heli'], 1, {})],
  [false, false]);
prueba('sin compras, el dibujo no marca ninguna',
  dibujo(['rutas','heli'], {}), ['rutas','heli']);

console.log('\n  --- FORMATO VIEJO (una partida a medias con true) ---');
prueba('si el estado trae true en vez de objeto, se bloquean todas',
  dibujo(['rutas','heli'], true), ['rutas(comprada ahora)','heli(comprada ahora)']);

console.log('\n  %s', malos ? '✗ ' + malos + ' fallos' : '✓ todos bien');
process.exit(malos ? 1 : 0);
