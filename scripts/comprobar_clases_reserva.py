"""Comprueba conteos agregados de anotaciones; no carga imágenes ni predicciones."""
import argparse,csv,json,hashlib
from pathlib import Path
from collections import Counter
p=argparse.ArgumentParser(description=__doc__);p.add_argument('--conteos',required=True,type=Path);p.add_argument('--particion',required=True,type=Path);p.add_argument('--salida',required=True,type=Path);a=p.parse_args()
with a.particion.open(encoding='utf-8-sig') as f:part=list(csv.DictReader(f))
ids={r['paciente'] for r in part if r['rol_propuesto']=='reserva_candidata'}
classes=['tumor_nonMitotic','lymphocyte','nonTILnonMQ_stromal']; counts={pid:Counter() for pid in ids}
with a.conteos.open(encoding='utf-8-sig') as f:
 for r in csv.DictReader(f):
  if r['paciente'] in ids and r['clase'] in classes:counts[r['paciente']][r['clase']]+=int(r['anotaciones'])
rows=[dict(paciente=pid,**{c:counts[pid][c] for c in classes}) for pid in sorted(ids)]
total=Counter()
for c in counts.values():total.update(c)
a.salida.mkdir(exist_ok=True,parents=True)
with (a.salida/'reserva_anotaciones_por_clase.csv').open('w',newline='') as f:
 w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
report={'unidad':'anotaciones oficiales agregadas; no recortes utilizables confirmados','totales':dict(total),'total':sum(total.values()),'pacientes_con_anotaciones':sum(bool(c) for c in counts.values()),'pacientes_con_cada_clase':{c:sum(v[c]>0 for v in counts.values()) for c in classes},'tres_clases_globales':all(total[c]>0 for c in classes),'sha256_conteos':hashlib.sha256(a.conteos.read_bytes()).hexdigest(),'decision':'Factible como reserva pequeña para clasificación de tres clases, sujeta a disponibilidad e integridad de imágenes y elegibilidad geométrica. No prueba suficiente de potencia ni validación clínica; mantener todas las clases en macro-F1 por paciente aunque falte alguna en su soporte.','no_ejecutado':'No se evaluaron modelos, no se inspeccionaron píxeles, no se verificaron recortes de reserva.'}
(a.salida/'viabilidad_reserva.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n');print(json.dumps(report,ensure_ascii=False,indent=2))
