#!/usr/bin/env python3
"""
Analisar conflitos e bloqueios no algoritmo de alocação.

Especificamente para 9anoB que só aloca 16/25 aulas.
"""

import json
from collections import defaultdict

dados = json.load(open('escola_database.json', encoding='utf-8'))

# Focar em 9anoB
turma_nome = '9anoB'

print(f"{'='*80}")
print(f"ANÁLISE DE BLOQUEIOS: {turma_nome}")
print(f"{'='*80}\n")

# 1. Listar todas as disciplinas esperadas
disciplinas_esperadas = []
carga_total = 0

for disc in dados['disciplinas']:
    if turma_nome in disc.get('carga_por_turma', {}):
        carga = disc['carga_por_turma'][turma_nome]
        professor = disc.get('professor_por_turma', {}).get(turma_nome, 'SEM PROFESSOR')
        disciplinas_esperadas.append({
            'nome': disc['nome'],
            'carga': carga,
            'professor': professor
        })
        carga_total += carga

print(f"Carga total esperada: {carga_total}h")
print(f"Períodos disponíveis: 5 (EF II)")
print(f"Dias disponíveis: 5")
print(f"Total de slots: 25\n")

print(f"--- DISCIPLINAS ESPERADAS ---")
for d in sorted(disciplinas_esperadas, key=lambda x: x['carga'], reverse=True):
    print(f"  {d['nome']:30s} {d['carga']}h - {d['professor']}")

# 2. Simular alocação ingênua
print(f"\n{'='*80}")
print(f"SIMULAÇÃO DE ALOCAÇÃO INGÊNUA (sem considerar conflitos)")
print(f"{'='*80}\n")

# Para cada professor, quantas aulas ele precisa dar nesta turma?
aulas_por_professor = defaultdict(list)
for d in disciplinas_esperadas:
    for _ in range(d['carga']):
        aulas_por_professor[d['professor']].append(d['nome'])

print(f"--- AULAS POR PROFESSOR ---")
for prof, aulas in sorted(aulas_por_professor.items(), key=lambda x: len(x[1]), reverse=True):
    print(f"  {prof:20s} {len(aulas)} aulas: {', '.join(set(aulas))}")

# 3. Verificar se há professores dando aula em outras turmas no mesmo turno
print(f"\n{'='*80}")
print(f"VERIFICAÇÃO DE CONFLITOS POTENCIAIS")
print(f"{'='*80}\n")

# Pegar turno de 9anoB
turno_9anoB = None
for t in dados['turmas']:
    if t['nome'] == turma_nome:
        turno_9anoB = t.get('turno', 'manha')
        break

print(f"Turno de {turma_nome}: {turno_9anoB}")

# Listar outras turmas no mesmo turno
outras_turmas_turno = []
for t in dados['turmas']:
    if t['nome'] != turma_nome and t.get('turno') == turno_9anoB:
        outras_turmas_turno.append(t['nome'])

print(f"Outras turmas no mesmo turno: {', '.join(outras_turmas_turno)}\n")

# Para cada professor de 9anoB, verificar se ele dá aula em outras turmas do mesmo turno
print(f"--- PROFESSORES COM POSSÍVEIS CONFLITOS ---")
for prof_nome in aulas_por_professor.keys():
    if prof_nome == 'SEM PROFESSOR':
        continue
    
    # Buscar outras turmas onde este professor dá aula no mesmo turno
    turmas_conflito = []
    carga_conflito = 0
    
    for disc in dados['disciplinas']:
        prof_por_turma = disc.get('professor_por_turma', {})
        for t_nome, t_prof in prof_por_turma.items():
            if t_prof == prof_nome and t_nome in outras_turmas_turno:
                carga_turma = disc.get('carga_por_turma', {}).get(t_nome, 0)
                turmas_conflito.append(f"{t_nome}:{disc['nome']}({carga_turma}h)")
                carga_conflito += carga_turma
    
    if turmas_conflito:
        aulas_9anoB = len(aulas_por_professor[prof_nome])
        print(f"\n{prof_nome}:")
        print(f"  Aulas em {turma_nome}: {aulas_9anoB}h")
        print(f"  Aulas em outras turmas do turno: {carga_conflito}h")
        print(f"  Total no turno: {aulas_9anoB + carga_conflito}h")
        print(f"  Distribuição:")
        for tc in turmas_conflito:
            print(f"    - {tc}")
        
        # Calcular se é possível alocar todas
        total_slots = 5 * 5  # 5 dias x 5 períodos
        if aulas_9anoB + carga_conflito > total_slots:
            print(f"  ❌ IMPOSSÍVEL: Mais aulas ({aulas_9anoB + carga_conflito}) do que slots ({total_slots})!")
        elif aulas_9anoB + carga_conflito == total_slots:
            print(f"  ⚠️ CRÍTICO: Sem margem de erro, qualquer conflito bloqueia!")
        else:
            margem = total_slots - (aulas_9anoB + carga_conflito)
            print(f"  ✅ POSSÍVEL: Margem de {margem} slots")

# 4. Análise de sobrecarga por dia
print(f"\n{'='*80}")
print(f"ANÁLISE DE SOBRECARGA")
print(f"{'='*80}\n")

# Para cada professor, calcular sua carga total vs limite
print(f"--- CARGA GLOBAL DOS PROFESSORES ---")
for prof_nome in sorted(aulas_por_professor.keys()):
    if prof_nome == 'SEM PROFESSOR':
        continue
    
    # Buscar dados do professor
    prof_data = None
    for p in dados['professores']:
        if p['nome'] == prof_nome:
            prof_data = p
            break
    
    if prof_data:
        carga_atribuida = prof_data.get('carga_horaria', 0)
        carga_maxima = prof_data.get('carga_horaria_maxima', 35)
        disponivel = carga_maxima - carga_atribuida
        
        status = "✅" if disponivel > 0 else "❌"
        print(f"{status} {prof_nome:20s} {carga_atribuida}/{carga_maxima}h (resta {disponivel}h)")
