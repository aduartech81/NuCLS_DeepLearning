import csv,re,json,unicodedata,hashlib
from pathlib import Path
from collections import Counter
import argparse
p=argparse.ArgumentParser(description='Unifica exportaciones Scopus, WoS e IEEE; no decide elegibilidad.')
p.add_argument('--entradas',type=Path,required=True)
p.add_argument('--salida',type=Path,required=True)
a=p.parse_args(); u=a.entradas; out=a.salida; out.mkdir(exist_ok=True,parents=True)
if (out/'cribado_unificado.csv').exists():
 raise SystemExit('La salida ya contiene un cribado. Use otra carpeta para conservar las decisiones existentes.')
def read(p):
 with p.open(encoding='utf-8-sig',newline='') as f:return list(csv.DictReader(f))
w=[]
for block in re.split(r'\nER\s*\n',(u/'savedrecs.txt').read_text(encoding='utf-8-sig')):
 if not re.search(r'^PT ',block,re.M):continue
 d={};k=None
 for l in block.splitlines():
  if re.match(r'^[A-Z0-9]{2} ',l):k=l[:2];d[k]=l[3:]
  elif l.startswith('   ') and k:d[k]+=' '+l.strip()
 w.append(d)
rows=[]
for source,data,tk,yk,dk,ak in [('Scopus',read(next(u.glob('export_ffb*.csv'))),'Title','Year','DOI','Abstract'),('WoS',w,'TI','PY','DI','AB'),('IEEE',read(u/'export2026.11.07-08.45.55.csv'),'Document Title','Publication Year','DOI','Abstract')]:
 for r in data:
  rows.append(dict(source=source,title=r.get(tk,''),year=int(r.get(yk,'0') or 0),doi=re.sub(r'^(https?://(dx\.)?doi.org/|doi:\s*)','',r.get(dk,'').strip().lower()),abstract=r.get(ak,'')))
def norm(t):return re.sub(r'[^a-z0-9]','',unicodedata.normalize('NFKD',t).encode('ascii','ignore').decode().lower())
inside=[r for r in rows if 2018<=r['year']<=2026]; groups=[]; bydoi={}
for r in inside:
 d=r['doi']
 if d and d in bydoi:groups[bydoi[d]].append(r)
 else:
  if d:bydoi[d]=len(groups)
  groups.append([r])
# Do not merge records by title alone: editions/corrections can share titles.
titles=Counter(norm(g[0]['title']) for g in groups)
fields=['id','titulo','doi','anos','bases','registros_fuente','coincidencia_titulo_por_revisar','prioridad','decision','motivo','arquitectura_exacta','dataset','entrada','metrica','calidad','revisor']
with (out/'cribado_unificado.csv').open('w',encoding='utf-8',newline='') as f:
 writer=csv.DictWriter(f,fieldnames=fields);writer.writeheader()
 for n,g in enumerate(groups,1):
  title=g[0]['title']; text=' '.join(r['title']+' '+r['abstract'] for r in g).lower()
  high=bool(re.search(r'nuclei|nucleus|nucls|pannuke',text)) and bool(re.search(r'classif',text))
  writer.writerow(dict(id=f'LIT-{n:04d}',titulo=title,doi=g[0]['doi'],anos=';'.join(map(str,sorted(set(r['year'] for r in g)))),bases=';'.join(sorted(set(r['source'] for r in g))),registros_fuente=len(g),coincidencia_titulo_por_revisar=titles[norm(title)]>1,prioridad='alta' if high else 'ordinaria',decision='por_revisar'))
summary={'exportados':len(rows),'en_periodo':len(inside),'fuera_periodo':len(rows)-len(inside),'duplicados_por_doi_retirados':len(inside)-len(groups),'registros_para_cribado':len(groups),'sin_doi':sum(not g[0]['doi'] for g in groups),'grupos_titulo_repetido_por_revisar':sum(v>1 for v in titles.values()),'estado':'Depuración por DOI; coincidencias por título requieren revisión. Ningún registro excluido por pertinencia todavía.'}
(out/'flujo_inicial.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(summary,ensure_ascii=False,indent=2))
print('\nTITULOS DE PRIORIDAD:')
for n,g in enumerate(groups,1):
 if re.search(r'(nuclei|nucleus|nuclear).*classif|classif.*(nuclei|nucleus|nuclear)|nucls',g[0]['title'],re.I):print(f'LIT-{n:04d}',g[0]['title'],g[0]['doi'])
