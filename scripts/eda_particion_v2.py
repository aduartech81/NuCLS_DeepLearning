"""EDA de metadatos de desarrollo v2; excluye la reserva antes de calcular resultados."""
import argparse, hashlib, io, json, zipfile
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

EXPECTED='4e1574051a66740c050c3cd66fb11d423f2c57f313a4d71c02f9b2f3a913c77c'
CLASSES=['tumor_nonMitotic','lymphocyte','nonTILnonMQ_stromal']
LABELS=['Tumorales','Linfocitos','Estromales']

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--control',type=Path,required=True);ap.add_argument('--salida',type=Path,default=Path('resultados_analizados/eda_v2'));ap.add_argument('--figuras',type=Path,default=Path('book/figuras'));args=ap.parse_args()
    digest=hashlib.sha256(args.control.read_bytes()).hexdigest()
    if digest!=EXPECTED:raise ValueError('ZIP distinto del control verificado')
    with zipfile.ZipFile(args.control) as z:
        df=pd.read_csv(z.open('seleccion_y_exclusiones.csv'))
    df=df[df.particion.isin(['train','validation']) & df.clase.isin(CLASSES)].copy()
    if set(df.particion)!= {'train','validation'}:raise ValueError('Particiones inesperadas')
    included=df[df.estado.eq('incluida')].copy()
    counts=included.groupby(['particion','clase']).size().unstack(fill_value=0).reindex(columns=CLASSES)
    assert counts.loc['train'].sum()==14539 and counts.loc['validation'].sum()==2049
    assert included.groupby('paciente').particion.nunique().max()==1
    assert included.groupby('tss').particion.nunique().max()==1
    args.salida.mkdir(parents=True,exist_ok=True);args.figuras.mkdir(parents=True,exist_ok=True)
    rng=np.random.default_rng(4101);rows=[]
    for split in ['train','validation']:
        ds=df[df.particion.eq(split)]; patients=sorted(ds.paciente.unique())
        n=ds.groupby(['paciente','clase']).size().unstack(fill_value=0).reindex(index=patients,columns=CLASSES,fill_value=0).to_numpy()
        k=ds[ds.estado.eq('incluida')].groupby(['paciente','clase']).size().unstack(fill_value=0).reindex(index=patients,columns=CLASSES,fill_value=0).to_numpy()
        ix=rng.integers(0,len(patients),size=(5000,len(patients)))
        kb=k[ix].sum(axis=1);nb=n[ix].sum(axis=1)
        retention=np.divide(kb,nb,out=np.full(kb.shape,np.nan),where=nb>0)
        proportion=kb/kb.sum(axis=1,keepdims=True)
        for j,c in enumerate(CLASSES):
            lo,hi=np.nanpercentile(retention[:,j],[2.5,97.5]);pl,ph=np.percentile(proportion[:,j],[2.5,97.5])
            rows.append(dict(particion=split,clase=c,anotaciones=int(n[:,j].sum()),recortes=int(k[:,j].sum()),retencion=float(k[:,j].sum()/n[:,j].sum()),retencion_ic95_inf=float(lo),retencion_ic95_sup=float(hi),proporcion=float(k[:,j].sum()/k.sum()),proporcion_ic95_inf=float(pl),proporcion_ic95_sup=float(ph)))
    summary=pd.DataFrame(rows);summary.to_csv(args.salida/'retencion_y_composicion.csv',index=False)
    patient=included.groupby(['particion','paciente','tss']).size().reset_index(name='recortes');patient.to_csv(args.salida/'recortes_por_paciente.csv',index=False)
    excluded=df.groupby(['particion','estado']).size().reset_index(name='anotaciones');excluded.to_csv(args.salida/'seleccion_por_motivo.csv',index=False)
    plt.rcParams.update({'font.family':'DejaVu Sans','font.size':10,'axes.spines.top':False,'axes.spines.right':False,'svg.fonttype':'none'})
    fig,ax=plt.subplots(1,3,figsize=(15,4.6),layout='constrained')
    colors=['#176B87','#D18C26'];names=['Entrenamiento','Validación'];x=np.arange(3)
    for i,(split,name,color) in enumerate(zip(['train','validation'],names,colors)):
        rr=summary[summary.particion.eq(split)].set_index('clase').loc[CLASSES]
        pos=x+(i-.5)*.36
        ax[0].bar(pos,rr.proporcion*100,width=.34,color=color,label=name)
        ax[1].errorbar(pos,rr.retencion*100,yerr=np.array([rr.retencion-rr.retencion_ic95_inf,rr.retencion_ic95_sup-rr.retencion])*100,fmt='o',capsize=4,color=color,label=name)
    for a in ax[:2]:a.set_xticks(x,LABELS);a.grid(axis='y',alpha=.18);a.set_axisbelow(True)
    ax[0].set(title='Composición de los recortes',ylabel='% de recortes por partición',ylim=(0,65));ax[0].legend(frameon=False)
    ax[1].set(title='Retención por clase',ylabel='% de anotaciones conservadas',ylim=(0,100))
    vals=[patient[patient.particion.eq(s)].recortes for s in ['train','validation']]
    ax[2].boxplot(vals,tick_labels=['Train (83)','Validación (21)'],showfliers=True)
    ax[2].set(title='Contribución por paciente',ylabel='Recortes por paciente');ax[2].grid(axis='y',alpha=.18)
    fig.savefig(args.figuras/'eda_desarrollo_v2.svg');plt.close(fig)
    report={'fuente_sha256':digest,'alcance':'Solo entrenamiento y validación; metadatos, sin análisis de píxeles ni predicciones de reserva','bootstrap':{'repeticiones':5000,'semilla':4101,'unidad':'paciente dentro de cada partición','intervalo':'percentil 95%; razón de totales de los pacientes remuestreados','limitacion':'Condicional a los TSS observados; no estima incertidumbre entre centros ni corrige decisiones históricas'},'pacientes':patient.groupby('particion').size().to_dict(),'resumen_recortes_por_paciente':{s:{'min':int(v.min()),'mediana':float(v.median()),'max':int(v.max())} for s,v in zip(['train','validation'],vals)}}
    (args.salida/'metodo.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
    print(summary.to_string(index=False));print(json.dumps(report,ensure_ascii=False))
if __name__=='__main__':main()
