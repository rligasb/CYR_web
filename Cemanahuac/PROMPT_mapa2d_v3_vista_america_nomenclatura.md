# PROMPT PARA CLAUDE CODE — Mapa Cemanáhuac v3: vista solo-América + nomenclatura "poblaciones originarias" + encender satélite

PROYECTO: Cemanáhuac — conoceteyreconocete.com/pueblos-indigenas/
REPO: rligasb/CYR_web (rama main, auto-deploy GitHub → Hostinger ~2 min)
ARCHIVO PRINCIPAL: pueblos-indigenas/index.html
- Windows (Code Desktop): G:\Mi unidad\Conocete y Reconocete\pueblos-indigenas\index.html
- WSL: /mnt/g/Mi unidad/Conocete y Reconocete/pueblos-indigenas/index.html

CONTEXTO: el index.html ya es el mapa Leaflet v2 (lista lateral de etnias + selección individual). Esta tarea NO cambia el stack (sigue Leaflet + Esri + Turf) ni la mecánica v2. Aprobado por Raúl. No improvises fuera de lo aquí descrito.

Es un sitio web real: puedes usar position fija/absoluta, media queries y CSS normal.

═══════════════════════════════════════════════════════════════
FASE 0 — VERIFICACIÓN, LECTURA Y BACKUP
═══════════════════════════════════════════════════════════════

1. Si corres en WSL, verifica montaje: ls "/mnt/g" || (sudo mkdir -p /mnt/g && sudo mount -t drvfs G: /mnt/g)
2. Lee COMPLETO el index.html actual. Ubica: el tileLayer de Esri, la vista/encuadre inicial (bounding box continental), capaPaises, la lógica de entrar a país / seleccionar etnia, openCard, y TODOS los textos visibles + los meta del <head>.
3. Backup antes de escribir: copia el index.html actual a pueblos-indigenas/index-v2.bak.html (NO borres los .bak previos: index-globo3d.bak.html, index-leaflet-v1.bak.html). Procede sin pausa.

═══════════════════════════════════════════════════════════════
FASE 1 — VISTA SOLO AMÉRICA (opción B: hemisferio con su océano)
═══════════════════════════════════════════════════════════════

Objetivo: que en ningún momento se vean Europa, África, Asia ni Oceanía. Solo América (continental + Caribe + Groenlandia occidental) y su océano inmediato. Esto se logra con TRES piezas:

1. POLÍGONO ENVOLVENTE DEL HEMISFERIO (simple, pocos vértices — NO la silueta de las costas):
   Punto de partida (lon/lat): oeste -170, este -34, norte 75, sur -58.
   Ajusta esos límites para que entren con holgura: Alaska (NO), Groenlandia occidental, el Caribe completo, y Tierra del Fuego (S), SIN dejar entrar Europa ni África por el este. Es un rectángulo/polígono de pocos vértices, no necesita seguir las costas.

2. MÁSCARA que oculta todo lo demás:
   - Usa turf.mask() (o construye manualmente un polígono "mundo con hueco" = anillo exterior mundial + anillo interior = el envolvente del hemisferio) para obtener "el mundo MENOS el hemisferio".
   - Dibújalo con L.geoJSON como una capa de relleno SÓLIDO del color de fondo de la identidad (el mismo fondo oscuro del body/contenedor del sitio), opacidad 1.
   - CRÍTICO: esta capa NO debe capturar clics → interactive:false (y/o un pane dedicado con pointer-events:none). Debe quedar por ENCIMA de los tiles satelitales pero por DEBAJO de capaPaises, de la capa de etnias y de los controles. Verifica el orden de panes/z-index.

3. ACOTAR LA NAVEGACIÓN:
   - map.setMaxBounds() al envolvente del hemisferio (con un pequeño margen) y maxBoundsViscosity: 1.0 (que no se pueda arrastrar fuera).
   - Fija minZoom al nivel en que el hemisferio llena el viewport, de modo que NO se pueda alejar lo suficiente para ver el mundo completo (calcula con map.getBoundsZoom() o fija un valor y ajústalo probando).
   - La vista inicial sigue siendo el encuadre de América (fitBounds al envolvente).

Resultado esperado: al cargar y en cualquier zoom/arrastre, solo se ve América y su mar; el resto del planeta queda tapado por la máscara. La mecánica v2 (clic país → panel lista → selección etnia → card) sigue intacta.

═══════════════════════════════════════════════════════════════
FASE 2 — NOMENCLATURA: "indígenas" → "poblaciones originarias"
═══════════════════════════════════════════════════════════════

Cambia el término SOLO en lo que el usuario LEE y en los meta. Usa criterio lingüístico (concordancia de género y número), NO un reemplazo ciego.

Término principal: "poblaciones originarias". En singular/contexto: "población originaria" o "pueblo originario" según suene natural. Ejemplos de mapeo:
- "Pueblos indígenas de [país]" → "Poblaciones originarias de [país]"
- "pueblos indígenas" → "poblaciones originarias"
- "territorios indígenas" → "territorios de poblaciones originarias" (o "territorios originarios" si el espacio es corto)
- cualquier "indígena/indígenas" en H1, título de pestaña, breadcrumb raíz, encabezado del panel de lista, hints, botones, disclaimer (texto alrededor; el nombre propio "Native Land" NO se traduce).

META / SEO (en el <head>):
- title, description, og:title, og:description → usar "poblaciones originarias".
- PERO conserva el término "indígenas" como apoyo de búsqueda: en la meta description y en keywords incluye AMBOS, p. ej. "...poblaciones originarias (pueblos indígenas) de América...". No queremos perder el tráfico de quien busca "pueblos indígenas".

NO TOCAR (exclusiones estrictas — romperían el sitio o el SEO):
- La URL/ruta /pueblos-indigenas/ y cualquier aparición de "pueblos-indigenas" en rutas, enlaces internos, canonical, og:url, sitemap.
- Nombres de archivo, IDs de elementos HTML, nombres de variables/funciones/clases JS, claves de objetos (p. ej. PUEBLOS_DATA), comentarios de código.
- El contenido de los datos (PUEBLOS_DATA, CORRECCIONES_MANUALES) salvo que alguna cadena se muestre como texto al usuario y contenga "indígena" en una frase visible — en ese caso ajústala con criterio, sin alterar claves ni nombres propios de etnias.

═══════════════════════════════════════════════════════════════
FASE 3 — DEPLOY DEL index.html
═══════════════════════════════════════════════════════════════

git add pueblos-indigenas/index.html pueblos-indigenas/index-v2.bak.html
git commit -m "feat: vista recortada a America (mascara hemisferio) + nomenclatura poblaciones originarias"
git push origin main

═══════════════════════════════════════════════════════════════
FASE 4 — ENCENDER SATÉLITE (deploy del .htaccess, con rollback)
═══════════════════════════════════════════════════════════════

El .htaccess de la raíz ya fue actualizado en disco (G:\Mi unidad\Conocete y Reconocete\.htaccess y su copia "htaccess"): se agregó *.arcgisonline.com al img-src del CSP, necesario para que el fondo satelital Esri cargue.

Despliega ese .htaccess a producción por el MISMO método con que se sube normalmente el .htaccess de este sitio (verifica si es git push con auto-deploy o FTP/lftp; podría estar en .gitignore — no asumas). Luego verifica:
1) el sitio responde HTTP 200 en https://conoceteyreconocete.com/ y en /pueblos-indigenas/
2) en la consola del módulo ya NO hay error CSP de arcgisonline y los tiles satelitales cargan dentro del recorte de América.
Si el sitio deja de responder tras este deploy, REVIERTE el .htaccess de inmediato y reporta.

═══════════════════════════════════════════════════════════════
RESTRICCIONES ABSOLUTAS
═══════════════════════════════════════════════════════════════

- Modificar/crear solo: pueblos-indigenas/index.html, su backup index-v2.bak.html, y (Fase 4) el .htaccess de la raíz ya preparado. Nada más.
- NO borrar archivos (ni .bak previos ni assets).
- NO cambiar la URL /pueblos-indigenas/, ni IDs, ni nombres de variables/funciones/archivos.
- CONSERVAR verbatim los DATOS: PUEBLOS_DATA, CORRECCIONES_MANUALES, getNombreEtnia, paletas, openCard/#cardOverlay.
- NO cambiar el stack (Leaflet + Esri + Turf) ni la mecánica v2.
- La máscara del hemisferio NO debe capturar clics.

═══════════════════════════════════════════════════════════════
REPORTE FINAL (solo estos puntos)
═══════════════════════════════════════════════════════════════

1. Backup index-v2.bak.html creado: confirmar.
2. Vista América: límites del envolvente usados, confirmación de que la máscara oculta otros continentes y NO bloquea clics, minZoom/maxBounds aplicados.
3. Nomenclatura: confirmar que se cambió el texto visible + meta a "poblaciones originarias", que se conservó "indígenas" en description/keywords, y que NO se tocó la URL ni los identificadores.
4. Commit hash del index.html + push.
5. Fase 4 satélite: método usado para el .htaccess y resultado de las 2 verificaciones (o rollback si falló).
6. URL: https://conoceteyreconocete.com/pueblos-indigenas/
No generes nada fuera de estos 6 puntos.
