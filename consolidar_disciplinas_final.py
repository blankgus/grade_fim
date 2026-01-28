#!/usr/bin/env python3
"""
Consolida disciplinas duplicadas e corrige nomes de professores
"""

import json
from datetime import datetime
import shutil
from collections import defaultdict

def consolidar_disciplinas():
    """Consolida disciplinas duplicadas em uma só"""
    
    print("=" * 100)
    print("🔧 CONSOLIDANDO DISCIPLINAS DUPLICADAS")
    print("=" * 100)
    print()
    
    # Carregar banco
    with open('escola_database.json', 'r', encoding='utf-8') as f:
        banco = json.load(f)
    
    # Backup
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_file = f'escola_database_backup_{timestamp}.json'
    shutil.copy('escola_database.json', backup_file)
    print(f"✅ Backup: {backup_file}\n")
    
    disciplinas = banco.get('disciplinas', [])
    
    print(f"📊 ANTES: {len(disciplinas)} disciplinas no banco\n")
    
    # Agrupar disciplinas por nome
    por_nome = defaultdict(list)
    for disc in disciplinas:
        por_nome[disc['nome']].append(disc)
    
    # Consolidar duplicatas
    novas_disciplinas = []
    consolidadas = 0
    
    for nome, discs in por_nome.items():
        if len(discs) == 1:
            # Não é duplicada, manter
            novas_disciplinas.append(discs[0])
        else:
            # Consolidar múltiplas em uma só
            print(f"🔄 Consolidando: {nome} ({len(discs)} registros)")
            
            disc_consolidada = discs[0].copy()
            
            # Unir turmas
            todas_turmas = set()
            for d in discs:
                todas_turmas.update(d.get('turmas', []))
            disc_consolidada['turmas'] = sorted(list(todas_turmas))
            
            # Unir carga_por_turma
            carga_por_turma = {}
            for d in discs:
                carga_por_turma.update(d.get('carga_por_turma', {}))
            disc_consolidada['carga_por_turma'] = carga_por_turma
            
            # Unir professor_por_turma
            professor_por_turma = {}
            for d in discs:
                professor_por_turma.update(d.get('professor_por_turma', {}))
            disc_consolidada['professor_por_turma'] = professor_por_turma
            
            print(f"  ✅ {len(todas_turmas)} turmas consolidadas")
            
            novas_disciplinas.append(disc_consolidada)
            consolidadas += len(discs) - 1
    
    banco['disciplinas'] = novas_disciplinas
    
    print()
    print(f"📊 DEPOIS: {len(novas_disciplinas)} disciplinas")
    print(f"✅ {consolidadas} duplicatas removidas\n")
    
    # Corrigir nomes de professores
    print("=" * 100)
    print("🔧 CORRIGINDO NOMES DE PROFESSORES NAS ATRIBUIÇÕES")
    print("=" * 100)
    print()
    
    mapeamento = {
        'Vladmir': 'Vlad',
        'César': 'Cesar',
        'Maria Luiza': 'Malu'
    }
    
    correcoes = 0
    for disc in banco['disciplinas']:
        prof_por_turma = disc.get('professor_por_turma', {})
        for turma, prof in list(prof_por_turma.items()):
            if prof in mapeamento:
                prof_novo = mapeamento[prof]
                prof_por_turma[turma] = prof_novo
                correcoes += 1
                print(f"  {disc['nome']:30s} | {turma}: {prof} → {prof_novo}")
    
    print()
    print(f"✅ {correcoes} atribuições corrigidas\n")
    
    # Adicionar professores faltantes conforme PDF
    print("=" * 100)
    print("🔧 ADICIONANDO PROFESSORES FALTANTES (conforme PDF)")
    print("=" * 100)
    print()
    
    # Mercado de Trabalho: Waldemar (conforme PDF página 3)
    mercado = next((d for d in banco['disciplinas'] if d['nome'] == 'Mercado de Trabalho'), None)
    if mercado:
        prof_por_turma = mercado.get('professor_por_turma', {})
        adicionados = 0
        for turma in ['1emB', '2emB', '2emA', '3emA', '3emB']:
            if turma not in prof_por_turma or not prof_por_turma[turma]:
                prof_por_turma[turma] = 'Waldemar'
                adicionados += 1
        mercado['professor_por_turma'] = prof_por_turma
        print(f"  ✅ Mercado de Trabalho: {adicionados} turmas atribuídas a Waldemar")
    
    # História EM: Waldemar (conforme PDF)
    historia = next((d for d in banco['disciplinas'] if d['nome'] == 'História'), None)
    if historia:
        prof_por_turma = historia.get('professor_por_turma', {})
        adicionados = 0
        for turma in ['1emA', '2emA', '3emA', '1emB', '2emB', '3emB']:
            if turma not in prof_por_turma or not prof_por_turma[turma]:
                prof_por_turma[turma] = 'Waldemar'
                adicionados += 1
        historia['professor_por_turma'] = prof_por_turma
        print(f"  ✅ História EM: {adicionados} turmas atribuídas a Waldemar")
    
    print()
    
    # Salvar
    with open('escola_database.json', 'w', encoding='utf-8') as f:
        json.dump(banco, f, indent=2, ensure_ascii=False)
    
    print("=" * 100)
    print("✅ CONCLUÍDO")
    print("=" * 100)
    print(f"  Disciplinas: {len(disciplinas)} → {len(novas_disciplinas)}")
    print(f"  Duplicatas removidas: {consolidadas}")
    print(f"  Nomes corrigidos: {correcoes} atribuições")
    print(f"  Professores adicionados: Mercado de Trabalho e História EM")
    print()
    print(f"💾 Salvo em: escola_database.json")
    print(f"📦 Backup: {backup_file}")
    print()

if __name__ == '__main__':
    consolidar_disciplinas()
