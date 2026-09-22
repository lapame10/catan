#!/usr/bin/env python3
"""El recuadro de devolver cartas del 7, bien en el movil.

Pam: "el recuadro de regresar las cartas cuando sale un 7, en el celular no se
ve bien".

Lo que estaba mal para un movil:
  1. Los botones - y + median 30x30: por debajo del minimo tactil comodo (44).
     Con el dedo se falla y acabas tocando el de al lado.
  2. El panel no tenia altura maxima: con los 5 recursos puede salirse por
     arriba y no hay forma de llegar al boton de ENTREGAR.
  3. Cada fila pedia demasiado ancho (icono + nombre + "tienes N" + botones) y
     en una pantalla estrecha se apretaba todo.
  4. No se podia hacer scroll dentro del panel.
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


# ==========================================================================
# el CSS, reescrito para el dedo
# ==========================================================================
rep("""  /* el panel para elegir recursos */
  .eligerec{display:none;background:rgba(20,14,8,.97);border-top:2px solid #c9a558;
    padding:12px 12px calc(12px + env(safe-area-inset-bottom));text-align:center;
    box-shadow:0 -8px 30px rgba(0,0,0,.7)}
  .eligerec.on{display:block}""",
    """  /* ===== LOS PANELES DE ABAJO (elegir recursos, descarte del 7, robar) =====
     Tienen que funcionar en un movil y CON EL DEDO:
       - altura maxima y scroll dentro, o con 5 recursos el boton de ENTREGAR
         se sale por arriba y no hay forma de llegar a el
       - botones GRANDES: el minimo comodo con el dedo son 44px
       - el hueco de abajo (safe-area) para que no lo tape la barra de Safari */
  .eligerec{display:none;background:rgba(20,14,8,.97);border-top:2px solid #c9a558;
    padding:12px 12px calc(14px + env(safe-area-inset-bottom));text-align:center;
    box-shadow:0 -8px 30px rgba(0,0,0,.7);
    max-height:82vh;overflow-y:auto;-webkit-overflow-scrolling:touch}
  .eligerec.on{display:block}""",
    'el panel: altura maxima y scroll')

rep("""  /* las filas del descarte del 7 */
  .descFila{display:flex;flex-direction:column;gap:6px;margin-bottom:11px}
  .descItem{display:flex;align-items:center;gap:8px;background:rgba(255,255,255,.05);
    border:1.5px solid #3a2b1c;border-radius:10px;padding:5px 8px}
  .descItem.vacio{opacity:.35}
  .descItem img{width:24px;height:24px;border-radius:50%;display:block}
  .descItem em{font-style:normal;font-family:Anton,sans-serif;font-size:10.5px;
    letter-spacing:.3px;min-width:44px;text-align:left}
  .descTienes{font-size:11px;color:#a89880;flex:1;text-align:left}
  .descBot{display:flex;align-items:center;gap:7px}
  .descBot button{width:30px;height:30px;border-radius:8px;border:1.5px solid #c9a558;
    background:rgba(201,165,88,.14);color:#f0d899;font-size:17px;font-weight:800;
    cursor:pointer;font-family:inherit;padding:0;line-height:1}
  .descBot button:disabled{opacity:.25;cursor:default}
  .descBot b{min-width:16px;text-align:center;color:#fff;font-size:14px}
  .descOk{width:100%;padding:11px;border-radius:11px;border:none;font-family:Anton,sans-serif;
    font-size:15px;letter-spacing:.6px;background:#5df08a;color:#10240f;cursor:pointer}
  .descOk:disabled{background:#3a2b1c;color:#7a6a50;cursor:default}""",
    """  /* ===== LAS FILAS DEL DESCARTE DEL 7 (para el dedo) ===== */
  .descFila{display:flex;flex-direction:column;gap:7px;margin-bottom:12px}
  .descItem{display:flex;align-items:center;gap:9px;background:rgba(255,255,255,.05);
    border:1.5px solid #3a2b1c;border-radius:11px;padding:7px 9px;min-height:52px}
  .descItem.vacio{opacity:.32}
  .descItem img{width:28px;height:28px;border-radius:50%;display:block;flex:none}
  .descItem em{font-style:normal;font-family:Anton,sans-serif;font-size:11.5px;
    letter-spacing:.3px;width:52px;text-align:left;flex:none}
  .descTienes{font-size:10.5px;color:#a89880;flex:1;text-align:left;line-height:1.25}
  .descBot{display:flex;align-items:center;gap:6px;flex:none}
  /* 44px: el minimo comodo para el dedo. Antes 30 y se fallaba al tocar. */
  .descBot button{width:44px;height:44px;border-radius:11px;border:1.5px solid #c9a558;
    background:rgba(201,165,88,.16);color:#f0d899;font-size:22px;font-weight:800;
    cursor:pointer;font-family:inherit;padding:0;line-height:1;
    display:flex;align-items:center;justify-content:center;touch-action:manipulation}
  .descBot button:active{background:rgba(201,165,88,.34)}
  .descBot button:disabled{opacity:.22;cursor:default}
  .descBot b{min-width:22px;text-align:center;color:#fff;font-size:17px;
    font-family:Anton,sans-serif}
  .descOk{width:100%;padding:15px;border-radius:12px;border:none;font-family:Anton,sans-serif;
    font-size:17px;letter-spacing:.6px;background:#5df08a;color:#10240f;cursor:pointer;
    touch-action:manipulation}
  .descOk:active{filter:brightness(1.12)}
  .descOk:disabled{background:#3a2b1c;color:#7a6a50;cursor:default}
  /* en pantallas muy bajas, aprieto un poco para que quepa todo */
  @media (max-height:620px){
    .descItem{min-height:44px;padding:5px 8px}
    .descBot button{width:38px;height:38px;font-size:19px}
    .descItem img{width:24px;height:24px}
  }""",
    'las filas del descarte, al dedo')

# el titulo y el subtitulo, mas legibles en movil
rep("""  .panelTit{font-family:Anton,sans-serif;font-size:17px;color:#f0d899;letter-spacing:.5px}
  .panelSub{font-size:12.5px;color:#e8dcc0;margin:5px 0 11px;line-height:1.5}""",
    """  .panelTit{font-family:Anton,sans-serif;font-size:18px;color:#f0d899;letter-spacing:.5px;
    line-height:1.25}
  .panelSub{font-size:13px;color:#e8dcc0;margin:6px 0 12px;line-height:1.5}""",
    'titulo y subtitulo mas legibles')

# el panel de elegir recursos y el de robar, tambien con sitios comodos
rep("""  .eligeBtn{position:relative;background:rgba(255,255,255,.05);border:2px solid #3a2b1c;
    border-radius:12px;padding:7px 9px 5px;cursor:pointer;display:flex;flex-direction:column;
    align-items:center;gap:3px;font-family:inherit;min-width:62px}""",
    """  .eligeBtn{position:relative;background:rgba(255,255,255,.05);border:2px solid #3a2b1c;
    border-radius:12px;padding:9px 10px 7px;cursor:pointer;display:flex;flex-direction:column;
    align-items:center;gap:4px;font-family:inherit;min-width:70px;min-height:76px;
    justify-content:center;touch-action:manipulation}""",
    'los botones de elegir recursos, mas grandes')

rep("""  .robaBtn{display:block;width:100%;margin:5px 0;padding:11px;border-radius:10px;
    border:1.5px solid #c9a558;background:rgba(201,165,88,.12);color:#f0d899;
    font-family:inherit;font-size:14px;font-weight:700;cursor:pointer}""",
    """  .robaBtn{display:block;width:100%;margin:6px 0;padding:15px;border-radius:11px;
    border:1.5px solid #c9a558;background:rgba(201,165,88,.12);color:#f0d899;
    font-family:inherit;font-size:15px;font-weight:700;cursor:pointer;
    touch-action:manipulation}
  .robaBtn:active{background:rgba(201,165,88,.3)}""",
    'los botones de robar, mas grandes')

open(RUTA, 'w', encoding='utf-8').write(s)
print()
print('  cambios:', toc)
