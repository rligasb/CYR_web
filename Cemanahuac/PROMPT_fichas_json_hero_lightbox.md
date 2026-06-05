# PROMPT PARA CLAUDE CODE — Fichas Cemanáhuac: datos a JSON externo + hero con foto del lugar + carrusel con lightbox

PROYECTO: Cemanáhuac — conoceteyreconocete.com/pueblos-indigenas/
ARCHIVO PRINCIPAL: pueblos-indigenas/index.html
- Windows: G:\Mi unidad\Conocete y Reconocete\pueblos-indigenas\index.html
- WSL: /mnt/g/Mi unidad/Conocete y Reconocete/pueblos-indigenas/index.html

OBJETIVO: preparar el sistema de fichas para escalar a cientos de pueblos. Tres cosas: (1) sacar los datos del HTML a un archivo pueblos.json editable; (2) el hero de la card muestra una foto apaisada del lugar característico (campo nuevo "lugar"); (3) las imágenes de trajes se ven en un carrusel con lightbox (ampliar al clic). NO cambies el stack (Leaflet+Esri+Turf), ni la mecánica (lista lateral/selección/card), ni la vista de América, ni la nomenclatura "poblaciones originarias".

REGLA CRÍTICA DE CONTENIDO: NO inventes URLs de imágenes ni textos. Las 14 fichas actuales se migran con lo que YA tienen; los campos de imágenes que aún no existen quedan VACÍOS (lugar: null, imagenes: []). El relleno real lo hará Laura después vía Google Sheets.

═══════════════════════════════════════════════════════════════
FASE 0 — LECTURA Y BACKUP
═══════════════════════════════════════════════════════════════
1. WSL: ls "/mnt/g" || (sudo mkdir -p /mnt/g && sudo mount -t drvfs G: /mnt/g)
2. Lee index.html. Ubica: const PUEBLOS_DATA, openCard(), el matching getNombreEtnia→clave (función que busca la ficha), #cardHero, #cardCarousel, isFicha/indicador de ficha de la lista.
3. Backup: index.html → pueblos-indigenas/index-v4.bak.html (NO borres .bak previos). Sigue sin pausa.

═══════════════════════════════════════════════════════════════
FASE 1 — DATOS A JSON EXTERNO
═══════════════════════════════════════════════════════════════
1. Crea pueblos-indigenas/pueblos.json migrando las 14 fichas actuales de PUEBLOS_DATA al esquema nuevo:
   {
     "Nahua": {
       "pais": "",                 // si lo sabes con certeza, ponlo; si no, deja ""
       "poblacion": "~1.5M hablantes",   // = el "tag" actual
       "region": "", "lengua": "",
       "lugar": null,              // VACÍO por ahora (no inventes URL)
       "customs": "…(verbatim del actual)…",
       "foods": ["…verbatim…"],
       "protocols": ["…verbatim…"],
       "imagenes": [],             // VACÍO por ahora
       "fuentes": []
     },
     … las 14 …
   }
   Conserva customs/foods/protocols VERBATIM de lo que ya existe. No inventes region/lengua/pais si no estás seguro: deja "".
2. En index.html: elimina el objeto PUEBLOS_DATA hardcodeado y, en su lugar, carga pueblos.json con fetch al iniciar (async; guarda el resultado en una variable equivalente). Conserva intacta la lógica de matching getNombreEtnia→clave y el indicador "tiene ficha" de la lista (ahora basados en el JSON cargado). Maneja con gracia el caso de error de carga (si el fetch falla, la card sigue abriendo con "Contenido próximamente").

═══════════════════════════════════════════════════════════════
FASE 2 — CARD: HERO CON LUGAR + CARRUSEL CON LIGHTBOX
═══════════════════════════════════════════════════════════════
A) HERO (#cardHero):
   - Si pueblo.lugar && pueblo.lugar.url → fondo = esa imagen (object-fit cover, apaisada) CON un degradado oscuro encima para que el texto (badge, título, población) siga legible. Muestra el crédito (pueblo.lugar.credito) en pequeño, discreto, en una esquina del hero.
   - Si no hay lugar → fallback al degradado de color actual (comportamiento de hoy).
   - Puedes subir un poco la altura del hero (actual 130px → ~160px) para que el paisaje se aprecie, SIN romper el layout de la card.

B) CARRUSEL (#cardCarousel):
   - Itera pueblo.imagenes[]; por cada una, una miniatura con la imagen (url) y su etiqueta = tipo (Mujer/Hombre/Ceremonial/Festivo u otro).
   - CLIC en una miniatura → LIGHTBOX: amplía la imagen a tamaño grande (sobre la card o sobre el viewport), con su pie (pie) y su crédito (credito) debajo. Cierra al tocar fuera, con la X o con Esc. Debe funcionar en desktop y en móvil, sin romper el scroll de la card. No uses position:fixed que colapse en móvil; prueba ambos.
   - Si imagenes está vacío → muestra placeholders dignos (las 4 etiquetas Mujer/Hombre/Ceremonial/Festivo en gris con "Imagen pendiente"), NO cajas rotas.
   - CADA imagen (hero y trajes) DEBE mostrar su crédito visible — es requisito legal de Wikimedia Commons.

NOTA CSP: el .htaccess ya permite commons.wikimedia.org y upload.wikimedia.org en img-src, así que las fotos de Commons cargan sin tocar nada. Si usan otro dominio de imagen, repórtalo (no toques el .htaccess).

═══════════════════════════════════════════════════════════════
FASE 3 — CONVERSOR PARA EL PIPELINE DE LAURA
═══════════════════════════════════════════════════════════════
Crea pueblos-indigenas/tools/convertir_pueblos.py que reciba dos CSV (exportados del Google Sheet de Laura) y genere pueblos.json con el esquema de arriba.

Hoja/CSV 1 — Pueblos.csv, columnas EXACTAS (una fila por pueblo):
  clave,pais,poblacion,region,lengua,customs,foods,protocols,lugar_url,lugar_pie,lugar_credito,lugar_fuente,fuentes
  - foods, protocols y fuentes vienen como texto separado por " | " (pipe con espacios) → conviértelos a arreglos.
  - lugar_* arman el objeto "lugar"; si lugar_url está vacío → "lugar": null.

Hoja/CSV 2 — Imagenes.csv, columnas EXACTAS (una fila por imagen de traje):
  clave,tipo,url,pie,credito,fuente
  - Agrupa por "clave" y arma el arreglo "imagenes" de cada pueblo.

El script: valida que no haya claves duplicadas, reporta filas con url vacía, y escribe pueblos.json. Documenta en un comentario al inicio cómo se ejecuta (python convertir_pueblos.py Pueblos.csv Imagenes.csv).

═══════════════════════════════════════════════════════════════
FASE 4 — DEPLOY
═══════════════════════════════════════════════════════════════
git add pueblos-indigenas/index.html pueblos-indigenas/pueblos.json pueblos-indigenas/index-v4.bak.html pueblos-indigenas/tools/convertir_pueblos.py
git commit -m "feat: fichas en pueblos.json externo + hero con foto del lugar + carrusel con lightbox + conversor CSV"
git push origin main

═══════════════════════════════════════════════════════════════
RESTRICCIONES
═══════════════════════════════════════════════════════════════
- NO inventar URLs de imágenes ni textos; campos sin dato → "" / null / [].
- Conservar verbatim customs/foods/protocols de las 14 fichas actuales.
- No cambiar stack, mecánica, vista de América ni nomenclatura.
- No tocar .htaccess.
- Solo crear/modificar: index.html, pueblos.json, tools/convertir_pueblos.py, backup index-v4.bak.html.

═══════════════════════════════════════════════════════════════
REPORTE FINAL (solo esto)
═══════════════════════════════════════════════════════════════
1. Backup index-v4.bak.html creado.
2. pueblos.json creado con las 14 fichas migradas (imágenes vacías); index.html ahora lo carga por fetch; matching y “tiene ficha” siguen OK.
3. Hero: lee lugar con degradado encima + crédito + fallback a degradado. Carrusel: lee imagenes[] con lightbox + crédito + placeholder digno cuando está vacío.
4. Conversor tools/convertir_pueblos.py creado, con las columnas documentadas.
5. Commit hash + push.
6. URL: https://conoceteyreconocete.com/pueblos-indigenas/
No generes nada fuera de estos 6 puntos.
