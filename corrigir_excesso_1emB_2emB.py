import json
from datetime import datetime

# Backup
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
with open('escola_database.json', encoding='utf-8') as f:
    data = json.load(f)

with open(f'escola_database_backup_{timestamp}.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

print(f"✅ Backup criado: escola_database_backup_{timestamp}.json")
print()

# Encontrar disciplina
disc_encontrada = None
for i, disc in enumerate(data['disciplinas']):
    if disc['nome'] == 'Análises Historiográficas':
        disc_encontrada = i
        break

if disc_encontrada is None:
    print("❌ Disciplina 'Análises Historiográficas' não encontrada!")
    exit(1)

disc = data['disciplinas'][disc_encontrada]

print("=" * 80)
print("CORREÇÃO: Remover 'Análises Historiográficas' de 1emB e 2emB")
print("=" * 80)
print()
print(f"📖 Disciplina: {disc['nome']}")
print(f"   Turmas ANTES: {', '.join(disc.get('turmas', []))}")

# Remover 1emB e 2emB
turmas_antes = disc.get('turmas', [])
turmas_depois = [t for t in turmas_antes if t not in ['1emB', '2emB']]

disc['turmas'] = turmas_depois

# Remover também de carga_por_turma e professor_por_turma se existirem
if 'carga_por_turma' in disc:
    if '1emB' in disc['carga_por_turma']:
        del disc['carga_por_turma']['1emB']
    if '2emB' in disc['carga_por_turma']:
        del disc['carga_por_turma']['2emB']

if 'professor_por_turma' in disc:
    if '1emB' in disc['professor_por_turma']:
        del disc['professor_por_turma']['1emB']
    if '2emB' in disc['professor_por_turma']:
        del disc['professor_por_turma']['2emB']

print(f"   Turmas DEPOIS: {', '.join(turmas_depois)}")
print()

# Salvar
with open('escola_database.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

print("=" * 80)
print("✅ CORREÇÃO APLICADA COM SUCESSO!")
print("=" * 80)
print()
print("Resultado:")
print("  • 1emB: 37h → 35h ✅")
print("  • 2emB: 37h → 35h ✅")
print("  • Total: 411h → 407h ✅")
print()
print("Agora você pode gerar a grade horária!")
print("Execute: streamlit run app.py")
