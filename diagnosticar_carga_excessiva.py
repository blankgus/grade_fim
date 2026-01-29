import json
from collections import defaultdict

with open('escola_database.json', encoding='utf-8') as f:
    data = json.load(f)

print("=" * 80)
print("DIAGNÓSTICO: CARGA EXCESSIVA NAS TURMAS")
print("=" * 80)

# Analisar carga por turma
carga_por_turma = defaultdict(int)
detalhes_por_turma = defaultdict(list)

for disc in data['disciplinas']:
    nome_disc = disc['nome']
    turmas = disc.get('turmas', [])
    carga_semanal = disc.get('carga_semanal', 0)
    carga_por_turma_dict = disc.get('carga_por_turma', {})
    
    for turma in turmas:
        # Priorizar carga específica, senão usar carga_semanal
        if carga_por_turma_dict and turma in carga_por_turma_dict:
            carga = carga_por_turma_dict[turma]
        else:
            carga = carga_semanal
        
        carga_por_turma[turma] += carga
        detalhes_por_turma[turma].append(f"{nome_disc}: {carga}h")

# Definir limites
limites = {
    '6anoA': 25, '7anoA': 25, '8anoA': 25, '9anoA': 25,
    '6anoB': 25, '7anoB': 25, '8anoB': 25, '9anoB': 25,
    '1emA': 35, '2emA': 35, '3emA': 35,
    '1emB': 35, '2emB': 35, '3emB': 35
}

print("\n📊 ANÁLISE DE CARGA POR TURMA:\n")

for turma in sorted(limites.keys()):
    limite = limites[turma]
    carga = carga_por_turma[turma]
    status = "✅" if carga <= limite else "❌"
    diferenca = carga - limite
    
    print(f"{status} {turma}: {carga}h / {limite}h", end="")
    if diferenca > 0:
        print(f" (EXCESSO: +{diferenca}h)")
    else:
        print()
    
    # Mostrar detalhes se houver excesso
    if diferenca > 0:
        print(f"   Disciplinas ({len(detalhes_por_turma[turma])}):")
        for detalhe in sorted(detalhes_por_turma[turma]):
            print(f"     • {detalhe}")
        print()

# Análise de disciplinas com carga duplicada
print("\n" + "=" * 80)
print("POSSÍVEIS PROBLEMAS:")
print("=" * 80)

problemas_encontrados = []

for disc in data['disciplinas']:
    nome_disc = disc['nome']
    turmas = disc.get('turmas', [])
    carga_semanal = disc.get('carga_semanal', 0)
    carga_por_turma_dict = disc.get('carga_por_turma', {})
    
    # Verificar se tem carga_por_turma mas não para todas as turmas
    if carga_por_turma_dict:
        turmas_sem_carga_especifica = [t for t in turmas if t not in carga_por_turma_dict]
        if turmas_sem_carga_especifica:
            problemas_encontrados.append({
                'tipo': 'CARGA_MISTA',
                'disciplina': nome_disc,
                'turmas': turmas,
                'turmas_sem_especifica': turmas_sem_carga_especifica,
                'carga_semanal': carga_semanal,
                'carga_por_turma': carga_por_turma_dict
            })

if problemas_encontrados:
    print("\n⚠️ DISCIPLINAS COM CONFIGURAÇÃO MISTA:")
    print("(Algumas turmas usam carga_semanal, outras usam carga_por_turma)\n")
    
    for prob in problemas_encontrados:
        print(f"📖 {prob['disciplina']}")
        print(f"   Turmas: {', '.join(prob['turmas'])}")
        print(f"   carga_semanal (padrão): {prob['carga_semanal']}h")
        print(f"   carga_por_turma: {prob['carga_por_turma']}")
        print(f"   ❌ Turmas SEM carga específica (usarão {prob['carga_semanal']}h):")
        for turma in prob['turmas_sem_especifica']:
            print(f"      • {turma}")
        print()
else:
    print("\n✅ Nenhum problema de configuração mista encontrado")

# Resumo total
print("\n" + "=" * 80)
print("RESUMO:")
print("=" * 80)
total_disciplinas = len(data['disciplinas'])
disciplinas_com_carga_por_turma = sum(1 for d in data['disciplinas'] if d.get('carga_por_turma'))

print(f"Total de disciplinas: {total_disciplinas}")
print(f"Disciplinas com carga_por_turma: {disciplinas_com_carga_por_turma}")
print(f"Turmas com excesso: {sum(1 for t, c in carga_por_turma.items() if c > limites.get(t, 35))}")
