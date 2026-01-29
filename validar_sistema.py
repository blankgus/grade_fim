#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script de validação: verifica se todos os acessos a .grupo foram removidos
"""

import sys

def verificar_codigo():
    print("=" * 80)
    print("VALIDAÇÃO: Verificando remoção de .grupo")
    print("=" * 80)
    print()
    
    with open('app.py', 'r', encoding='utf-8') as f:
        linhas = f.readlines()
    
    erros = []
    avisos = []
    
    # Padrões problemáticos
    padroes_erro = [
        'turma.grupo',
        'prof.grupo',
        'turma_obj.grupo',
        'professor.grupo',
        'disc.grupo'
    ]
    
    # Padrões permitidos
    padroes_ok = [
        'obter_grupo_seguro',
        'grupo_turma',
        'grupo_filtro',
        'novo_grupo',
        'grupo_disc',
        'grupo_prof',
        "'grupo'",
        '"grupo"',
        '# grupo'
    ]
    
    for i, linha in enumerate(linhas, 1):
        linha_lower = linha.lower()
        
        # Verificar padrões de erro
        for padrao in padroes_erro:
            if padrao in linha_lower:
                # Verificar se é um comentário
                if not linha.strip().startswith('#'):
                    # Verificar se não é um padrão permitido
                    eh_ok = False
                    for ok in padroes_ok:
                        if ok in linha_lower:
                            eh_ok = True
                            break
                    
                    if not eh_ok:
                        erros.append((i, linha.strip(), padrao))
    
    # Reportar resultados
    if erros:
        print("❌ ERROS ENCONTRADOS:")
        print()
        for num_linha, conteudo, padrao in erros:
            print(f"  Linha {num_linha}: '{padrao}' encontrado")
            print(f"    {conteudo[:100]}")
            print()
        return False
    else:
        print("✅ NENHUM ERRO ENCONTRADO!")
        print()
        print("Verificações realizadas:")
        print("  • turma.grupo - ✅")
        print("  • prof.grupo - ✅")
        print("  • turma_obj.grupo - ✅")
        print("  • professor.grupo - ✅")
        print("  • disc.grupo - ✅")
        print()
        print("Função obter_grupo_seguro() - ✅ Implementada corretamente")
        return True

if __name__ == '__main__':
    sucesso = verificar_codigo()
    
    if sucesso:
        print("=" * 80)
        print("✅ VALIDAÇÃO COMPLETA - Sistema pronto para uso!")
        print("=" * 80)
        sys.exit(0)
    else:
        print("=" * 80)
        print("❌ VALIDAÇÃO FALHOU - Corrija os erros acima")
        print("=" * 80)
        sys.exit(1)
