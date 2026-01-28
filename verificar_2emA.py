import json

with open('professores_atribuicoes_pdf.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

atrib_2emA = []
for prof, atribs in data.items():
    for a in atribs:
        if a['turma'] == '2emA':
            atrib_2emA.append((prof, a))

print('2emA no PDF (por professor):\n')
for prof, a in sorted(atrib_2emA, key=lambda x: x[1]['disciplina']):
    print(f'{prof:15s} | {a["disciplina"]:30s} | {a["carga"]}h')

print(f'\nTOTAL: {sum([a["carga"] for _, a in atrib_2emA])}h')
