"""Reproduce la figura desde los 12 PNG y sus hashes publicados; no accede al test."""
from pathlib import Path
import json,hashlib
from PIL import Image
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
R=Path(__file__).resolve().parents[1]
data=json.loads((R/'evidencias/galeria_train.json').read_text())['registros']
names={'tumor_nonMitotic':'Núcleo tumoral no mitótico','lymphocyte':'Linfocito','nonTILnonMQ_stromal':'Núcleo estromal'}
fig,axes=plt.subplots(3,4,figsize=(10,8.2),layout='constrained')
for row,(cls,title) in enumerate(names.items()):
 samples=[x for x in data if x['clase']==cls];assert len(samples)==4
 for col,item in enumerate(samples):
  p=R/'book/figuras/galeria'/item['archivo'];assert hashlib.sha256(p.read_bytes()).hexdigest()==item['sha256']
  assert item['particion']=='entrenamiento'
  with Image.open(p) as im:
   assert im.size==(128,128) and im.mode=='RGB'
   ax=axes[row,col];ax.imshow(im,interpolation='nearest')
  ax.set_xticks([]);ax.set_yticks([])
  ax.set_title(item['paciente']+'\n'+item['fila'],fontsize=8,color='#243c50')
  if col==0:ax.set_ylabel(title,fontsize=11)
fig.suptitle('Qué recibe el clasificador: 12 recortes reales de entrenamiento',fontsize=15,color='#17384a',weight='bold')
fig.savefig(R/'book/figuras/galeria_train.jpg',dpi=145,bbox_inches='tight');plt.close(fig)
print('Galería reproducida; hashes y formatos verificados.')
