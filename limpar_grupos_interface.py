#!/usr/bin/env python3
"""
Remove TODAS as referências a grupos da interface do app.py
"""

with open('app.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

new_lines = []
skip_next = 0

for i, line in enumerate(lines):
    if skip_next > 0:
        skip_next -= 1
        continue
    
    # Remover linhas com filtro de grupo
    if 'grupo_filtro = st.selectbox("Filtrar por Grupo"' in line:
        print(f"Removendo linha {i+1}: filtro de grupo")
        continue
    
    # Remover linhas com seleção de grupo em formulários
    if 'grupo = st.selectbox("Grupo*"' in line:
        print(f"Removendo linha {i+1}: seleção de grupo")
        continue
    
    # Remover linhas que usam grupo_filtro para filtrar
    if 'if grupo_filtro != "Todos":' in line:
        print(f"Removendo linha {i+1}: if grupo_filtro")
        # Pular também a próxima linha (a lista filtrada)
        skip_next = 1
        continue
    
    # Remover else que segue o if grupo_filtro
    if i > 0 and 'else:' in line and 'if grupo_filtro' in lines[i-2]:
        print(f"Removendo linha {i+1}: else de grupo_filtro")
        skip_next = 1  # Pular a próxima linha também
        continue
    
    # Remover parâmetro grupo= em criações de objetos
    if ', grupo,' in line or ', grupo)' in line:
        line = line.replace(', grupo,', ',')
        line = line.replace(', grupo)', ')')
        print(f"Removendo parâmetro grupo da linha {i+1}")
    
    # Remover exibição de grupo em expanders
    if '[obter_grupo_seguro(' in line:
        line = line.replace(' [{obter_grupo_seguro(disc)}]', '')
        line = line.replace(' [{obter_grupo_seguro(prof)}]', '')
        line = line.replace(' [{obter_grupo_seguro(turma)}]', '')
        line = line.replace(' [{obter_grupo_seguro(t)}]', '')
        print(f"Removendo exibição de grupo da linha {i+1}")
    
    # Remover linhas que definem grupo_filtro_prof
    if 'grupo_filtro_prof = grupo' in line:
        print(f"Removendo linha {i+1}: grupo_filtro_prof")
        continue
    
    # Remover verificações de grupo de professor
    if 'prof_grupo = obter_grupo_seguro(prof)' in line:
        print(f"Removendo linha {i+1}: prof_grupo")
        continue
    
    if 'if prof_grupo in [' in line:
        print(f"Removendo linha {i+1}: verificação prof_grupo")
        continue
    
    new_lines.append(line)

with open('app.py', 'w', encoding='utf-8') as f:
    f.writelines(new_lines)

print(f"\n✅ {len(lines) - len(new_lines)} linhas removidas")
print(f"Arquivo final: {len(new_lines)} linhas")
