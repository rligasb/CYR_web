-- Migración: agregar campo email_enviado a tabla firmas
-- Proyecto: Cemanáhuac — Envío Masivo
-- Fecha: 2026-05-27
-- Ejecutar en: Supabase SQL Editor → https://supabase.com/dashboard/project/swbbcidwsbksdxxipedo

ALTER TABLE firmas
ADD COLUMN IF NOT EXISTS email_enviado BOOLEAN DEFAULT false;

-- Verificar que el campo fue creado correctamente
SELECT column_name, data_type, column_default
FROM information_schema.columns
WHERE table_name = 'firmas' AND column_name = 'email_enviado';

-- (Opcional) Ver cuántos registros tienen email válido y están pendientes de envío
SELECT
  COUNT(*) FILTER (WHERE email IS NOT NULL AND email_enviado = false) AS pendientes,
  COUNT(*) FILTER (WHERE email IS NOT NULL AND email_enviado = true)  AS enviados,
  COUNT(*) FILTER (WHERE email IS NULL)                               AS sin_email,
  COUNT(*)                                                            AS total
FROM firmas;
