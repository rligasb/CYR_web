# PROMPT: Fichas v2 — Ronda 3 (Alimentos faltantes) + corrección nombre Totonaca
## Proyecto: módulo `/pueblos-indigenas/` de conoceteyreconocete.com
## Fecha: 2026-06-04

---

### CONTEXTO

Tercera y última ronda automatizada. Alcance muy específico:
1. Buscar imagen de `"Alimentos"` para 5 fichas mexicanas que aún no la tienen
2. Corregir el nombre visible del pueblo Totonaca en la UI

Directorio de trabajo: `G:\Mi unidad\Conocete y Reconocete\`

---

### PASO 0 — BACKUP

```bash
cp pueblos-indigenas/pueblos.json pueblos-indigenas/pueblos.bak4.json
```

---

## TAREA 1 — Imagen de Alimentos para 5 fichas

Agregar una imagen de tipo `"Alimentos"` a cada una de estas fichas. Solo buscar si el tipo `"Alimentos"` sigue ausente en `imagenes[]` — no reemplazar nada.

**Mismo protocolo de licencias y crédito que rondas anteriores** (CC BY/SA/0 o PD; limpiar HTML del Artist; formato `"Autor — LicenseShortName"`; `"fuente": "Wikimedia Commons"`).

### Búsquedas por ficha

**Totonac** — buscar en este orden hasta encontrar imagen con licencia válida:
1. Categoría Commons: `Zacahuil` — el zacahuil es el platillo más emblemático de la cultura totonaca (tamal gigante de maíz martajado cocido en pozo de tierra)
2. Búsqueda texto: `zacahuil food Mexico`
3. Categoría: `Veracruz cuisine`
4. Si no hay: `vanilla Mexico traditional` (la vainilla es originaria del Totonacapan)

**Ñuu Savi** (Mixtec) — buscar en este orden:
1. Categoría: `Oaxacan cuisine`
2. Búsqueda texto: `mole negro oaxaca`
3. Categoría: `Mezcal Mexico`
4. Búsqueda texto: `tlayuda oaxaca food`

**Comcáac** (Seri) — buscar en este orden:
1. Búsqueda texto: `pitaya cardón Sonora`
2. Búsqueda texto: `pitahaya fruit Mexico`
3. Categoría: `Sonoran cuisine`
4. Búsqueda texto: `caracol marino Mexico food`

**Mazahua** — buscar en este orden:
1. Búsqueda texto: `mole de olla Mexico`
2. Categoría: `Mexican cuisine Estado de Mexico`
3. Búsqueda texto: `mixiote Mexico food`
4. Búsqueda texto: `escamoles Mexico`

**Amuzgo** — buscar en este orden:
1. Categoría: `Oaxacan cuisine`
2. Búsqueda texto: `iguana en mole verde Oaxaca`
3. Búsqueda texto: `tejate drink Mexico`
4. Búsqueda texto: `memela maiz negro Mexico`

---

## TAREA 2 — Corrección del nombre visible "Totonaca"

### Contexto importante
La clave del objeto en `pueblos.json` es `"Totonac"` — **NO cambiarla** porque es el identificador que usa el mapa Leaflet para hacer match con el territorio de Native Land Digital. Si se cambia la clave, el territorio deja de iluminarse al hacer clic.

### Lo que hay que hacer

**En `pueblos-indigenas/pueblos.json`:** agregar campo `"nombre"` a la ficha Totonac:
```json
"Totonac": {
  "nombre": "Totonaca",
  "pais": "México",
  "wikipedia": "...",
  ...
}
```

**En `pueblos-indigenas/index.html`:** localizar todos los lugares donde el código usa la clave del objeto (por ejemplo `nombre_etnia`, el string `"Totonac"`, o como header de la card) para mostrar el nombre del pueblo en la UI. Modificar la lógica para que, cuando exista el campo `pueblo.nombre`, use ese valor en lugar de la clave del objeto.

Ejemplo de lógica (adaptar al código real):
```javascript
// Antes
const nombreVisible = claveEtnia; // "Totonac"

// Después
const nombreVisible = pueblo.nombre || claveEtnia; // "Totonaca" si existe, si no la clave
```

Esto aplica en: el título de la card, la lista lateral de etnias, cualquier tooltip o label del mapa que use la clave como nombre visible.

**Verificar** que el mapeo del territorio en el mapa siga funcionando (la clave `"Totonac"` debe seguir siendo el identificador de lookup, solo el nombre visible cambia).

---

## PASO FINAL — Verificar y commit

```bash
python3 -m json.tool pueblos-indigenas/pueblos.json > /dev/null && echo "JSON válido"

git add -A
git commit -m "fichas ronda3: Alimentos Totonaca/Ñuu Savi/Comcáac/Mazahua/Amuzgo; nombre display Totonaca"
git push origin main
```

---

## REPORTE

Al terminar:
1. ✅ Imágenes de Alimentos agregadas (pueblo + URL encontrada o ⚠️ no encontrado)
2. ✅ Confirmación de que el nombre "Totonaca" aparece correcto en la UI
3. ✅ Confirmación de que el territorio Totonac sigue matcheando en el mapa
4. ✅ Commit SHA
