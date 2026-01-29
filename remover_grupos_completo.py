#!/usr/bin/env python3
"""
Remove todas as referências a 'grupo' do app.py.

O sistema não usa mais grupos A/B para disciplinas.
Todas as disciplinas são únicas.
"""

import re

# Ler app.py
with open('app.py', 'r', encoding='utf-8') as f:
    conteudo = f.read()

print("=== REMOVENDO REFERÊNCIAS A GRUPOS ===\n")

# 1. Remover função obter_grupo_seguro
print("1. Removendo função obter_grupo_seguro...")
conteudo = re.sub(
    r'def obter_grupo_seguro\(.*?\):\s*""".*?"""\s*try:.*?except:.*?return "A"\s*\n',
    '',
    conteudo,
    flags=re.DOTALL
)

# 2. Simplificar obter_professores_para_disciplina
print("2. Simplificando obter_professores_para_disciplina...")
conteudo = re.sub(
    r'def obter_professores_para_disciplina\(disciplina_nome, grupo=None\):',
    'def obter_professores_para_disciplina(disciplina_nome):',
    conteudo
)

# Remover verificação de grupo dentro da função
conteudo = re.sub(
    r'(\s+)for professor in st\.session_state\.professores:\s+if disciplina_nome in professor\.disciplinas:\s+# Verificar se o grupo do professor é compatível\s+if grupo:.*?else:\s+professores_disponiveis\.append\(professor\)',
    r'\1for professor in st.session_state.professores:\n\1    if disciplina_nome in professor.disciplinas:\n\1        professores_disponiveis.append(professor)',
    conteudo,
    flags=re.DOTALL
)

# 3. Remover função verificar_professor_comprometido
print("3. Removendo função verificar_professor_comprometido...")
conteudo = re.sub(
    r'def verificar_professor_comprometido\(professor, disciplina_nome, grupo\):.*?return False\s*\n',
    '',
    conteudo,
    flags=re.DOTALL
)

# 4. Remover referências a turma.grupo
print("4. Removendo referências a turma.grupo...")
conteudo = re.sub(r'grupo_turma = turma\.grupo', "# grupo removido", conteudo)
conteudo = re.sub(r'turma_obj\.grupo if turma_obj else [\'"]A[\'"]', '"NENHUM"', conteudo)

# 5. Remover verificações de grupo em disciplinas
print("5. Removendo verificações obter_grupo_seguro(disc)...")
conteudo = re.sub(r' and obter_grupo_seguro\(disc\) == grupo_turma', '', conteudo)
conteudo = re.sub(r'obter_grupo_seguro\(disc\)', '"NENHUM"', conteudo)

# 6. Remover parâmetros grupo em chamadas de função
print("6. Removendo parâmetros grupo em chamadas...")
conteudo = re.sub(r'obter_professores_para_disciplina\(([^,]+), grupo_turma\)', r'obter_professores_para_disciplina(\1)', conteudo)
conteudo = re.sub(r'verificar_professor_comprometido\(([^,]+), ([^,]+), grupo_turma\)', r'# verificar_professor_comprometido removido', conteudo)

# 7. Remover 'grupo' de dicionários
print("7. Removendo chave 'grupo' de dicionários...")
conteudo = re.sub(r",\s*['\"]grupo['\"]:\s*grupo_turma", '', conteudo)
conteudo = re.sub(r"['\"]grupo['\"]:\s*grupo_turma,?", '', conteudo)

# 8. Remover _calcular_prioridade com grupo
print("8. Simplificando _calcular_prioridade...")
conteudo = re.sub(
    r'def _calcular_prioridade\(self, disciplina, grupo\):',
    'def _calcular_prioridade(self, disciplina):',
    conteudo
)
conteudo = re.sub(r'if prof\.grupo in \[grupo, "AMBOS"\]:', 'if True:  # grupo removido', conteudo)
conteudo = re.sub(r"['\"]prioridade['\"]:\s*self\._calcular_prioridade\(disc\.nome, grupo_turma\)", r"'prioridade': self._calcular_prioridade(disc.nome)", conteudo)

# Salvar
with open('app.py', 'w', encoding='utf-8') as f:
    f.write(conteudo)

print("\n✅ Todas as referências a grupos foram removidas de app.py")
print("\nVerificando se ainda há referências...")

# Contar referências restantes
import subprocess
try:
    result = subprocess.run(['grep', '-c', 'grupo', 'app.py'], capture_output=True, text=True)
    count = result.stdout.strip()
    if count and count != '0':
        print(f"⚠️  Ainda há {count} referências a 'grupo' no arquivo")
    else:
        print("✅ Nenhuma referência a 'grupo' encontrada!")
except:
    # grep não disponível no Windows, usar Python
    with open('app.py', 'r', encoding='utf-8') as f:
        lines = f.readlines()
    count = sum(1 for line in lines if 'grupo' in line.lower() and not line.strip().startswith('#'))
    if count > 0:
        print(f"⚠️  Ainda há {count} linhas com 'grupo'")
        print("\nLinhas encontradas:")
        for i, line in enumerate(lines, 1):
            if 'grupo' in line.lower() and not line.strip().startswith('#'):
                print(f"  Linha {i}: {line.strip()}")
    else:
        print("✅ Nenhuma referência ativa a 'grupo' encontrada!")
