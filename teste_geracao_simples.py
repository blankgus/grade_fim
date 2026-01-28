#!/usr/bin/env python3
"""
Script simples para testar se o gerador está funcionando.
"""

from database import carregar_turmas, carregar_professores, carregar_disciplinas
from simple_scheduler import SimpleGradeHoraria

def teste_rapido():
    """Teste rápido de uma turma"""
    print("Carregando dados...")
    turmas = carregar_turmas()
    professores = carregar_professores()
    disciplinas = carregar_disciplinas()
    salas = []  # Não usado no algoritmo atual
    
    print(f"✅ {len(turmas)} turmas, {len(professores)} professores, {len(disciplinas)} disciplinas")
    
    # Testar geração completa
    print("\nGerando grade completa...")
    scheduler = SimpleGradeHoraria(turmas, professores, disciplinas, salas)
    
    # Simular streamlit.info e write
    import sys
    class FakeStreamlit:
        @staticmethod
        def info(msg):
            print(f"ℹ️  {msg}")
        
        @staticmethod
        def write(msg):
            print(f"   {msg}")
        
        @staticmethod
        def warning(msg):
            print(f"⚠️  {msg}")
        
        @staticmethod
        def error(msg):
            print(f"❌ {msg}")
        
        @staticmethod
        def success(msg):
            print(f"✅ {msg}")
    
    # Substituir st temporariamente
    import simple_scheduler
    simple_scheduler.st = FakeStreamlit()
    
    resultado = scheduler.gerar_grade()
    
    if resultado['sucesso']:
        print(f"\n✅ SUCESSO!")
        print(f"Total de aulas: {len(resultado['aulas'])}")
        
        # Analisar por turma
        aulas_por_turma = {}
        for aula in resultado['aulas']:
            turma = aula['turma']
            if turma not in aulas_por_turma:
                aulas_por_turma[turma] = []
            aulas_por_turma[turma].append(aula)
        
        print(f"\n--- AULAS POR TURMA ---")
        for turma_nome in sorted(aulas_por_turma.keys()):
            aulas = aulas_por_turma[turma_nome]
            carga = len(aulas)
            limite = 25 if 'ano' in turma_nome else 35
            status = "✅" if carga == limite else f"❌ ({carga}/{limite})"
            print(f"  {turma_nome:10s} {status}")
            
            if carga != limite:
                # Mostrar quais disciplinas estão na turma
                disc_count = {}
                for aula in aulas:
                    disc = aula['disciplina']
                    disc_count[disc] = disc_count.get(disc, 0) + 1
                
                print(f"    Disciplinas alocadas:")
                for disc, count in sorted(disc_count.items()):
                    print(f"      {disc}: {count}h")
                
                # Verificar quais faltam
                print(f"    Disciplinas esperadas:")
                for disc in disciplinas:
                    if turma_nome in disc.turmas:
                        carga_esperada = disc.obter_carga_turma(turma_nome)
                        carga_alocada = disc_count.get(disc.nome, 0)
                        if carga_alocada < carga_esperada:
                            print(f"      {disc.nome}: {carga_alocada}/{carga_esperada}h ❌ FALTANDO {carga_esperada - carga_alocada}h")
    else:
        print(f"\n❌ FALHA: {resultado.get('mensagem', 'Erro desconhecido')}")
        
        if 'detalhes' in resultado:
            print(f"\nDetalhes:")
            for turma, info in resultado['detalhes'].items():
                if isinstance(info, dict) and not info.get('completa', True):
                    print(f"\n  {turma}:")
                    print(f"    Alocadas: {info.get('alocadas', 0)}")
                    print(f"    Faltantes: {info.get('faltantes', 0)}")

if __name__ == '__main__':
    teste_rapido()
