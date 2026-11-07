"""Cruza metadatos históricos y del piloto. No abre imágenes ni evalúa modelos."""
import argparse,csv,io,json,hashlib,zipfile
from collections import Counter
from pathlib import Path
p=argparse.ArgumentParser(description=__doc__)
p.add_argument('--historico',type=Path,required=True);p.add_argument('--particion',type=Path,required=True);p.add_argument('--piloto-zip',type=Path,required=True);p.add_argument('--salida',type=Path,required=True)
a=p.parse_args()
def read(path):
 with path.open(encoding='utf-8-sig',newline='') as f:return list(csv.DictReader(f))
h=read(a.historico); part=read(a.particion)
with zipfile.ZipFile(a.piloto_zip) as z:
 raw=z.read('manifiesto.csv'); pilot=list(csv.DictReader(io.StringIO(raw.decode('utf-8-sig'))))
if hashlib.sha256(raw).hexdigest()!='d287767a890607533e87ef4958612ceb8a4d77738af698f2e06b26e5a828f9de':raise ValueError('Manifiesto diferente del piloto entrenado')
hist={r['patient'] for r in h}; seen={r['paciente'] for r in pilot};res={r['paciente'] for r in part if r['particion_v1']=='reserva_exploratoria'}
train={r['paciente'] for r in pilot if r['particion']=='entrenamiento' and r['estado']=='incluida'}
val={r['paciente'] for r in pilot if r['particion']=='validacion' and r['estado']=='incluida'}
def site(patient):return patient.split('-')[1]
report={'procedencia':[{'archivo':x.name,'sha256':hashlib.sha256(x.read_bytes()).hexdigest()} for x in [a.historico,a.particion,a.piloto_zip]],'pacientes_historicos':len(hist),'pacientes_piloto_train':len(train),'pacientes_piloto_validacion':len(val),'pacientes_reserva':sorted(res),'reserva_en_historico':sorted(res&hist),'reserva_en_manifiesto_piloto':sorted(res&seen),'sitios_reserva':dict(Counter(site(x) for x in res)),'sitios_reserva_compartidos_con_desarrollo':sorted({site(x) for x in res}&{site(x) for x in hist|seen}),'sitios_train_validacion_compartidos':sorted({site(x) for x in train}&{site(x) for x in val}),'alcance':'Ausencia en estos manifiestos, no prueba de ausencia de exposición en toda actividad previa. Códigos TCGA TSS son procedencia; requieren contraste con folds oficiales antes de equipararlos a hospitales o adquisición.','decision':'Reserva candidata, no test definitivo ni validación externa por centro. No se abrieron imágenes, etiquetas individuales de reserva ni predicciones de reserva.'}
a.salida.mkdir(parents=True,exist_ok=True);(a.salida/'auditoria_reserva.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n');print(json.dumps(report,ensure_ascii=False,indent=2))
