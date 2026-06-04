#!/usr/bin/env python3
"""
Conversor CSV → pueblos.json para Cemanáhuac
=============================================
Uso:
    python convertir_pueblos.py Pueblos.csv Imagenes.csv

Genera pueblos.json en el directorio actual (sube un nivel desde tools/).

Hojas de Google Sheets que exportar como CSV:

Hoja 1 — Pueblos.csv (una fila por pueblo):
    clave, pais, poblacion, region, lengua,
    customs, foods, protocols,
    lugar_url, lugar_pie, lugar_credito, lugar_fuente,
    fuentes

    • foods, protocols y fuentes → texto separado por " | "
    • lugar_url vacía → "lugar": null

Hoja 2 — Imagenes.csv (una fila por imagen de traje):
    clave, tipo, url, pie, credito, fuente
"""

import csv, json, sys, os

PIPE = ' | '

def load_pueblos(path):
    pueblos = {}
    with open(path, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            clave = row['clave'].strip()
            if not clave:
                continue
            if clave in pueblos:
                print(f'[ADVERTENCIA] Clave duplicada en Pueblos.csv: "{clave}" — se usa la primera aparición')
                continue

            lugar = None
            if row.get('lugar_url', '').strip():
                lugar = {
                    'url':    row['lugar_url'].strip(),
                    'pie':    row.get('lugar_pie', '').strip(),
                    'credito': row.get('lugar_credito', '').strip(),
                    'fuente': row.get('lugar_fuente', '').strip()
                }

            foods     = [x.strip() for x in row.get('foods', '').split(PIPE) if x.strip()]
            protocols = [x.strip() for x in row.get('protocols', '').split(PIPE) if x.strip()]
            fuentes   = [x.strip() for x in row.get('fuentes', '').split(PIPE) if x.strip()]

            pueblos[clave] = {
                'pais':      row.get('pais', '').strip(),
                'poblacion': row.get('poblacion', '').strip(),
                'region':    row.get('region', '').strip(),
                'lengua':    row.get('lengua', '').strip(),
                'lugar':     lugar,
                'customs':   row.get('customs', '').strip(),
                'foods':     foods,
                'protocols': protocols,
                'imagenes':  [],   # se rellena desde Imagenes.csv
                'fuentes':   fuentes
            }
    return pueblos


def load_imagenes(path, pueblos):
    errores = 0
    with open(path, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            clave = row['clave'].strip()
            url   = row.get('url', '').strip()

            if not clave:
                continue
            if clave not in pueblos:
                print(f'[ADVERTENCIA] Imagenes.csv: clave "{clave}" no existe en Pueblos.csv — fila ignorada')
                continue
            if not url:
                print(f'[AVISO] Imagenes.csv: URL vacía para clave="{clave}", tipo="{row.get("tipo","")}" — fila ignorada')
                errores += 1
                continue

            pueblos[clave]['imagenes'].append({
                'tipo':    row.get('tipo', '').strip(),
                'url':     url,
                'pie':     row.get('pie', '').strip(),
                'credito': row.get('credito', '').strip(),
                'fuente':  row.get('fuente', '').strip()
            })

    if errores:
        print(f'[RESUMEN] {errores} imagen(es) con URL vacía ignoradas.')
    return pueblos


def main():
    if len(sys.argv) < 3:
        print('Uso: python convertir_pueblos.py Pueblos.csv Imagenes.csv')
        sys.exit(1)

    pueblos_csv  = sys.argv[1]
    imagenes_csv = sys.argv[2]

    for p in [pueblos_csv, imagenes_csv]:
        if not os.path.exists(p):
            print(f'Error: no se encuentra el archivo "{p}"')
            sys.exit(1)

    pueblos = load_pueblos(pueblos_csv)
    print(f'Pueblos cargados: {len(pueblos)}')

    pueblos = load_imagenes(imagenes_csv, pueblos)
    total_imgs = sum(len(v['imagenes']) for v in pueblos.values())
    print(f'Imágenes cargadas: {total_imgs}')

    # Salida: un nivel arriba de tools/
    out_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    out_path = os.path.join(out_dir, 'pueblos.json')
    with open(out_path, 'w', encoding='utf-8') as f:
        json.dump(pueblos, f, ensure_ascii=False, indent=2)

    print(f'Archivo generado: {out_path}')
    print('Listo.')


if __name__ == '__main__':
    main()
