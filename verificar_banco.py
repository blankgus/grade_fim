import json

with open('escola_database.json', encoding='utf-8') as f:
    data = json.load(f)

if data['disciplinas']:
    disc = data['disciplinas'][0]
    print('Primeira disciplina:')
    print(f"  Nome: {disc.get('nome', 'N/A')}")
    print(f"  Tem carga_por_turma: {'carga_por_turma' in disc}")
    print(f"  Tem professor_por_turma: {'professor_por_turma' in disc}")
    print(f"  Turmas: {len(disc.get('turmas', []))}")
    
    if 'carga_por_turma' in disc:
        print(f"  carga_por_turma: {disc['carga_por_turma']}")
    if 'professor_por_turma' in disc:
        print(f"  professor_por_turma: {disc['professor_por_turma']}")

print(f"\nTotal disciplinas: {len(data['disciplinas'])}")
print(f"Total professores: {len(data['professores'])}")
print(f"Total turmas: {len(data['turmas'])}")
