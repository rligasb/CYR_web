# PROMPT: Fichas v2 — Segunda ronda de imágenes (búsqueda por categorías de Commons)
## Proyecto: módulo `/pueblos-indigenas/` de conoceteyreconocete.com
## Fecha: 2026-06-04

---

### CONTEXTO

Segunda ronda de búsqueda de imágenes para fichas mexicanas. La primera ronda usó búsqueda de texto libre en Commons y tuvo cobertura limitada. Esta ronda usa **búsqueda por categorías**, que es más precisa y rica para pueblos indígenas.

Directorio de trabajo: `G:\Mi unidad\Conocete y Reconocete\`
Archivo a modificar: `pueblos-indigenas/pueblos.json`

**Regla fundamental:** solo agregar imágenes donde el tipo falta. No reemplazar imágenes que ya existen. No tocar fichas con los 4 tipos base completos.

---

### PASO 0 — BACKUP

```bash
cp pueblos-indigenas/pueblos.json pueblos-indigenas/pueblos.bak3.json
```

---

### PASO 1 — Identificar huecos

Leer `pueblos.json`. Para cada ficha donde `pais` contiene `"México"`:
- Listar qué tipos del conjunto `{Mujer, Hombre, Arquitectura, Alimentos}` faltan en `imagenes[]`
- Prioridad de búsqueda: **Mujer > Hombre > Alimentos > Arquitectura** (Arquitectura tuvo buena cobertura en la ronda anterior; solo buscarla si aún falta)

---

### PASO 2 — API de Commons por categorías

**Endpoint:**
```
https://commons.wikimedia.org/w/api.php?action=query&generator=categorymembers&gcmtitle=Category:[CATEGORÍA]&gcmtype=file&prop=imageinfo&iiprop=url|extmetadata&format=json&gcmlimit=20&iiurlwidth=1200
```

**Criterios de selección y extracción de crédito:** idénticos a la ronda anterior (licencias CC BY/SA/0 o PD; limpiar HTML del campo Artist; formato `"Autor — LicenseShortName"`).

---

### PASO 3 — Mapa pueblo → categorías de Commons

Para cada pueblo, buscar en las categorías en el orden listado. Tomar la primera imagen válida encontrada para cada tipo faltante.

#### Tipos de vestimenta (Mujer / Hombre)

| Pueblo (clave JSON) | Categorías a buscar en Commons |
|---|---|
| Nahua | `Nahua people`, `Nahua clothing`, `Aztec clothing` |
| Maya | `Maya clothing`, `Maya textiles`, `Maya people of Mexico` |
| Zapotec | `Zapotec people`, `Zapotec clothing` |
| Totonac | *(ya tiene Mujer y Ceremonial — buscar solo Hombre y Alimentos)* |
| Tzotzil | `Tzotzil people`, `Tzotzil clothing`, `Indigenous clothing Chiapas` |
| Tzeltal | `Tzeltal people`, `Tzeltal textiles`, `Indigenous people Chiapas` |
| P'urhépecha | `Purépecha people`, `Purépecha clothing` |
| Rarámuri | `Rarámuri people`, `Tarahumara people`, `Tarahumara clothing` |
| Wixárika | `Huichol people`, `Huichol clothing`, `Wixaritari` |
| Hñähñu | `Otomi people`, `Otomi textiles`, `Otomi clothing` |
| Tojolabal | `Tojolabal people`, `Indigenous people Chiapas` |
| Ñuu Savi | `Mixtec people`, `Mixtec clothing`, `Mixtec textiles` |
| Mixe | `Mixe people`, `Indigenous people Oaxaca` |
| Tének | `Huastec people`, `Teenek people`, `Indigenous people Huasteca` |
| Chinantla | `Chinantec people`, `Indigenous people Oaxaca` |
| Mazateco | `Mazatec people`, `Indigenous people Oaxaca` |
| Chatino | `Chatino people`, `Indigenous people Oaxaca` |
| Ikoots | `Huave people`, `Ikoots people`, `Indigenous people Oaxaca` |
| Comcáac | *(ya tiene Mujer — buscar solo Hombre y Alimentos)* |
| Yoeme | `Yaqui people`, `Yaqui clothing` |
| Yoreme | `Mayo people Sonora`, `Yoreme people` |
| Náayerite | `Cora people Mexico`, `Nayeri people` |
| Mazahua | `Mazahua people`, `Indigenous people Estado de Mexico` |
| Zoque | `Zoque people`, `Indigenous people Chiapas` |
| Tepehuán | `Tepehuán people`, `O'dam people` |
| Ch'ol | `Chol people`, `Ch'ol people`, `Indigenous people Chiapas` |
| Me'phaa | `Tlapanec people`, `Me'phaa people`, `Indigenous people Guerrero` |
| Chontal de Tabasco | `Chontal people Tabasco`, `Yokot'an people` |
| Tepehua | `Tepehua people`, `Indigenous people Veracruz` |
| Amuzgo | *(ya tiene Mujer — buscar solo Hombre y Alimentos)* |
| Popoluca | `Popoluca people`, `Indigenous people Veracruz` |
| Guarijío | *(pueblo pequeño — omitir vestimenta si no hay; buscar solo Arquitectura/Paisaje)* |
| Matlatzinca | *(pueblo pequeño — omitir si no hay)* |
| Tlahuica | *(pueblo pequeño — omitir si no hay)* |
| Pame | *(pueblo pequeño — omitir si no hay)* |
| Chichimeco Jonaz | *(pueblo pequeño — omitir si no hay)* |
| Cuicateco | `Cuicatec people`, `Indigenous people Oaxaca` |
| Cochimí | *(extinto — solo buscar pinturas rupestres para Arquitectura si falta)* |
| Kiliwa | *(extinto — omitir)* |
| Paipai | *(pueblo pequeño — omitir si no hay)* |
| Ópata | *(extinto — omitir)* |
| Pericú | *(extinto — solo buscar pinturas rupestres si falta Arquitectura)* |
| Caxcán | *(extinto — omitir)* |

#### Tipo Alimentos

Para el tipo `"Alimentos"`, buscar el platillo más representativo usando el primer elemento de `foods[]` de cada ficha como query principal, con estas categorías de Commons:

| Platillo / ingrediente | Categorías a buscar |
|---|---|
| Tamales | `Tamales`, `Mexican tamales` |
| Pozole | `Pozole` |
| Tlayudas | `Tlayuda`, `Oaxacan cuisine` |
| Cochinita pibil | `Cochinita pibil` |
| Pipián | `Pipian sauce`, `Mexican cuisine` |
| Mole | `Mole sauce`, `Mole negro`, `Oaxacan cuisine` |
| Zacahuil | `Zacahuil`, `Huastecan cuisine` |
| Uchepos / Corundas | `Uchepos`, `Corundas`, `Michoacan cuisine` |
| Pachamanca | `Pachamanca` |
| Cuy | `Cuy food`, `Guinea pig food` |
| Muday / Chicha | `Chicha`, `Muday` |
| Fry bread | `Fry bread`, `Native American food` |
| Mbejú | `Mbeju`, `Paraguayan cuisine` |
| Curanto | `Curanto` |
| Tejuino / Tesgüino | `Tejuino`, `Tesguino` |

Si el platillo no tiene categoría en Commons, buscar por el nombre del pueblo + `cuisine` o `food`: `[pueblo name] cuisine`, `[pueblo name] traditional food`.

#### Tipo Arquitectura (solo si falta)

Si alguna ficha mexicana todavía no tiene imagen de `"Arquitectura"`, usar estas categorías:

| Pueblo | Sitio / categoría |
|---|---|
| Nahua | `Tenochtitlan`, `Templo Mayor Mexico City` |
| Maya | `Chichen Itza`, `Uxmal`, `Palenque` |
| Zapotec | `Monte Albán`, `Mitla` |
| Mazateco | `Huautla de Jimenez` |
| Tének | `Tamuin`, `Huastec architecture` |
| Mazahua | `Nevado de Toluca`, `Valle de Toluca` |
| Chinantla | `Papaloapan river`, `Oaxaca forest` |
| Zoque | `Chicoasen`, `El Chichonal volcano` |
| Náayerite | `Nayarit mountains`, `Sierra del Nayar` |

---

### PASO 4 — Commit

```bash
# Verificar JSON válido
python3 -m json.tool pueblos-indigenas/pueblos.json > /dev/null && echo "JSON válido"

git add -A
git commit -m "fichas v2 ronda2: imágenes por categorías Commons — Mujer/Hombre/Alimentos México"
git push origin main
```

---

### REPORTE FINAL

Al terminar, reportar:
1. ✅ Imágenes nuevas agregadas (cantidad y por tipo)
2. ✅ Fichas mexicanas que ahora tienen los 4 tipos completos
3. ⚠️ Tipos que siguen faltando tras ambas rondas (pueblo + tipo)
4. ✅ Commit SHA
