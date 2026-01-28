#!/usr/bin/env python3
"""
Corrige atribuições de Anna Maria (deve ser Anna no PDF)
"""

import json
from datetime import datetime
import shutil

# Carregar banco
with open('escola_database.json', 'r', encoding='utf-8') as f:
    banco = json.load(f)

# Backup
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
backup_file = f'escola_database_backup_{timestamp}.json'
shutil.copy('escola_database.json', backup_file)

print("=" * 120)
print("🔧 CORRIGINDO ATRIBUIÇÕES DE ANNA MARIA")
print("=" * 120)
print()

# Anna no PDF dá Filosofia e Sociologia para todas as turmas de EM
# Mas no banco está como "Anna Maria" e o PDF tem "Anna"

# Atualizar professor_por_turma para usar "Anna Maria"
correcoes = 0

for disc in banco['disciplinas']:
    if disc['nome'] in ['Filosofia', 'Sociologia']:
        prof_por_turma = disc.get('professor_por_turma', {})
        
        for turma, prof in list(prof_por_turma.items()):
            if prof == 'Anna':
                prof_por_turma[turma] = 'Anna Maria'
                correcoes += 1
                print(f"  ✅ {disc['nome']:20s} | {turma}: Anna → Anna Maria")

print()
print(f"✅ {correcoes} atribuições corrigidas")
print()

# Salvar
with open('escola_database.json', 'w', encoding='utf-8') as f:
    json.dump(banco, f, indent=2, ensure_ascii=False)

print(f"💾 Salvo: escola_database.json")
print(f"📦 Backup: {backup_file}")
print()

# Recalcular cargas
from collections import defaultdict
profs_cargas = defaultdict(int)

for disc in banco['disciplinas']:
    for turma, carga in disc.get('carga_por_turma', {}).items():
        prof_nome = disc.get('professor_por_turma', {}).get(turma)
        if prof_nome:
            profs_cargas[prof_nome] += carga

print("📊 Cargas após correção:\n")
print(f"  Anna Maria: {profs_cargas['Anna Maria']}h")
print(f"  Marcão: {profs_cargas['Marcão']}h (não tem aulas na grade, apenas turmas infantis)")
print()
