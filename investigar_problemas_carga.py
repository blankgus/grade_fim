#!/usr/bin/env python3
"""
Investiga os problemas de carga das turmas 1emB, 2emA e 2emB
"""

import json

with open('escola_database.json', 'r', encoding='utf-8') as f:
    banco = json.load(f)

turmas_problema = ['1emB', '2emA', '2emB']

print("=" * 120)
print("🔍 INVESTIGAÇÃO: Turmas com problemas de carga")
print("=" * 120)
print()

for turma_nome in turmas_problema:
    print(f"\n{'='*120}")
    print(f"📚 TURMA: {turma_nome}")
    print(f"{'='*120}\n")
    
    # Listar todas as disciplinas desta turma
    disciplinas_turma = []
    carga_total = 0
    
    for disc in banco['disciplinas']:
        if turma_nome in disc.get('turmas', []):
            carga = disc['carga_por_turma'].get(turma_nome, 0)
            professor = disc['professor_por_turma'].get(turma_nome, '❌ SEM PROFESSOR')
            
            disciplinas_turma.append({
                'nome': disc['nome'],
                'carga': carga,
                'professor': professor
            })
            carga_total += carga
    
    # Ordenar por nome
    disciplinas_turma.sort(key=lambda x: x['nome'])
    
    # Tabela
    print(f"{'Disciplina':<35} | {'Carga':<6} | Professor")
    print("-" * 120)
    
    for d in disciplinas_turma:
        print(f"{d['nome']:<35} | {d['carga']:>4}h | {d['professor']}")
    
    print("-" * 120)
    print(f"{'TOTAL':<35} | {carga_total:>4}h")
    
    # Análise
    limite = 35  # Ensino Médio
    diferenca = carga_total - limite
    
    if diferenca > 0:
        print(f"\n❌ EXCESSO DE {diferenca}h")
    elif diferenca < 0:
        print(f"\n⚠️ FALTAM {-diferenca}h")
    else:
        print(f"\n✅ CARGA CORRETA")
    
    print(f"\nTotal de disciplinas: {len(disciplinas_turma)}")

print()
print()
print("=" * 120)
print("💡 ANÁLISE")
print("=" * 120)
print()
print("Para identificar as disciplinas extras/faltantes, compare com o PDF:")
print("  1. Abra o PDF grade2026.pdf")
print("  2. Procure a 'caixa' de cada professor que dá aula nestas turmas")
print("  3. Verifique se todas as disciplinas listadas acima estão no PDF")
print()
