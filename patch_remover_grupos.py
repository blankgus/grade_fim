#!/usr/bin/env python3
"""
Patch simples: Remover APENAS as funcionalidades de grupo que causam erro.
Manter o resto do código funcionando.
"""

# Ler arquivo
with open('app.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

print("=== APLICANDO PATCH PARA REMOVER GRUPOS ===\n")

# Lista de modificações
modificacoes = 0

# Nova lista de linhas
new_lines = []

skip_until = 0
for i, line in enumerate(lines):
    # Se estamos pulando linhas, verificar se já passou
    if i < skip_until:
        continue
    
    # 1. Remover função obter_grupo_seguro completa
    if 'def obter_grupo_seguro' in line:
        print(f"Removendo função obter_grupo_seguro (linha {i+1})")
        # Pular até o próximo 'def' ou linha não indentada
        j = i + 1
        while j < len(lines) and (lines[j].startswith('    ') or lines[j].strip() == ''):
            j += 1
        skip_until = j
        modificacoes += 1
        continue
    
    # 2. Remover função verificar_professor_comprometido
    if 'def verificar_professor_comprometido' in line:
        print(f"Removendo função verificar_professor_comprometido (linha {i+1})")
        j = i + 1
        while j < len(lines) and (lines[j].startswith('    ') or lines[j].strip() == ''):
            j += 1
        skip_until = j
        modificacoes += 1
        continue
    
    # 3. Substituir obter_grupo_seguro por valor padrão
    if 'obter_grupo_seguro(' in line:
        original = line
        line = line.replace('obter_grupo_seguro(turma)', '"A"')
        line = line.replace('obter_grupo_seguro(disc)', '"A"')
        line = line.replace('obter_grupo_seguro(prof)', '"A"')
        line = line.replace('obter_grupo_seguro(t)', '"A"')
        line = line.replace('obter_grupo_seguro(p)', '"A"')
        line = line.replace('obter_grupo_seguro(d)', '"A"')
        line = line.replace('obter_grupo_seguro(turma_obj)', '"A"')
        if line != original:
            modificacoes += 1
    
    # 4. Remover linhas com turma.grupo, turma_obj.grupo, disc.grupo
    if '.grupo' in line and '=' in line:
        if 'grupo_turma =' in line or 'novo_grupo =' in line or 'grupo_disc =' in line:
            # Comentar linha
            line = '    # ' + line.lstrip() + '  # grupo removido\n'
            modificacoes += 1
        elif 'turma.grupo =' in line or 'prof.grupo =' in line or 'disc.grupo =' in line:
            line = '    # ' + line.lstrip() + '  # grupo removido\n'
            modificacoes += 1
    
    # 5. Remover parâmetro grupo de chamadas de função
    if 'obter_professores_para_disciplina(' in line and ', grupo' in line:
        line = line.replace(', grupo_turma)', ')')
        line = line.replace(', grupo_disc)', ')')
        line = line.replace(', grupo)', ')')
        modificacoes += 1
    
    # 6. Comentar verificar_professor_comprometido
    if 'verificar_professor_comprometido(' in line:
        line = '    # ' + line.lstrip() + '  # função removida\n'
        modificacoes += 1
    
    # 7. Remover filtros de grupo
    if 'grupo_filtro' in line and ('selectbox' in line or 'Filtrar por Grupo' in line):
        # Comentar linha
        line = '    # ' + line.lstrip() + '  # filtro de grupo removido\n'
        modificacoes += 1
    
    # 8. Remover seleção de grupo em formulários
    if '"Grupo*"' in line or "'Grupo*'" in line:
        # Comentar esta linha e as próximas 2
        line = '    # ' + line.lstrip() + '  # seleção de grupo removida\n'
        modificacoes += 1
    
    # 9. Remover "Grade por Grupo"
    if 'Grade por Grupo' in line:
        continue  # Pular completamente
    
    new_lines.append(line)

# Salvar
with open('app.py', 'w', encoding='utf-8') as f:
    f.writelines(new_lines)

print(f"\n✅ Patch aplicado! {modificacoes} modificações realizadas")
print("\n📝 Backup salvo em: app_backup_antes_remover_grupos.py")
print("\n⚠️  ATENÇÃO: Algumas funções podem precisar de ajustes manuais")
print("   Teste o Streamlit e verifique se há erros")
