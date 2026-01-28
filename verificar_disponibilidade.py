#!/usr/bin/env python3
"""Verificar disponibilidade dos professores problemáticos"""
import json

dados = json.load(open('escola_database.json', encoding='utf-8'))
profs_problema = ['Marina', 'Malu', 'Laís', 'Cesar', 'Heliana', 'Matheus', 'Rene']

print("=== DISPONIBILIDADE DOS PROFESSORES PROBLEMÁTICOS ===\n")

for p in dados['professores']:
    if p['nome'] in profs_problema:
        disp = p.get('disponibilidade', [])
        indisp = p.get('horarios_indisponiveis', [])
        carga = p.get('carga_horaria', 0)
        max_carga = p.get('carga_horaria_maxima', 35)
        
        print(f"{p['nome']:15s}")
        print(f"  Disponibilidade: {disp} ({len(disp)} dias)")
        print(f"  Horários indisponíveis: {len(indisp)} slots")
        if indisp:
            print(f"    {indisp}")
        print(f"  Carga: {carga}/{max_carga}h (resta {max_carga - carga}h)")
        print()
