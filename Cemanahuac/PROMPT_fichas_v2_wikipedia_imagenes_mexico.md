# PROMPT: Fichas v2 — Campo Wikipedia + Imágenes México
## Proyecto: módulo `/pueblos-indigenas/` de conoceteyreconocete.com
## Fecha: 2026-06-04

---

### CONTEXTO TÉCNICO

Módulo `pueblos-indigenas/` del repo `rligasb/CYR_web` (rama main, auto-deploy a Hostinger).  
El mapa usa Leaflet 2D + satélite Esri. Al hacer clic en un país → lista de poblaciones originarias → clic en una → card con hero (foto del lugar) + carrusel de imágenes + costumbres, alimentos, protocolos.  
Datos: `pueblos-indigenas/pueblos.json` (fetch asíncrono).  
UI: `pueblos-indigenas/index.html`.

Directorio de trabajo: `G:\Mi unidad\Conocete y Reconocete\`

---

### PASO 0 — BACKUP OBLIGATORIO (ejecutar antes de cualquier cambio)

```bash
cp pueblos-indigenas/pueblos.json pueblos-indigenas/pueblos.bak2.json
cp pueblos-indigenas/index.html pueblos-indigenas/index-v5.bak.html
```

---

## FASE 1 — Agregar campo `"wikipedia"` a las 55 fichas

Para **cada entrada** del JSON agregar el campo `"wikipedia"` con la URL del artículo Wikipedia más relevante sobre ese pueblo. Va al mismo nivel que `pais`, `poblacion`, etc.

**Lógica de resolución (en orden):**

1. Si ya existe una URL de `es.wikipedia.org` en el array `fuentes[]` → usarla directamente.
2. Si no existe en ES pero sí en `en.wikipedia.org` en `fuentes[]` → usar esa.
3. Si no hay ninguna → consultar la API de Wikipedia ES:
   ```
   https://es.wikipedia.org/w/api.php?action=query&list=search&srsearch=[NOMBRE_PUEBLO]&format=json&srlimit=3
   ```
   Tomar el primer resultado cuyo título contenga el nombre del pueblo o palabras clave relacionadas. Construir URL: `https://es.wikipedia.org/wiki/[page.title encodeURIComponent]`.  
   Si no hay resultado útil en ES, repetir con EN: `https://en.wikipedia.org/w/api.php?...`.

4. Si después de los tres pasos no se encuentra nada, dejar `"wikipedia": null`.

**Ejemplo de resultado:**
```json
"Nahua": {
  "pais": "México",
  "wikipedia": "https://es.wikipedia.org/wiki/Nahuas",
  "poblacion": "~1.5M hablantes",
  ...
}
```

---

## FASE 2 — Reclasificar tipos de imágenes existentes (todas las fichas, retroactivo)

**Tipos válidos en el nuevo esquema:**

| Tipo | Descripción |
|------|-------------|
| `"Mujer"` | Vestimenta o retrato de mujer de la comunidad |
| `"Hombre"` | Vestimenta o retrato de hombre de la comunidad |
| `"Arquitectura"` | Sitio arqueológico, construcción o ciudad representativa |
| `"Alimentos"` | Platillo, ingrediente o escena gastronómica |
| `"Ceremonial"` | Danza o ritual con reconocimiento cultural internacional propio — solo cuando aplique explícitamente |
| `"Arte"` | Objeto de arte sagrado o artesanía sin equivalente en los tipos anteriores — conservar solo donde ya existe y no encaja en otro tipo |

**Reglas de reclasificación para imágenes que ya existen:**

- `"Mujer"` → sin cambio
- `"Hombre"` → sin cambio
- `"Ceremonial"` existente → evaluar caso por caso:
  - Totonac (Danzantes de Papantla / Voladores): **CONSERVAR** como `"Ceremonial"` — reconocimiento mundial indiscutible
  - Yoeme (Danza del Venado / Maso): **CONSERVAR** como `"Ceremonial"`
  - Yoreme (Danza del pascola): **CONSERVAR** como `"Ceremonial"`
  - P'urhépecha (Danzantes tarascas): **CONSERVAR** como `"Ceremonial"`
  - Cualquier otro: si la imagen muestra una construcción → reclasificar a `"Arquitectura"`; si muestra comida → `"Alimentos"`; si es claramente una práctica ritual reconocida → conservar `"Ceremonial"`
- `"Arte"` existente → conservar como `"Arte"` (ejemplo: cuadro de estambre wixárika / nierika — es arte sagrado sin equivalente en los otros tipos)

---

## FASE 3 — Completar imágenes faltantes para fichas de México

**Alcance:** procesar únicamente las fichas donde `pais` contiene la cadena `"México"` (incluyendo fichas plurinacionales como `"México / Guatemala / Belice / Honduras"`).

Para cada ficha en ese conjunto:
1. Identificar qué tipos del conjunto base `{Mujer, Hombre, Arquitectura, Alimentos}` le faltan.
2. Para cada tipo faltante, buscar en Wikimedia Commons una imagen con licencia libre.
3. Si se encuentra → agregar al array `imagenes[]`. Si no → dejar ese tipo sin imagen (no forzar ni inventar).

### API de Wikimedia Commons

**Endpoint de búsqueda:**
```
https://commons.wikimedia.org/w/api.php?action=query&generator=search&gsrsearch=[QUERY]&gsrnamespace=6&prop=imageinfo&iiprop=url|extmetadata&format=json&gsrlimit=10&iiurlwidth=1200
```

**Queries sugeridas por tipo** — adaptar `[PUEBLO]` al nombre del pueblo y usar el contexto de `region`, `customs` y `foods` de la ficha:

- **`"Mujer"`**: `[PUEBLO] woman traditional clothing`, `[PUEBLO] mujer traje tradicional`, `indigenous woman [REGION] Mexico`
- **`"Hombre"`**: `[PUEBLO] man traditional clothing`, `[PUEBLO] hombre traje tradicional`, `indigenous man [REGION] Mexico`
- **`"Arquitectura"`**: usar el sitio específico mencionado en `customs` — ejemplos: `El Tajin pyramid`, `Monte Alban Oaxaca`, `Palenque ruins`, `Tenochtitlan`, `Mitla`, `Paquime`, `Tzintzuntzan`, `pinturas rupestres Sierra San Francisco`, etc. Si no hay sitio específico: `[PUEBLO] archaeological site Mexico`
- **`"Alimentos"`**: usar el primer platillo de `foods[]` — ejemplos: `cochinita pibil`, `tlayudas oaxaca`, `pachamanca Peru`, `mapuche curanto`, `pozole mexicano`. También: `[PUEBLO] food traditional Mexico`

Si la primera query no retorna resultados válidos, intentar al menos una query alternativa antes de desistir.

### Criterios de selección de imagen

**Licencias aceptadas** (verificar `extmetadata.LicenseShortName.value`):
```
CC BY, CC BY 2.0, CC BY 3.0, CC BY 4.0,
CC BY-SA, CC BY-SA 2.0, CC BY-SA 3.0, CC BY-SA 4.0,
CC0, Public Domain, PD-old, PD
```
**Rechazar** cualquier otra (en especial `Fair use`, `Non-free`).

Tomar la **primera imagen** de los resultados que:
- Cumpla la licencia
- Sea claramente representativa del tipo buscado (no ambigua, no turística genérica)
- No muestre ceremonia sagrada si `protocols[]` de la ficha indica restricción de fotografía ceremonial — en ese caso buscar imagen alternativa del mismo tipo

### Extracción del crédito

- Autor: `extmetadata.Artist.value` — limpiar etiquetas HTML (usar regex o parser); quedarse con texto plano
- Licencia: `extmetadata.LicenseShortName.value`
- Campo `credito` en el JSON: `"[Autor limpio] — [LicenseShortName]"`
- Campo `fuente`: siempre `"Wikimedia Commons"`

### Formato de cada imagen agregada al JSON

```json
{
  "tipo": "Hombre",
  "url": "https://upload.wikimedia.org/wikipedia/commons/x/xx/Nombre_archivo.jpg",
  "pie": "Descripción breve en español de lo que muestra la imagen",
  "credito": "Nombre Autor — CC BY-SA 4.0",
  "fuente": "Wikimedia Commons"
}
```

### Casos especiales — pueblos extintos o muy pequeños

Para fichas de pueblos extintos o con < 1000 hablantes activos (Cochimí, Kiliwa, Pericú, Caxcán, Ópata, Matlatzinca, Tlahuica, Guarijío, Pame, Chichimeco Jonaz):
- Si no hay imágenes de vestimenta en Commons → omitir ese tipo sin imagen (no forzar)
- Para `"Arquitectura"`: buscar pinturas rupestres, sitios o vestigios — suelen existir con licencia libre
- Para `"Alimentos"`: buscar platillos regionales de su área (Sonora, Oaxaca, Baja California, etc.) — pueden no tener fotos propias del pueblo pero sí del platillo

---

## FASE 4 — Actualizar UI: botón "Conoce más en Wikipedia" en la card

En `pueblos-indigenas/index.html`, localizar el template o función JS que construye el HTML de la card del pueblo (el panel o modal con costumbres, alimentos, protocolos, carrusel).

Agregar al final del contenido de la card —antes del cierre del contenedor principal— el siguiente elemento, **solo si `pueblo.wikipedia` no es null**:

```html
<a href="${pueblo.wikipedia}" 
   target="_blank" 
   rel="noopener noreferrer" 
   class="wiki-link">
  📖 Conoce más en Wikipedia →
</a>
```

**CSS a agregar** (en el bloque `<style>` existente o al final del mismo):
```css
.wiki-link {
  display: inline-block;
  margin-top: 14px;
  padding: 6px 14px;
  background: transparent;
  border: 1px solid rgba(255,255,255,0.35);
  border-radius: 4px;
  color: #bbb;
  font-size: 0.82rem;
  text-decoration: none;
  letter-spacing: 0.02em;
  transition: background 0.2s ease, color 0.2s ease;
}
.wiki-link:hover {
  background: rgba(255,255,255,0.1);
  color: #fff;
}
```

Si el campo `wikipedia` es `null` o `undefined`, el botón **no debe renderizarse** (condicional explícito en el template).

---

## VERIFICACIÓN Y COMMIT

```bash
# Verificar que el JSON es válido
python3 -m json.tool pueblos-indigenas/pueblos.json > /dev/null && echo "JSON válido"

# Si es válido, commit y push
git add -A
git commit -m "fichas v2: campo wikipedia, tipos imagen v2 (Mujer/Hombre/Arquitectura/Alimentos), imágenes México via Commons, botón Wikipedia en card"
git push origin main
```

---

## RESUMEN DE ENTREGABLES

Al terminar, reportar:
1. ✅ Cuántas fichas tienen ahora el campo `wikipedia` (de 55 total)
2. ✅ Cuántas fichas de México quedaron con los 4 tipos base completos
3. ⚠️ Qué fichas no encontraron imagen para algún tipo (listar pueblo + tipo faltante)
4. ✅ Commit SHA del deploy
