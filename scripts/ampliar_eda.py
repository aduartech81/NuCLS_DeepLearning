"""Resumen RGB ponderado por píxel y entropía de clases a partir de auditorías."""
from pathlib import Path
import numpy as np
import pandas as pd
R=Path(__file__).resolve().parents[1]
def main():
 q=pd.read_csv(R/'evidencias/calidad_por_imagen.csv')
 assert len(q)==1182 and q.paciente.nunique()==79
 w=q.ancho*q.alto
 rows=[]
 for c in 'RGB':
  mu=np.average(q[c+'_media'],weights=w)
  var=np.average(q[c+'_sd']**2+q[c+'_media']**2,weights=w)-mu**2
  rows.append(dict(canal=c,pixeles=int(w.sum()),media=mu,sd=np.sqrt(var),media_0_1=mu/255,sd_0_1=np.sqrt(var)/255))
 pd.DataFrame(rows).to_csv(R/'evidencias/rgb_campos_train.csv',index=False)
 s=pd.read_csv(R/'evidencias/seleccion_clases.csv');rows=[]
 for part,g in s.groupby('particion'):
  p=g.incluidas.to_numpy()/g.incluidas.sum();h=-np.sum(p*np.log2(p))
  rows.append(dict(particion=part,recortes=int(g.incluidas.sum()),entropia_bits=h,entropia_normalizada=h/np.log2(3),razon_max_min=p.max()/p.min()))
 pd.DataFrame(rows).to_csv(R/'evidencias/entropia_clases.csv',index=False)
 print(pd.read_csv(R/'evidencias/rgb_campos_train.csv').to_string(index=False))
 print(pd.DataFrame(rows).to_string(index=False))
if __name__=='__main__':main()
