#!/usr/bin/env python3
"""
Verifica disciplinas duplicadas e problemas de alocação
"""

import json
from collections import defaultdict

with open('escola_database.json', 'r', encoding='utf-8') as f:
    banco = json.load(f)

disciplinas = banco.get('disciplinas', [])

print('='*100)
print('DIAGNÓSTICO: DISCIPLINAS NO BANCO')
print('='*100)
print()

# Agrupar por nome base (sem sufixo)
por_nome = defaultdict(list)

for disc in disciplinas:
    nome = disc['nome']
    # Remover sufixo A/B se existir
    nome_base = nome.rstrip(' A').rstrip(' B')
    por_nome[nome_base].append(disc)

# Mostrar apenas as que têm duplicatas
print('🔴 DISCIPLINAS COM SUFIXO A/B (DUPLICADAS):')
print()
duplicadas = {k: v for k, v in por_nome.items() if len(v) > 1}

if duplicadas:
    for nome_base, discs in sorted(duplicadas.items()):
        print(f'{nome_base}:')
        for disc in discs:
            turmas = ', '.join(disc.get('turmas', []))
            carga_por_turma = disc.get('carga_por_turma', {})
            prof_por_turma = disc.get('professor_por_turma', {})
            print(f'  • {disc["nome"]:35s} | Turmas: {turmas or "(vazio)"}')
            if prof_por_turma:
                print(f'    Professores: {prof_por_turma}')
        print()
else:
    print('  ✅ Nenhuma disciplina duplicada encontrada')
    print()

print('='*100)
print(f'📊 RESUMO:')
print('='*100)
print(f'  Disciplinas duplicadas: {len(duplicadas)}')
print(f'  Disciplinas únicas: {len(por_nome)}')
print(f'  Total no banco: {len(disciplinas)}')
print()

# Verificar disciplinas problemáticas mencionadas
print('='*100)
print('🔍 DISCIPLINAS PROBLEMÁTICAS MENCIONADAS:')
print('='*100)
print()

problemas = ['Educação Física', 'Dinâmica', 'Mercado de Trabalho', 'Oralidade', 'História']

for nome_prob in problemas:
    # Buscar todas as variações
    encontradas = [d for d in disciplinas if nome_prob.lower() in d['nome'].lower()]
    
    if encontradas:
        print(f'{nome_prob}:')
        for disc in encontradas:
            turmas = disc.get('turmas', [])
            prof_por_turma = disc.get('professor_por_turma', {})
            carga_por_turma = disc.get('carga_por_turma', {})
            
            print(f'  • Nome: {disc["nome"]}')
            print(f'    ID: {disc.get("id", "sem id")}')
            print(f'    Turmas: {", ".join(turmas) if turmas else "(vazio)"}')
            print(f'    Professores: {prof_por_turma if prof_por_turma else "(vazio)"}')
            print(f'    Cargas: {carga_por_turma if carga_por_turma else "(vazio)"}')
        print()
    else:
        print(f'{nome_prob}: ❌ NÃO ENCONTRADA')
        print()
