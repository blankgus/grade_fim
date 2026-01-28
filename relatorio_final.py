#!/usr/bin/env python3
"""
RELATÓRIO FINAL: Análise completa da sincronização
"""

import json
from collections import defaultdict

with open('escola_database.json', 'r', encoding='utf-8') as f:
    banco = json.load(f)

print("=" * 120)
print("📊 RELATÓRIO FINAL: Sincronização PDF → Banco")
print("=" * 120)
print()

# Calcular cargas
cargas = defaultdict(int)
for disc in banco['disciplinas']:
    for turma, carga in disc.get('carga_por_turma', {}).items():
        cargas[turma] += carga

# Turmas
turmas_em = ['1emA', '1emB', '2emA', '2emB', '3emA', '3emB']
turmas_ef = ['6anoA', '6anoB', '7anoA', '7anoB', '8anoA', '8anoB', '9anoA', '9anoB']

LIMITE_EM = 35
LIMITE_EF = 25

print("📚 TURMAS - CARGA HORÁRIA:")
print()

print("Ensino Médio:")
for turma in turmas_em:
    carga = cargas.get(turma, 0)
    diferenca = carga - LIMITE_EM
    
    if diferenca == 0:
        status = "✅"
    elif diferenca > 0:
        status = f"❌ +{diferenca}h"
    else:
        status = f"⚠️ -{abs(diferenca)}h"
    
    print(f"  {turma:10s} | {carga:2d}h / {LIMITE_EM}h | {status}")

print()
print("Ensino Fundamental II:")
for turma in turmas_ef:
    carga = cargas.get(turma, 0)
    diferenca = carga - LIMITE_EF
    
    if diferenca == 0:
        status = "✅"
    elif diferenca > 0:
        status = f"❌ +{diferenca}h"
    else:
        status = f"⚠️ -{abs(diferenca)}h"
    
    print(f"  {turma:10s} | {carga:2d}h / {LIMITE_EF}h | {status}")

print()
print()
print("=" * 120)
print("🔍 ANÁLISE DAS TURMAS COM EXCESSO (1emB e 2emB)")
print("=" * 120)
print()

print("Conforme o PDF grade2026.pdf, essas turmas têm DISCIPLINAS ELETIVAS SIMULTÂNEAS:")
print()
print("1. Educação Financeira (Ricardo, 2h) ⟷ Mercado de Trabalho (Waldemar, 2h)")
print("   → Alunos escolhem UMA das duas")
print("   → Acontecem no MESMO horário")
print()
print("2. Oralidade (Heliana, 1h) ⟷ Análises Químicas (Vlad, 1h)")
print("   → Alunos escolhem UMA das duas")
print("   → Acontecem no MESMO horário")
print()
print("3. Práticas experimentais (Vlad, 2h) ⟷ Análises Historiográficas (Waldemar, 2h)")
print("   → Alunos escolhem UMA das duas")
print("   → Acontecem no MESMO horário")
print()
print("TOTAL de pares eletivos: 3 pares x 2 turmas = 6 conflitos de horário")
print()
print("=" * 120)
print("💡 INTERPRETAÇÃO CORRETA:")
print("=" * 120)
print()
print("O PDF lista TODAS as disciplinas (incluindo as eletivas), mas indica que algumas")
print("devem ter 'horário batendo'. Isso significa:")
print()
print("  ❌ NÃO É um erro de carga horária")
print("  ✅ É uma RESTRIÇÃO para o gerador de grades")
print()
print("As turmas 1emB e 2emB TÊM 40h de disciplinas cadastradas, mas apenas 35h acontecem")
print("por semana porque 5h são de eletivas simultâneas (alunos escolhem).")
print()
print("=" * 120)
print("🎯 SOLUÇÃO:")
print("=" * 120)
print()
print("Há 2 abordagens possíveis:")
print()
print("OPÇÃO 1 - SIMPLIFICAR (Recomendada):")
print("  → Manter apenas UMA disciplina de cada par eletivo")
print("  → Remove: Mercado de Trabalho, Análises Químicas, Análises Historiográficas de 1emB e 2emB")
print("  → Resultado: 35h exatas")
print("  → Vantagem: Grade simples, sem conflitos")
print()
print("OPÇÃO 2 - MANTER ELETIVAS:")
print("  → Manter todas as disciplinas")
print("  → Marcar como 'eletivas' no sistema")
print("  → Gerador de grades deve alocar no mesmo horário")
print("  → Resultado: 40h cadastradas, 35h na grade")
print("  → Vantagem: Reflete a realidade das eletivas")
print("  → Desvantagem: Sistema mais complexo")
print()
print("=" * 120)

# Salvar relatório
with open('RELATORIO_FINAL_SINCRONIZACAO.md', 'w', encoding='utf-8') as f:
    f.write("# Relatório Final - Sincronização PDF → Banco\n\n")
    f.write("## Resumo\n\n")
    f.write(f"- **Turmas**: {len(turmas_em) + len(turmas_ef)}\n")
    f.write(f"- **Disciplinas**: {len(banco['disciplinas'])}\n")
    f.write(f"- **Professores**: {len(banco['professores'])}\n\n")
    f.write("## Turmas com Carga Correta\n\n")
    
    corretas = [t for t in turmas_em + turmas_ef if cargas.get(t, 0) == (LIMITE_EM if t in turmas_em else LIMITE_EF)]
    f.write(f"**{len(corretas)}/{len(turmas_em) + len(turmas_ef)} turmas com carga perfeita:**\n\n")
    for t in corretas:
        f.write(f"- {t}\n")
    
    f.write("\n## Turmas com Problemas\n\n")
    
    problemas = [t for t in turmas_em + turmas_ef if cargas.get(t, 0) != (LIMITE_EM if t in turmas_em else LIMITE_EF)]
    for t in problemas:
        carga = cargas.get(t, 0)
        limite = LIMITE_EM if t in turmas_em else LIMITE_EF
        diferenca = carga - limite
        f.write(f"### {t}\n\n")
        f.write(f"- Carga atual: {carga}h\n")
        f.write(f"- Limite: {limite}h\n")
        f.write(f"- Diferença: {diferenca:+d}h\n\n")
    
    f.write("\n## Conclusão\n\n")
    f.write("As turmas 1emB e 2emB têm 5h a mais devido a disciplinas eletivas simultâneas.\n")
    f.write("Isso está CORRETO conforme o PDF, que indica que esses horários devem 'bater'.\n\n")
    f.write("**Próximo passo**: Decidir se simplifica (remove eletivas) ou mantém (implementa suporte a eletivas).\n")

print("✅ Relatório salvo em: RELATORIO_FINAL_SINCRONIZACAO.md")
print()
