"""Audita un CSV original de Scopus sin modificarlo. Solo biblioteca estándar.
La prioridad automática organiza lectura; no determina inclusión científica.
"""
import argparse, csv, hashlib, json, re
from collections import Counter
from pathlib import Path

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--entrada', type=Path, required=True)
    p.add_argument('--salida', type=Path, required=True)
    a=p.parse_args(); raw=a.entrada.read_bytes()
    with a.entrada.open(encoding='utf-8-sig', newline='') as f: rows=list(csv.DictReader(f))
    a.salida.mkdir(parents=True, exist_ok=True)
    def year(r):
        try: return int(r.get('Year',''))
        except ValueError: return None
    def duplicates(key):
        counts=Counter(r.get(key,'').strip().casefold() for r in rows if r.get(key,'').strip())
        return sum(n-1 for n in counts.values() if n>1)
    def abstract_ok(r):
        return r.get('Abstract','').strip().casefold() not in ('','[no abstract available]','no abstract available')
    summary={'fuente':'Scopus','archivo_original':a.entrada.name,'sha256':hashlib.sha256(raw).hexdigest(),
      'registros':len(rows),'periodo_analitico':[2018,2026],
      'dentro_periodo':sum(year(r) is not None and 2018<=year(r)<=2026 for r in rows),
      'por_ano':dict(sorted(Counter(str(year(r)) for r in rows).items())),
      'sin_doi':sum(not r.get('DOI','').strip() for r in rows),
      'resumen_utilizable':sum(abstract_ok(r) for r in rows),
      'duplicados_excedentes':{k:duplicates(k) for k in ['EID','DOI','Title']},
      'consulta_exacta':'No contenida en CSV; requiere historial de búsqueda.',
      'advertencia':'Prioridad léxica no equivale a elegibilidad. No se excluyen artículos por prioridad.'}
    fields=['eid','doi','titulo','ano','revista','en_periodo','prioridad_lectura','decision','motivo','revisor']
    priorities=Counter()
    with (a.salida/'scopus_cribado.csv').open('w',encoding='utf-8',newline='') as f:
        w=csv.DictWriter(f, fieldnames=fields); w.writeheader()
        for r in rows:
            text=' '.join(r.get(k,'') for k in ['Title','Abstract','Author Keywords']).lower()
            nuclear=bool(re.search(r'\bnuclei\b|\bnucleus\b|\bnuclear\b|nucls|pannuke',text))
            classification=bool(re.search(r'classif|cell typ|nuclear typ',text))
            histology=bool(re.search(r'histolog|histopatholog|h&e|hematoxylin|haematoxylin',text))
            priority='alta' if nuclear and classification and histology else ('media' if nuclear else 'ordinaria')
            eligible=year(r) is not None and 2018<=year(r)<=2026
            priorities[priority]+=1
            w.writerow(dict(eid=r.get('EID',''),doi=r.get('DOI',''),titulo=r.get('Title',''),ano=r.get('Year',''),revista=r.get('Source title',''),en_periodo=eligible,prioridad_lectura=priority,decision='por_revisar' if eligible else 'fuera_ventana_temporal',motivo='' if eligible else 'Año fuera de 2018–2026; conservar para trazabilidad',revisor=''))
    summary['prioridades_lectura']=dict(priorities)
    (a.salida/'auditoria_scopus.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(summary,ensure_ascii=False,indent=2))
if __name__=='__main__': main()
