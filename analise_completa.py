import json
from collections import defaultdict

# Carregar banco
with open('escola_database.json', encoding='utf-8') as f:
    data = json.load(f)

print("=" * 80)
print("ANÁLISE DETALHADA: 1emB e 2emB")
print("=" * 80)

for turma_alvo in ['1emB', '2emB', '1emA', '3emB']:
    print(f"\n{'='*80}")
    print(f"📚 TURMA: {turma_alvo}")
    print('='*80)
    
    disciplinas_turma = []
    total = 0
    
    for disc in data['disciplinas']:
        if turma_alvo in disc.get('turmas', []):
            # Verificar carga específica ou usar padrão
            carga_por_turma = disc.get('carga_por_turma', {})
            if carga_por_turma and turma_alvo in carga_por_turma:
                carga = carga_por_turma[turma_alvo]
            else:
                carga = disc.get('carga_semanal', 0)
            
            disciplinas_turma.append({
                'nome': disc['nome'],
                'carga': carga
            })
            total += carga
    
    # Ordenar por carga (decrescente)
    disciplinas_turma.sort(key=lambda x: x['carga'], reverse=True)
    
    print(f"\nDisciplinas ({len(disciplinas_turma)}):\n")
    for disc in disciplinas_turma:
        print(f"  {disc['carga']}h - {disc['nome']}")
    
    limite = 35
    print(f"\n{'─'*80}")
    print(f"TOTAL: {total}h / {limite}h", end="")
    
    diferenca = total - limite
    if diferenca > 0:
        print(f" ❌ EXCESSO: +{diferenca}h")
        print(f"\n💡 SUGESTÃO: Remover {diferenca}h")
    elif diferenca < 0:
        print(f" ⚠️  FALTA: {abs(diferenca)}h")
        print(f"\n💡 SUGESTÃO: Adicionar {abs(diferenca)}h")
    else:
        print(f" ✅ PERFEITO!")

print("\n" + "=" * 80)
print("COMPARAÇÃO: O QUE MUDAR PARA IGUALAR 1emB/2emB com 1emA/3emB")
print("=" * 80)

# Comparar disciplinas
disciplinas_1emA = {}
disciplinas_1emB = {}
disciplinas_2emB = {}
disciplinas_3emB = {}

for disc in data['disciplinas']:
    nome = disc['nome']
    carga_por_turma = disc.get('carga_por_turma', {})
    carga_semanal = disc.get('carga_semanal', 0)
    
    if '1emA' in disc.get('turmas', []):
        carga = carga_por_turma.get('1emA', carga_semanal)
        disciplinas_1emA[nome] = carga
    
    if '1emB' in disc.get('turmas', []):
        carga = carga_por_turma.get('1emB', carga_semanal)
        disciplinas_1emB[nome] = carga
    
    if '2emB' in disc.get('turmas', []):
        carga = carga_por_turma.get('2emB', carga_semanal)
        disciplinas_2emB[nome] = carga
    
    if '3emB' in disc.get('turmas', []):
        carga = carga_por_turma.get('3emB', carga_semanal)
        disciplinas_3emB[nome] = carga

print("\n🔍 Diferenças entre 1emA (34h ✅) e 1emB (37h ❌):\n")
todas_disciplinas = set(disciplinas_1emA.keys()) | set(disciplinas_1emB.keys())
diferencas = []

for disc in sorted(todas_disciplinas):
    carga_A = disciplinas_1emA.get(disc, 0)
    carga_B = disciplinas_1emB.get(disc, 0)
    if carga_A != carga_B:
        dif = carga_B - carga_A
        diferencas.append((disc, carga_A, carga_B, dif))
        print(f"  • {disc}: 1emA={carga_A}h vs 1emB={carga_B}h ({dif:+d}h)")

if not diferencas:
    print("  ✅ Nenhuma diferença encontrada")

print("\n🔍 Diferenças entre 1emA (34h ✅) e 2emB (37h ❌):\n")
todas_disciplinas = set(disciplinas_1emA.keys()) | set(disciplinas_2emB.keys())
diferencas = []

for disc in sorted(todas_disciplinas):
    carga_A = disciplinas_1emA.get(disc, 0)
    carga_B = disciplinas_2emB.get(disc, 0)
    if carga_A != carga_B:
        dif = carga_B - carga_A
        diferencas.append((disc, carga_A, carga_B, dif))
        print(f"  • {disc}: 1emA={carga_A}h vs 2emB={carga_B}h ({dif:+d}h)")

if not diferencas:
    print("  ✅ Nenhuma diferença encontrada")

print("\n" + "=" * 80)
print("✂️  OPÇÕES DE CORTE PARA 1emB e 2emB (remover 2h):")
print("=" * 80)

print("\nOpção 1 - Cortar 2h de UMA disciplina:")
for disc in disciplinas_1emB:
    if disciplinas_1emB[disc] >= 3:
        print(f"  • {disc}: {disciplinas_1emB[disc]}h → {disciplinas_1emB[disc]-2}h")

print("\nOpção 2 - Cortar 1h de DUAS disciplinas:")
for disc in disciplinas_1emB:
    if disciplinas_1emB[disc] >= 2:
        print(f"  • {disc}: {disciplinas_1emB[disc]}h → {disciplinas_1emB[disc]-1}h")
