#!/usr/bin/env python3
"""
Atualiza cargas horárias dos professores conforme suas atribuições reais
"""

import json
from datetime import datetime
import shutil
from collections import defaultdict

# Carregar banco
with open('escola_database.json', 'r', encoding='utf-8') as f:
    banco = json.load(f)

# Backup
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
backup_file = f'escola_database_backup_{timestamp}.json'
shutil.copy('escola_database.json', backup_file)

print("=" * 120)
print("🔧 ATUALIZANDO CARGAS HORÁRIAS DOS PROFESSORES")
print("=" * 120)
print()
print(f"✅ Backup: {backup_file}\n")

# Calcular carga real de cada professor
profs_cargas = defaultdict(int)

for disc in banco['disciplinas']:
    for turma, carga in disc.get('carga_por_turma', {}).items():
        prof_nome = disc.get('professor_por_turma', {}).get(turma)
        if prof_nome:
            profs_cargas[prof_nome] += carga

print("📊 Cargas calculadas:\n")

# Atualizar professores
for prof in banco['professores']:
    nome = prof['nome']
    carga_atual = prof.get('carga_horaria', 0)
    carga_real = profs_cargas.get(nome, 0)
    
    if carga_real > 0:
        prof['carga_horaria'] = carga_real
        
        if carga_atual != carga_real:
            print(f"  ✅ {nome:20s}: {carga_atual}h → {carga_real}h")
        else:
            print(f"  ✓ {nome:20s}: {carga_real}h (sem alteração)")
    else:
        print(f"  ⚠️ {nome:20s}: SEM ATRIBUIÇÕES")

# Corrigir disponibilidade (se for lista, converter para dicionário)
print()
print("🔧 Corrigindo disponibilidade dos professores:\n")

dias_semana = ['segunda', 'terca', 'quarta', 'quinta', 'sexta']

for prof in banco['professores']:
    disponibilidade = prof.get('disponibilidade', {})
    
    # Se for lista, converter para dicionário
    if isinstance(disponibilidade, list):
        nova_disponibilidade = {dia: True for dia in disponibilidade}
        # Adicionar dias faltantes como False
        for dia in dias_semana:
            if dia not in nova_disponibilidade:
                nova_disponibilidade[dia] = False
        
        prof['disponibilidade'] = nova_disponibilidade
        print(f"  ✅ {prof['nome']:20s}: convertido de lista para dicionário")
    elif isinstance(disponibilidade, dict):
        # Garantir que todos os dias estão presentes
        for dia in dias_semana:
            if dia not in disponibilidade:
                disponibilidade[dia] = True  # Por padrão, disponível
        print(f"  ✓ {prof['nome']:20s}: disponibilidade OK")
    else:
        # Criar disponibilidade padrão (todos os dias)
        prof['disponibilidade'] = {dia: True for dia in dias_semana}
        print(f"  ⚠️ {prof['nome']:20s}: criada disponibilidade padrão (todos os dias)")

# Salvar
with open('escola_database.json', 'w', encoding='utf-8') as f:
    json.dump(banco, f, indent=2, ensure_ascii=False)

print()
print("=" * 120)
print("✅ ATUALIZAÇÃO CONCLUÍDA")
print("=" * 120)
print(f"  Total de professores: {len(banco['professores'])}")
print(f"  Carga total atribuída: {sum(profs_cargas.values())}h")
print(f"  Backup: {backup_file}")
print()
