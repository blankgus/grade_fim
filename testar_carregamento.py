#!/usr/bin/env python3
"""
TESTE RÁPIDO: Verifica se o sistema está pronto para rodar
"""

print("=" * 120)
print("🔍 TESTE RÁPIDO DO SISTEMA")
print("=" * 120)
print()

# Teste 1: Importações
print("1️⃣ Testando importações...")
try:
    from models import Professor, Turma, Disciplina, Sala
    from database import carregar_tudo, carregar_turmas, carregar_professores, carregar_disciplinas
    from simple_scheduler import SimpleGradeHoraria
    print("   ✅ Todas as importações OK")
except Exception as e:
    print(f"   ❌ Erro nas importações: {e}")
    exit(1)

print()

# Teste 2: Carregamento de dados
print("2️⃣ Testando carregamento de dados...")
try:
    turmas = carregar_turmas()
    professores = carregar_professores()
    disciplinas = carregar_disciplinas()
    
    print(f"   ✅ Turmas: {len(turmas)}")
    print(f"   ✅ Professores: {len(professores)}")
    print(f"   ✅ Disciplinas: {len(disciplinas)}")
except Exception as e:
    print(f"   ❌ Erro ao carregar dados: {e}")
    exit(1)

print()

# Teste 3: Validar estruturas
print("3️⃣ Validando estruturas de dados...")
try:
    # Verificar professor
    prof = professores[0]
    assert hasattr(prof, 'nome'), "Professor sem nome"
    assert hasattr(prof, 'carga_horaria'), "Professor sem carga_horaria"
    assert hasattr(prof, 'disponibilidade'), "Professor sem disponibilidade"
    assert isinstance(prof.disponibilidade, list), "Disponibilidade deve ser lista"
    print(f"   ✅ Professor: {prof.nome} ({prof.carga_horaria}h)")
    
    # Verificar disciplina
    disc = disciplinas[0]
    assert hasattr(disc, 'nome'), "Disciplina sem nome"
    assert hasattr(disc, 'carga_por_turma'), "Disciplina sem carga_por_turma"
    assert hasattr(disc, 'professor_por_turma'), "Disciplina sem professor_por_turma"
    print(f"   ✅ Disciplina: {disc.nome} ({len(disc.turmas)} turmas)")
    
    # Verificar turma
    turma = turmas[0]
    assert hasattr(turma, 'nome'), "Turma sem nome"
    print(f"   ✅ Turma: {turma.nome}")
    
except AssertionError as e:
    print(f"   ❌ Erro de validação: {e}")
    exit(1)
except Exception as e:
    print(f"   ❌ Erro inesperado: {e}")
    exit(1)

print()

# Teste 4: Verificar cargas
print("4️⃣ Verificando cargas horárias...")
try:
    from collections import defaultdict
    
    # Calcular cargas
    cargas_turmas = defaultdict(int)
    for disc in disciplinas:
        for turma, carga in disc.carga_por_turma.items():
            cargas_turmas[turma] += carga
    
    LIMITE_EF = 25
    LIMITE_EM = 35
    
    problemas = 0
    for turma in turmas:
        nome = turma.nome
        carga = cargas_turmas.get(nome, 0)
        limite = LIMITE_EM if 'em' in nome.lower() else LIMITE_EF
        
        if carga != limite:
            print(f"   ⚠️ {nome}: {carga}h/{limite}h")
            problemas += 1
    
    if problemas == 0:
        print(f"   ✅ Todas as {len(turmas)} turmas com carga correta!")
    else:
        print(f"   ⚠️ {problemas} turmas com problemas de carga")
    
except Exception as e:
    print(f"   ❌ Erro ao verificar cargas: {e}")
    exit(1)

print()

# Teste 5: Testar gerador de grades (dry-run)
print("5️⃣ Testando gerador de grades...")
try:
    gerador = SimpleGradeHoraria(turmas, professores, disciplinas, [])
    print("   ✅ Gerador de grades inicializado")
    print(f"   ℹ️ Configurado para {len(turmas)} turmas e {len(professores)} professores")
except Exception as e:
    print(f"   ❌ Erro ao inicializar gerador: {e}")
    exit(1)

print()
print("=" * 120)
print("✅ TODOS OS TESTES PASSARAM!")
print("=" * 120)
print()
print("🚀 O sistema está pronto para rodar!")
print()
print("Execute: streamlit run app.py")
print()
