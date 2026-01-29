#!/usr/bin/env python3
"""
Análise: Por que não conseguimos alocar todas as 410 aulas?

Hipótese: Professores que dão aula tanto em EM quanto em EF
têm conflitos de horário real porque os horários se sobrepõem.
"""

print("=== ANÁLISE DE HORÁRIOS REAIS ===\n")
print("EM - 7 períodos:")
print("  1: 07:00 (único EM)")
print("  2: 07:50 (= EF período 1)")
print("  3: 08:40 (= EF período 2)")
print("  4: 09:50 (= EF período 3)")
print("  5: 10:40 (= EF período 4)")
print("  6: 11:30 (= EF período 5)")
print("  7: 12:20 (único EM)")
print()
print("EF - 5 períodos:")
print("  1: 07:50 (= EM período 2)")
print("  2: 08:40 (= EM período 3)")
print("  3: 09:50 (= EM período 4)")
print("  4: 10:40 (= EM período 5)")
print("  5: 11:30 (= EM período 6)")
print()
print("Slots REAIS únicos por dia:")
print("  07:00 (somente EM)")
print("  07:50, 08:40, 09:50, 10:40, 11:30 (EM e EF compartilhados)")
print("  12:20 (somente EM)")
print()
print("Total: 7 slots reais por dia × 5 dias = 35 slots máximos por professor")
print()
print("PROBLEMA: Professores que dão aula em EM e EF estão limitados a 35 aulas,")
print("mesmo que teoricamente tenham 35h + 25h = 60h de períodos!")
print()

import json

dados = json.load(open('escola_database.json', encoding='utf-8'))

# Verificar quais professores dão aula em EM E EF
print("=== PROFESSORES QUE DÃO AULA EM EM E EF ===\n")

for prof in dados['professores']:
    turmas_em = set()
    turmas_ef = set()
    carga_em = 0
    carga_ef = 0
    
    for disc in dados['disciplinas']:
        for turma, prof_turma in disc.get('professor_por_turma', {}).items():
            if prof_turma == prof['nome']:
                carga = disc.get('carga_por_turma', {}).get(turma, 0)
                if 'em' in turma.lower():
                    turmas_em.add(turma)
                    carga_em += carga
                else:
                    turmas_ef.add(turma)
                    carga_ef += carga
    
    if turmas_em and turmas_ef:
        total = carga_em + carga_ef
        print(f"{prof['nome']:20s} EM: {carga_em}h  EF: {carga_ef}h  Total: {total}h")
        if total > 35:
            print(f"  ⚠️ IMPOSSÍVEL: {total}h > 35 slots reais!")
        print()
