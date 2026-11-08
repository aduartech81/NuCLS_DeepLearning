"""Verifica conciliación bibliográfica sin acceder a Colab ni a la reserva."""
import argparse
import collections
import csv
import hashlib
import json
from pathlib import Path

def verificar(root, entradas=None):
    ev = root / 'evidencias/literatura'
    def leer(nombre):
        with (ev / nombre).open(encoding='utf-8', newline='') as f:
            return list(csv.DictReader(f))
    rows = leer('cribado_consolidado.csv')
    counts = dict(collections.Counter(r['decision'] for r in rows))
    p = json.loads((ev / 'progreso_lectura.json').read_text())
    f = json.loads((ev / 'flujo_prisma_parcial.json').read_text())
    assert len(rows) == len({r['id'] for r in rows}) == p['registros'] == 1330
    assert counts == p['decisiones'] == f['estados_mutuamente_excluyentes']
    assert counts.get('por_revisar',0) == p['registros_sin_decision'] == f['sin_revision']
    assert len(rows) - counts.get('por_revisar',0) == p['registros_con_decision'] == f['con_decision_o_derivacion']
    assert 1717 == 69 + 318 + len(rows)
    assert f['exclusiones_explicitas_titulo_resumen'] == counts['excluir_por_titulo'] + counts['excluir_por_resumen']
    assert f['contexto_y_metodologia'] == sum(counts[k] for k in ['contexto_tarea_distinta','fuente_metodologica','revision_secundaria'])
    assert f['registros_con_lectura_texto_documentada'] == counts['texto_completo_extraido'] + counts['texto_completo_revisado']
    assert f['pendientes_resumen'] == counts.get('revisar_resumen',0)
    assert f['pendientes_texto_completo'] == counts.get('recuperar_texto_completo',0)
    assert len(leer('informes_no_recuperados_20261108.csv')) == counts['no_recuperado_al_corte'] == f['informes_no_recuperados'] == 13
    assert 166 == sum(f['capas_sintesis'].values())
    index = {r['id']: r for r in rows}
    batch = leer('cribado_adicional_34.csv')
    assert len(batch) == len({x['id'] for x in batch}) == 34
    nuevas=leer('evaluaciones_texto_20261108.csv')
    assert len(nuevas)==len({x['id'] for x in nuevas})==16
    assert all(index[x['id']]['decision']=='texto_completo_revisado' and x['fuente'] and x['secciones_leidas'] for x in nuevas)
    terceras=leer('evaluaciones_texto_cierre_20261108.csv')
    assert len(terceras)==len({x['id'] for x in terceras})
    assert all(index[x['id']]['decision']=='texto_completo_revisado' and x['fuente'] and x['secciones_leidas'] for x in terceras)
    posteriores={x['id'] for x in leer('lecturas_texto_ampliadas.csv')+nuevas+terceras}
    posteriores.update(r['id'] for r in rows if r['decision'] in ['duplicado_tardio','no_recuperado_al_corte'])
    assert counts.get('duplicado_tardio',0)==f.get('duplicados_tardios',0)
    adjudicacion=leer('adjudicacion_sintesis_20261108.csv')
    assert len(adjudicacion)==len({r['id'] for r in adjudicacion})==f['registros_con_lectura_texto_documentada']
    assert dict(collections.Counter(r['grupo_sintesis'] for r in adjudicacion))==f['capas_sintesis']
    posteriores.update(r['id'] for r in rows if r['decision'] in ['duplicado_tardio','no_recuperado_al_corte'])
    assert counts.get('duplicado_tardio',0)==f.get('duplicados_tardios',0)
    adjudicacion=leer('adjudicacion_sintesis_20261108.csv')
    assert len(adjudicacion)==len({r['id'] for r in adjudicacion})==f['registros_con_lectura_texto_documentada']
    assert dict(collections.Counter(r['grupo_sintesis'] for r in adjudicacion))==f['capas_sintesis']
    for x in batch:
        if x['id'] not in posteriores:
            assert x['decision'] == index[x['id']]['decision']
            assert x['motivo'] == index[x['id']]['motivo']
        assert x['sha256_resumen'] and x['nivel_lectura']
    titulos=leer('cribado_titulos_ampliado.csv')
    resumenes=leer('cribado_resumenes_ampliado.csv')
    assert len(titulos)==len({x['id'] for x in titulos})==1174
    assert len(resumenes)==len({x['id'] for x in resumenes})==364
    for x in resumenes:
        if x['id'] not in posteriores:
            assert x['decision']==index[x['id']]['decision']
        assert len(x['sha256_resumen'])==64
    assert len(leer('lecturas_texto_ampliadas.csv'))==7
    exact = collections.defaultdict(set)
    for x in leer('comparadores_texto_completo.csv'):
        if x['arquitectura_identificada'] == 'True':
            exact[x['modelo']].add(x['doi'].lower())
    freq = leer('frecuencia_comparadores_verificados.csv')
    assert {x['modelo']: int(x['estudios_verificados']) for x in freq} == {k:len(v) for k,v in exact.items()}
    for x in freq:
        assert set(x['doi'].split('; ')) == exact[x['modelo']]
    grupos={x['doi']:x['grupo_evidencia'] for x in leer('grupos_evidencia.csv')}
    for x in leer('frecuencia_sensibilidad_estudios.csv'):
        ds=exact[x['modelo']]
        assert int(x['publicaciones'])==len(ds)
        assert int(x['grupos_conservadores'])==len({grupos[d] for d in ds})
    assert len(leer('pendientes_texto_completo.csv'))==f['pendientes_texto_completo']
    assert (root/'assets/flujo_literatura.svg').read_bytes() == (root/'book/figuras/flujo_literatura.svg').read_bytes()
    if entradas:
        for x in json.loads((ev/'procedencia.json').read_text()):
            data = (entradas/x['archivo']).read_bytes()
            assert len(data) == x['bytes']
            assert hashlib.sha256(data).hexdigest() == x['sha256'], x['archivo']
    print(f"Conciliación correcta: {len(rows)} registros; {p['registros_con_decision']} atendidos; {p['registros_sin_decision']} sin primera decisión; {f['pendientes_texto_completo']} pendientes de texto. Frecuencias exactas verificadas; corte documental con informes no recuperados registrados por separado.")

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--entradas', type=Path, help='Carpeta opcional de exportaciones originales')
    args = parser.parse_args()
    verificar(Path(__file__).resolve().parents[1], args.entradas)
