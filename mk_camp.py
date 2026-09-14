import json, random, math, urllib.request, sys

COLS = [3, 4, 5, 4, 3]
MAZO = ['flight']*4 + ['board']*4 + ['climb']*4 + ['ride']*3 + ['jump']*3 + ['nofly']
NUMS = [2,3,3,4,4,5,5,6,6,8,8,9,9,10,10,11,11,12]
random.shuffle(MAZO); random.shuffle(NUMS)
hs = []; k = 0; ni = 0
for c, n in enumerate(COLS):
    for i in range(n):
        r = MAZO[k]; k += 1
        num = None if r == 'nofly' else NUMS[ni]
        if r != 'nofly': ni += 1
        hs.append({'c': c, 'i': i, 'rec': r, 'num': num})

R = 46.0; RX = 1.5*R; RY = math.sqrt(3)*R
nC = len(COLS); CX = ((nC-1)*RX + 2*R)/2; CY = ((max(COLS)-1)*RY + RY)/2
V = {}
for idx, h in enumerate(hs):
    cx = CX + (h['c'] - (nC-1)/2)*RX
    y0 = CY - ((COLS[h['c']]-1)*RY)/2
    cy = y0 + h['i']*RY
    for kk in range(6):
        p = (round(cx + R*math.cos(math.radians(60*kk)), 1),
             round(cy + R*math.sin(math.radians(60*kk)), 1))
        V.setdefault(p, {'n': 0, 'hex': idx}); V[p]['n'] += 1

interiores = sorted([p for p, v in V.items() if v['n'] >= 3])
print('  cruces interiores (donde SI se puede construir):', len(interiores))

def dist(a, b): return math.hypot(a[0]-b[0], a[1]-b[1])
def vt(a): return 'v#%s#%s' % (a[0], a[1])
def ar(a, b): return 'a#%s#%s|a#%s#%s' % (a[0], a[1], b[0], b[1])

# Pam: camp en un interior, ruta hacia un interior PEGADO, y un tercer interior lejos
c1 = interiores[0]
c2 = sorted([p for p in interiores if 0 < dist(p, c1) < R*1.9], key=lambda p: dist(p, c1))[0]
lejos = sorted([p for p in interiores if dist(p, c1) > R*2.5], key=lambda p: -dist(p, c1))
c3 = lejos[0] if lejos else interiores[-1]

ids = ['j1', 'bot1']
sala = {
  'fase': 'juego', 'anfitrion': 'j1', 'creada': 1,
  'jugadores': {'j1': {'nombre': 'Pam', 'color': 'rojo'},
                'bot1': {'nombre': '\U0001F916 Ana', 'color': 'azul', 'esBot': True}},
  'hexes': hs, 'orden': ids + ids[::-1], 'colocadoEn': 4, 'colocPaso': None, 'turno': 'j1',
  'piezas': {
    'j1': {'base': [{'k': vt(c1), 'hex': V[c1]['hex']}], 'hub': [],
           'camino': [{'k': ar(c1, c2), 'v': ['a#%s#%s' % (c1[0], c1[1]), 'a#%s#%s' % (c2[0], c2[1])]}]},
    'bot1': {'base': [{'k': vt(c3), 'hex': V[c3]['hex']}], 'hub': [], 'camino': []}},
  'dados': {'d1': 2, 'd2': 3, 'total': 5},
  'pa': {'j1': 3, 'bot1': 3}, 'ofertas': {},
  'recursos': {'j1': {'flight': 4, 'board': 4, 'ride': 4, 'climb': 4, 'jump': 4},
               'bot1': {'flight': 2, 'board': 2, 'ride': 2, 'climb': 2, 'jump': 2}},
  'clima': 0, 'avMazo': ['spot']*5, 'cartas': {}, 'gratis': {}, 'helis': {},
  'logros': {}, 'ganador': None, 'mueveElClima': None,
  '_prueba': {'c1': vt(c1), 'c2': vt(c2), 'ruta': ar(c1, c2)},
}
req = urllib.request.Request(
    'https://plan-gym-8aff7-default-rtdb.firebaseio.com/extreme/salas/CAMP.json',
    data=json.dumps(sala).encode(), method='PUT',
    headers={'Content-Type': 'application/json'})
urllib.request.urlopen(req)
print('  sala CAMP rehecha con cruces INTERIORES  ✓')
print('  camp de Pam:', vt(c1), '(toca', V[c1]['n'], 'hexagonos)')
print('  su ruta:', ar(c1, c2))
