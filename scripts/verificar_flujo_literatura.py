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
    assert counts['por_revisar'] == p['registros_sin_decision'] == f['sin_revision']
    assert len(rows) - counts['por_revisar'] == p['registros_con_decision'] == f['con_decision_o_derivacion']
    assert 1717 == 69 + 318 + len(rows)
    assert f['exclusiones_explicitas_titulo_resumen'] == counts['excluir_por_titulo'] + counts['excluir_por_resumen']
    assert f['contexto_y_metodologia'] == sum(counts[k] for k in ['contexto_tarea_distinta','fuente_metodologica','revision_secundaria'])
    assert f['registros_con_lectura_texto_documentada'] == counts['texto_completo_extraido'] + counts['texto_completo_revisado']
    assert f['pendientes_resumen'] == counts['revisar_resumen']
    assert f['pendientes_texto_completo'] == counts['recuperar_texto_completo']
    index = {r['id']: r for r in rows}
    batch = leer('cribado_adicional_34.csv')
    assert len(batch) == len({x['id'] for x in batch}) == 34
    for x in batch:
        assert x['decision'] == index[x['id']]['decision']
        assert x['motivo'] == index[x['id']]['motivo']
        assert x['sha256_resumen'] and x['nivel_lectura']
    exact = collections.defaultdict(set)
    for x in leer('comparadores_texto_completo.csv'):
        if x['arquitectura_identificada'] == 'True':
            exact[x['modelo']].add(x['doi'].lower())
    freq = leer('frecuencia_comparadores_verificados.csv')
    assert {x['modelo']: int(x['estudios_verificados']) for x in freq} == {k:len(v) for k,v in exact.items()}
    for x in freq:
        assert set(x['doi'].split('; ')) == exact[x['modelo']]
    assert (root/'assets/flujo_literatura.svg').read_bytes() == (root/'book/figuras/flujo_literatura.svg').read_bytes()
    if entradas:
        for x in json.loads((ev/'procedencia.json').read_text()):
            data = (entradas/x['archivo']).read_bytes()
            assert len(data) == x['bytes']
            assert hashlib.sha256(data).hexdigest() == x['sha256'], x['archivo']
    print(f"Conciliación correcta: {len(rows)} registros; {p['registros_con_decision']} atendidos; {p['registros_sin_decision']} pendientes. Frecuencias exactas verificadas; inclusión final no establecida.")

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--entradas', type=Path, help='Carpeta opcional de exportaciones originales')
    args = parser.parse_args()
    verificar(Path(__file__).resolve().parents[1], args.entradas)
