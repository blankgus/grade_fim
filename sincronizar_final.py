#!/usr/bin/env python3
"""
SINCRONIZAÇÃO TOTAL: Limpa e reconstrói o banco a partir do PDF
Remove TUDO e recria exatamente como está no PDF
"""

import json
from datetime import datetime
import shutil
from collections import defaultdict

print("=" * 120)
print("🔄 SINCRONIZAÇÃO TOTAL: PDF → BANCO")
print("=" * 120)
print()

# Carregar PDF
try:
    with open('atribuicoes_extraidas_corrigidas.json', 'r', encoding='utf-8') as f:
        pdf_data = json.load(f)
except:
    print("❌ Arquivo atribuicoes_extraidas_corrigidas.json não encontrado")
    exit(1)

# Carregar banco
with open('escola_database.json', 'r', encoding='utf-8') as f:
    banco = json.load(f)

# Backup
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
backup_file = f'escola_database_backup_{timestamp}.json'
shutil.copy('escola_database.json', backup_file)
print(f"✅ Backup: {backup_file}\n")

# Manter apenas turmas da grade (6ano-9ano e 1em-3em)
turmas_validas = [t for t in banco['turmas'] if any(x in t['nome'] for x in ['6ano', '7ano', '8ano', '9ano', '1em', '2em', '3em'])]
print(f"📚 Turmas válidas: {len(turmas_validas)}")
for t in turmas_validas:
    print(f"   • {t['nome']}")
print()

# Extrair dados do PDF
# Agrupar por disciplina
disciplinas_pdf = defaultdict(lambda: {
    'turmas': set(),
    'carga_por_turma': {},
    'turmas_cargas': []
})

for atrib in pdf_data:
    turma = atrib['turma']
    disciplina = atrib['disciplina']
    carga = atrib['carga']
    
    # Filtrar apenas turmas válidas
    if turma not in [t['nome'] for t in turmas_validas]:
        continue
    
    disciplinas_pdf[disciplina]['turmas'].add(turma)
    disciplinas_pdf[disciplina]['carga_por_turma'][turma] = carga
    disciplinas_pdf[disciplina]['turmas_cargas'].append((turma, carga))

print(f"📋 Disciplinas no PDF: {len(disciplinas_pdf)}")
print()

# Mapear nomes de disciplinas do PDF para o banco
# Para manter as cores e configurações existentes
mapeamento_nomes = {
    'Ed. Financeira': 'Educação Financeira',
    'Práticas Historiográficas': 'Práticas Historiográficas',  # Manter nome do PDF
    'Redação': 'Redação',  # Nova disciplina
    'Oralidade': 'Oralidade',  # Sem "(Eletiva)"
    'Tecnologia e Saúde': 'Tecnologia e Saúde',
    'Fenômenos Biológicos': 'Fenômenos Biológicos',
}

# Buscar disciplinas antigas para manter IDs e cores
disciplinas_antigas = {d['nome']: d for d in banco.get('disciplinas', [])}

# Criar novas disciplinas
novas_disciplinas = []

for nome_pdf, dados in sorted(disciplinas_pdf.items()):
    # Nome normalizado
    nome_final = mapeamento_nomes.get(nome_pdf, nome_pdf)
    
    # Buscar disciplina antiga
    disc_antiga = disciplinas_antigas.get(nome_final) or disciplinas_antigas.get(nome_pdf)
    
    # Criar nova disciplina
    nova_disc = {
        'nome': nome_final,
        'carga_semanal': max(dados['carga_por_turma'].values()) if dados['carga_por_turma'] else 1,
        'tipo': disc_antiga.get('tipo', 'media') if disc_antiga else 'media',
        'turmas': sorted(list(dados['turmas'])),
        'carga_por_turma': dados['carga_por_turma'],
        'professor_por_turma': {},  # Será preenchido depois
        'cor_fundo': disc_antiga.get('cor_fundo', '#4A90E2') if disc_antiga else '#4A90E2',
        'cor_fonte': disc_antiga.get('cor_fonte', '#FFFFFF') if disc_antiga else '#FFFFFF',
        'id': disc_antiga.get('id') if disc_antiga else None
    }
    
    # Remover id None
    if nova_disc['id'] is None:
        del nova_disc['id']
    
    novas_disciplinas.append(nova_disc)

print(f"✅ {len(novas_disciplinas)} disciplinas criadas\n")

# Agora, atribuir professores do PDF para as disciplinas
# Para isso, precisamos extrair do PDF quem dá cada disciplina em cada turma

# Mapear professor -> turmas/disciplinas do PDF original
print("=" * 120)
print("🔍 Extraindo professores do PDF (manual)")
print("=" * 120)
print()
print("⚠️ O PDF não tem o nome do professor em cada atribuição!")
print("   É necessário extrair manualmente das 'caixas' de cada professor no PDF.")
print()
print("Opções:")
print("1. Popular com professores existentes no banco (manter atribuições atuais)")
print("2. Deixar sem professores (atribuir manualmente depois)")
print()

# OPÇÃO 1: Manter atribuições de professores do banco antigo
print("Escolhendo OPÇÃO 1: Manter atribuições existentes\n")

for nova_disc in novas_disciplinas:
    nome = nova_disc['nome']
    
    # Buscar disciplina antiga
    disc_antiga = disciplinas_antigas.get(nome)
    
    if disc_antiga:
        # Copiar professores que ainda fazem sentido
        prof_antiga = disc_antiga.get('professor_por_turma', {})
        
        # Filtrar apenas turmas que existem na nova disciplina
        prof_nova = {}
        for turma in nova_disc['turmas']:
            if turma in prof_antiga:
                prof_nova[turma] = prof_antiga[turma]
        
        nova_disc['professor_por_turma'] = prof_nova
        
        if prof_nova:
            print(f"✅ {nome}: {len(prof_nova)} professores mantidos")

print()

# Substituir disciplinas no banco
banco['turmas'] = turmas_validas
banco['disciplinas'] = novas_disciplinas

# Salvar
with open('escola_database.json', 'w', encoding='utf-8') as f:
    json.dump(banco, f, indent=2, ensure_ascii=False)

print()
print("=" * 120)
print("✅ SINCRONIZAÇÃO CONCLUÍDA")
print("=" * 120)
print(f"  Turmas: {len(turmas_validas)}")
print(f"  Disciplinas: {len(novas_disciplinas)}")
print(f"  Backup: {backup_file}")
print()
print("⚠️ IMPORTANTE:")
print("   As atribuições de professores foram mantidas do banco antigo.")
print("   Verifique no Streamlit se todos os professores estão corretos.")
print()
