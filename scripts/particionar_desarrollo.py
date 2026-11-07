"""Partición por TSS sin consultar imágenes, etiquetas ni rendimiento de modelos."""
import argparse, csv, hashlib, io, itertools, json
from collections import Counter
from pathlib import Path


def partition(rows):
    if len({r['paciente'] for r in rows}) != len(rows):
        raise ValueError('Pacientes duplicados')
    development = [r for r in rows if r['rol_propuesto'] == 'desarrollo']
    counts = Counter(r['tss'] for r in development)
    if '' in counts or len(counts) < 3:
        raise ValueError('Se requieren al menos tres TSS identificados')
    # Tamaño objetivo fijado antes de consultar resultados; desempate estable por hash.
    sites = sorted(counts)
    choices = []
    for size in range(2, len(sites)):
        for group in itertools.combinations(sites, size):
            n = sum(counts[s] for s in group)
            tie = hashlib.sha256(('NuCLS-v2-4101|' + '|'.join(group)).encode()).hexdigest()
            choices.append((abs(n / len(development) - .20), tie, group))
    validation = set(min(choices)[2])
    output = []
    for row in sorted(rows, key=lambda r: r['paciente']):
        role = row['rol_propuesto']
        split = ('validation' if row['tss'] in validation else 'train') if role == 'desarrollo' else role
        output.append(dict(row, particion_v2=split))
    groups = {k: {r['tss'] for r in output if r['particion_v2'] == k}
              for k in ['train', 'validation', 'reserva_candidata']}
    for a, b in itertools.combinations(groups, 2):
        if groups[a] & groups[b]:
            raise ValueError(f'TSS compartidos: {a}, {b}')
    return output, groups


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--entrada', type=Path, required=True)
    p.add_argument('--salida', type=Path, required=True)
    a = p.parse_args()
    raw = a.entrada.read_bytes()
    rows, groups = partition(list(csv.DictReader(io.StringIO(raw.decode('utf-8-sig')))))
    a.salida.mkdir(parents=True, exist_ok=True)
    dest = a.salida / 'particion_por_tss_v2.csv'
    buf = io.StringIO(newline='')
    writer = csv.DictWriter(buf, fieldnames=list(rows[0]), lineterminator='\n')
    writer.writeheader(); writer.writerows(rows)
    payload = buf.getvalue().encode()
    if dest.exists() and dest.read_bytes() != payload:
        raise SystemExit('No se sobrescribe una partición diferente')
    dest.write_bytes(payload)
    report = dict(estado='ASIGNACION_REPRODUCIBLE_PREVIA_A_RECORTES',
                  objetivo_validation=.20, criterio='Minimizar desviación del 20% de pacientes, mínimo dos TSS en validación; desempate SHA256 con identificador fijo.',
                  sha256_entrada=hashlib.sha256(raw).hexdigest(),
                  sha256_particion=hashlib.sha256(payload).hexdigest(),
                  pacientes=dict(Counter(r['particion_v2'] for r in rows)),
                  tss={k: sorted(v) for k, v in groups.items()},
                  limitacion='No borra exposición histórica. Reserva candidata pequeña; verificar recortes y representación de clases en desarrollo antes de entrenar. No se seleccionó la partición por resultados de modelos.')
    (a.salida / 'control_particion_v2.json').write_text(json.dumps(report, ensure_ascii=False, indent=2)+'\n')
    print(json.dumps(report, ensure_ascii=False, indent=2))

if __name__ == '__main__':
    main()
