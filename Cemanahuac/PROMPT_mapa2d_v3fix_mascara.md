# PROMPT PARA CLAUDE CODE — Mapa Cemanáhuac v3-FIX: la máscara no oculta el hemisferio oriental (world wrap)

PROYECTO: Cemanáhuac — conoceteyreconocete.com/pueblos-indigenas/
ARCHIVO: pueblos-indigenas/index.html
- Windows: G:\Mi unidad\Conocete y Reconocete\pueblos-indigenas\index.html
- WSL: /mnt/g/Mi unidad/Conocete y Reconocete/pueblos-indigenas/index.html

SÍNTOMA (confirmado en captura): la vista NO quedó recortada a América. En pantalla ancha se ven Asia y Australia completas a la izquierda del recuadro de América. La máscara solo tapa una franja a la derecha/arriba.

CAUSA RAÍZ: world wrap. El tileLayer de Leaflet repite el mundo horizontalmente; la máscara (turf.mask) cubre UNA sola copia del mundo, pero la copia repetida que se dibuja a la izquierda (hemisferio oriental) queda sin enmascarar. No es error de cálculo de la máscara: es una segunda copia del mundo sin tapar.

No cambies el stack (Leaflet + Esri + Turf) ni la mecánica (lista lateral / selección / card). Solo arreglar la vista.

═══════════════════════════════════════════════════════════════
FASE 0 — LECTURA Y BACKUP
═══════════════════════════════════════════════════════════════
1. WSL: ls "/mnt/g" || (sudo mkdir -p /mnt/g && sudo mount -t drvfs G: /mnt/g)
2. Lee index.html. Ubica: el L.tileLayer de Esri (sus opciones), la creación de la máscara (turf.mask) y su pane, y las opciones de L.map (maxBounds, minZoom).
3. Backup: copia index.html → pueblos-indigenas/index-v3.bak.html (NO borres los .bak previos). Sigue sin pausa.

═══════════════════════════════════════════════════════════════
FASE 1 — ARREGLO
═══════════════════════════════════════════════════════════════

1. NO REPETIR EL MUNDO — corrige la causa raíz:
   - En el L.tileLayer de Esri añade la opción `noWrap: true`.
   - En las opciones de L.map añade `worldCopyJump: false`. Conserva maxBounds y maxBoundsViscosity: 1.0.

2. MÁSCARA ROBUSTA — reemplaza turf.mask por un polígono manual con hueco (determinista; Leaflet perfora el hueco usando el primer anillo como contorno y el segundo como agujero, sin depender del winding ni de turf):

   const anilloMundo  = [[-85,-180],[-85,180],[85,180],[85,-180]];        // exterior (lat,lng)
   const huecoAmerica = [[-58,-170],[-58,-34],[75,-34],[75,-170]];        // hueco = envolvente de América
   L.polygon([anilloMundo, huecoAmerica], {
     pane: 'mascaraPane',          // el pane existente z-index 350 (arriba de tiles, debajo de vectores)
     fillColor: '#0d1117',
     fillOpacity: 1,
     stroke: false,
     interactive: false
   }).addTo(map);

   Elimina la generación anterior con turf.mask y su capa. Mantén el pane mascaraPane con pointerEvents:none / interactive:false para que NO capture clics.

3. FONDO CONTINUO: pon el background del contenedor #map en #0d1117, para que las bandas laterales (fuera de la única copia del mundo, en pantallas anchas) se vean como fondo oscuro continuo y no gris/blanco.

4. ENCUADRE: con noWrap, en pantallas anchas pueden quedar bandas oscuras a los lados de América; es aceptable (se ve "América aislada"). Si quieres reducirlas, sube minZoom lo justo para que el envolvente de América llene más el ancho, SIN cortar Alaska arriba ni Tierra del Fuego abajo. Prueba en viewport ancho (~1280px) y angosto (móvil).

CRITERIO DE ÉXITO (verifícalo TÚ antes del deploy, no el HTTP 200):
Abre el módulo y confirma que NO se ven Asia, Europa, África ni Australia en NINGÚN zoom, arrastre ni en pantalla ancha. Solo América y su océano. Si todavía asoma cualquier otro continente, no despliegues: revisa noWrap y el orden del pane de la máscara.

═══════════════════════════════════════════════════════════════
FASE 2 — DEPLOY
═══════════════════════════════════════════════════════════════
git add pueblos-indigenas/index.html pueblos-indigenas/index-v3.bak.html
git commit -m "fix: mascara hemisferio con noWrap + poligono manual (oculta copia repetida del mundo, vista solo America)"
git push origin main

═══════════════════════════════════════════════════════════════
RESTRICCIONES
═══════════════════════════════════════════════════════════════
- Solo index.html + backup index-v3.bak.html. No tocar .htaccess, datos, URL, IDs, nombres.
- No cambiar stack ni mecánica (lista lateral / selección / card / nomenclatura ya aplicada).

═══════════════════════════════════════════════════════════════
REPORTE FINAL (solo esto)
═══════════════════════════════════════════════════════════════
1. Backup index-v3.bak.html creado.
2. Qué se aplicó: noWrap en tiles, worldCopyJump:false, máscara manual con hueco, fondo #0d1117.
3. Confirmación EXPLÍCITA de que en pantalla ANCHA ya no se ve ningún otro continente (solo América).
4. Commit hash + push.
5. URL: https://conoceteyreconocete.com/pueblos-indigenas/
No generes nada fuera de estos 5 puntos.
