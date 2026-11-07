"""Análisis exploratorio por semillas y planificación; no entrena modelos."""
from pathlib import Path
from itertools import combinations
import math
import numpy as np
import pandas as pd
from scipy.stats import norm, chi2, t, nct, wilcoxon
from scipy.optimize import brentq
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'resultados_analizados'
LABEL = {'cnn_local':'CNN local', 'resnet18':'ResNet18', 'mobilenet_v2':'MobileNetV2'}
DELTA, ALPHA, POWER = .02, .05, .8

def power_t(n, effect, alpha):
    critical = t.ppf(1-alpha/2, n-1)
    return nct.sf(critical,n-1,effect*np.sqrt(n)) + nct.sf(critical,n-1,-effect*np.sqrt(n))

def main():
    data = pd.read_csv(OUT/'corridas_verificadas.csv')
    assert not data.duplicated(['modelo','semilla']).any()
    pivot = data.pivot(index='semilla',columns='modelo',values='macro_f1')
    assert pivot.shape == (5,3) and not pivot.isna().any().any()
    summary = data.groupby('modelo').macro_f1.agg(['count','mean','std'])
    summary['cv_porcentaje'] = 100*summary['std']/summary['mean']
    summary.to_csv(OUT/'variabilidad_semillas.csv')
    rows = []
    for a,b in combinations(LABEL,2):
        d = (pivot[b]-pivot[a]).to_numpy()
        sd = d.std(ddof=1)
        # Exact signed ranks valid here: no zeros or absolute ties after 12 decimals.
        dr = np.round(d,12)
        assert np.all(dr != 0) and len(np.unique(np.abs(dr))) == len(dr)
        z = norm.ppf(1-ALPHA/2)+norm.ppf(POWER)
        zb = norm.ppf(1-ALPHA/6)+norm.ppf(POWER)
        n_t = next(n for n in range(5,10001) if power_t(n,DELTA/sd,ALPHA/3)>=POWER)
        sd_upper = sd*np.sqrt(4/chi2.ppf(.05,4))
        n_conservative = next(n for n in range(5,10001) if power_t(n,DELTA/sd_upper,ALPHA/3)>=POWER)
        mde_t = brentq(lambda e:power_t(5,e,ALPHA/3)-POWER, .00001,5)*sd
        rows.append(dict(comparacion=f'{LABEL[b]} − {LABEL[a]}', n=5,
          diferencia_media=d.mean(),sd_diferencias=sd,delta_sobre_sd=DELTA/sd,
          p_wilcoxon=wilcoxon(dr,method='exact').pvalue,
          R_normal=math.ceil((z*sd/DELTA)**2),
          R_normal_bonferroni=math.ceil((zb*sd/DELTA)**2),
          R_t_bonferroni=n_t,R_t_sigma_superior=n_conservative,
          MDE_normal_5=z*sd/np.sqrt(5),MDE_t_bonferroni_5=mde_t))
    df = pd.DataFrame(rows)
    order = np.argsort(df.p_wilcoxon.to_numpy())
    adjusted = np.minimum(1,np.maximum.accumulate((3-np.arange(3))*df.p_wilcoxon.to_numpy()[order]))
    df['p_holm'] = 0.
    df.loc[order,'p_holm'] = adjusted
    df.to_csv(OUT/'planificacion_semillas.csv',index=False)
    plt.rcParams.update({'font.family':'DejaVu Sans','font.size':11,'svg.fonttype':'none'})
    fig,axs=plt.subplots(1,2,figsize=(12,4.6),layout='constrained')
    colors=['#18364b','#078781','#cf8b2c']
    for i,(name,label) in enumerate(LABEL.items()):
        vals = pivot[name].to_numpy()*100
        axs[0].scatter(np.full(5,i)+np.linspace(-.12,.12,5),vals,color=colors[i],s=45)
        axs[0].errorbar(i,vals.mean(),yerr=vals.std(ddof=1),color=colors[i],fmt='_',markersize=24,capsize=7,lw=2)
    axs[0].set_xticks(range(3),list(LABEL.values()))
    axs[0].set_ylabel('Macro-F1 de validación (%)')
    axs[0].set_title('Cada punto representa una semilla',loc='left',weight='bold')
    axs[1].barh(df.comparacion,df.MDE_t_bonferroni_5*100,color='#078781')
    axs[1].axvline(2,color='#cf8b2c',ls='--',label='Margen práctico: 2 puntos')
    axs[1].set_xlabel('Diferencia mínima detectable (puntos porcentuales)')
    axs[1].set_title('Sensibilidad con cinco pares',loc='left',weight='bold')
    axs[1].legend(loc='lower right',fontsize=9)
    for ax in axs:
        ax.spines[['top','right']].set_visible(False)
        ax.grid(axis='y' if ax is axs[0] else 'x',alpha=.15)
        ax.set_axisbelow(True)
    fig.savefig(ROOT/'book/figuras/visual_planificacion.svg',bbox_inches='tight')
    plt.close(fig)
    print(summary.to_string())
    print(df.to_string(index=False))

if __name__=='__main__':
    main()
