from pathlib import Path
import zipfile,json,hashlib,io
import pandas as pd,numpy as np
from sklearn.metrics import confusion_matrix,balanced_accuracy_score
import argparse
ap=argparse.ArgumentParser();ap.add_argument('--pixeles',type=Path,required=True);ap.add_argument('--control-recortes',type=Path,required=True);args=ap.parse_args()
r=Path(__file__).resolve().parents[1];zpath=args.pixeles;out=r/'resultados_analizados/eda_pixeles_v2';out.mkdir(exist_ok=True)
with zipfile.ZipFile(zpath) as z:
 d=json.loads(z.read('resumen.json'));df=pd.read_csv(z.open('descriptores_recortes.csv'));hist=pd.read_csv(z.open('histogramas.csv'))
assert d['script_sha256']==hashlib.sha256((r/'scripts/completar_eda_pixeles_v2.py').read_bytes()).hexdigest()
assert d['manifiesto_sha256']=='623adf36520751addc324e44cd1b89d95e47842e53cda494914c0248a8be86d4'
with zipfile.ZipFile(args.control_recortes) as z:m=pd.read_csv(z.open('manifiesto.csv'))
m=m[m.particion.isin(['train','validation'])]
key=['archivo','paciente','tss','particion','clase'];pd.testing.assert_frame_equal(df[key].sort_values('archivo').reset_index(drop=True),m[key].sort_values('archivo').reset_index(drop=True))
assert len(df)==16588 and df.paciente.nunique()==104 and df.archivo.nunique()==len(df)
assert df.groupby('paciente').particion.nunique().max()==1 and df.groupby('tss').particion.nunique().max()==1
features=['R_media','G_media','B_media','R_sd','G_sd','B_sd','saturacion_media','fondo_fraccion','laplaciano_var','entropia_gris']
assert np.isfinite(df[features].to_numpy()).all()
assert (df[[v for v in features if v!='entropia_gris']]>=0).all().all()
train=df[df.particion.eq('train')];mu=train[['R_media','G_media','B_media']].mean().to_numpy();sd=np.sqrt((train[['R_sd','G_sd','B_sd']].to_numpy()**2+train[['R_media','G_media','B_media']].to_numpy()**2).mean(0)-mu**2)
assert np.allclose(mu,d['normalizacion_train']['media_RGB_0_1'],atol=1e-10);assert np.allclose(sd,d['normalizacion_train']['sd_RGB_0_1'],atol=1e-10)
for (part,cls,channel),g in hist.groupby(['particion','clase','canal']):
 assert len(g)==32 and g.pixeles.sum()==len(df[(df.particion==part)&(df.clase==cls)])*16384
checks={}
for name in ['diagnostico_dominio','diagnostico_sitio']:
 x=d[name];pred=pd.DataFrame(x['predicciones']);assert len(pred)==x['n_pacientes'] and pred.paciente.nunique()==len(pred)
 assert np.array_equal(confusion_matrix(pred.real,pred.prediccion,labels=x['clases']),x['confusion'])
 assert np.isclose(balanced_accuracy_score(pred.real,pred.prediccion),x['balanced_accuracy'])
 pred.to_csv(out/(name+'_predicciones.csv'),index=False);checks[name]='Matriz y balanced accuracy recalculadas'
# Verificación independiente de dHash por distancia de Hamming, sin acceso a píxeles.
a=np.array([int(x,16) for x in df[df.particion=='train'].dhash],dtype=np.uint64);b=np.array([int(x,16) for x in df[df.particion=='validation'].dhash],dtype=np.uint64);lut=np.array([i.bit_count() for i in range(256)],dtype=np.uint8);n=0
for start in range(0,len(a),128):
 v=np.bitwise_xor(a[start:start+128,None],b[None,:]);distance=lut[v.view(np.uint8).reshape(len(v),len(b),8)].sum(2);n+=int((distance<=4).sum())
assert n==d['similitud']['candidatos']==0;assert len(a)*len(b)==d['similitud']['pares_examinados']
patient=df.groupby(['paciente','particion','tss'])[features].median().reset_index();patient.to_csv(out/'medianas_por_paciente.csv',index=False)
# Resúmenes de distribución de los recortes, separados por clase y partición.
rows=[]
for (part,cls),g in df.groupby(['particion','clase']):
 for feat in features:
  rows.append(dict(particion=part,clase=cls,descriptor=feat,n=len(g),media=g[feat].mean(),sd=g[feat].std(),mediana=g[feat].median(),p25=g[feat].quantile(.25),p75=g[feat].quantile(.75)))
pd.DataFrame(rows).to_csv(out/'descriptores_por_clase.csv',index=False);hist.to_csv(out/'histogramas.csv',index=False)
(out/'resumen.json').write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
audit={'archivo_fuente':zpath.name,'sha256_zip':hashlib.sha256(zpath.read_bytes()).hexdigest(),'recortes_verificados':len(df),'pacientes':df.paciente.nunique(),'script_coincide':True,'manifiesto_coincide':True,'media_sd_rgb_recalculadas':True,'histogramas_conteos_correctos':True,'diagnosticos':checks,'similitud_hamming_recalculada':{'pares':len(a)*len(b),'candidatos':n},'alcance':'Se recalcularon resultados desde descriptores y hashes; no se recibieron ni decodificaron los píxeles. AUC adversarial registrada por el script, no recalculable desde predicciones duras exportadas.'}
(out/'verificacion.json').write_text(json.dumps(audit,ensure_ascii=False,indent=2)+'\n');print(json.dumps(audit,ensure_ascii=False))
