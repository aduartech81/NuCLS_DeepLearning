"""Audita folds del inventario aportado y propone una reserva sin compartir TSS.
No congela un test ni afirma ausencia de exposición previa. No lee imágenes.
"""
import argparse,csv,io,json,zipfile,hashlib
from pathlib import Path
p=argparse.ArgumentParser(description=__doc__);p.add_argument('--tablas',required=True,type=Path);p.add_argument('--salida',required=True,type=Path);a=p.parse_args()
with zipfile.ZipFile(a.tablas) as z:
 raw=z.read('particiones_oficiales.csv');rows=list(csv.DictReader(io.StringIO(raw.decode('utf-8-sig'))))
report=[]
for fold in range(1,6):
 tr=[r for r in rows if r['archivo']==f'fold_{fold}_train'];te=[r for r in rows if r['archivo']==f'fold_{fold}_test']
 report.append({'fold':fold,'pacientes_train':len({r['paciente'] for r in tr}),'pacientes_test':len({r['paciente'] for r in te}),'tss_compartidos':sorted({r['hospital'] for r in tr}&{r['hospital'] for r in te}),'test_sin_registro_previo':sum(r['uso_previo']=='sin_registro' for r in te)})
unique={}
for r in rows:
 if r['archivo'].startswith('fold_999_'): continue
 if r['paciente'] in unique:
  assert all(unique[r['paciente']][k]==r[k] for k in ['hospital','uso_previo'])
 unique[r['paciente']]=r
reserve={r['paciente'] for r in unique.values() if r['uso_previo']=='sin_registro'};sites={unique[x]['hospital'] for x in reserve}
proposed=[]
for pid,r in sorted(unique.items()):
 role='reserva_candidata' if pid in reserve else ('excluido_por_procedencia_de_reserva' if r['hospital'] in sites else 'desarrollo')
 proposed.append(dict(paciente=pid,tss=r['hospital'],uso_previo=r['uso_previo'],rol_propuesto=role))
assert not {r['tss'] for r in proposed if r['rol_propuesto']=='desarrollo'} & sites
assert len(proposed)==len({r['paciente'] for r in proposed})
a.salida.mkdir(parents=True,exist_ok=True)
with (a.salida/'particion_candidata_por_sitio.csv').open('w',newline='') as f:
 w=csv.DictWriter(f,fieldnames=list(proposed[0]));w.writeheader();w.writerows(proposed)
from collections import Counter
summary={'estado':'PROPUESTA_NO_CONGELADA','fuente':'particiones_oficiales.csv del archivo TABLAS_QC.zip aportado; no revalidado byte a byte contra descarga remota','sha256_fuente':hashlib.sha256(raw).hexdigest(),'folds':report,'roles':dict(Counter(r['rol_propuesto'] for r in proposed)),'tss_reserva':sorted(sites),'limitacion':'La exclusión por TSS evita compartir procedencia en el nuevo entrenamiento, pero no revierte exposición ni decisiones históricas. La reserva candidata requiere control de disponibilidad, clases y acceso previo antes de definir test.','sin_acceso_a_imagenes':True}
(a.salida/'evaluacion_folds_y_propuesta.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2)+'\n');print(json.dumps(summary,ensure_ascii=False,indent=2))
