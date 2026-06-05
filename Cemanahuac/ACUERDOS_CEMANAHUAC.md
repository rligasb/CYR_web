# ACUERDOS OPERATIVOS — Proyecto CEMANÁHUAC

> FUENTE ÚNICA DE VERDAD del proyecto Cemanáhuac (separado de ACUERDOS.md de Ruta Estratégica).
> La memoria de Claude y los historiales de chat NO son fuente válida.
> Creado: 03/06/2026

---

## CONTEXTO DEL PROYECTO
Cemanáhuac: movimiento para conectar pueblos indígenas y conciencia a lo largo de las Américas. Líder/cliente: Laura González Hernández. Web: conoceteyreconocete.com. Raúl = ejecutor técnico y arquitecto de sistemas.

Workstreams conocidos: (1) campaña de email masivo; (2) globo 3D /pueblos-indigenas/ (Three.js); (3) bot/comunidad WhatsApp (en evaluación).

---

## C-001 — 03/06/2026 — Reconfiguración de la campaña de email masivo (corrección de bloqueo SMTP por rate-limit de Hostinger)

**Diagnóstico.** Las ejecuciones del 1, 2 y 3 de junio fallaron en el nodo "Enviar Correo" con `451 4.3.0 Temporary lookup failure / all recipients were rejected`. Causa: throttle de Hostinger por exceder ~500 correos/hora (el Wait de 3s daba ~1.200/h). NO era cuenta bloqueada permanente — test SMTP manual el 2026-06-03 16:59 UTC devolvió 250 OK. El warmup gradual no resolvía esto porque el cuello de botella no es reputación de IP sino el límite duro de la cuenta de hosting.

**Hechos del entorno (verificados).**
- Workflow n8n: ID `NTF1YrNpg2icbYu6`, instancia `libera.app.n8n.cloud`.
- SMTP: Hostinger (`smtp.hostinger.com`:465 SSL), buzón remitente `cemanahuac@conoceteyreconocete.com`.
- Plan Hostinger: 3.000 correos/día (techo diario); ~500/h (techo horario).
- n8n Cloud: sin timeout fijo confirmado (piso empírico ≥63 min, por ejecuciones exitosas de 1h+ en mayo). NO se asume "sin límite".
- Pendientes de envío al 03/06: 2.328 registros (`email_enviado=false`) en la tabla `firmas`, Supabase `swbbcidwsbksdxxipedo.supabase.co`.
- La fuente de verdad del workflow es PRODUCCIÓN (GET vía REST API), NO el JSON local en disco (estaba desactualizado; hay otra mano editándolo).

**Cambios aplicados en producción (vía REST API de n8n con X-N8N-API-KEY; PUT 200; verificado 5/5):**
1. Wait (node-wait-011): 3s → 8s (~450/h, bajo el techo horario de Hostinger).
2. Obtener Registros (node-getrows-003): URL fija con `&limit=350&order=id`; filtro de email válido `email=like.*@*.*_*` preservado.
3. Normalizar País — alias añadidos: `estados unidos→usa`, `romania→rumania`, `spania→espana`, `otro→grupo España`, `alte→grupo España`. (Producción ya traía además: eeuu, united states, roumanie, spagna, spain.)
4. Cron (node-cron-001): SIN cambios aún → `0 15 * * *` (1 disparo/día, 9 AM México).

**Decisiones de negocio.**
- Los 28 contactos con país "Otro"/"Alte" se invitan A PROPÓSITO al grupo de WhatsApp de España (link `https://chat.whatsapp.com/G29f4kAeGODJEJcyZEjFuX`). Decisión consciente de Raúl (no hay grupo "general" aparte; España hace de cajón).
- Los 79 con país real mal escrito (Estados Unidos 64, România/Romania 11, Spania 4) se corrigen vía alias de normalización (su grupo de país ya existía), NO editando la BD.

**Arquitectura acordada — FASE 3 (PENDIENTE de activar):**
- Cron a 7 disparos: `0 15,16,17,18,19,20,21 * * *` (9 AM–3 PM México) = 7 × 350 = ~2.450/día, bajo el techo de 3.000/día de Hostinger; cada ejecución ~47 min (dentro del piso de 63 min).
- Con eso, los 2.328 pendientes salen en ~1 día.
- ACTIVAR SOLO tras validar que la tanda natural del 04/06 (350 correos con la config nueva) sale sin rebotes 451 y con los links correctos.

**Pendiente inmediato (próximo paso).**
- Revisar la tanda del 04/06/2026 9 AM México: enviados, rebotes 451, y que un "Estados Unidos" y un "Otro" hayan recibido con su link correcto. Si limpia → activar FASE 3 (cron de 7 disparos). Si rebota → diagnosticar antes de soltar el volumen.

**Notas operativas / seguridad.**
- La API key de n8n (X-N8N-API-KEY) NO se guarda en disco ni en este archivo (ACUERDOS vive en Drive; sería un secreto sincronizado a la nube). Se pasa a Code por sesión.
- Migración a SMTP transaccional (Amazon SES / Brevo de pago) queda como opción de fondo SOLO si el envío masivo se vuelve recurrente; los free tiers (Brevo 300/día; SendGrid ya sin free permanente) no alcanzan el volumen. No se hizo hoy.
- El conector n8n de Claude.ai no es inventario fiable de la instancia; la verificación y edición de workflows se hace por Claude Code vía REST API, no por el MCP de n8n.
