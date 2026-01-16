"""
Script de Verificação Automática de Conflitos
Executa verificações detalhadas na grade gerada
"""

import json
import os
from collections import defaultdict

def verificar_conflitos_professores(aulas):
    """Verifica se há professores em múltiplas salas ao mesmo tempo"""
    conflitos = []
    
    # Mapear professor -> (dia, horario) -> [turmas]
    prof_horarios = defaultdict(lambda: defaultdict(list))
    
    for aula in aulas:
        professor = aula.get('professor')
        dia = aula.get('dia')
        horario = aula.get('horario')
        turma = aula.get('turma')
        
        if not all([professor, dia, horario, turma]):
            continue
        
        prof_horarios[professor][(dia, horario)].append(turma)
    
    # Detectar conflitos
    for professor, horarios in prof_horarios.items():
        for (dia, horario), turmas in horarios.items():
            if len(turmas) > 1:
                conflitos.append({
                    'professor': professor,
                    'dia': dia,
                    'horario': horario,
                    'turmas': turmas,
                    'quantidade': len(turmas)
                })
    
    return conflitos


def verificar_conflitos_turmas(aulas):
    """Verifica se há turmas com múltiplas disciplinas no mesmo horário"""
    conflitos = []
    
    # Mapear turma -> (dia, horario) -> [disciplinas]
    turma_horarios = defaultdict(lambda: defaultdict(list))
    
    for aula in aulas:
        turma = aula.get('turma')
        dia = aula.get('dia')
        horario = aula.get('horario')
        disciplina = aula.get('disciplina')
        
        if not all([turma, dia, horario, disciplina]):
            continue
        
        turma_horarios[turma][(dia, horario)].append(disciplina)
    
    # Detectar conflitos
    for turma, horarios in turma_horarios.items():
        for (dia, horario), disciplinas in horarios.items():
            if len(disciplinas) > 1:
                conflitos.append({
                    'turma': turma,
                    'dia': dia,
                    'horario': horario,
                    'disciplinas': disciplinas,
                    'quantidade': len(disciplinas)
                })
    
    return conflitos


def verificar_limites_professores(aulas, professores):
    """Verifica se professores excederam limites de carga horária"""
    problemas = []
    
    # Contar aulas por professor
    aulas_por_professor = defaultdict(int)
    for aula in aulas:
        professor = aula.get('professor')
        if professor:
            aulas_por_professor[professor] += 1
    
    # Verificar limites
    for prof in professores:
        nome = prof.get('nome')
        if not nome:
            continue
        
        carga_atual = aulas_por_professor.get(nome, 0)
        
        # Determinar limite baseado nas disciplinas
        disciplinas = prof.get('disciplinas', [])
        tem_em = False
        tem_efii = False
        
        for disc_nome in disciplinas:
            if any(em in disc_nome.lower() for em in ['1em', '2em', '3em']):
                tem_em = True
            else:
                tem_efii = True
        
        if tem_efii and not tem_em:
            limite = 25
            segmento = "EF_II"
        elif tem_em and not tem_efii:
            limite = 35
            segmento = "EM"
        else:
            limite = 35
            segmento = "AMBOS"
        
        if carga_atual > limite:
            problemas.append({
                'professor': nome,
                'carga_atual': carga_atual,
                'limite': limite,
                'segmento': segmento,
                'excesso': carga_atual - limite
            })
    
    return problemas


def analisar_grade(db_file='escola_database.json'):
    """Análise completa da grade"""
    
    print("=" * 70)
    print("🔍 VERIFICAÇÃO AUTOMÁTICA DE CONFLITOS - Grade Horária")
    print("=" * 70)
    print()
    
    # Carregar dados
    if not os.path.exists(db_file):
        print(f"❌ Arquivo '{db_file}' não encontrado!")
        print("   Execute 'streamlit run app.py' e gere uma grade primeiro.")
        return
    
    with open(db_file, 'r', encoding='utf-8') as f:
        dados = json.load(f)
    
    aulas = dados.get('aulas', [])
    professores = dados.get('professores', [])
    turmas = dados.get('turmas', [])
    disciplinas = dados.get('disciplinas', [])
    
    print(f"📊 DADOS CARREGADOS:")
    print(f"   - Aulas: {len(aulas)}")
    print(f"   - Professores: {len(professores)}")
    print(f"   - Turmas: {len(turmas)}")
    print(f"   - Disciplinas: {len(disciplinas)}")
    print()
    
    if not aulas:
        print("⚠️  Nenhuma aula gerada ainda.")
        print("   Vá para a aba 'Gerar Grade' no sistema e gere uma grade.")
        return
    
    # TESTE 1: Conflitos de Professores
    print("=" * 70)
    print("TESTE 1: CONFLITOS DE PROFESSORES")
    print("=" * 70)
    
    conflitos_prof = verificar_conflitos_professores(aulas)
    
    if conflitos_prof:
        print(f"❌ FALHOU: {len(conflitos_prof)} conflitos detectados!")
        print()
        print("Detalhes:")
        for i, conf in enumerate(conflitos_prof[:5], 1):
            print(f"   {i}. Professor: {conf['professor']}")
            print(f"      Dia: {conf['dia']}, Horário: {conf['horario']}º")
            print(f"      Turmas: {', '.join(conf['turmas'])} ({conf['quantidade']} ao mesmo tempo)")
            print()
        
        if len(conflitos_prof) > 5:
            print(f"   ... e mais {len(conflitos_prof) - 5} conflitos")
        print()
    else:
        print("✅ PASSOU: Nenhum professor em múltiplas salas ao mesmo tempo!")
        print()
    
    # TESTE 2: Conflitos de Turmas
    print("=" * 70)
    print("TESTE 2: CONFLITOS DE TURMAS")
    print("=" * 70)
    
    conflitos_turma = verificar_conflitos_turmas(aulas)
    
    if conflitos_turma:
        print(f"❌ FALHOU: {len(conflitos_turma)} conflitos detectados!")
        print()
        print("Detalhes:")
        for i, conf in enumerate(conflitos_turma[:5], 1):
            print(f"   {i}. Turma: {conf['turma']}")
            print(f"      Dia: {conf['dia']}, Horário: {conf['horario']}º")
            print(f"      Disciplinas: {', '.join(conf['disciplinas'])} ({conf['quantidade']} ao mesmo tempo)")
            print()
        
        if len(conflitos_turma) > 5:
            print(f"   ... e mais {len(conflitos_turma) - 5} conflitos")
        print()
    else:
        print("✅ PASSOU: Nenhuma turma com múltiplas disciplinas ao mesmo tempo!")
        print()
    
    # TESTE 3: Limites de Professores
    print("=" * 70)
    print("TESTE 3: LIMITES DE CARGA HORÁRIA")
    print("=" * 70)
    
    limites_excedidos = verificar_limites_professores(aulas, professores)
    
    if limites_excedidos:
        print(f"❌ FALHOU: {len(limites_excedidos)} professores excederam limites!")
        print()
        print("Detalhes:")
        for i, prob in enumerate(limites_excedidos, 1):
            print(f"   {i}. Professor: {prob['professor']}")
            print(f"      Carga: {prob['carga_atual']}h / Limite: {prob['limite']}h ({prob['segmento']})")
            print(f"      Excesso: +{prob['excesso']}h")
            print()
    else:
        print("✅ PASSOU: Todos os professores dentro dos limites de carga!")
        print()
    
    # RESUMO FINAL
    print("=" * 70)
    print("📋 RESUMO FINAL")
    print("=" * 70)
    
    total_testes = 3
    testes_passaram = 0
    
    if not conflitos_prof:
        testes_passaram += 1
    if not conflitos_turma:
        testes_passaram += 1
    if not limites_excedidos:
        testes_passaram += 1
    
    print(f"Testes Executados: {total_testes}")
    print(f"Testes Passaram: {testes_passaram}")
    print(f"Testes Falharam: {total_testes - testes_passaram}")
    print()
    
    if testes_passaram == total_testes:
        print("🎉 SUCESSO! Todos os testes passaram!")
        print("   A grade está livre de conflitos.")
    else:
        print("⚠️  ATENÇÃO! Alguns testes falharam.")
        print("   Recomendações:")
        if conflitos_prof:
            print("   - Use o botão 'Corrigir Conflitos' no sistema")
        if limites_excedidos:
            print("   - Redistribua aulas ou adicione mais professores")
        if conflitos_turma:
            print("   - Regenere a grade com o algoritmo corrigido")
    
    print()
    print("=" * 70)


if __name__ == '__main__':
    analisar_grade()
