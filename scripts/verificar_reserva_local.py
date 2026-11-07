"""Verifica pares PNG/CSV de seis pacientes QC, sin entrenar ni mostrar imágenes.
Lee encabezados PNG, tablas y hashes. No genera predicciones ni cambia originales.
"""
import argparse,csv,io,json,zipfile,struct,hashlib,math
from pathlib import Path
from datetime import datetime
PATIENTS={'TCGA-A7-A6VY','TCGA-AN-A0AR','TCGA-AO-A0J2','TCGA-AO-A0J6','TCGA-AO-A124','TCGA-AO-A129'}
CLASSES={'tumor_nonMitotic','lymphocyte','nonTILnonMQ_stromal'}
def main():
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--datos',required=True,type=Path);p.add_argument('--salida',type=Path,default=Path.cwd());a=p.parse_args()
 if not a.datos.is_dir():raise SystemExit('No existe la carpeta indicada en --datos')
 dest=a.salida/('CONTROL_RESERVA_'+datetime.now().strftime('%Y%m%d_%H%M%S'));dest.mkdir(parents=True,exist_ok=False)
 content={};sources={};errors=[];duplicates=0
 def add(name,raw,source):
  nonlocal duplicates
  q=Path(name);stem=q.stem;role=q.parent.name.lower()
  if stem[:12] not in PATIENTS or (role,q.suffix.lower()) not in {('rgb','.png'),('csv','.csv')}:return
  key=(stem,role)
  if key in content:
   duplicates+=1
   if content[key]!=raw:errors.append('Copias distintas: '+stem+' '+role)
   return
  content[key]=raw;sources[key]=source
 def candidate(name):
  q=Path(name)
  return q.stem[:12] in PATIENTS and q.parent.name.lower() in {'rgb','csv'} and any(x.lower()=='qc' for x in q.parts)
 for zpath in sorted(a.datos.rglob('*.zip')):
  if not zpath.name.lower().startswith('qc'):continue
  try:
   with zipfile.ZipFile(zpath) as z:
    for n in z.namelist():
     if candidate(n):add(n,z.read(n),str(zpath)+'::'+n)
  except Exception as e:errors.append(str(zpath)+': '+str(e))
 for f in sorted(a.datos.rglob('*')):
  if f.is_file() and candidate(str(f)):
   try:add(str(f),f.read_bytes(),str(f))
   except Exception as e:errors.append(str(f)+': '+str(e))
 records=[]
 for stem in sorted({k[0] for k in content}):
  try:
   png=content[stem,'rgb'];table=content[stem,'csv']
   if png[:8]!=b'\x89PNG\r\n\x1a\n' or png[12:16]!=b'IHDR':raise ValueError('Encabezado PNG inválido')
   width,height=struct.unpack('>II',png[16:24]);counts={c:0 for c in CLASSES};interior={c:0 for c in CLASSES};invalid=0
   for row in csv.DictReader(io.StringIO(table.decode('utf-8-sig'))):
    c=row['main_classification']
    if c not in CLASSES:continue
    counts[c]+=1
    try:
     x,y,X,Y=[float(row[k]) for k in ['xmin','ymin','xmax','ymax']]
     if not all(map(math.isfinite,[x,y,X,Y])) or X<=x or Y<=y:raise ValueError()
     # Geometric feasibility of an entire centered 128px window, not a final crop manifest.
     cx=(x+X)/2;cy=(y+Y)/2
     if x>=0 and y>=0 and X<=width and Y<=height and X-x<=128 and Y-y<=128 and 64<=cx<=width-64 and 64<=cy<=height-64:interior[c]+=1
    except (ValueError,TypeError):invalid+=1
   records.append(dict(paciente=stem[:12],campo=stem,ancho=width,alto=height,anotaciones=counts,ventana128_geometricamente_posible=interior,cajas_invalidas=invalid,sha_png=hashlib.sha256(png).hexdigest(),sha_csv=hashlib.sha256(table).hexdigest()))
  except Exception as e:errors.append(stem+': '+str(e))
 report=dict(estado='VERIFICACION_TECNICA_NO_EVALUACION',pacientes_esperados=sorted(PATIENTS),pacientes_encontrados=sorted({r['paciente'] for r in records}),errores=errors,copias_repetidas=duplicates,campos=records,limitacion='Se verifican encabezados y hashes; no se decodifican todos los píxeles ni se comprueba identidad biológica. Conteo geométrico orientativo, no manifiesto final.')
 (dest/'resumen.json').write_text(json.dumps(report,ensure_ascii=False,indent=2))
 archive=dest.with_suffix('.zip')
 with zipfile.ZipFile(archive,'w',zipfile.ZIP_DEFLATED) as z:z.write(dest/'resumen.json','resumen.json')
 print('Campos:',len(records),'Pacientes:',len(report['pacientes_encontrados']),'Errores:',len(errors));print('Adjunta este archivo:',archive)
 if not records:print('No se encontraron pares QC. Revisa la carpeta de datos y conserva el ZIP generado para diagnóstico.')
if __name__=='__main__':main()
