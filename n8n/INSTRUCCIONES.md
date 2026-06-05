# Instrucciones — Workflow Cemanáhuac Envío Masivo

## Archivos generados
| Archivo | Descripción |
|---|---|
| `migration.sql` | Ejecutar en Supabase **primero** |
| `workflow-cemanahuac.json` | Importar en n8n |
| `generar_workflow.py` | Script Python que generó el JSON (no se importa) |

---

## PASO 1 — Ejecutar migración en Supabase

1. Ir a: https://supabase.com/dashboard/project/swbbcidwsbksdxxipedo
2. Menú izquierdo → **SQL Editor**
3. Copiar y pegar el contenido de `migration.sql`
4. Ejecutar → verificar que devuelve `email_enviado | boolean | false`

---

## PASO 2 — Crear credencial SMTP en n8n

1. Ir a: https://libera.app.n8n.cloud
2. Menú → **Credentials** → **Add credential**
3. Buscar: `SMTP`
4. Rellenar:
   - **Name:** `SMTP Cemanáhuac`
   - **Host:** `smtp.hostinger.com`
   - **Port:** `465`
   - **Secure:** `SSL`
   - **User:** `cemanahuac@conoceteyreconocete.com`
   - **Password:** `Gawk-Conjoined-Dazzler-Staleness9-Cassette-Scabby`
5. Clic en **Test connection** → debe decir "Connection tested successfully"
6. **Save** → anotar el ID de la credencial (aparece en la URL)

---

## PASO 3 — Importar el workflow

1. En n8n → **Workflows** → botón `+` → **Import from file**
2. Seleccionar: `workflow-cemanahuac.json`
3. El workflow se carga con 12 nodos

---

## PASO 4 — Conectar la credencial SMTP

Al importar, el nodo **Enviar Correo** muestra un error de credencial (el JSON tiene un placeholder). Para corregirlo:

1. Hacer clic en el nodo **Enviar Correo**
2. En el campo **Credential for SMTP** → seleccionar `SMTP Cemanáhuac`
3. Cerrar el panel

---

## PASO 5 — Configurar la zona horaria del Cron

El cron está configurado como `0 15 * * *` = 15:00 UTC = **9:00 AM México (CST)**.

Si n8n usa otra zona horaria base, ajustar la expresión:
- 9 AM UTC-6 (México/Colombia) → `0 15 * * *`
- 9 AM UTC-5 (Colombia en verano) → `0 14 * * *`
- Ajustar en el nodo **Disparador Cron** → campo **Cron Expression**

---

## PASO 6 — Ajustar FECHA_INICIO (calentamiento)

En el nodo **Calcular Límite**, la variable `FECHA_INICIO` define desde cuándo se cuenta el calentamiento:

```javascript
const FECHA_INICIO = '2026-05-27';
```

- Si el primer envío es hoy 27 mayo → dejar como está (Día 1 = 200 correos)
- Si se pospone → cambiar la fecha al día real del primer envío

**Tabla de límites automáticos:**
| Día | Correos máx |
|-----|-------------|
| 1 | 200 |
| 2 | 400 |
| 3 | 700 |
| 4 | 1,200 |
| 5 | 2,000 |
| 6+ | 3,000 |

---

## PASO 7 — Activar el workflow

1. En n8n, abrir el workflow **Cemanáhuac — Envío Masivo**
2. Toggle superior derecho → **Active** (se pone azul)
3. El workflow ejecutará automáticamente a las 9 AM cada día

---

## Ejecución manual (prueba)

Para probar sin esperar el cron:
1. Abrir el workflow
2. Clic en **Execute Workflow** (botón de play)
3. Monitorear el panel de ejecución

---

## Flujo de datos

```
Cron (9 AM diario)
  └→ Calcular Límite (límite según día de calentamiento)
       └→ Obtener Registros (Supabase: email!=null AND email_enviado=false, LIMIT=N)
            └→ Separar Registros (array → items individuales)
                 └→ Iterar Registros (1 por 1)
                      └→ Normalizar País (lowercase sin acentos, lookup WhatsApp)
                           ├→ [País encontrado] Preparar HTML
                           │      └→ Enviar Correo (SMTP)
                           │           └→ Marcar Enviado (PATCH Supabase)
                           │                └→ Esperar 3s ─┐
                           └→ [País NO encontrado]         │
                                  Log Error                │
                                      └──────────────────→ ┤
                                                           │
                                        ←──────────────────┘ (loop)
```

---

## Monitoreo

- **Ejecuciones:** n8n → Executions → filtrar por "Cemanáhuac"
- **Errores de país:** en el log de ejecución, nodo "Log País No Encontrado" muestra los países no mapeados
- **Progreso:** en Supabase SQL Editor:
  ```sql
  SELECT
    COUNT(*) FILTER (WHERE email_enviado = true)  AS enviados,
    COUNT(*) FILTER (WHERE email_enviado = false AND email IS NOT NULL) AS pendientes
  FROM firmas;
  ```
