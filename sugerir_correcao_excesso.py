import json
from collections import defaultdict

# Carregar banco
with open('escola_database.json', encoding='utf-8') as f:
    data = json.load(f)

print("=" * 80)
print("CORRIGIR EXCESSO DE CARGA EM 1emB E 2emB")
print("=" * 80)
print()

# Identificar disciplinas que têm 1emB e 2emB
disciplinas_com_excesso = []

for disc in data['disciplinas']:
    turmas = disc.get('turmas', [])
    carga_por_turma = disc.get('carga_por_turma', {})
    
    if '1emB' in turmas or '2emB' in turmas:
        disciplinas_com_excesso.append({
            'nome': disc['nome'],
            'turmas': turmas,
            'carga_semanal': disc.get('carga_semanal', 0),
            'carga_por_turma': carga_por_turma
        })

print("📋 Disciplinas que afetam 1emB e 2emB:\n")
for disc in disciplinas_com_excesso:
    nome = disc['nome']
    print(f"• {nome}")
    
    for turma in ['1emB', '2emB']:
        if turma in disc['turmas']:
            if disc['carga_por_turma'] and turma in disc['carga_por_turma']:
                carga = disc['carga_por_turma'][turma]
            else:
                carga = disc['carga_semanal']
            print(f"  └─ {turma}: {carga}h")

print()
print("=" * 80)
print("SUGESTÕES PARA REDUZIR 2h:")
print("=" * 80)
print()
print("Opções:")
print("1. Reduzir 2h de uma disciplina que tem 3h ou 4h")
print("2. Reduzir 1h de duas disciplinas que têm 2h")
print("3. Verificar se alguma disciplina foi cadastrada duas vezes")
print()

# Contar disciplinas por carga
disciplinas_4h = []
disciplinas_3h = []
disciplinas_2h = []

for disc in disciplinas_com_excesso:
    for turma in ['1emB', '2emB']:
        if turma in disc['turmas']:
            if disc['carga_por_turma'] and turma in disc['carga_por_turma']:
                carga = disc['carga_por_turma'][turma]
            else:
                carga = disc['carga_semanal']
            
            if carga == 4:
                disciplinas_4h.append(disc['nome'])
            elif carga == 3:
                disciplinas_3h.append(disc['nome'])
            elif carga == 2:
                disciplinas_2h.append(disc['nome'])

if disciplinas_4h:
    print(f"📊 Disciplinas com 4h (podem reduzir para 2h):")
    for nome in set(disciplinas_4h):
        print(f"  • {nome}")
    print()

if disciplinas_3h:
    print(f"📊 Disciplinas com 3h (podem reduzir para 1h ou 2h):")
    for nome in set(disciplinas_3h):
        print(f"  • {nome}")
    print()

if disciplinas_2h:
    print(f"📊 Disciplinas com 2h (podem reduzir para 1h):")
    for nome in set(disciplinas_2h):
        print(f"  • {nome}")
    print()

print("=" * 80)
print("IMPORTANTE:")
print("Você precisa decidir qual(is) disciplina(s) reduzir.")
print("Use a interface do Streamlit para editar as cargas de 1emB e 2emB.")
print("=" * 80)
