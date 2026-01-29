import sys
sys.path.insert(0, '.')

from models import Disciplina
from collections import defaultdict
import json

# Carregar banco
with open('escola_database.json', encoding='utf-8') as f:
    data = json.load(f)

# Converter para objetos
disciplinas = []
for disc_data in data['disciplinas']:
    disc = Disciplina(
        nome=disc_data['nome'],
        carga_semanal=disc_data.get('carga_semanal', 2),
        tipo=disc_data.get('tipo', 'media'),
        turmas=disc_data.get('turmas', []),
        cor_fundo=disc_data.get('cor_fundo', '#4A90E2'),
        cor_fonte=disc_data.get('cor_fonte', '#FFFFFF'),
        carga_por_turma=disc_data.get('carga_por_turma', {}),
        professor_por_turma=disc_data.get('professor_por_turma', {})
    )
    disciplinas.append(disc)

# Calcular carga por turma usando o método correto
carga_por_turma = defaultdict(int)

for disc in disciplinas:
    for turma in disc.turmas:
        carga = disc.obter_carga_turma(turma)
        carga_por_turma[turma] += carga

# Limites
limites = {
    '6anoA': 25, '7anoA': 25, '8anoA': 25, '9anoA': 25,
    '6anoB': 25, '7anoB': 25, '8anoB': 25, '9anoB': 25,
    '1emA': 35, '2emA': 35, '3emA': 35,
    '1emB': 35, '2emB': 35, '3emB': 35
}

print("=" * 60)
print("TESTE DO MÉTODO obter_carga_turma()")
print("=" * 60)
print()

problemas = 0
for turma in sorted(limites.keys()):
    limite = limites[turma]
    carga = carga_por_turma[turma]
    
    if carga > limite:
        status = "❌"
        problemas += 1
    elif carga == limite:
        status = "✅"
    else:
        status = "⚠️ "
    
    diferenca = carga - limite
    print(f"{status} {turma}: {carga}h / {limite}h", end="")
    if diferenca != 0:
        print(f" ({diferenca:+d}h)")
    else:
        print()

print()
print("=" * 60)
if problemas == 0:
    print("✅ TODAS AS TURMAS DENTRO DO LIMITE!")
else:
    print(f"❌ {problemas} turma(s) com excesso de carga")
print("=" * 60)
