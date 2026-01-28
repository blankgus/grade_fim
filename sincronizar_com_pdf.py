#!/usr/bin/env python3
"""
SINCRONIZAÇÃO TOTAL FINAL: PDF → BANCO
Reconstrói TODAS as disciplinas e atribuições exatamente como no PDF
"""

import json
from datetime import datetime
import shutil
from collections import defaultdict

print("=" * 120)
print("🔄 SINCRONIZAÇÃO TOTAL: PDF → BANCO (com professores)")
print("=" * 120)
print()

# Carregar atribuições dos professores do PDF
with open('professores_atribuicoes_pdf.json', 'r', encoding='utf-8') as f:
    professores_pdf = json.load(f)

# Carregar banco
with open('escola_database.json', 'r', encoding='utf-8') as f:
    banco = json.load(f)

# Backup
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
backup_file = f'escola_database_backup_{timestamp}.json'
shutil.copy('escola_database.json', backup_file)
print(f"✅ Backup: {backup_file}\n")

# Turmas válidas (6ano-9ano e 1em-3em, A e B)
turmas_validas = [t for t in banco['turmas'] if any(x in t['nome'] for x in ['6ano', '7ano', '8ano', '9ano', '1em', '2em', '3em'])]
print(f"📚 Turmas válidas: {len(turmas_validas)}")

# Construir estrutura de disciplinas a partir das atribuições dos professores
# disciplina -> turma -> (professor, carga)
disciplinas_data = defaultdict(lambda: defaultdict(lambda: {'professor': None, 'carga': 0}))

total_atribuicoes = 0
for professor, atribuicoes in professores_pdf.items():
    for atrib in atribuicoes:
        turma = atrib['turma']
        disciplina = atrib['disciplina']
        carga = atrib['carga']
        
        # Filtrar apenas turmas válidas
        if turma not in [t['nome'] for t in turmas_validas]:
            continue
        
        disciplinas_data[disciplina][turma]['professor'] = professor
        disciplinas_data[disciplina][turma]['carga'] = carga
        total_atribuicoes += 1

print(f"📋 Disciplinas extraídas: {len(disciplinas_data)}")
print(f"📝 Atribuições totais: {total_atribuicoes}\n")

# Buscar disciplinas antigas para manter configurações
disciplinas_antigas = {d['nome']: d for d in banco.get('disciplinas', [])}

# Criar novas disciplinas
novas_disciplinas = []

for nome_disciplina, turmas_data in sorted(disciplinas_data.items()):
    # Buscar disciplina antiga para manter cores e tipo
    disc_antiga = disciplinas_antigas.get(nome_disciplina)
    
    # Construir listas
    turmas_list = sorted(list(turmas_data.keys()))
    carga_por_turma = {turma: data['carga'] for turma, data in turmas_data.items()}
    professor_por_turma = {turma: data['professor'] for turma, data in turmas_data.items()}
    
    # Criar nova disciplina
    nova_disc = {
        'nome': nome_disciplina,
        'carga_semanal': max(carga_por_turma.values()) if carga_por_turma else 1,
        'tipo': disc_antiga.get('tipo', 'media') if disc_antiga else 'media',
        'turmas': turmas_list,
        'carga_por_turma': carga_por_turma,
        'professor_por_turma': professor_por_turma,
        'cor_fundo': disc_antiga.get('cor_fundo', '#4A90E2') if disc_antiga else '#4A90E2',
        'cor_fonte': disc_antiga.get('cor_fonte', '#FFFFFF') if disc_antiga else '#FFFFFF',
        'id': disc_antiga.get('id') if disc_antiga else None
    }
    
    # Remover id None (será gerado automaticamente)
    if nova_disc['id'] is None:
        del nova_disc['id']
    
    novas_disciplinas.append(nova_disc)
    
    print(f"✅ {nome_disciplina:30s} | {len(turmas_list)} turmas | {len([p for p in professor_por_turma.values() if p])} professores")

print()

# Substituir no banco
banco['turmas'] = turmas_validas
banco['disciplinas'] = novas_disciplinas

# Salvar
with open('escola_database.json', 'w', encoding='utf-8') as f:
    json.dump(banco, f, indent=2, ensure_ascii=False)

print()
print("=" * 120)
print("✅ SINCRONIZAÇÃO CONCLUÍDA")
print("=" * 120)
print(f"  Turmas: {len(turmas_validas)}")
print(f"  Disciplinas: {len(novas_disciplinas)}")
print(f"  Atribuições: {total_atribuicoes}")
print(f"  Backup: {backup_file}")
print()

# Validar cargas por turma
print("=" * 120)
print("📊 VALIDAÇÃO: Carga horária por turma")
print("=" * 120)
print()

cargas_por_turma = defaultdict(int)
for disc in novas_disciplinas:
    for turma, carga in disc['carga_por_turma'].items():
        cargas_por_turma[turma] += carga

# Limites esperados
LIMITE_EF = 25  # 6º-9º ano
LIMITE_EM = 35  # 1º-3º EM

for turma in sorted([t['nome'] for t in turmas_validas]):
    carga = cargas_por_turma.get(turma, 0)
    
    # Determinar limite
    if 'em' in turma.lower():
        limite = LIMITE_EM
    else:
        limite = LIMITE_EF
    
    # Status
    if carga == limite:
        status = "✅"
    elif carga < limite:
        status = f"⚠️ FALTA {limite - carga}h"
    else:
        status = f"❌ EXCESSO {carga - limite}h"
    
    print(f"{turma:10s} | {carga:2d}h / {limite}h | {status}")

print()

# Verificar professores sem atribuições
print("=" * 120)
print("🔍 PROFESSORES: Verificação de cargas")
print("=" * 120)
print()

professores_banco = {p['nome']: p.get('carga_horaria', 0) for p in banco.get('professores', [])}

professores_atribuidos = defaultdict(int)
for disc in novas_disciplinas:
    for turma, prof in disc['professor_por_turma'].items():
        if prof:
            carga = disc['carga_por_turma'].get(turma, 0)
            professores_atribuidos[prof] += carga

for prof_nome in sorted(professores_banco.keys()):
    carga_esperada = professores_banco[prof_nome]
    carga_atribuida = professores_atribuidos.get(prof_nome, 0)
    
    if carga_atribuida == carga_esperada:
        status = "✅"
    elif carga_atribuida < carga_esperada:
        status = f"⚠️ FALTA {carga_esperada - carga_atribuida}h"
    else:
        status = f"⚠️ EXCESSO {carga_atribuida - carga_esperada}h"
    
    if carga_atribuida > 0:
        print(f"{prof_nome:20s} | Esperado: {carga_esperada:2d}h | Atribuído: {carga_atribuida:2d}h | {status}")

print()
print("✅ Sincronização concluída! Execute o app Streamlit para testar.")
print()
