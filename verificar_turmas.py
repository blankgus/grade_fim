import json

# Carregar dados
with open('escola_database.json', encoding='utf-8') as f:
    data = json.load(f)

print("=== DISCIPLINAS PARA 1emA E 3emB ===\n")

# Verificar 1emA
print("🎯 TURMA: 1emA")
total_1emA = 0
for disc in data['disciplinas']:
    if '1emA' in disc.get('turmas', []):
        carga = disc.get('carga_por_turma', {}).get('1emA', disc.get('carga_semanal', 0))
        total_1emA += carga
        prof = disc.get('professor_por_turma', {}).get('1emA', 'Não atribuído')
        print(f"  • {disc['nome']}: {carga}h (Prof: {prof})")

print(f"\n  TOTAL: {total_1emA}h / 35h máximo")
print(f"  STATUS: {'✅ OK' if total_1emA <= 35 else f'❌ EXCESSO de {total_1emA - 35}h'}\n")

# Verificar 3emB
print("🎯 TURMA: 3emB")
total_3emB = 0
for disc in data['disciplinas']:
    if '3emB' in disc.get('turmas', []):
        carga = disc.get('carga_por_turma', {}).get('3emB', disc.get('carga_semanal', 0))
        total_3emB += carga
        prof = disc.get('professor_por_turma', {}).get('3emB', 'Não atribuído')
        print(f"  • {disc['nome']}: {carga}h (Prof: {prof})")

print(f"\n  TOTAL: {total_3emB}h / 35h máximo")
print(f"  STATUS: {'✅ OK' if total_3emB <= 35 else f'❌ EXCESSO de {total_3emB - 35}h'}")
