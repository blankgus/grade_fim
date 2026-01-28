#!/usr/bin/env python3
"""
Script para testar geração de grade e identificar problemas de alocação.
"""

import sys
from database import carregar_turmas, carregar_professores, carregar_disciplinas
from simple_scheduler import SimpleGradeHoraria

def testar_geracao_grade(turma_nome):
    """Testa geração de grade para uma turma específica"""
    print(f"\n{'='*80}")
    print(f"TESTE DE GERAÇÃO: {turma_nome}")
    print(f"{'='*80}")
    
    # Carregar dados
    turmas = carregar_turmas()
    professores = carregar_professores()
    disciplinas = carregar_disciplinas()
    
    # Encontrar turma
    turma = None
    for t in turmas:
        if t.nome == turma_nome:
            turma = t
            break
    
    if not turma:
        print(f"❌ Turma {turma_nome} não encontrada!")
        return
    
    print(f"\nTurma: {turma.nome}")
    print(f"Série: {turma.serie}")
    print(f"Turno: {turma.turno}")
    print(f"Segmento: {turma.segmento}")
    
    # Disciplinas da turma
    print(f"\n--- DISCIPLINAS ---")
    disciplinas_turma = []
    carga_total = 0
    
    for disc in disciplinas:
        if turma_nome in disc.turmas:
            carga = disc.obter_carga_turma(turma_nome)
            professor = disc.professor_por_turma.get(turma_nome, 'SEM PROFESSOR')
            disciplinas_turma.append({
                'disc': disc,
                'carga': carga,
                'professor': professor
            })
            carga_total += carga
            print(f"  {disc.nome:30s} {carga}h - {professor}")
    
    print(f"\nTotal: {carga_total}h")
    
    # Criar scheduler
    scheduler = SimpleGradeHoraria()
    
    # Gerar grade
    print(f"\n--- GERANDO GRADE ---")
    resultado = scheduler.gerar_grade_turma(turma, disciplinas, professores)
    
    if not resultado['sucesso']:
        print(f"❌ FALHA: {resultado.get('mensagem', 'Erro desconhecido')}")
        
        # Mostrar conflitos
        if 'conflitos' in resultado:
            print(f"\n--- CONFLITOS ---")
            for conflito in resultado['conflitos']:
                print(f"  {conflito}")
        
        # Mostrar aulas não alocadas
        if 'nao_alocadas' in resultado:
            print(f"\n--- AULAS NÃO ALOCADAS ---")
            nao_alocadas = resultado['nao_alocadas']
            for item in nao_alocadas:
                print(f"  {item['disciplina']:30s} {item['professor']:20s} (faltam {item.get('quantidade', '?')} aulas)")
        
        return False
    
    # Sucesso - analisar grade
    grade = resultado['grade']
    
    print(f"\n✅ Grade gerada com sucesso!")
    print(f"Total de aulas alocadas: {len(grade)}")
    
    # Agrupar por dia
    aulas_por_dia = {}
    for aula in grade:
        dia = aula['dia']
        if dia not in aulas_por_dia:
            aulas_por_dia[dia] = []
        aulas_por_dia[dia].append(aula)
    
    print(f"\n--- DISTRIBUIÇÃO POR DIA ---")
    dias_ordem = ['segunda', 'terca', 'quarta', 'quinta', 'sexta']
    for dia in dias_ordem:
        if dia in aulas_por_dia:
            aulas = aulas_por_dia[dia]
            print(f"  {dia.capitalize():10s} {len(aulas)} aulas")
            for aula in sorted(aulas, key=lambda a: a['horario']):
                print(f"    {aula['horario']} - {aula['disciplina']:30s} ({aula['professor']})")
        else:
            print(f"  {dia.capitalize():10s} 0 aulas ❌ DIA VAZIO!")
    
    # Verificar se todas as disciplinas foram alocadas
    print(f"\n--- VERIFICAÇÃO DE COMPLETUDE ---")
    aulas_por_disciplina = {}
    for aula in grade:
        disc = aula['disciplina']
        aulas_por_disciplina[disc] = aulas_por_disciplina.get(disc, 0) + 1
    
    todas_ok = True
    for item in disciplinas_turma:
        disc_nome = item['disc'].nome
        alocadas = aulas_por_disciplina.get(disc_nome, 0)
        esperadas = item['carga']
        
        if alocadas == esperadas:
            print(f"  ✅ {disc_nome:30s} {alocadas}/{esperadas}h")
        else:
            print(f"  ❌ {disc_nome:30s} {alocadas}/{esperadas}h (faltam {esperadas - alocadas}h)")
            todas_ok = False
    
    if todas_ok:
        print(f"\n✅ TODAS AS DISCIPLINAS ALOCADAS CORRETAMENTE!")
    else:
        print(f"\n❌ ALGUMAS DISCIPLINAS NÃO FORAM COMPLETAMENTE ALOCADAS")
    
    return todas_ok

if __name__ == '__main__':
    # Testar turmas problemáticas
    turmas_teste = ['9anoB', '7anoB', '6anoA', '7anoA', '8anoA', '8anoB', '9anoA', '2emB', '1emA']
    
    total = len(turmas_teste)
    sucesso = 0
    
    for turma in turmas_teste:
        if testar_geracao_grade(turma):
            sucesso += 1
    
    print(f"\n{'='*80}")
    print(f"RESULTADO FINAL: {sucesso}/{total} turmas geradas com sucesso")
    print(f"{'='*80}")
