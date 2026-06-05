# PROMPT PARA CLAUDE CODE — Mapa Cemanáhuac v4: vista limpia de América (sin máscara)

PROYECTO: Cemanáhuac — conoceteyreconocete.com/pueblos-indigenas/
ARCHIVO: pueblos-indigenas/index.html
- Windows: G:\Mi unidad\Conocete y Reconocete\pueblos-indigenas\index.html
- WSL: /mnt/g/Mi unidad/Conocete y Reconocete/pueblos-indigenas/index.html

DECISIÓN DE RAÚL: la máscara hemisférica quedó mal (recuadro blanco que debía ser negro + bordes rectos artificiales + se siente recargada). Se ELIMINA la máscara. En su lugar: vista limpia que aterriza en América con el satélite natural (océanos reales, sin recuadros ni cortes) y un candado de navegación para que no se pueda salir al resto del mundo.

No cambies el stack (Leaflet + Esri + Turf) ni la mecánica (lista lateral / selección de etnia / card / nomenclatura "poblaciones originarias", todo eso se queda igual).

═══════════════════════════════════════════════════════════════
FASE 0 — LECTURA Y BACKUP
═══════════════════════════════════════════════════════════════
1. WSL: ls "/mnt/g" || (sudo mkdir -p /mnt/g && sudo mount -t drvfs G: /mnt/g)
2. Lee index.html. Ubica: la máscara (L.polygon anilloMundo/huecoAmerica + pane mascaraPane), el L.tileLayer de Esri, las opciones de L.map (maxBounds, minZoom), el contenedor #map, y el panel de lista (#panelEtnias o equivalente).
3. Backup: index.html → pueblos-indigenas/index-v3fix.bak.html (NO borres los .bak previos). Sigue sin pausa.

═══════════════════════════════════════════════════════════════
FASE 1 — CAMBIOS
═══════════════════════════════════════════════════════════════

1. ELIMINAR LA MÁSCARA POR COMPLETO:
   - Borra el L.polygon([anilloMundo, huecoAmerica]) y todo lo asociado a la máscara.
   - Borra el pane mascaraPane y su configuración de z-index, si solo servía para la máscara.
   - Resultado: el satélite Esri se ve natural, sin recuadro ni bordes.

2. ARREGLAR EL RECUADRO BLANCO:
   - En la captura aparece un recuadro blanco en el borde izquierdo con un texto cortado tipo "…not available". Localiza su origen (lo más probable: el panel de lista #panelEtnias asomando con fondo claro y un placeholder, o algún overlay/control). 
   - En la VISTA INICIAL (continente, sin país seleccionado) ese panel NO debe asomar: debe estar oculto (display:none o fuera de viewport) hasta que se entra a un país. Cuando aparezca (al entrar a un país) su fondo debe ser el de la identidad (oscuro), nunca blanco. Corrige posición/visibilidad/fondo.

3. CANDADO DE NAVEGACIÓN (esto es lo que mantiene la vista en América SIN máscara):
   - Conserva noWrap: true en el tileLayer y worldCopyJump: false en L.map (para que el mundo no se repita).
   - maxBounds acotado al hemisferio occidental CON colchón de océano pero SIN tierra ajena. Punto de partida (lat,lng): suroeste [-58, -180], noreste [78, -25]. Ajusta el borde ESTE para que NO asome la costa de África (si a minZoom en pantalla ancha asoma África, recorta el borde este hacia -28/-30; prefiere recortar un poco de océano antes que mostrar otro continente). maxBoundsViscosity: 1.0.
   - minZoom: fíjalo de modo que NO se pueda alejar lo suficiente para ver el mundo completo y que América llene la vista en alto. Prueba valores (≈3) en viewport ancho (~1280px) y angosto (móvil).
   - Vista inicial: fitBounds al área de América (mismo encuadre que ya usabas).

4. FONDO: pon el background de #map en un tono oscuro de la identidad (#0d1117 o un azul océano profundo). Así, si en algún borde aparece zona fuera del mundo único (por noWrap), se ve como fondo oscuro continuo y NUNCA blanco.

CRITERIO DE ÉXITO (verifícalo TÚ abriendo el módulo, no por HTTP 200):
- Al cargar se ve América con su satélite y océanos, de forma natural y LIMPIA: sin recuadro blanco, sin bordes rectos de máscara, sin sensación recargada.
- No se puede arrastrar ni alejar hasta ver Europa/Asia/África/Australia como masas de tierra.
- En pantalla ancha los bordes muestran océano o fondo oscuro, nunca blanco ni tierra ajena.
- La mecánica (clic país → panel lista → seleccionar etnia → card) sigue funcionando, en desktop y móvil.
Si algo de esto falla, no despliegues; corrígelo.

═══════════════════════════════════════════════════════════════
FASE 2 — DEPLOY
═══════════════════════════════════════════════════════════════
git add pueblos-indigenas/index.html pueblos-indigenas/index-v3fix.bak.html
git commit -m "feat: vista limpia de America sin mascara (satelite natural + candado de navegacion), arregla recuadro blanco"
git push origin main

═══════════════════════════════════════════════════════════════
RESTRICCIONES
═══════════════════════════════════════════════════════════════
- Solo index.html + backup index-v3fix.bak.html. No tocar .htaccess, datos, URL, IDs, nombres.
- No cambiar stack ni mecánica (lista / selección / card / nomenclatura ya aplicada).
- No reintroducir máscara ni recuadros.

═══════════════════════════════════════════════════════════════
REPORTE FINAL (solo esto)
═══════════════════════════════════════════════════════════════
1. Backup index-v3fix.bak.html creado.
2. Confirmar: máscara eliminada; origen del recuadro blanco identificado y corregido (qué era).
3. Candado aplicado: valores finales de maxBounds y minZoom; confirmación de que no se puede salir a otros continentes y de que en pantalla ancha no se ve blanco ni tierra ajena.
4. Confirmar que la mecánica (lista / selección / card) sigue OK en desktop y móvil.
5. Commit hash + push.
6. URL: https://conoceteyreconocete.com/pueblos-indigenas/
No generes nada fuera de estos 6 puntos.
