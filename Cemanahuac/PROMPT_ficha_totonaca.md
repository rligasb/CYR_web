# PROMPT PARA CLAUDE CODE — Publicar ficha piloto "Totonaca" en pueblos.json (texto + imágenes resueltas vía API de Commons)

PROYECTO: Cemanáhuac — conoceteyreconocete.com/pueblos-indigenas/
ARCHIVO: pueblos-indigenas/pueblos.json
- Windows: G:\Mi unidad\Conocete y Reconocete\pueblos-indigenas\pueblos.json
- WSL: /mnt/g/Mi unidad/Conocete y Reconocete/pueblos-indigenas/pueblos.json

OBJETIVO: agregar (o actualizar) la ficha del pueblo Totonaca en pueblos.json, con el texto YA redactado abajo y con las imágenes resueltas automáticamente desde la API de Wikimedia Commons (URL real + autor + licencia). No inventes URLs ni créditos: si un archivo no se resuelve, omítelo y repórtalo.

═══════════════════════════════════════════════════════════════
FASE 0 — VERIFICAR CLAVE Y BACKUP
═══════════════════════════════════════════════════════════════
1. WSL: ls "/mnt/g" || (sudo mkdir -p /mnt/g && sudo mount -t drvfs G: /mnt/g)
2. CLAVE CORRECTA: en index.html revisa getNombreEtnia() y CORRECCIONES_MANUALES para saber con qué nombre exacto aparece el territorio totonaca en el sistema (probablemente "Totonac" o "Totonaca"). La clave de esta ficha en pueblos.json DEBE ser esa, para que la card matchee al hacer clic en el territorio. Usa esa clave exacta. Si hay ambas formas, usa la que devuelve getNombreEtnia para ese territorio.
3. Backup: copia pueblos.json → pueblos.bak.json antes de editar.

═══════════════════════════════════════════════════════════════
FASE 1 — TEXTO DE LA FICHA (verbatim)
═══════════════════════════════════════════════════════════════
Inserta/actualiza la entrada con esta clave y estos valores exactos:

"pais": "México"
"poblacion": "Más de 200 mil hablantes de totonaco"
"region": "Totonacapan — norte de Veracruz y Sierra Norte de Puebla"
"lengua": "Totonaco (familia totonaco-tepehua)"
"customs": "El corazón espiritual totonaca late en tres lugares que dan nombre al pueblo: 'tutunakú' significa 'tres corazones', por Cempoala, El Tajín y el Castillo de Teayo. El Tajín, su ciudad más célebre, floreció entre los años 600 y 1200 y es Patrimonio Mundial desde 1992, con su icónica Pirámide de los Nichos. La región es cuna de la Danza de los Voladores y de la vainilla, originaria de esta tierra: los totonacas fueron, hasta el siglo XIX, los principales productores mundiales de su 'oro negro'."
"foods": ["Pipián (salsa de pepita de calabaza)", "Mole de Totonacapan", "Zacahuil", "Pulacles (tamales de frijol ceremoniales)", "Platillos y dulces con vainilla"]
"protocols": ["La Danza de los Voladores es un rito sagrado, no un espectáculo", "Pedir permiso antes de fotografiar ceremonias", "Tratar El Tajín y los sitios rituales con respeto"]
"fuentes": ["https://es.wikipedia.org/wiki/Cultura_totonaca", "https://es.wikipedia.org/wiki/Pueblo_totonaca", "https://en.wikipedia.org/wiki/El_Taj%C3%ADn", "https://lugares.inah.gob.mx/es/taxonomy/term/56106", "https://catalogo.inpi.gob.mx/totonaco/"]

═══════════════════════════════════════════════════════════════
FASE 2 — RESOLVER IMÁGENES VÍA API DE WIKIMEDIA COMMONS
═══════════════════════════════════════════════════════════════
Para cada archivo candidato, consulta la API de Commons para obtener URL real, autor y licencia. Endpoint:
  https://commons.wikimedia.org/w/api.php?action=query&titles=File:<NOMBRE>&prop=imageinfo&iiprop=url|extmetadata&format=json
De la respuesta toma:
  - url real → imageinfo[0].url  (será de upload.wikimedia.org)
  - autor → extmetadata.Artist (limpia el HTML, deja el nombre)
  - licencia → extmetadata.LicenseShortName (p. ej. "CC BY-SA 3.0")
Arma: "credito": "<autor> — <licencia>", "fuente": "Wikimedia Commons", "url": "<url real>".
Si el título exacto no existe (varía en mayúsculas/guiones), búscalo dentro de Category:Totonac o Category:Pyramid of the Niches, Tajín y usa el más adecuado; reporta cuál usaste. Si una imagen NO tiene licencia libre (CC BY / CC BY-SA / dominio público), NO la incluyas y repórtalo.

CANDIDATAS:
- lugar (hero, apaisado):
    File:El Tajín Pirámide de los Nichos.JPG   → "pie": "El Tajín — Pirámide de los Nichos"
    (si no resuelve, usa otra de Category:Pyramid of the Niches, Tajín con licencia CC, p. ej. "El Tajin, Pyramid of the Niches (20064136414).jpg")
- imagenes[]:
    File:MUJERES TOTONACAS.jpg   → "tipo": "Mujer",      "pie": "Mujeres totonacas"
    File:Danzantes Papantla.JPG  → "tipo": "Ceremonial", "pie": "Danzantes de Papantla"
- Traje "Hombre" y "Festivo": NO hay candidata aún → déjalos fuera (el carrusel es variable; mostrará placeholder donde falte).

Estructura resultante de la ficha (ejemplo de forma):
  "lugar": { "url": "...", "pie": "El Tajín — Pirámide de los Nichos", "credito": "<autor> — <licencia>", "fuente": "Wikimedia Commons" },
  "imagenes": [
    { "tipo": "Mujer", "url": "...", "pie": "Mujeres totonacas", "credito": "...", "fuente": "Wikimedia Commons" },
    { "tipo": "Ceremonial", "url": "...", "pie": "Danzantes de Papantla", "credito": "...", "fuente": "Wikimedia Commons" }
  ]
Si alguna no se resolvió: lugar: null o imagenes sin ese item.

═══════════════════════════════════════════════════════════════
FASE 3 — DEPLOY
═══════════════════════════════════════════════════════════════
Valida que pueblos.json siga siendo JSON válido (parsea sin error).
git add pueblos-indigenas/pueblos.json pueblos-indigenas/pueblos.bak.json
git commit -m "content: ficha piloto Totonaca (texto + imagenes Commons con credito via API)"
git push origin main

═══════════════════════════════════════════════════════════════
RESTRICCIONES
═══════════════════════════════════════════════════════════════
- NO inventar URLs ni créditos: todo dato de imagen sale de la API de Commons. Lo que no se resuelva, se omite y se reporta.
- Toda imagen incluida DEBE llevar credito (autor + licencia). Sin crédito → no se incluye.
- Solo modificar pueblos.json (+ backup). No tocar index.html, .htaccess, ni otros datos.
- No alterar las otras 14 fichas.

═══════════════════════════════════════════════════════════════
REPORTE FINAL (solo esto)
═══════════════════════════════════════════════════════════════
1. Clave usada para la ficha (la que matchea el territorio totonaca) y confirmación de backup.
2. Imágenes resueltas: por cada una, archivo + URL real + autor + licencia; y cuáles se omitieron y por qué.
3. Confirmación de que pueblos.json es JSON válido.
4. Commit hash + push.
5. URL: https://conoceteyreconocete.com/pueblos-indigenas/ → entrar a México, clic en el territorio totonaca.
No generes nada fuera de estos 5 puntos.
