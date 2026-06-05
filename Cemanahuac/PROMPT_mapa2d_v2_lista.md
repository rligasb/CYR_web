# PROMPT PARA CLAUDE CODE — Mapa Cemanáhuac v2: lista lateral de etnias + selección individual

PROYECTO: Cemanáhuac — conoceteyreconocete.com/pueblos-indigenas/
REPO: rligasb/CYR_web (rama main, auto-deploy GitHub → Hostinger ~2 min)
ARCHIVO A MODIFICAR: pueblos-indigenas/index.html
- Windows (Code Desktop): G:\Mi unidad\Conocete y Reconocete\pueblos-indigenas\index.html
- WSL: /mnt/g/Mi unidad/Conocete y Reconocete/pueblos-indigenas/index.html

CONTEXTO: el index.html ya es el mapa 2D Leaflet (Esri satelital + Turf) que tú generaste. Esta tarea CAMBIA el comportamiento de la interacción, NO el stack. Aprobado por Raúl. No cambies el stack (sigue Leaflet + Esri + Turf). No improvises fuera de lo aquí descrito.

NOTA: este es un sitio web real; puedes usar position:fixed/absolute, media queries y todo CSS normal sin restricciones.

═══════════════════════════════════════════════════════════════
CAMBIO DE COMPORTAMIENTO (qué queremos)
═══════════════════════════════════════════════════════════════

HOY: clic en país → fitBounds + se pintan TODOS los territorios del país a la vez (amontonados).
NUEVO:
1. Clic en país → el país se encuadra DESPLAZADO a la izquierda, dejando hueco a la derecha; aparece un PANEL con el LISTADO de etnias de ese país. NO se pintan los territorios todavía.
2. La lista muestra TODAS las etnias del país. Las que tienen ficha completa van PRIMERO (con un indicador), el resto después. Búsqueda por texto incluida.
3. Clic en una etnia de la lista → en el mapa se ilumina SOLO el área de influencia de esa etnia (una a la vez) + se abre el POPUP centrado existente (#cardOverlay / openCard) con su ficha (trajes hombre/mujer, comida, costumbres, protocolos). Los que no tienen ficha abren el popup con "Contenido completo próximamente".
4. Debe funcionar bien en MÓVIL (especificación abajo).

═══════════════════════════════════════════════════════════════
FASE 0 — LECTURA Y BACKUP (no modifiques aún)
═══════════════════════════════════════════════════════════════

1. Si corres en WSL, verifica montaje G: antes de tocar nada: ls "/mnt/g" || (sudo mkdir -p /mnt/g && sudo mount -t drvfs G: /mnt/g)
2. Lee COMPLETO el index.html actual y ubica:
   - la función que se ejecuta al hacer clic en un país (probablemente entrarPais() o similar) y el punto donde HOY pinta todos los territorios;
   - el filtrado país↔territorios con Turf (se REUSA);
   - la función openCard() y el overlay #cardOverlay (se REUSAN tal cual);
   - getNombreEtnia(), PUEBLOS_DATA, CORRECCIONES_MANUALES, paletas, breadcrumb, controles del header.
3. Identifica la lógica EXACTA con que openCard decide si una etnia tiene ficha (match contra PUEBLOS_DATA). Esa MISMA lógica debe usarse para marcar "tiene ficha" en la lista, para que el indicador y el popup sean consistentes.

Backup antes de escribir: copia el index.html actual a pueblos-indigenas/index-leaflet-v1.bak.html (NO borres index-globo3d.bak.html). Procede luego sin pausa.

═══════════════════════════════════════════════════════════════
FASE 1 — DESKTOP
═══════════════════════════════════════════════════════════════

PANEL DE LISTA (#panelEtnias):
- Contenedor a la DERECHA, debajo del header, ancho 320px, alto hasta el borde inferior, scroll vertical. z-index por encima del mapa pero por debajo de #cardOverlay y del header. Estilo acorde a la identidad (paleta oro/oscuro ya existente; bordes y tipografía Cemanáhuac).
- Contenido:
  · Encabezado: nombre del país + conteo "N pueblos (M con ficha)".
  · Input de búsqueda (filtra los items por texto en vivo, en JS, sin recargar).
  · Lista de items.
- Oculto en la vista de América; aparece al entrar a un país; se oculta al hacer reset.

ENTRAR A UN PAÍS (modifica la función existente):
1. Filtra con Turf los territorios cuyo polígono intersecta el país (REUSA el filtrado actual). Cachea el GeoJSON de territorios; no lo recargues en cada clic. Envuelve cada test en try/catch (geometrías sucias de Native Land → saltar el feature, no abortar).
2. Construye la lista de etnias ÚNICAS por nombre en español (dedupe con getNombreEtnia). Guarda, por cada nombre, el conjunto de features que le corresponden (una etnia puede tener varios polígonos).
3. Ordena: primero las que tienen ficha (match en PUEBLOS_DATA), luego el resto; dentro de cada grupo, alfabético es-MX (localeCompare). Inserta un separador sutil entre ambos grupos ("Con información" / "Por documentar") — discreto, no chillón.
4. Render de la lista: cada item = nombre + indicador de ficha (las con ficha llevan un check/punto dorado; las sin ficha, atenuadas). onclick → seleccionarEtnia(nombre).
5. NO pintes los territorios en este paso. El mapa queda con el país encuadrado a la izquierda.
6. Encuadre desplazado a la izquierda:
   map.fitBounds(boundsDelPais, { paddingTopLeft: [30, 30], paddingBottomRight: [350, 30], animate: true })
   (350 = ancho del panel + margen, para que el país quede en el hueco izquierdo).
7. Oculta la capa de países (capaPaises) mientras estás dentro. Breadcrumb: "Cemanáhuac › [País]".

SELECCIONAR UNA ETNIA — seleccionarEtnia(nombre):
1. Quita el resalte anterior si existe (una etnia a la vez): elimina la capa de la etnia previa.
2. Reúne TODOS los features del país con getNombreEtnia === nombre y dibújalos con L.geoJSON en color de resalte (ámbar/oro de la identidad), fillOpacity ~0.55, borde del mismo tono. Guarda como capaEtniaActiva.
3. map.fitBounds(capaEtniaActiva.getBounds(), { paddingTopLeft:[30,30], paddingBottomRight:[350,30], animate:true, maxZoom: 7 }) — mantiene el desplazamiento a la izquierda.
4. Abre el popup existente: openCard(featureRepresentativo, color). NO rediseñes la card; úsala tal cual (hero, trajes hombre/mujer, comida, costumbres, protocolos; "próximamente" si no hay ficha).
5. Marca el item activo en la lista. Breadcrumb: "Cemanáhuac › [País] › [Etnia]".
6. Cerrar la card NO borra el resalte ni la lista: el usuario sigue viendo el mapa con la etnia iluminada y la lista para elegir otra.

RESET (botón ↺):
- Oculta #panelEtnias, elimina capaEtniaActiva, vuelve a mostrar capaPaises, fitBounds al bounding box continental (suroeste [-56,-82], noreste [60,-34]), cierra la card, breadcrumb a "El continente americano".

LIMPIEZA:
- ELIMINA el bloque que hoy pinta todos los territorios al entrar a un país. Conserva el filtrado Turf (se reusa para construir la lista y agrupar por nombre).
- Conserva intactos: openCard/#cardOverlay, PUEBLOS_DATA, CORRECCIONES_MANUALES, getNombreEtnia, paletas, meta SEO/OG, identidad.

═══════════════════════════════════════════════════════════════
FASE 2 — MÓVIL (debe quedar usable, no un parche)
═══════════════════════════════════════════════════════════════

Breakpoint: max-width 720px. Detecta con window.matchMedia y recalcula en resize/orientationchange.

En móvil:
- El #panelEtnias NO va a la derecha: va como HOJA INFERIOR (bottom sheet) de ancho 100%, alto ~45vh, con un "handle" (barrita) arriba para colapsar/expandir y un botón/gesto para minimizarla y ver el mapa completo. El mapa ocupa la parte superior.
- Encuadre del país en móvil: usa padding INFERIOR en vez de derecho →
  map.fitBounds(bounds, { paddingTopLeft:[20,20], paddingBottomRight:[20, alturaHojaInferior+20], animate:true })
- Al seleccionar etnia: se ilumina en el mapa (arriba) y se abre la card. En móvil la card debe ser prácticamente pantalla completa (width 100%, max-height 100%, scroll interno). Verifica el CSS actual de #cardOverlay/#card y ajústalo para móvil si no lo está ya.
- La búsqueda y la lista funcionan igual dentro de la hoja inferior.

═══════════════════════════════════════════════════════════════
FASE 3 — DEPLOY
═══════════════════════════════════════════════════════════════

git add pueblos-indigenas/index.html pueblos-indigenas/index-leaflet-v1.bak.html
git commit -m "feat: mapa pueblos indigenas v2 - lista lateral de etnias + seleccion individual (desktop y movil)"
git push origin main

═══════════════════════════════════════════════════════════════
RESTRICCIONES ABSOLUTAS
═══════════════════════════════════════════════════════════════

- Solo modificar/crear: pueblos-indigenas/index.html y el backup index-leaflet-v1.bak.html. Nada más.
- NO borrar ningún archivo (ni los .bak previos ni los assets).
- NO tocar el .htaccess (el fondo satelital se resuelve por separado).
- CONSERVAR verbatim: PUEBLOS_DATA, CORRECCIONES_MANUALES, getNombreEtnia, paletas, openCard/#cardOverlay, meta SEO/OG.
- NO inventar fichas ni alterar PUEBLOS_DATA.
- NO cambiar el stack (Leaflet + Esri + Turf).
- Una etnia resaltada a la vez (no varias simultáneas).

═══════════════════════════════════════════════════════════════
REPORTE FINAL (solo estos puntos)
═══════════════════════════════════════════════════════════════

1. Backup index-leaflet-v1.bak.html creado: confirmar.
2. Desktop: confirmar panel derecho con lista (con-ficha primero + búsqueda), país encuadrado a la izquierda, selección individual ilumina solo esa etnia, card abre.
3. Móvil: confirmar hoja inferior, encuadre con padding inferior, card a pantalla completa.
4. Salidas de consola al entrar a un país de prueba (p. ej. México): nº de pueblos en lista y nº con ficha.
5. Commit hash + push confirmado.
6. URL: https://conoceteyreconocete.com/pueblos-indigenas/
No generes nada fuera de estos 6 puntos.
