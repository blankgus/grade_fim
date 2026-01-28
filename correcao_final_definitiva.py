#!/usr/bin/env python3
"""
CORREÇÃO CUIDADOSA: Remove apenas as turmas eletivas, mantém todos os professores
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
print("🔧 CORREÇÃO CUIDADOSA - Mantendo professores")
print("=" * 120)
print()
print(f"✅ Backup: {backup_file}\n")

# Verificar professores ANTES
print("📊 Cargas dos professores ANTES:")
profs_antes = defaultdict(int)
for disc in banco['disciplinas']:
    for turma, carga in disc.get('carga_por_turma', {}).items():
        prof = disc.get('professor_por_turma', {}).get(turma)
        if prof:
            profs_antes[prof] += carga

for prof, carga in sorted(profs_antes.items()):
    print(f"  {prof:20s}: {carga:2d}h")
print(f"\n  Total: {sum(profs_antes.values())}h\n")

# 1. Corrigir Matemática em 2emA (2h → 4h)
print("1️⃣ Corrigindo Matemática em 2emA:")
for disc in banco['disciplinas']:
    if disc['nome'] == 'Matemática':
        if '2emA' in disc.get('carga_por_turma', {}):
            carga_antiga = disc['carga_por_turma']['2emA']
            disc['carga_por_turma']['2emA'] = 4
            print(f"   ✅ Matemática | 2emA: {carga_antiga}h → 4h")
            # Professor já está correto (Santiago ou Cesar)

print()

# 2. Remover APENAS as turmas eletivas (1emB e 2emB) das disciplinas específicas
print("2️⃣ Removendo turmas eletivas de disciplinas específicas:")
print("   (Mantém as outras turmas e professores intactos)\n")

# Disciplinas eletivas que devem ser removidas APENAS de 1emB e 2emB
eletivas_remover = {
    'Mercado de trabalho': ['1emB', '2emB'],
    'Análises Químicas': ['1emB', '2emB'],
    'Análises Historiográficas': ['1emB', '2emB'],
}

for nome_disc, turmas_remover in eletivas_remover.items():
    for disc in banco['disciplinas']:
        if disc['nome'] == nome_disc:
            turmas = disc.get('turmas', [])
            carga_por_turma = disc.get('carga_por_turma', {})
            prof_por_turma = disc.get('professor_por_turma', {})
            
            for turma in turmas_remover:
                if turma in turmas:
                    carga = carga_por_turma.get(turma, 0)
                    prof = prof_por_turma.get(turma, 'sem professor')
                    print(f"   ❌ {nome_disc:30s} | {turma} ({carga}h, {prof})")
                    
                    # Remover apenas desta turma
                    turmas.remove(turma)
                    if turma in carga_por_turma:
                        del carga_por_turma[turma]
                    if turma in prof_por_turma:
                        del prof_por_turma[turma]
            
            disc['turmas'] = turmas
            disc['carga_por_turma'] = carga_por_turma
            disc['professor_por_turma'] = prof_por_turma

print()

# Salvar
with open('escola_database.json', 'w', encoding='utf-8') as f:
    json.dump(banco, f, indent=2, ensure_ascii=False)

# Verificar professores DEPOIS
print("📊 Cargas dos professores DEPOIS:")
profs_depois = defaultdict(int)
for disc in banco['disciplinas']:
    for turma, carga in disc.get('carga_por_turma', {}).items():
        prof = disc.get('professor_por_turma', {}).get(turma)
        if prof:
            profs_depois[prof] += carga

for prof, carga in sorted(profs_depois.items()):
    diferenca = carga - profs_antes[prof]
    if diferenca != 0:
        print(f"  {prof:20s}: {carga:2d}h (diferença: {diferenca:+d}h)")
    else:
        print(f"  {prof:20s}: {carga:2d}h")

print(f"\n  Total: {sum(profs_depois.values())}h\n")

# Validar turmas
cargas = defaultdict(int)
for disc in banco['disciplinas']:
    for turma, carga in disc.get('carga_por_turma', {}).items():
        cargas[turma] += carga

print("=" * 120)
print("✅ VALIDAÇÃO: Cargas por turma")
print("=" * 120)
print()

LIMITE_EF = 25
LIMITE_EM = 35

turmas_ef = ['6anoA', '6anoB', '7anoA', '7anoB', '8anoA', '8anoB', '9anoA', '9anoB']
turmas_em = ['1emA', '1emB', '2emA', '2emB', '3emA', '3emB']

print("Ensino Fundamental II:")
perfeitas_ef = 0
for turma in turmas_ef:
    carga = cargas.get(turma, 0)
    diferenca = carga - LIMITE_EF
    
    if diferenca == 0:
        status = "✅"
        perfeitas_ef += 1
    elif diferenca < 0:
        status = f"⚠️ FALTA {-diferenca}h"
    else:
        status = f"❌ EXCESSO {diferenca}h"
    
    print(f"  {turma:10s} | {carga:2d}h / {LIMITE_EF}h | {status}")

print()
print("Ensino Médio:")
perfeitas_em = 0
for turma in turmas_em:
    carga = cargas.get(turma, 0)
    diferenca = carga - LIMITE_EM
    
    if diferenca == 0:
        status = "✅"
        perfeitas_em += 1
    elif diferenca < 0:
        status = f"⚠️ FALTA {-diferenca}h"
    else:
        status = f"❌ EXCESSO {diferenca}h"
    
    print(f"  {turma:10s} | {carga:2d}h / {LIMITE_EM}h | {status}")

print()
print("=" * 120)
print(f"📊 RESULTADO: {perfeitas_ef + perfeitas_em}/{len(turmas_ef) + len(turmas_em)} turmas perfeitas")
print("=" * 120)
print()

if perfeitas_ef + perfeitas_em == len(turmas_ef) + len(turmas_em):
    print("🎉 PERFEITO! Todas as turmas corretas e professores mantidos!")
else:
    print(f"⚠️ {len(turmas_ef) + len(turmas_em) - perfeitas_ef - perfeitas_em} turmas ainda com problemas")

print()
print(f"💾 Salvo: escola_database.json")
print(f"📦 Backup: {backup_file}")
print()
