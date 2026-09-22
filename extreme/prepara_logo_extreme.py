#!/usr/bin/env python3
"""Prepara el logo de EXTREME (el hexagono con el parapente) como icono de app.

La imagen viene con un margen blanco alrededor del cuadrado de madera. Para un
icono hay que:
  1. recortar ese blanco
  2. dejarlo CUADRADO (los iconos son cuadrados; iOS y Android redondean ellos)
  3. sacar los tamanos que pide una PWA: 192 y 512, mas un apple-touch-icon 180
"""
from PIL import Image, ImageChops
import os

ORIGEN = '/Users/lapame10/.hermes/cache/images/img_b9abcac9d804.jpg'
DEST = '/Users/lapame10/.hermes/workspace/catan/extreme'
arte = os.path.join(DEST, 'arte')

im = Image.open(ORIGEN).convert('RGB')
print('  original:', im.size)

# --- 1) recortar el blanco de alrededor ---
# comparo contra blanco puro y busco donde deja de serlo
fondo = Image.new('RGB', im.size, (255, 255, 255))
dif = ImageChops.difference(im, fondo).convert('L')
# umbral: todo lo que no sea casi blanco cuenta como dibujo
borde = dif.point(lambda p: 255 if p > 12 else 0)
caja = borde.getbbox()
print('  el dibujo ocupa:', caja)
rec = im.crop(caja)
print('  recortado:', rec.size)

# --- 2) dejarlo cuadrado y con un pelin de aire ---
w, h = rec.size
lado = max(w, h)
# 4% de margen, que los iconos quedan mejor con un poco de aire
lado = int(lado * 1.06)
cuadro = Image.new('RGB', (lado, lado), (255, 255, 255))
cuadro.paste(rec, ((lado - w) // 2, (lado - h) // 2))
print('  cuadrado con aire:', cuadro.size)

os.makedirs(arte, exist_ok=True)

# --- 3) los tamanos ---
for n in (192, 512, 180):
    ic = cuadro.resize((n, n), Image.LANCZOS)
    nombre = ('icono-%d.png' % n) if n != 180 else 'apple-touch-icon.png'
    ruta = os.path.join(arte, nombre)
    ic.save(ruta, 'PNG', optimize=True)
    print('  %-22s %d x %d  (%d B)' % (nombre, n, n, os.path.getsize(ruta)))

# y una copia cuadrada mas grande, por si luego hace falta
cuadro.resize((1024, 1024), Image.LANCZOS).save(os.path.join(arte, 'logo-1024.png'), 'PNG', optimize=True)
print('  logo-1024.png          1024 x 1024')

# una version pequeña para la cabecera, recortada al hexagono (sin el marco cuadrado)
cab = cuadro.resize((240, 240), Image.LANCZOS)
cab.save(os.path.join(arte, 'logo.png'), 'PNG', optimize=True)
print('  logo.png               240 x 240  (para la cabecera)')
