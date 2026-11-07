"""Cuantifica completitud y entropía del manifiesto de desarrollo v2."""
import argparse, collections, csv, hashlib, io, json, math, zipfile
from pathlib import Path

def auditar(control):
    with zipfile.ZipFile(control) as z:
        raw=z.read('manifiesto.csv')
    sha=hashlib.sha256(raw).hexdigest()
    if sha!='623adf36520751addc324e44cd1b89d95e47842e53cda494914c0248a8be86d4':
        raise ValueError('Manifiesto distinto del verificado')
    rows=list(csv.DictReader(io.StringIO(raw.decode())))
    fields=['paciente','tss','particion','clase','archivo','sha_pixeles','sha_archivo']
    out={}
    for part in ['train','validation']:
        rr=[x for x in rows if x['particion']==part]
        counts=collections.Counter(x['clase'] for x in rr);n=len(rr)
        h=-sum((v/n)*math.log2(v/n) for v in counts.values())
        out[part]={'n':n,'clases':dict(counts),'entropia_bits':h,'entropia_normalizada':h/math.log2(3),'faltantes':{k:sum(not x.get(k,'').strip() for x in rr) for k in fields}}
    return {'manifest_sha256':sha,'resultados':out}

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--control',type=Path,required=True);p.add_argument('--salida',type=Path,required=True);a=p.parse_args()
    result=auditar(a.control);a.salida.parent.mkdir(parents=True,exist_ok=True)
    a.salida.write_text(json.dumps(result,indent=2),encoding='utf-8')
    print(a.salida)
