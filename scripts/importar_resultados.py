"""Importa evidencia del piloto sin pesos ni imágenes; rechaza rutas inseguras."""
from pathlib import Path
import argparse, zipfile, json, csv
p=argparse.ArgumentParser();p.add_argument('zip');a=p.parse_args()
root=Path(__file__).resolve().parents[1];out=root/'resultados'
with zipfile.ZipFile(a.zip) as z:
 entries=[f for f in z.infolist() if not f.is_dir()]
 if sum(f.file_size for f in entries)>250_000_000:raise ValueError('ZIP superior al límite de evidencia de 250 MB')
 for f in entries:
  target=(out/f.filename).resolve()
  if not target.is_relative_to(out.resolve()):raise ValueError('Ruta fuera de resultados')
  if target.suffix not in {'.json','.csv','.txt','.html'}:raise ValueError('Archivo no admitido: '+f.filename)
  if target.exists():raise FileExistsError('Ya existe evidencia. Conserve o renombre resultados antes de importar.')
 if 'resumen_modelos.csv' not in z.namelist():raise ValueError('Falta resumen_modelos.csv en la raíz del ZIP')
 rows=list(csv.DictReader(z.read('resumen_modelos.csv').decode().splitlines()))
 required={'modelo','ejecuciones','macro_f1_media','macro_f1_sd'}
 if not rows or not required.issubset(rows[0]):raise ValueError('Resumen vacío o esquema incorrecto')
 for row in rows:
  if row['modelo'] not in {'cnn_local','resnet18','mobilenet_v2'}:raise ValueError('Modelo inesperado')
  if not 0<=float(row['macro_f1_media'])<=1:raise ValueError('F1 fuera de rango')
 for f in entries:
  target=out/f.filename;target.parent.mkdir(parents=True,exist_ok=True);target.write_bytes(z.read(f))
 print('Evidencia importada. Corridas por modelo:',{r['modelo']:r['ejecuciones'] for r in rows})
 print('Reejecutar notebook y reconstruir JBook; el dashboard lee el resumen al abrir su pestaña de modelos.')
