"""Empaqueta los recortes v2 para Colab sin transformarlos ni analizarlos."""
import argparse,csv,hashlib,zipfile
from pathlib import Path
EXPECTED='623adf36520751addc324e44cd1b89d95e47842e53cda494914c0248a8be86d4'
def main():
 p=argparse.ArgumentParser();p.add_argument('--datos',type=Path,required=True);p.add_argument('--zip',type=Path,required=True);a=p.parse_args();root=a.datos.expanduser().resolve();out=a.zip.expanduser().resolve()
 if out.is_relative_to(root):raise ValueError('El ZIP debe quedar fuera de los datos')
 raw=(root/'manifiesto.csv').read_bytes()
 if hashlib.sha256(raw).hexdigest()!=EXPECTED:raise ValueError('Manifiesto diferente del verificado')
 rows=list(csv.DictReader(raw.decode().splitlines()));assert len(rows)==17557
 out.parent.mkdir(parents=True,exist_ok=True)
 # Modo x: nunca reemplaza un archivo existente.
 if out.exists():raise FileExistsError(out)
 temporary=out.with_name(out.name+'.parcial')
 with zipfile.ZipFile(temporary,'x',compression=zipfile.ZIP_DEFLATED,compresslevel=1) as z:
  z.writestr('manifiesto.csv',raw)
  for i,row in enumerate(rows,1):
   path=(root/row['archivo']).resolve()
   if not path.is_relative_to(root):raise ValueError('Ruta fuera del conjunto')
   b=path.read_bytes()
   if hashlib.sha256(b).hexdigest()!=row['sha_archivo']:raise ValueError('Archivo modificado: '+str(path))
   z.writestr(row['archivo'],b)
   if i%1000==0:print('Archivos empaquetados:',i,'/',len(rows),flush=True)
 if out.exists():raise FileExistsError(out)
 temporary.replace(out)
 print('ZIP listo:',out,'\nIncluye datos de reserva solo para transporte; no se ejecutó inferencia.')
if __name__=='__main__':main()
