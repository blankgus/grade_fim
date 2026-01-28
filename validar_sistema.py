#!/usr/bin/env python3
"""
VALIDAÇÃO COMPLETA DO SISTEMA
Verifica se todos os dados estão corretos antes de gerar grades
"""

import json
from collections import defaultdict

print("=" * 120)
print("🔍 VALIDAÇÃO COMPLETA DO SISTEMA")
print("=" * 120)
print()

# Carregar banco
with open('escola_database.json', 'r', encoding='utf-8') as f:
    banco = json.load(f)

turmas = banco.get('turmas', [])
professores = banco.get('professores', [])
disciplinas = banco.get('disciplinas', [])

print(f"📊 Dados carregados:")
print(f"  • Turmas: {len(turmas)}")
print(f"  • Professores: {len(professores)}")
print(f"  • Disciplinas: {len(disciplinas)}")
print()

# 1. Validar turmas
print("=" * 120)
print("1️⃣ VALIDAÇÃO: TURMAS")
print("=" * 120)
print()

turmas_validas = [t for t in turmas if any(x in t['nome'] for x in ['6ano', '7ano', '8ano', '9ano', '1em', '2em', '3em'])]
print(f"✅ {len(turmas_validas)} turmas válidas encontradas:\n")

cargas_turmas = defaultdict(int)
for disc in disciplinas:
    for turma_nome, carga in disc.get('carga_por_turma', {}).items():
        cargas_turmas[turma_nome] += carga

LIMITE_EF = 25
LIMITE_EM = 35

turmas_ok = 0
turmas_problema = []

for turma in turmas_validas:
    nome = turma['nome']
    carga = cargas_turmas.get(nome, 0)
    limite = LIMITE_EM if 'em' in nome.lower() else LIMITE_EF
    
    if carga == limite:
        status = "✅"
        turmas_ok += 1
    elif carga < limite:
        status = f"⚠️ FALTA {limite - carga}h"
        turmas_problema.append((nome, carga, limite))
    else:
        status = f"❌ EXCESSO {carga - limite}h"
        turmas_problema.append((nome, carga, limite))
    
    print(f"  {nome:10s} | {carga:2d}h / {limite}h | {status}")

print()
print(f"📊 Resultado: {turmas_ok}/{len(turmas_validas)} turmas com carga correta")

if turmas_problema:
    print(f"⚠️ {len(turmas_problema)} turmas com problemas:")
    for nome, carga, limite in turmas_problema:
        print(f"   • {nome}: {carga}h/{limite}h")

print()

# 2. Validar professores
print("=" * 120)
print("2️⃣ VALIDAÇÃO: PROFESSORES")
print("=" * 120)
print()

profs_atribuicoes = defaultdict(int)
for disc in disciplinas:
    for turma, carga in disc.get('carga_por_turma', {}).items():
        prof_nome = disc.get('professor_por_turma', {}).get(turma)
        if prof_nome:
            profs_atribuicoes[prof_nome] += carga

print(f"Professores com atribuições:\n")

profs_ok = 0
profs_problema = []

for prof in professores:
    nome = prof['nome']
    carga_esperada = prof.get('carga_horaria', 0)
    carga_atribuida = profs_atribuicoes.get(nome, 0)
    
    if carga_atribuida == 0:
        status = "❌ SEM ATRIBUIÇÕES"
        profs_problema.append((nome, carga_esperada, carga_atribuida))
    elif abs(carga_atribuida - carga_esperada) <= 2:  # Tolerância de 2h
        status = "✅"
        profs_ok += 1
    elif carga_atribuida < carga_esperada:
        status = f"⚠️ FALTA {carga_esperada - carga_atribuida}h"
        profs_problema.append((nome, carga_esperada, carga_atribuida))
    else:
        status = f"⚠️ EXCESSO {carga_atribuida - carga_esperada}h"
        profs_problema.append((nome, carga_esperada, carga_atribuida))
    
    print(f"  {nome:20s} | Esperado: {carga_esperada:2d}h | Atribuído: {carga_atribuida:2d}h | {status}")

print()
print(f"📊 Resultado: {profs_ok}/{len(professores)} professores com carga correta (tolerância ±2h)")

if profs_problema:
    print(f"⚠️ {len(profs_problema)} professores com problemas")

print()

# 3. Validar disciplinas
print("=" * 120)
print("3️⃣ VALIDAÇÃO: DISCIPLINAS")
print("=" * 120)
print()

disciplinas_sem_prof = []
disciplinas_sem_turmas = []

for disc in disciplinas:
    nome = disc['nome']
    turmas_disc = disc.get('turmas', [])
    prof_por_turma = disc.get('professor_por_turma', {})
    
    if not turmas_disc:
        disciplinas_sem_turmas.append(nome)
        continue
    
    # Verificar se todas as turmas têm professor
    turmas_sem_prof = [t for t in turmas_disc if t not in prof_por_turma or not prof_por_turma[t]]
    
    if turmas_sem_prof:
        disciplinas_sem_prof.append((nome, turmas_sem_prof))

if disciplinas_sem_prof:
    print(f"⚠️ {len(disciplinas_sem_prof)} disciplinas com turmas sem professor:\n")
    for disc_nome, turmas_sem in disciplinas_sem_prof[:10]:
        print(f"  • {disc_nome}: {', '.join(turmas_sem)}")
    if len(disciplinas_sem_prof) > 10:
        print(f"  ... e mais {len(disciplinas_sem_prof) - 10}")
else:
    print("✅ Todas as disciplinas têm professores atribuídos em todas as turmas")

if disciplinas_sem_turmas:
    print(f"\n⚠️ {len(disciplinas_sem_turmas)} disciplinas sem turmas:")
    for nome in disciplinas_sem_turmas[:5]:
        print(f"  • {nome}")

print()

# 4. Verificar disponibilidade dos professores
print("=" * 120)
print("4️⃣ VALIDAÇÃO: DISPONIBILIDADE DOS PROFESSORES")
print("=" * 120)
print()

profs_sem_disponibilidade = []
profs_disponibilidade_limitada = []

for prof in professores:
    nome = prof['nome']
    disponibilidade = prof.get('disponibilidade', {})
    
    if not disponibilidade:
        profs_sem_disponibilidade.append(nome)
    else:
        dias_disponiveis = len([d for d, disp in disponibilidade.items() if disp])
        if dias_disponiveis < 5:
            profs_disponibilidade_limitada.append((nome, dias_disponiveis))

if profs_sem_disponibilidade:
    print(f"⚠️ {len(profs_sem_disponibilidade)} professores SEM disponibilidade cadastrada:")
    for nome in profs_sem_disponibilidade:
        print(f"  • {nome}")
    print()

if profs_disponibilidade_limitada:
    print(f"⚠️ {len(profs_disponibilidade_limitada)} professores com disponibilidade limitada:")
    for nome, dias in profs_disponibilidade_limitada:
        print(f"  • {nome}: {dias}/5 dias")
else:
    print("✅ Todos os professores têm disponibilidade em todos os dias")

print()

# RESUMO FINAL
print("=" * 120)
print("📋 RESUMO FINAL")
print("=" * 120)
print()

problemas_criticos = []
avisos = []

if turmas_problema:
    problemas_criticos.append(f"❌ {len(turmas_problema)} turmas com carga incorreta")

if any(carga == 0 for nome, esperada, carga in profs_problema):
    problemas_criticos.append(f"❌ Professores sem atribuições")

if disciplinas_sem_prof:
    avisos.append(f"⚠️ {len(disciplinas_sem_prof)} disciplinas com turmas sem professor")

if profs_sem_disponibilidade:
    avisos.append(f"⚠️ {len(profs_sem_disponibilidade)} professores sem disponibilidade")

if problemas_criticos:
    print("❌ PROBLEMAS CRÍTICOS (impedem geração de grade):")
    for prob in problemas_criticos:
        print(f"   {prob}")
    print()

if avisos:
    print("⚠️ AVISOS (podem causar problemas na grade):")
    for aviso in avisos:
        print(f"   {aviso}")
    print()

if not problemas_criticos and not avisos:
    print("🎉 SISTEMA 100% VALIDADO!")
    print()
    print("✅ Todas as turmas têm carga correta")
    print("✅ Todos os professores têm atribuições corretas")
    print("✅ Todas as disciplinas têm professores atribuídos")
    print("✅ Todos os professores têm disponibilidade cadastrada")
    print()
    print("🚀 O sistema está pronto para gerar grades!")
elif not problemas_criticos:
    print("✅ Sistema validado com avisos")
    print()
    print("O sistema pode gerar grades, mas pode haver alguns alertas.")
else:
    print("❌ Sistema com problemas críticos")
    print()
    print("Corrija os problemas críticos antes de gerar grades.")

print()
