#!/usr/bin/env python3
"""
Script para corrigir atribuições de Marcão baseado no PDF.

Segundo a imagem fornecida, Marcão dá:
- 9°B - 2h (Educação Física)
- 1°EMB - 1h (Educação Física)
- 2°EMB - 1h (Educação Física)
- 3°EMB - 2h (Educação Física)
- 2°EMA - 1h (Educação Física)
- 3°EMA - 2h (Educação Física)
Total: 9h

Disponibilidade: Quarta e Sexta, 7h às 12h20
"""

import json
from datetime import datetime

def criar_backup():
    """Cria backup do banco antes de modificar"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    with open('escola_database.json', 'r', encoding='utf-8') as f:
        dados = json.load(f)
    
    backup_file = f'escola_database_backup_{timestamp}.json'
    with open(backup_file, 'w', encoding='utf-8') as f:
        json.dump(dados, f, indent=2, ensure_ascii=False)
    
    print(f"✅ Backup criado: {backup_file}")
    return dados

def corrigir_marcao():
    """Corrige atribuições de Marcão"""
    dados = criar_backup()
    
    # Atribuições de Marcão segundo o PDF
    atribuicoes_marcao = {
        '9anoB': 2,
        '1emB': 1,
        '2emB': 1,
        '3emB': 2,
        '2emA': 1,
        '3emA': 2
    }
    
    total_carga_marcao = sum(atribuicoes_marcao.values())
    print(f"\n=== CORREÇÃO DE MARCÃO ===")
    print(f"Carga total: {total_carga_marcao}h")
    print(f"Turmas: {list(atribuicoes_marcao.keys())}")
    
    # 1. Atualizar carga_horaria de Marcão
    for prof in dados['professores']:
        if prof['nome'] == 'Marcão':
            prof['carga_horaria'] = total_carga_marcao
            print(f"\n✅ Carga de Marcão: 0h → {total_carga_marcao}h")
            break
    
    # 2. Atualizar professor_por_turma em Educação Física
    for disc in dados['disciplinas']:
        if disc['nome'] == 'Educação Física':
            prof_por_turma = disc.get('professor_por_turma', {})
            
            alteracoes = 0
            for turma, carga in atribuicoes_marcao.items():
                prof_atual = prof_por_turma.get(turma, 'NENHUM')
                prof_por_turma[turma] = 'Marcão'
                print(f"  {turma}: {prof_atual} → Marcão ({carga}h)")
                alteracoes += 1
            
            disc['professor_por_turma'] = prof_por_turma
            print(f"\n✅ {alteracoes} atribuições transferidas para Marcão")
            break
    
    # 3. Atualizar carga_horaria de Andréia (remover turmas de Marcão)
    carga_andreia = 0
    for disc in dados['disciplinas']:
        if disc['nome'] == 'Educação Física':
            for turma, prof in disc['professor_por_turma'].items():
                if prof == 'Andréia':
                    carga_andreia += disc['carga_por_turma'].get(turma, 0)
    
    for prof in dados['professores']:
        if prof['nome'] == 'Andréia':
            carga_antiga = prof['carga_horaria']
            prof['carga_horaria'] = carga_andreia
            print(f"\n✅ Carga de Andréia: {carga_antiga}h → {carga_andreia}h")
            break
    
    # 4. Salvar
    with open('escola_database.json', 'w', encoding='utf-8') as f:
        json.dump(dados, f, indent=2, ensure_ascii=False)
    
    print(f"\n✅ Banco atualizado com sucesso!")
    
    # 5. Validar
    print(f"\n=== VALIDAÇÃO ===")
    total_ed_fisica = 0
    for disc in dados['disciplinas']:
        if disc['nome'] == 'Educação Física':
            for turma, carga in disc['carga_por_turma'].items():
                prof = disc['professor_por_turma'].get(turma, 'SEM PROFESSOR')
                total_ed_fisica += carga
                if turma in atribuicoes_marcao:
                    status = "✅" if prof == 'Marcão' else "❌"
                    print(f"{status} {turma}: {prof} ({carga}h)")
    
    print(f"\nTotal Educação Física: {total_ed_fisica}h")
    print(f"  Marcão: {total_carga_marcao}h")
    print(f"  Andréia: {carga_andreia}h")
    print(f"  Soma: {total_carga_marcao + carga_andreia}h")

if __name__ == '__main__':
    corrigir_marcao()
