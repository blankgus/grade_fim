#!/usr/bin/env python3
"""
Limpar linhas comentadas incorretamente que causam erro de sintaxe
"""

with open('app.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

print("=== LIMPANDO ERROS DE SINTAXE ===\n")

new_lines = []
for i, line in enumerate(lines):
    # Remover linhas com sintaxe inválida (if # ...:)
    if line.strip().startswith('if # '):
        print(f"Removendo linha {i+1}: {line.strip()}")
        continue
    
    # Remover linhas vazias de comentário que quebram blocos
    if line.strip() == '#':
        continue
    
    new_lines.append(line)

with open('app.py', 'w', encoding='utf-8') as f:
    f.writelines(new_lines)

print("\n✅ Erros de sintaxe corrigidos")
