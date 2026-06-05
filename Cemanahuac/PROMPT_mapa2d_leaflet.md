# PROMPT PARA CLAUDE CODE — Migración mapa Cemanáhuac: globo 3D Three.js → mapa 2D Leaflet

PROYECTO: Cemanáhuac — conoceteyreconocete.com/pueblos-indigenas/
REPO: rligasb/CYR_web (rama main, auto-deploy GitHub → Hostinger, ~2 min)
ARCHIVO A REESCRIBIR: pueblos-indigenas/index.html
- Ruta Windows (Code Desktop): G:\Mi unidad\Conocete y Reconocete\pueblos-indigenas\index.html
- Ruta WSL: /mnt/g/Mi unidad/Conocete y Reconocete/pueblos-indigenas/index.html

Esta tarea reescribe el módulo del globo 3D (Three.js) a un mapa 2D navegable con Leaflet y fondo satelital, CONSERVANDO los datos y la ficha cultural ya construidos. La decisión y el stack fueron aprobados por Raúl. No improvises ni cambies el stack: Leaflet + Esri World Imagery + Turf.js.

═══════════════════════════════════════════════════════════════
FASE 0 — VERIFICACIÓN Y LECTURA (no modifiques nada todavía)
═══════════════════════════════════════════════════════════════

1. Si corres en WSL, verifica que G: esté montado antes de tocar nada:
   ls "/mnt/g" || (sudo mkdir -p /mnt/g && sudo mount -t drvfs G: /mnt/g)
2. Lee COMPLETO el index.html actual y localiza/extrae los bloques que se CONSERVAN VERBATIM (cópialos al archivo nuevo sin reescribirlos a mano):
   - const AMERICA_IDS  (mapa id numérico TopoJSON → nombre país)
   - const PAISES_AMERICA  (Set de 35 nombres exactos de countries-50m.json)
   - const COUNTRY_PALETTE  y  const ETHNIC_PALETTE
   - const PUEBLOS_DATA  (las 14 fichas — íntegro)
   - const CORRECCIONES_MANUALES  (diccionario gigante de nombres traducidos — íntegro, es trabajo manual valioso, NO lo regeneres)
   - function getNombreEtnia()
   - Todo el bloque HTML+CSS de la tarjeta (#cardOverlay, #card, .card-*) y sus funciones openCard()/closeCard()
   - El <head> completo con sus meta SEO/OpenGraph (title, canonical, og:*, icon, fuentes Google)
   - El header de identidad (#hdr: logo "Cemanáhuac", tagline, #breadcrumb, controles) y el #disclaimer de Native Land
   - La paleta de color de la UI (oro #c8a96e, terracota, fondo oscuro) — el look se mantiene
3. Confirma que estos assets existen en la carpeta pueblos-indigenas/ (NO los modifiques ni los borres):
   - territories_americas.geojson  (~2.4 MB, 1.412 territorios)
   - countries-50m.json  (TopoJSON de países)
   Los archivos del globo (earth-blue-marble.jpg, earth-topology.png, territories.geojson) quedan sin uso pero NO se borran (por si se revierte).

Completada la lectura, procede automáticamente a la Fase 1 (sin pausa de confirmación).

═══════════════════════════════════════════════════════════════
FASE 1 — BACKUP OBLIGATORIO ANTES DE REESCRIBIR
═══════════════════════════════════════════════════════════════

Copia el index.html actual a un respaldo dentro de la misma carpeta, para poder volver al globo si Raúl no aprueba:
   pueblos-indigenas/index-globo3d.bak.html
(usa cp / copy según entorno). NO borres nada. Este backup es condición para continuar.

═══════════════════════════════════════════════════════════════
FASE 2 — CONSTRUIR EL NUEVO index.html (mapa 2D Leaflet)
═══════════════════════════════════════════════════════════════

STACK (CDN, sin build, todo en un solo index.html igual que ahora):
- Leaflet 1.9.4  → CSS https://unpkg.com/leaflet@1.9.4/dist/leaflet.css  + JS https://unpkg.com/leaflet@1.9.4/dist/leaflet.js
- Turf.js        → https://unpkg.com/@turf/turf@6/turf.min.js
- topojson-client → https://cdn.jsdelivr.net/npm/topojson-client@3/dist/topojson-client.min.js  (para convertir countries-50m.json a GeoJSON)
- Mantén las fuentes Google ya usadas (Cormorant Garamond + Lato) y la paleta actual.

NOTA DE COMPATIBILIDAD CSP: el sitio tiene .htaccess con CSP estricta (puede bloquear los CDN nuevos). Tras el deploy, si la consola muestra bloqueos CSP de unpkg.com / jsdelivr.net / arcgisonline.com, NO toques el .htaccess por tu cuenta: REPORTA exactamente qué dominios bloqueó la CSP y detente — Raúl/Claude.ai deciden el ajuste del .htaccess en una tarea aparte. (Alternativa preferible si quieres evitarlo de raíz: descarga leaflet.css, leaflet.js y turf.min.js como archivos locales en pueblos-indigenas/vendor/ y referéncialos localmente, igual que ya se hace con los GeoJSON; si tomas esta vía, inclúyela en el reporte.)

CAPA BASE (fondo satelital):
- Esri World Imagery, gratis y sin API key:
  L.tileLayer('https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}',
    { attribution: 'Imagery © Esri, Maxar, Earthstar Geographics', maxZoom: 18 })

MAPA:
- Contenedor <div id="map"> a pantalla completa, DETRÁS del header y de la card (z-index del mapa por debajo; el #hdr y #cardOverlay ya tienen z-index alto, respétalos).
- Vista inicial centrada en América. Usa fitBounds con un bounding box continental aprox: suroeste [-56, -82], noreste [60, -34] (formato Leaflet [lat, lon]). Ajusta si hace falta para que entren Alaska/Canadá arriba y Patagonia abajo.
- Deshabilita el zoom-control por defecto de Leaflet (zoomControl:false) — usa los botones +/−/↺ que ya están en #hdr, cableados a map.zoomIn(), map.zoomOut() y la función de reset.

CAPA DE PAÍSES (visible al inicio):
- Carga countries-50m.json, conviértelo con topojson.feature(topo, topo.objects.countries), filtra por PAISES_AMERICA (nombre) — 35 países.
- Píntalos con L.geoJSON: relleno semitransparente con color de COUNTRY_PALETTE (uno por país, por índice), fillOpacity ~0.35, borde sutil (color oro #c8a96e o blanco, weight 1, opacity 0.6).
- onEachFeature por país:
    · mouseover → resalta (fillOpacity ~0.55) + tooltip con el nombre (usa AMERICA_IDS[+id] || properties.name) — tooltip estilo Leaflet o el #tooltip existente.
    · mouseout → restaura.
    · click → entrarPais(countryFeature, nombre, color).
- Guarda la referencia a esta capa (capaPaises) para poder ocultarla/mostrarla.

ENTRAR A UN PAÍS — entrarPais():
1. map.fitBounds(L.geoJSON(countryFeature).getBounds(), { padding:[40,40], maxZoom:6 })  → este es el "vuelo al país" (reemplaza el flyToCountry roto del globo; aquí funciona de cajón, sin fórmulas de rotación).
2. Oculta capaPaises (map.removeLayer o capaPaises.setStyle no-display; lo más limpio: removeLayer).
3. Filtra los territorios del país y píntalos (ver siguiente bloque).
4. Actualiza el breadcrumb: "América › [País]" y luego "· N pueblos" cuando sepas el conteo.
5. setHint('Clic en un territorio para ver su ficha').

CAPA DE TERRITORIOS ÉTNICOS (oculta hasta entrar a un país):
- Al entrar a un país, carga territories_americas.geojson (cárgalo una sola vez y cachéalo en memoria; no lo recargues en cada clic).
- FILTRADO territorio↔país con Turf.js (esto elimina la grilla 8×8 imprecisa del globo):
    · Primero filtra por bounding box para velocidad: descarta territorios cuyo bbox (turf.bbox) no solape el bbox del país.
    · Sobre los candidatos, confirma con turf.booleanIntersects(territorioFeature, countryFeature).
    · Maneja Polygon y MultiPolygon. Envuelve en try/catch (algunos polígonos de Native Land vienen con geometrías sucias; si turf lanza error en uno, sáltalo y continúa, no abortes).
- Pinta los territorios encontrados con L.geoJSON:
    · color por índice (reusa la lógica de color del globo: HSL con ángulo dorado 137.508°, o ETHNIC_PALETTE), fillOpacity ~0.45, borde del mismo color.
    · nombre = getNombreEtnia(feature).
    · mouseover → resalta (fillOpacity ~0.7) + tooltip con el nombre.
    · mouseout → restaura.
    · click → openCard(feature, color)  (la MISMA card que ya existe; no la rediseñes).
- Si el país no tiene territorios → breadcrumb "· 0 pueblos" + hint "No se encontraron territorios registrados en este país".

RESET (botón ↺):
- map.fitBounds al bounding box continental inicial.
- Quita la capa de territorios, vuelve a añadir capaPaises.
- closeCard(), breadcrumb a "El continente americano", hint inicial.

CARD:
- Conserva openCard(feature, color) tal como está: lee properties.Name/name, busca coincidencia en PUEBLOS_DATA, llena hero/carrusel/foods/customs/protocols. Para territorios sin ficha, mantiene el "Contenido completo próximamente". El botón CTA sigue abriendo native-land.ca.

LIMPIEZA:
- Elimina del archivo TODO el código Three.js y de geometría esférica que ya no aplica: THREE.*, escena/cámara/renderer, latLonToVec3, pointToLatLon, crearRellenoFan (fan triangulation), flyToCountry, shortestRotation, el loop animate(), estrellas, raycaster, latLon helpers de esfera, y TODOS los console.log de depuración [FLY2]/[FRAME1].
- pointInPolygon/pointInFeature ya no hacen falta para clic (Leaflet + Turf lo resuelven); puedes eliminarlos salvo que los uses en el filtrado (preferible Turf).
- Quita las referencias a earth-blue-marble.jpg / earth-topology.png del código (los archivos quedan en disco, pero el HTML ya no los carga).
- Quita la NATIVE_LAND_API_KEY hardcodeada: ya no se usa en runtime (los datos son locales). No la dejes en el HTML público.

IDENTIDAD / LOOK:
- Conserva el header Cemanáhuac, tagline, breadcrumb, controles dorados, disclaimer y la paleta. El resultado debe SENTIRSE Cemanáhuac: controles oro sobre el mapa satelital, tipografía Cormorant/Lato, card terracota/crema igual que ahora.

CONSOLE (para verificación):
- console.log('[Cemanáhuac] países cargados:', N)  → debe ser 35
- console.log('[Cemanáhuac] territorios totales:', allTerritories.length)  → debe ser 1412
- Al entrar a un país: console.log('[Cemanáhuac]', nombrePais, '→ territorios:', encontrados.length)

═══════════════════════════════════════════════════════════════
FASE 3 — DEPLOY
═══════════════════════════════════════════════════════════════

git add pueblos-indigenas/index.html pueblos-indigenas/index-globo3d.bak.html
git commit -m "feat: migra mapa pueblos indigenas de globo 3D Three.js a mapa 2D Leaflet con fondo satelital (reusa datos y ficha)"
git push origin main

═══════════════════════════════════════════════════════════════
RESTRICCIONES ABSOLUTAS
═══════════════════════════════════════════════════════════════

- Solo modificar/crear: pueblos-indigenas/index.html  y  pueblos-indigenas/index-globo3d.bak.html (backup). Si optas por vendorizar las librerías, también pueblos-indigenas/vendor/*. Nada más del repo.
- NO borrar ningún archivo (ni los assets del globo).
- NO tocar el .htaccess. Si la CSP bloquea CDN, reportar y detenerse (o vendorizar local).
- CONSERVAR verbatim: PUEBLOS_DATA, CORRECCIONES_MANUALES, getNombreEtnia, AMERICA_IDS, PAISES_AMERICA, paletas, card, meta SEO/OG.
- NO cambiar el stack aprobado (Leaflet + Esri + Turf).
- NO inventar fichas de pueblos ni alterar el contenido de PUEBLOS_DATA.

═══════════════════════════════════════════════════════════════
REPORTE FINAL (imprime solo esto al terminar)
═══════════════════════════════════════════════════════════════

1. Confirmación de que el backup index-globo3d.bak.html se creó.
2. Vía elegida para las librerías: CDN o vendorizado local (y si hubo bloqueo CSP, qué dominios).
3. Estructura del nuevo index.html (secciones principales) y nº de líneas.
4. Salidas de consola observadas (países cargados, territorios totales).
5. Commit hash + confirmación de push.
6. URL para verificar: https://conoceteyreconocete.com/pueblos-indigenas/
No generes contenido adicional fuera de estos 6 puntos.
