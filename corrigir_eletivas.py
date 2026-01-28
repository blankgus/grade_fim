#!/usr/bin/env python3
"""
Remove disciplinas eletivas/compartilhadas que não devem contar na carga
Baseado no PDF: disciplinas que têm horários batendo entre turmas
"""

import json
from datetime import datetime
import shutil

print("=" * 120)
print("🔧 CORRIGINDO: Disciplinas Eletivas/Compartilhadas")
print("=" * 120)
print()

# Carregar banco
with open('escola_database.json', 'r', encoding='utf-8') as f:
    banco = json.load(f)

# Backup
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
backup_file = f'escola_database_backup_{timestamp}.json'
shutil.copy('escola_database.json', backup_file)
print(f"✅ Backup: {backup_file}\n")

# Disciplinas que são ELETIVAS e devem ser removidas das turmas 1emB e 2emB
# Conforme PDF: essas têm horários batendo
disciplinas_eletivas_remover = {
    'Análises Historiográficas': ['1emB', '2emB'],  # Horário bate com Práticas do Vlad
    'Análises Químicas': ['1emB', '2emB'],  # Horário bate com Oralidade da Heliana
    'Práticas experimentais': ['1emB', '2emB'],  # Horário bate com Análises Hist do Waldemar
    'Tecnologia e Saúde': ['1emB', '2emB'],  # Pode ser eletiva também
}

# Para 2emA, adicionar Matemática (está com 2h, deveria ter 4h)
# E remover disciplinas extras
disciplinas_eletivas_remover_2emA = {
    'Análises Historiográficas': ['2emA'],
    'Tecnologia e Saúde': ['2emA'],
}

print("🔍 Disciplinas eletivas que serão removidas:\n")

removidas_total = 0
carga_removida_total = 0

for disc in banco['disciplinas']:
    nome = disc['nome']
    turmas = disc.get('turmas', [])
    carga_por_turma = disc.get('carga_por_turma', {})
    prof_por_turma = disc.get('professor_por_turma', {})
    
    turmas_remover = []
    
    # Verificar se é eletiva
    if nome in disciplinas_eletivas_remover:
        turmas_remover = disciplinas_eletivas_remover[nome]
    elif nome in disciplinas_eletivas_remover_2emA:
        turmas_remover = disciplinas_eletivas_remover_2emA[nome]
    
    if turmas_remover:
        for turma in turmas_remover:
            if turma in turmas:
                carga = carga_por_turma.get(turma, 0)
                print(f"  ❌ {nome:35s} | {turma} ({carga}h)")
                
                # Remover
                turmas.remove(turma)
                if turma in carga_por_turma:
                    del carga_por_turma[turma]
                if turma in prof_por_turma:
                    del prof_por_turma[turma]
                
                removidas_total += 1
                carga_removida_total += carga
        
        disc['turmas'] = turmas
        disc['carga_por_turma'] = carga_por_turma
        disc['professor_por_turma'] = prof_por_turma

print()
print(f"✅ {removidas_total} atribuições eletivas removidas ({carga_removida_total}h)")
print()

# Corrigir Matemática em 2emA (está com 2h, deveria ter 4h)
print("🔧 Corrigindo Matemática em 2emA:\n")
for disc in banco['disciplinas']:
    if disc['nome'] == 'Matemática':
        if '2emA' in disc.get('carga_por_turma', {}):
            carga_antiga = disc['carga_por_turma']['2emA']
            disc['carga_por_turma']['2emA'] = 4
            print(f"  ✅ Matemática | 2emA: {carga_antiga}h → 4h")

print()

# Salvar
with open('escola_database.json', 'w', encoding='utf-8') as f:
    json.dump(banco, f, indent=2, ensure_ascii=False)

print()
print("=" * 120)
print("📊 VALIDAÇÃO: Carga horária após correção")
print("=" * 120)
print()

# Calcular cargas
from collections import defaultdict
cargas = defaultdict(int)

for disc in banco['disciplinas']:
    for turma, carga in disc.get('carga_por_turma', {}).items():
        cargas[turma] += carga

# Limites
LIMITE_EM = 35

turmas_verificar = ['1emA', '1emB', '2emA', '2emB', '3emA', '3emB']

for turma in turmas_verificar:
    carga = cargas.get(turma, 0)
    diferenca = carga - LIMITE_EM
    
    if diferenca == 0:
        status = "✅"
    elif diferenca < 0:
        status = f"⚠️ FALTA {-diferenca}h"
    else:
        status = f"❌ EXCESSO {diferenca}h"
    
    print(f"{turma:10s} | {carga:2d}h / {LIMITE_EM}h | {status}")

print()
print(f"💾 Salvo em: escola_database.json")
print(f"📦 Backup: {backup_file}")
print()
