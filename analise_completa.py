#!/usr/bin/env python3
"""
Análise completa: PDF vs Banco
Verifica TODAS as atribuições (professor + turma + disciplina + carga)
"""

import json
from collections import defaultdict

# Carregar dados extraídos do PDF
try:
    with open('atribuicoes_extraidas_corrigidas.json', 'r', encoding='utf-8') as f:
        pdf_data = json.load(f)
except:
    print("❌ Arquivo atribuicoes_extraidas_corrigidas.json não encontrado")
    print("   Executar: python corrigir_nomes_disciplinas.py")
    exit(1)

# Carregar banco
with open('escola_database.json', 'r', encoding='utf-8') as f:
    banco = json.load(f)

print("=" * 120)
print("📊 ANÁLISE COMPLETA: PDF vs BANCO")
print("=" * 120)
print()

# Organizar dados do PDF por turma
pdf_por_turma = defaultdict(list)
for atrib in pdf_data:
    turma = atrib['turma']
    pdf_por_turma[turma].append({
        'disciplina': atrib['disciplina'],
        'carga': atrib['carga']
    })

# Organizar dados do BANCO por turma
banco_por_turma = defaultdict(list)
for disc in banco['disciplinas']:
    carga_por_turma = disc.get('carga_por_turma', {})
    prof_por_turma = disc.get('professor_por_turma', {})
    
    for turma, carga in carga_por_turma.items():
        professor = prof_por_turma.get(turma, '❌ SEM PROFESSOR')
        banco_por_turma[turma].append({
            'disciplina': disc['nome'],
            'carga': carga,
            'professor': professor
        })

# Comparar turma por turma
turmas = sorted(set(list(pdf_por_turma.keys()) + list(banco_por_turma.keys())))

problemas_gerais = {
    'turmas_com_falta': [],
    'turmas_com_excesso': [],
    'disciplinas_sem_professor': [],
    'disciplinas_faltando': [],
    'cargas_diferentes': []
}

for turma in turmas:
    pdf_turma = pdf_por_turma.get(turma, [])
    banco_turma = banco_por_turma.get(turma, [])
    
    # Calcular cargas totais
    carga_pdf = sum(d['carga'] for d in pdf_turma)
    carga_banco = sum(d['carga'] for d in banco_turma)
    
    print(f"\n{'='*120}")
    print(f"📚 TURMA: {turma}")
    print(f"{'='*120}")
    
    # Status da carga
    if carga_pdf == carga_banco:
        status = "✅"
    elif carga_banco < carga_pdf:
        status = "⚠️ FALTA"
        problemas_gerais['turmas_com_falta'].append(turma)
    else:
        status = "⚠️ EXCESSO"
        problemas_gerais['turmas_com_excesso'].append(turma)
    
    print(f"{status} PDF: {carga_pdf}h | Banco: {carga_banco}h | Diferença: {carga_banco - carga_pdf:+d}h")
    print()
    
    # Criar dicionários de disciplinas
    pdf_dict = {d['disciplina']: d['carga'] for d in pdf_turma}
    banco_dict = {d['disciplina']: (d['carga'], d['professor']) for d in banco_turma}
    
    todas_disciplinas = sorted(set(list(pdf_dict.keys()) + list(banco_dict.keys())))
    
    # Tabela de comparação
    print(f"{'Disciplina':<35} | {'PDF':<6} | {'Banco':<6} | {'Professor':<20} | Status")
    print("-" * 120)
    
    for disc in todas_disciplinas:
        carga_pdf_disc = pdf_dict.get(disc, 0)
        banco_info = banco_dict.get(disc, (0, ''))
        carga_banco_disc = banco_info[0]
        professor = banco_info[1] if len(banco_info) > 1 else ''
        
        # Status
        if disc not in pdf_dict:
            status = "⚠️ EXTRA no banco"
        elif disc not in banco_dict:
            status = "❌ FALTANDO no banco"
            problemas_gerais['disciplinas_faltando'].append(f"{turma} - {disc}")
        elif carga_pdf_disc != carga_banco_disc:
            status = f"⚠️ Carga diferente ({carga_banco_disc - carga_pdf_disc:+d}h)"
            problemas_gerais['cargas_diferentes'].append(f"{turma} - {disc}")
        elif not professor or professor == '❌ SEM PROFESSOR':
            status = "❌ SEM PROFESSOR"
            problemas_gerais['disciplinas_sem_professor'].append(f"{turma} - {disc}")
        else:
            status = "✅ OK"
        
        print(f"{disc:<35} | {carga_pdf_disc:>4}h | {carga_banco_disc:>4}h | {professor:<20} | {status}")

print()
print()
print("=" * 120)
print("📋 RESUMO DOS PROBLEMAS")
print("=" * 120)
print()

if problemas_gerais['turmas_com_falta']:
    print(f"⚠️ TURMAS COM FALTA DE CARGA ({len(problemas_gerais['turmas_com_falta'])}):")
    for turma in problemas_gerais['turmas_com_falta']:
        print(f"   • {turma}")
    print()

if problemas_gerais['turmas_com_excesso']:
    print(f"⚠️ TURMAS COM EXCESSO DE CARGA ({len(problemas_gerais['turmas_com_excesso'])}):")
    for turma in problemas_gerais['turmas_com_excesso']:
        print(f"   • {turma}")
    print()

if problemas_gerais['disciplinas_faltando']:
    print(f"❌ DISCIPLINAS FALTANDO NO BANCO ({len(problemas_gerais['disciplinas_faltando'])}):")
    for item in problemas_gerais['disciplinas_faltando'][:20]:  # Mostrar apenas as primeiras 20
        print(f"   • {item}")
    if len(problemas_gerais['disciplinas_faltando']) > 20:
        print(f"   ... e mais {len(problemas_gerais['disciplinas_faltando']) - 20}")
    print()

if problemas_gerais['disciplinas_sem_professor']:
    print(f"❌ DISCIPLINAS SEM PROFESSOR ({len(problemas_gerais['disciplinas_sem_professor'])}):")
    for item in problemas_gerais['disciplinas_sem_professor'][:20]:
        print(f"   • {item}")
    if len(problemas_gerais['disciplinas_sem_professor']) > 20:
        print(f"   ... e mais {len(problemas_gerais['disciplinas_sem_professor']) - 20}")
    print()

if problemas_gerais['cargas_diferentes']:
    print(f"⚠️ CARGAS DIFERENTES ({len(problemas_gerais['cargas_diferentes'])}):")
    for item in problemas_gerais['cargas_diferentes'][:20]:
        print(f"   • {item}")
    if len(problemas_gerais['cargas_diferentes']) > 20:
        print(f"   ... e mais {len(problemas_gerais['cargas_diferentes']) - 20}")
    print()

print()
print("=" * 120)
print("🎯 PRÓXIMAS AÇÕES RECOMENDADAS:")
print("=" * 120)
print()

if problemas_gerais['disciplinas_faltando']:
    print("1. Adicionar disciplinas faltantes no banco")
if problemas_gerais['disciplinas_sem_professor']:
    print("2. Atribuir professores às disciplinas sem professor")
if problemas_gerais['cargas_diferentes']:
    print("3. Corrigir cargas horárias diferentes")
if problemas_gerais['turmas_com_falta'] or problemas_gerais['turmas_com_excesso']:
    print("4. Revisar cargas totais das turmas")

print()
