#!/usr/bin/env python3
"""
Script para analisar por que aulas não estão sendo alocadas.

Foca especialmente em 9anoB que tem apenas 16/25 aulas alocadas.
"""

import json
from collections import defaultdict

def carregar_dados():
    with open('escola_database.json', 'r', encoding='utf-8') as f:
        return json.load(f)

def analisar_turma(dados, turma_nome):
    """Analisa detalhadamente uma turma"""
    print(f"\n{'='*80}")
    print(f"ANÁLISE DETALHADA: {turma_nome}")
    print(f"{'='*80}")
    
    # 1. Carga esperada
    turma_data = None
    for t in dados['turmas']:
        if t['nome'] == turma_nome:
            turma_data = t
            break
    
    if not turma_data:
        print(f"❌ Turma {turma_nome} não encontrada!")
        return
    
    periodo = turma_data['periodo']
    horarios_turma = turma_data.get('horarios', [])
    
    print(f"\nTurma: {turma_nome}")
    print(f"Período: {periodo}")
    print(f"Horários: {len(horarios_turma)} slots")
    
    # 2. Disciplinas da turma
    disciplinas_turma = []
    carga_total = 0
    
    for disc in dados['disciplinas']:
        if turma_nome in disc.get('carga_por_turma', {}):
            carga = disc['carga_por_turma'][turma_nome]
            professor = disc.get('professor_por_turma', {}).get(turma_nome, 'SEM PROFESSOR')
            disciplinas_turma.append({
                'nome': disc['nome'],
                'carga': carga,
                'professor': professor,
                'tipo': disc.get('tipo', 'media')
            })
            carga_total += carga
    
    print(f"Carga total esperada: {carga_total}h")
    print(f"\n--- DISCIPLINAS DA TURMA ---")
    for d in sorted(disciplinas_turma, key=lambda x: x['carga'], reverse=True):
        print(f"  {d['nome']:30s} {d['carga']}h - {d['professor']:20s} ({d['tipo']})")
    
    # 3. Analisar professores
    print(f"\n--- ANÁLISE DE PROFESSORES ---")
    professores_info = {}
    
    for disc in disciplinas_turma:
        prof_nome = disc['professor']
        if prof_nome == 'SEM PROFESSOR':
            print(f"❌ {disc['nome']}: SEM PROFESSOR ATRIBUÍDO!")
            continue
        
        if prof_nome not in professores_info:
            # Buscar dados do professor
            for p in dados['professores']:
                if p['nome'] == prof_nome:
                    professores_info[prof_nome] = {
                        'carga_atribuida': p.get('carga_horaria', 0),
                        'carga_maxima': p.get('carga_horaria_maxima', 35),
                        'disponibilidade': p.get('disponibilidade', []),
                        'horarios_indisponiveis': p.get('horarios_indisponiveis', []),
                        'disciplinas_turma': []
                    }
                    break
        
        if prof_nome in professores_info:
            professores_info[prof_nome]['disciplinas_turma'].append(disc)
    
    for prof_nome, info in sorted(professores_info.items()):
        carga_turma = sum(d['carga'] for d in info['disciplinas_turma'])
        disponivel = info['carga_maxima'] - info['carga_atribuida']
        
        status = "✅" if disponivel >= 0 else "❌"
        print(f"\n{status} {prof_nome}:")
        print(f"    Carga nesta turma: {carga_turma}h")
        print(f"    Carga total atribuída: {info['carga_atribuida']}h / {info['carga_maxima']}h")
        print(f"    Disponível: {disponivel}h")
        print(f"    Dias disponíveis: {', '.join(info['disponibilidade'])}")
        print(f"    Horários indisponíveis: {len(info['horarios_indisponiveis'])} slots")
        
        if disponivel < 0:
            print(f"    ⚠️ SOBRECARGA: Professor tem {-disponivel}h a mais!")
        
        # Verificar conflitos de período
        for p in dados['professores']:
            if p['nome'] == prof_nome:
                # Verificar se professor dá aula em outras turmas no mesmo período
                outras_turmas_periodo = []
                for disc in dados['disciplinas']:
                    prof_por_turma = disc.get('professor_por_turma', {})
                    for t_nome, t_prof in prof_por_turma.items():
                        if t_prof == prof_nome and t_nome != turma_nome:
                            # Verificar período da outra turma
                            for turma_check in dados['turmas']:
                                if turma_check['nome'] == t_nome and turma_check['periodo'] == periodo:
                                    outras_turmas_periodo.append({
                                        'turma': t_nome,
                                        'disciplina': disc['nome'],
                                        'carga': disc['carga_por_turma'].get(t_nome, 0)
                                    })
                
                if outras_turmas_periodo:
                    print(f"    ⚠️ CONFLITO DE PERÍODO: Professor também dá aula em:")
                    for ot in outras_turmas_periodo:
                        print(f"       - {ot['turma']}: {ot['disciplina']} ({ot['carga']}h)")
    
    # 4. Resumo
    print(f"\n--- RESUMO ---")
    total_professores = len(professores_info)
    professores_ok = sum(1 for info in professores_info.values() 
                        if info['carga_maxima'] - info['carga_atribuida'] >= 0)
    professores_sobrecarga = total_professores - professores_ok
    
    print(f"Total de professores: {total_professores}")
    print(f"  ✅ Com carga OK: {professores_ok}")
    print(f"  ❌ Com sobrecarga: {professores_sobrecarga}")
    print(f"Carga total: {carga_total}h")

def analisar_geral(dados):
    """Análise geral do sistema"""
    print(f"\n{'='*80}")
    print(f"ANÁLISE GERAL DO SISTEMA")
    print(f"{'='*80}")
    
    # Cargas por professor
    print(f"\n--- CARGA DOS PROFESSORES ---")
    professores_carga = []
    
    for prof in dados['professores']:
        nome = prof['nome']
        carga_atribuida = prof.get('carga_horaria', 0)
        carga_maxima = prof.get('carga_horaria_maxima', 35)
        disponivel = carga_maxima - carga_atribuida
        
        professores_carga.append({
            'nome': nome,
            'atribuida': carga_atribuida,
            'maxima': carga_maxima,
            'disponivel': disponivel,
            'percentual': (carga_atribuida / carga_maxima * 100) if carga_maxima > 0 else 0
        })
    
    # Ordenar por percentual usado
    for p in sorted(professores_carga, key=lambda x: x['percentual'], reverse=True):
        status = "✅" if p['disponivel'] >= 0 else "❌"
        barra = "█" * int(p['percentual'] / 5)
        print(f"{status} {p['nome']:20s} {p['atribuida']:2d}/{p['maxima']:2d}h ({p['percentual']:5.1f}%) {barra}")
    
    # Turmas
    print(f"\n--- TURMAS ---")
    turmas_info = []
    
    for turma in dados['turmas']:
        nome = turma['nome']
        carga_total = 0
        
        for disc in dados['disciplinas']:
            if nome in disc.get('carga_por_turma', {}):
                carga_total += disc['carga_por_turma'][nome]
        
        limite = 25 if 'ano' in nome else 35
        status = "✅" if carga_total == limite else "❌"
        turmas_info.append({
            'nome': nome,
            'carga': carga_total,
            'limite': limite,
            'status': status
        })
    
    for t in sorted(turmas_info, key=lambda x: x['carga']):
        print(f"{t['status']} {t['nome']:10s} {t['carga']:2d}/{t['limite']:2d}h")
    
    turmas_ok = sum(1 for t in turmas_info if t['carga'] == t['limite'])
    print(f"\nTotal: {turmas_ok}/{len(turmas_info)} turmas com carga correta")

if __name__ == '__main__':
    dados = carregar_dados()
    
    # Análise geral primeiro
    analisar_geral(dados)
    
    # Análises detalhadas das turmas problemáticas
    turmas_problema = ['9anoB', '7anoB', '6anoA', '7anoA', '8anoA', '8anoB', '9anoA', '2emB']
    
    for turma in turmas_problema:
        analisar_turma(dados, turma)
