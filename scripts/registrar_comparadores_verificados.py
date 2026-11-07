from pathlib import Path
import csv,json
from collections import defaultdict
r=Path(__file__).resolve().parents[1];o=r/'evidencias/literatura';rows=[]
def add(study,doi,model,task,data,metric,value,role,exact=True):rows.append(dict(estudio=study,doi=doi,modelo=model,problema=task,dataset=data,metricas=metric,valores=value,funcion=role,arquitectura_identificada=exact))
for model,f1,n in [('softmaxCNN_IN27_BN',.7124,899200),('softmaxCNN_32_BN',.7439,944032),('AlexNet_adaptada_RCC',.7664,197731396),('CIFAR_VGG',.7708,8956484),('GoogLeNet_adaptada_RCC',.7856,11526988),('WRN_adaptada_RCC',.6227,23542788)]:
 add('RCCNet 2018','10.1109/icarcv.2018.8581147',model,'Clasificación nuclear, cuatro clases','CRCHistoPhenotypes','F1 ponderado',f'{f1:.4f}','referencia')
for model,f1,auc in [('CNN3L',.8040,.9441),('AlexNet',.8216,.9386),('VGG16',.8689,.9757),('VGG19',.8578,.9701),('ResNet50',.8892,.9799),('InceptionV3',.8175,.9538),('DenseNet121',.8706,.9756)]:
 add('OLConvNet','10.1145/3345318',model,'Clasificación nuclear, cuatro clases','Colon, recortes 27×27','F1; AUC multiclase',f'{f1:.4f}; {auc:.4f}','referencia_ablacion')
add('GrEp 2026','10.1016/j.patcog.2025.112197','ResNet18','Subclasificación epitelial binaria','TCGA','F epitelial; F maligno; F normal','87.58±0.97; 90.83±0.84; 82.01±1.22 (%)','referencia_ablacion')
add('Sánchez-Torres 2026','10.1155/acis/4540418','ResNet50','Clasificación nuclear, cinco clases','PanNuke con contexto','F1 por clase (%)','82.90; 71.49; 71.98; 71.49; 49.39','comparacion_directa')
add('Sánchez-Torres 2026','10.1155/acis/4540418','ViT_no_especificada','Clasificación nuclear, cinco clases','PanNuke con contexto','F1 por clase (%)','82.19; 69.01; 70.19; 71.59; 47.93','comparacion_directa',False)
with (o/'comparadores_texto_completo.csv').open('w') as f:w=csv.DictWriter(f,list(rows[0]));w.writeheader();w.writerows(rows)
refs=defaultdict(set)
for x in rows:
 if x['arquitectura_identificada']:refs[x['modelo']].add(x['doi'])
freq=[dict(modelo=k,estudios_verificados=len(v),doi='; '.join(sorted(v)),alcance='Cuatro textos con extracción; no frecuencia del corpus completo') for k,v in sorted(refs.items(),key=lambda kv:(-len(kv[1]),kv[0]))]
with (o/'frecuencia_comparadores_verificados.csv').open('w') as f:w=csv.DictWriter(f,list(freq[0]));w.writeheader();w.writerows(freq)
assert refs['ResNet50']=={'10.1145/3345318','10.1155/acis/4540418'}
print(freq)
