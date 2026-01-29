import json
from collections import defaultdict

# Carregar banco
with open('escola_database.json', encoding='utf-8') as f:
    data = json.load(f)

DIAS_SEMANA = ["seg", "ter", "qua", "qui", "sex"]

# Horários por segmento
HORARIOS_EM = [
    "07:00", "07:50", "08:40", "09:50", "10:40", "11:30", "12:20"
]
HORARIOS_EF = [
    "07:50", "08:40", "09:50", "10:40", "11:30"
]

print("=" * 80)
print("DIAGNÓSTICO: POR QUE NÃO PODE GERAR?")
print("=" * 80)

# Calcular aulas necessárias (usando obter_carga_turma)
total_aulas = 0
aulas_por_turma = {}

for turma_data in data['turmas']:
    turma_nome = turma_data['nome']
    aulas_turma = 0
    
    for disc in data['disciplinas']:
        if turma_nome in disc.get('turmas', []):
            # Usar carga específica ou padrão
            carga_por_turma = disc.get('carga_por_turma', {})
            if carga_por_turma and turma_nome in carga_por_turma:
                carga = carga_por_turma[turma_nome]
            else:
                carga = disc.get('carga_semanal', 0)
            
            aulas_turma += carga
    
    aulas_por_turma[turma_nome] = aulas_turma
    total_aulas += aulas_turma

print(f"\n📊 Total de aulas necessárias: {total_aulas}h\n")

# Calcular capacidade de horários
capacidade_total = 0
for turma_data in data['turmas']:
    turma_nome = turma_data['nome']
    segmento = turma_data.get('segmento', '')
    
    # Determinar horários
    if 'em' in turma_nome.lower() or segmento == 'EM':
        horarios = HORARIOS_EM
    else:
        horarios = HORARIOS_EF
    
    capacidade_turma = len(DIAS_SEMANA) * len(horarios)
    capacidade_total += capacidade_turma
    
    necessario = aulas_por_turma.get(turma_nome, 0)
    status = "✅" if necessario <= capacidade_turma else "❌"
    
    print(f"{status} {turma_nome}: {necessario}h / {capacidade_turma}h slots ({len(horarios)} períodos × 5 dias)")

print(f"\n{'='*80}")
print(f"CAPACIDADE TOTAL: {capacidade_total}h")
print(f"NECESSÁRIO: {total_aulas}h")
print(f"DIFERENÇA: {capacidade_total - total_aulas:+d}h")
print('='*80)

if total_aulas > capacidade_total:
    print("\n❌ BLOQUEADO: Total de aulas excede capacidade de horários")
    print(f"   Você precisa remover {total_aulas - capacidade_total}h no total")
else:
    print("\n✅ OK: Há capacidade suficiente de horários")

# Calcular capacidade dos professores
print("\n" + "=" * 80)
print("CAPACIDADE DOS PROFESSORES")
print("=" * 80)

capacidade_professores = 0
for prof_data in data['professores']:
    limite = prof_data.get('carga_horaria_maxima', 35)
    capacidade_professores += limite

print(f"\nTotal de professores: {len(data['professores'])}")
print(f"Capacidade total: {capacidade_professores}h")
print(f"Necessário: {total_aulas}h")
print(f"Diferença: {capacidade_professores - total_aulas:+d}h")

if total_aulas > capacidade_professores:
    print("\n❌ BLOQUEADO: Total de aulas excede capacidade dos professores")
else:
    print("\n✅ OK: Há capacidade suficiente de professores")

# Mostrar turmas problemáticas
print("\n" + "=" * 80)
print("TURMAS COM EXCESSO:")
print("=" * 80)

limites = {
    '6anoA': 25, '7anoA': 25, '8anoA': 25, '9anoA': 25,
    '6anoB': 25, '7anoB': 25, '8anoB': 25, '9anoB': 25,
    '1emA': 35, '2emA': 35, '3emA': 35,
    '1emB': 35, '2emB': 35, '3emB': 35
}

total_excesso = 0
for turma, carga in aulas_por_turma.items():
    limite = limites.get(turma, 35)
    if carga > limite:
        excesso = carga - limite
        total_excesso += excesso
        print(f"❌ {turma}: {carga}h / {limite}h (+{excesso}h)")

print(f"\n💡 Total a remover: {total_excesso}h")
