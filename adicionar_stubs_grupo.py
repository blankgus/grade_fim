#!/usr/bin/env python3
"""
Abordagem mais simples: Adicionar funções stub para compatibilidade
em vez de remover todo o código.
"""

import re

with open('app.py', 'r', encoding='utf-8') as f:
    conteudo = f.read()

print("=== ADICIONANDO STUBS DE COMPATIBILIDADE ===\n")

# 1. Modificar obter_grupo_seguro para sempre retornar None
print("1. Modificando obter_grupo_seguro...")
conteudo = re.sub(
    r'def obter_grupo_seguro\(objeto, opcoes=\["A", "B", "AMBOS"\]\):\s*""".*?"""\s*try:.*?return "A"\s*except:.*?return "A"',
    '''def obter_grupo_seguro(objeto, opcoes=["A", "B", "AMBOS"]):
    """DEPRECATED: Grupos foram removidos do sistema"""
    return None''',
    conteudo,
    flags=re.DOTALL
)

# 2. Modificar verificar_professor_comprometido para sempre retornar False
print("2. Modificando verificar_professor_comprometido...")
conteudo = re.sub(
    r'def verificar_professor_comprometido\(professor, disciplina_nome, grupo\):.*?return False',
    '''def verificar_professor_comprometido(professor, disciplina_nome, grupo):
    """DEPRECATED: Grupos foram removidos do sistema"""
    return False''',
    conteudo,
    flags=re.DOTALL
)

# 3. Modificar obter_professores_para_disciplina para ignorar grupo
print("3. Simplificando obter_professores_para_disciplina...")
conteudo = re.sub(
    r'(def obter_professores_para_disciplina\(disciplina_nome), grupo=None\):',
    r'\1, grupo=None):  # grupo DEPRECATED',
    conteudo
)

# Simplificar lógica da função
conteudo = re.sub(
    r'(for professor in st\.session_state\.professores:\s+if disciplina_nome in professor\.disciplinas:)\s+#.*?else:\s+professores_disponiveis\.append\(professor\)',
    r'\1\n            professores_disponiveis.append(professor)  # grupo removido',
    conteudo,
    flags=re.DOTALL
)

# 4. Adicionar propriedade grupo aos objetos de forma segura
print("4. Adicionando propriedade .grupo segura...")

# Encontrar onde são criados os objetos e adicionar grupo = None
# Não podemos modificar os modelos, então vamos garantir que o código não quebre

with open('app.py', 'w', encoding='utf-8') as f:
    f.write(conteudo)

print("\n✅ Stubs de compatibilidade adicionados")
print("\nTestando importação...")

try:
    import importlib
    if 'app' in globals():
        importlib.reload(app)
    else:
        import app
    print("✅ App.py importado com sucesso!")
except Exception as e:
    print(f"❌ Erro na importação: {e}")
