"""Genera recortes NuCLS QC sin entrenar ni evaluar modelos. Requiere Pillow."""
import argparse, csv, hashlib, io, json, math, sys, zipfile
from collections import Counter, defaultdict
from datetime import datetime
from pathlib import Path
from PIL import Image, __version__ as pillow_version

CLASSES = ('tumor_nonMitotic', 'lymphocyte', 'nonTILnonMQ_stromal')
PARTITION_CSV = 'paciente,tss,uso_previo,rol_propuesto,particion_v2\nTCGA-A1-A0SP,A1,test,desarrollo,train\nTCGA-A2-A04P,A2,validation,desarrollo,train\nTCGA-A2-A04Q,A2,train,desarrollo,train\nTCGA-A2-A04T,A2,train,desarrollo,train\nTCGA-A2-A0CM,A2,train,desarrollo,train\nTCGA-A2-A0D0,A2,validation,desarrollo,train\nTCGA-A2-A0D2,A2,train,desarrollo,train\nTCGA-A2-A0ST,A2,train,desarrollo,train\nTCGA-A2-A0SX,A2,train,desarrollo,train\nTCGA-A2-A0T0,A2,train,desarrollo,train\nTCGA-A2-A0T2,A2,train,desarrollo,train\nTCGA-A2-A0YE,A2,validation,desarrollo,train\nTCGA-A2-A0YM,A2,train,desarrollo,train\nTCGA-A2-A1G6,A2,validation,desarrollo,train\nTCGA-A2-A3XS,A2,train,desarrollo,train\nTCGA-A2-A3XT,A2,train,desarrollo,train\nTCGA-A2-A3XU,A2,train,desarrollo,train\nTCGA-A2-A3XX,A2,train,desarrollo,train\nTCGA-A2-A3XY,A2,train,desarrollo,train\nTCGA-A7-A0CE,A7,validation,excluido_por_procedencia_de_reserva,excluido_por_procedencia_de_reserva\nTCGA-A7-A0DA,A7,train,excluido_por_procedencia_de_reserva,excluido_por_procedencia_de_reserva\nTCGA-A7-A26I,A7,train,excluido_por_procedencia_de_reserva,excluido_por_procedencia_de_reserva\nTCGA-A7-A4SD,A7,train,excluido_por_procedencia_de_reserva,excluido_por_procedencia_de_reserva\nTCGA-A7-A4SE,A7,train,excluido_por_procedencia_de_reserva,excluido_por_procedencia_de_reserva\nTCGA-A7-A6VV,A7,train,excluido_por_procedencia_de_reserva,excluido_por_procedencia_de_reserva\nTCGA-A7-A6VW,A7,train,excluido_por_procedencia_de_reserva,excluido_por_procedencia_de_reserva\nTCGA-A7-A6VY,A7,sin_registro,reserva_candidata,reserva_candidata\nTCGA-AC-A2BK,AC,test,desarrollo,train\nTCGA-AC-A6IW,AC,test,desarrollo,train\nTCGA-AN-A0AL,AN,validation,excluido_por_procedencia_de_reserva,excluido_por_procedencia_de_reserva\nTCGA-AN-A0AR,AN,sin_registro,reserva_candidata,reserva_candidata\nTCGA-AN-A0AT,AN,train,excluido_por_procedencia_de_reserva,excluido_por_procedencia_de_reserva\nTCGA-AN-A0G0,AN,train,excluido_por_procedencia_de_reserva,excluido_por_procedencia_de_reserva\nTCGA-AN-A0XU,AN,validation,excluido_por_procedencia_de_reserva,excluido_por_procedencia_de_reserva\nTCGA-AO-A0J2,AO,sin_registro,reserva_candidata,reserva_candidata\nTCGA-AO-A0J4,AO,train,excluido_por_procedencia_de_reserva,excluido_por_procedencia_de_reserva\nTCGA-AO-A0J6,AO,sin_registro,reserva_candidata,reserva_candidata\nTCGA-AO-A124,AO,sin_registro,reserva_candidata,reserva_candidata\nTCGA-AO-A129,AO,sin_registro,reserva_candidata,reserva_candidata\nTCGA-AO-A12F,AO,train,excluido_por_procedencia_de_reserva,excluido_por_procedencia_de_reserva\nTCGA-AO-A1KR,AO,train,excluido_por_procedencia_de_reserva,excluido_por_procedencia_de_reserva\nTCGA-AQ-A04J,AQ,train,desarrollo,validation\nTCGA-AQ-A54N,AQ,train,desarrollo,validation\nTCGA-AR-A0TS,AR,validation,desarrollo,train\nTCGA-AR-A0TU,AR,train,desarrollo,train\nTCGA-AR-A0U1,AR,validation,desarrollo,train\nTCGA-AR-A0U4,AR,train,desarrollo,train\nTCGA-AR-A1AQ,AR,train,desarrollo,train\nTCGA-AR-A1AR,AR,validation,desarrollo,train\nTCGA-AR-A1AY,AR,candidatos,desarrollo,train\nTCGA-AR-A256,AR,validation,desarrollo,train\nTCGA-BH-A0AV,BH,test,desarrollo,validation\nTCGA-BH-A0B3,BH,test,desarrollo,validation\nTCGA-BH-A0B9,BH,test,desarrollo,validation\nTCGA-BH-A0BG,BH,test,desarrollo,validation\nTCGA-BH-A0BL,BH,test,desarrollo,validation\nTCGA-BH-A0BW,BH,candidatos,desarrollo,validation\nTCGA-BH-A0E0,BH,test,desarrollo,validation\nTCGA-BH-A0E6,BH,test,desarrollo,validation\nTCGA-BH-A0WA,BH,test,desarrollo,validation\nTCGA-BH-A18G,BH,test,desarrollo,validation\nTCGA-BH-A18V,BH,test,desarrollo,validation\nTCGA-BH-A1EW,BH,test,desarrollo,validation\nTCGA-BH-A1F6,BH,test,desarrollo,validation\nTCGA-C8-A12V,C8,train,desarrollo,train\nTCGA-C8-A131,C8,candidatos,desarrollo,train\nTCGA-C8-A1HJ,C8,train,desarrollo,train\nTCGA-C8-A26Y,C8,train,desarrollo,train\nTCGA-C8-A27B,C8,train,desarrollo,train\nTCGA-D8-A13Z,D8,train,desarrollo,train\nTCGA-D8-A142,D8,train,desarrollo,train\nTCGA-D8-A143,D8,train,desarrollo,train\nTCGA-D8-A147,D8,train,desarrollo,train\nTCGA-D8-A1JF,D8,train,desarrollo,train\nTCGA-D8-A1JG,D8,train,desarrollo,train\nTCGA-D8-A1JL,D8,train,desarrollo,train\nTCGA-D8-A1XK,D8,train,desarrollo,train\nTCGA-D8-A1XQ,D8,train,desarrollo,train\nTCGA-D8-A27F,D8,validation,desarrollo,train\nTCGA-D8-A27H,D8,train,desarrollo,train\nTCGA-D8-A27M,D8,train,desarrollo,train\nTCGA-E2-A14N,E2,candidatos,desarrollo,train\nTCGA-E2-A14R,E2,train,desarrollo,train\nTCGA-E2-A14X,E2,validation,desarrollo,train\nTCGA-E2-A150,E2,train,desarrollo,train\nTCGA-E2-A158,E2,train,desarrollo,train\nTCGA-E2-A159,E2,train,desarrollo,train\nTCGA-E2-A1AZ,E2,train,desarrollo,train\nTCGA-E2-A1B6,E2,train,desarrollo,train\nTCGA-E2-A1L7,E2,train,desarrollo,train\nTCGA-E2-A1LH,E2,train,desarrollo,train\nTCGA-E2-A1LI,E2,train,desarrollo,train\nTCGA-E2-A1LK,E2,validation,desarrollo,train\nTCGA-E2-A1LS,E2,train,desarrollo,train\nTCGA-E2-A573,E2,train,desarrollo,train\nTCGA-E2-A574,E2,validation,desarrollo,train\nTCGA-EW-A1OV,EW,train,desarrollo,train\nTCGA-EW-A1OW,EW,train,desarrollo,train\nTCGA-EW-A1P1,EW,train,desarrollo,train\nTCGA-EW-A1P7,EW,candidatos,desarrollo,train\nTCGA-EW-A1P8,EW,train,desarrollo,train\nTCGA-EW-A1PB,EW,validation,desarrollo,train\nTCGA-EW-A1PH,EW,train,desarrollo,train\nTCGA-EW-A3U0,EW,train,desarrollo,train\nTCGA-EW-A6SB,EW,train,desarrollo,train\nTCGA-GI-A2C9,GI,train,desarrollo,train\nTCGA-GM-A2DB,GM,validation,desarrollo,train\nTCGA-GM-A2DD,GM,train,desarrollo,train\nTCGA-GM-A2DF,GM,train,desarrollo,train\nTCGA-GM-A2DH,GM,train,desarrollo,train\nTCGA-GM-A2DI,GM,train,desarrollo,train\nTCGA-GM-A3XL,GM,train,desarrollo,train\nTCGA-LL-A441,LL,train,desarrollo,train\nTCGA-LL-A5YO,LL,validation,desarrollo,train\nTCGA-LL-A73Y,LL,train,desarrollo,train\nTCGA-LL-A740,LL,train,desarrollo,train\nTCGA-OL-A5D6,OL,candidatos,desarrollo,validation\nTCGA-OL-A5D7,OL,test,desarrollo,validation\nTCGA-OL-A5RW,OL,test,desarrollo,validation\nTCGA-OL-A66I,OL,test,desarrollo,validation\nTCGA-OL-A66P,OL,test,desarrollo,validation\nTCGA-OL-A6VO,OL,test,desarrollo,validation\nTCGA-S3-AA10,S3,validation,desarrollo,train\nTCGA-S3-AA15,S3,train,desarrollo,train\n'
PARTITION_SHA = '2366c63a248ca9b77fe9e6a9abf6163954496c1a5cc2a8edb13da5d2cd69eaac'


def window(row, width, height):
    try:
        x, y, X, Y = [float(row[k]) for k in ('xmin','ymin','xmax','ymax')]
        if not all(map(math.isfinite, (x,y,X,Y))):
            return None, 'coordenada_no_finita'
    except (ValueError, TypeError, KeyError):
        return None, 'coordenada_invalida'
    if X <= x or Y <= y:
        return None, 'caja_invalida'
    if x < 0 or y < 0 or X > width or Y > height:
        return None, 'caja_fuera_de_imagen'
    left, top = math.floor((x+X)/2-64), math.floor((y+Y)/2-64)
    box = (left, top, left+128, top+128)
    if left < 0 or top < 0 or box[2] > width or box[3] > height:
        return None, 'requiere_relleno'
    if not (left <= x and top <= y and box[2] >= X and box[3] >= Y):
        return None, 'caja_no_contenida'
    return box, 'incluida'


def csv_write(path, rows):
    fields = list(dict.fromkeys(k for r in rows for k in r)) or ['estado']
    with path.open('w', newline='', encoding='utf-8') as f:
        w = csv.DictWriter(f, fieldnames=fields); w.writeheader(); w.writerows(rows)


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--datos', type=Path, required=True)
    p.add_argument('--salida', type=Path, required=True)
    a = p.parse_args()
    if not a.datos.is_dir():
        raise SystemExit('La carpeta --datos no existe')
    if hashlib.sha256(PARTITION_CSV.encode()).hexdigest() != PARTITION_SHA:
        raise SystemExit('Partición incorporada alterada')
    rows = list(csv.DictReader(io.StringIO(PARTITION_CSV)))
    assign = {r['paciente']: r for r in rows if r['particion_v2'] in ('train','validation','reserva_candidata')}
    dest = a.salida / ('NuCLS_RECORTES_V2_' + datetime.now().strftime('%Y%m%d_%H%M%S_%f'))
    dest.mkdir(parents=True, exist_ok=False)
    sources = defaultdict(list); errors = []; records = []; fields = []; hashes = defaultdict(list)
    def key(name):
        q = Path(name)
        if q.stem[:12] not in assign or not any(s.lower() == 'qc' for s in q.parts): return None
        if (q.parent.name.lower(), q.suffix.lower()) not in {('rgb','.png'), ('csv','.csv')}: return None
        return q.stem, q.parent.name.lower()
    print('Buscando archivos QC...', flush=True)
    for zpath in sorted(a.datos.rglob('*.zip')):
        if not zpath.name.lower().startswith('qc'): continue
        try:
            with zipfile.ZipFile(zpath) as z:
                for info in z.infolist():
                    k = key(info.filename)
                    if k: sources[k].append((zpath, info))
        except Exception as e: errors.append(str(zpath)+': '+str(e))
    for path in sorted(a.datos.rglob('*')):
        if path.is_file():
            k = key(str(path))
            if k: sources[k].append((path, None))
    def read(k):
        found = sources[k]
        if not found: raise ValueError('Falta archivo '+str(k))
        data = None
        for path, info in found:
            if info is None: raw = path.read_bytes()
            else:
                with zipfile.ZipFile(path) as z: raw = z.read(info)
            if data is not None and data != raw: raise ValueError('Copias diferentes '+str(k))
            data = raw
        return data
    stems = sorted({k[0] for k in sources})
    for n, stem in enumerate(stems, 1):
        patient = stem[:12]; split = assign[patient]['particion_v2']
        try:
            raw = read((stem,'rgb')); table = read((stem,'csv'))
            with Image.open(io.BytesIO(raw)) as image:
                image.load()
                if image.mode != 'RGB': raise ValueError('Modo distinto de RGB: '+image.mode)
                width, height = image.size
                shai = hashlib.sha256(raw).hexdigest(); shac = hashlib.sha256(table).hexdigest()
                fields.append(dict(paciente=patient,particion=split,campo=stem,ancho=width,alto=height,sha_png=shai,sha_csv=shac))
                reader = csv.DictReader(io.StringIO(table.decode('utf-8-sig')))
                required = {'main_classification','xmin','ymin','xmax','ymax'}
                if not required.issubset(reader.fieldnames or []): raise ValueError('Faltan columnas CSV')
                for j, row in enumerate(reader):
                    cls = row['main_classification']
                    rec = dict(paciente=patient,tss=assign[patient]['tss'],particion=split,imagen=stem,fila=j,clase=cls,sha_imagen=shai,sha_anotaciones=shac)
                    records.append(rec)
                    if cls not in CLASSES: rec['estado']='clase_fuera_del_objetivo'; continue
                    box, status = window(row,width,height); rec['estado']=status
                    for k in ('xmin','ymin','xmax','ymax'): rec[k]=row[k]
                    if box is None: continue
                    rec.update(dict(zip(('left','top','right','bottom'),box)))
                    patch = image.crop(box)
                    if patch.size != (128,128): raise ValueError('Dimensiones de recorte incorrectas')
                    pixelhash = hashlib.sha256(patch.tobytes()).hexdigest()
                    rel = Path(split)/cls/(stem+'__'+str(j)+'.png')
                    target = dest/rel; target.parent.mkdir(parents=True,exist_ok=True); patch.save(target)
                    rec.update(archivo=rel.as_posix(),sha_pixeles=pixelhash,sha_archivo=hashlib.sha256(target.read_bytes()).hexdigest())
                    hashes[pixelhash].append(dict(paciente=patient,particion=split,archivo=rel.as_posix(),clase=cls))
        except Exception as e: errors.append(stem+': '+str(e))
        if n % 50 == 0 or n == len(stems): print('Campos procesados:', n,'/',len(stems),flush=True)
    included = [r for r in records if r['estado']=='incluida' and 'archivo' in r]
    duplicates = [dict(sha256=h,registros=rr) for h,rr in hashes.items() if len(rr)>1]
    cross = [d for d in duplicates if len({r['particion'] for r in d['registros']})>1]
    missing = sorted(set(assign)-{r['paciente'] for r in fields})
    absent_crops = sorted(set(assign)-{r['paciente'] for r in included})
    counts = Counter((r['particion'],r['clase']) for r in included)
    empty = [(s,c) for s in ('train','validation','reserva_candidata') for c in CLASSES if not counts[s,c]]
    report = dict(estado='BLOQUEADO' if errors or cross or missing or empty or absent_crops else 'CONTROL_TECNICO_COMPLETADO_NO_AUTORIZA_ENTRENAMIENTO',
        pacientes_esperados=len(assign),campos=len(fields),recortes=len(included),errores=errors,pacientes_sin_campos=missing,pacientes_sin_recortes=absent_crops,
        clases_vacias=empty,duplicados_exactos_entre_grupos=len(cross),grupos_duplicados_exactos=len(duplicates),
        conteos=[dict(particion=s,clase=c,recortes=v) for (s,c),v in sorted(counts.items())],
        exclusiones=dict(Counter(r['estado'] for r in records if r['estado']!='incluida')),
        sha256_particion=PARTITION_SHA,pillow=pillow_version,python=sys.version,
        regla='128px RGB nativos; centro de caja con floor; caja completamente contenida; sin relleno, escalado ni recorte de cajas fuera de imagen.',
        limitaciones=['No detecta casi duplicados ni valida identidad biológica.','Recortes vecinos pueden solaparse dentro de un paciente.','No se normaliza escala física: 128px pueden abarcar áreas diferentes.','Reserva no evaluada por modelos.','La regla v2 rechaza cajas fuera del campo; el piloto recortaba esas cajas al borde. No comparar retención como si las reglas fueran idénticas.'])
    csv_write(dest/'manifiesto.csv', included); csv_write(dest/'seleccion_y_exclusiones.csv',records);csv_write(dest/'campos.csv',fields)
    (dest/'particion.csv').write_text(PARTITION_CSV)
    (dest/'resumen.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
    (dest/'duplicados.json').write_text(json.dumps(duplicates,ensure_ascii=False,indent=2)+'\n')
    archive = dest.parent/(dest.name+'_CONTROL.zip')
    with zipfile.ZipFile(archive,'w',zipfile.ZIP_DEFLATED) as z:
        for name in ('manifiesto.csv','seleccion_y_exclusiones.csv','campos.csv','particion.csv','resumen.json','duplicados.json'):z.write(dest/name,name)
    print('Estado:',report['estado']);print('Recortes guardados en:',dest);print('ADJUNTA ESTE ZIP:',archive)
    if report['estado']=='BLOQUEADO': raise SystemExit(2)

if __name__=='__main__': main()
