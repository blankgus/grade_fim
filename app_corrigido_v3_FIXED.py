# app_corrigido_v3_FIXED.py - VERSÃO COMPLETA CORRIGIDA
import streamlit as st
import pandas as pd
import database
from session_state import init_session_state
from auto_save import salvar_tudo
from models import Turma, Professor, Disciplina, Sala, DIAS_SEMANA, Aula
import io
import traceback
from datetime import datetime
import random

# ============================================
# CONFIGURAÇÃO DE PÁGINA
# ============================================
st.set_page_config(page_title="Escola Timetable", layout="wide")
st.title("🕒 Gerador Inteligente de Grade Horária")

# ============================================
# VERIFICAÇÃO DE ALGORITMOS
# ============================================
ALGORITMOS_DISPONIVEIS = True
try:
    # Tentar importar algoritmo corrigido primeiro
    from simple_scheduler_final import SimpleGradeHoraria
    ALGORITMO_DISPONIVEL = "CORRIGIDO"
    st.sidebar.success("✅ Algoritmo CORRIGIDO disponível")
except ImportError:
    try:
        # Fallback para algoritmo original
        from simple_scheduler import SimpleGradeHoraria
        ALGORITMO_DISPONIVEL = "ORIGINAL"
        st.sidebar.warning("⚠️ Usando algoritmo ORIGINAL")
    except ImportError:
        ALGORITMOS_DISPONIVEIS = False
        ALGORITMO_DISPONIVEL = "NENHUM"
        st.sidebar.error("❌ Nenhum algoritmo disponível")
        
        class SimpleGradeHoraria:
            def __init__(self, *args, **kwargs):
                self.turmas = []
                self.professores = []
                self.disciplinas = []
                self.salas = []
            
            def gerar_grade(self):
                st.error("❌ Nenhum algoritmo de geração disponível!")
                return []

# ============================================
# INICIALIZAÇÃO
# ============================================
try:
    init_session_state()
    st.success("✅ Sistema inicializado com sucesso!")
except Exception as e:
    st.error(f"❌ Erro na inicialização: {str(e)}")
    st.code(traceback.format_exc())
    if st.button("🔄 Resetar Banco de Dados"):
        database.resetar_banco()
        st.rerun()
    st.stop()

# ============================================
# CONSTANTES E LIMITES
# ============================================
LIMITE_HORAS_EFII = 25  # horas semanais máximas para professores de EF II
LIMITE_HORAS_EM = 35    # horas semanais máximas para professores de EM

# ============================================
# FUNÇÕES AUXILIARES CORRIGIDAS
# ============================================

def obter_grupo_seguro(objeto, opcoes=["A", "B", "AMBOS"]):
    """Obtém o grupo de um objeto de forma segura"""
    try:
        if hasattr(objeto, 'grupo'):
            grupo = objeto.grupo
            if grupo in opcoes:
                return grupo
        return "A"
    except:
        return "A"

def obter_segmento_turma(turma_nome):
    """Determina o segmento da turma baseado no nome"""
    if not turma_nome:
        return "EF_II"
    
    turma_nome_lower = turma_nome.lower()
    
    # Verificar se é EM
    if 'em' in turma_nome_lower:
        return "EM"
    # Verificar se é EF II
    elif any(x in turma_nome_lower for x in ['6', '7', '8', '9', 'ano', 'ef']):
        return "EF_II"
    else:
        try:
            if turma_nome_lower[0].isdigit():
                return "EF_II"
            else:
                return "EM"
        except:
            return "EF_II"

def obter_segmento_professor(professor):
    """Determina o segmento principal do professor baseado nas disciplinas que ministra"""
    if not hasattr(professor, 'disciplinas') or not professor.disciplinas:
        return "AMBOS"
    
    # Verificar disciplinas do professor
    tem_efii = False
    tem_em = False
    
    for disc_nome in professor.disciplinas:
        # Encontrar disciplina correspondente
        for disc in st.session_state.disciplinas:
            if disc.nome == disc_nome:
                # Verificar turmas desta disciplina
                for turma_nome in disc.turmas:
                    segmento = obter_segmento_turma(turma_nome)
                    if segmento == "EF_II":
                        tem_efii = True
                    elif segmento == "EM":
                        tem_em = True
    
    if tem_efii and tem_em:
        return "AMBOS"
    elif tem_efii:
        return "EF_II"
    elif tem_em:
        return "EM"
    else:
        return "AMBOS"

def obter_limite_horas_professor(professor):
    """Retorna o limite de horas semanais para o professor"""
    segmento = obter_segmento_professor(professor)
    
    if segmento == "EF_II":
        return LIMITE_HORAS_EFII
    elif segmento == "EM":
        return LIMITE_HORAS_EM
    else:
        # Para professores que dão aula em ambos, usar o limite maior
        return LIMITE_HORAS_EM

def calcular_horas_professor(professor, aulas):
    """Calcula horas semanais do professor baseado nas aulas"""
    total_horas = 0
    
    for aula in aulas:
        if obter_professor_aula(aula) == professor.nome:
            # Cada aula = 1 hora
            total_horas += 1
    
    return total_horas

def obter_horarios_turma(turma_nome):
    """Retorna os períodos disponíveis para a turma"""
    segmento = obter_segmento_turma(turma_nome)
    if segmento == "EM":
        return [1, 2, 3, 4, 5, 6, 7]  # 7 períodos para EM
    else:
        return [1, 2, 3, 4, 5]  # 5 períodos para EF II

def obter_horario_real(turma_nome, periodo):
    """Retorna o horário real formatado COM INTERVALO CORRETO"""
    segmento = obter_segmento_turma(turma_nome)
    
    if segmento == "EM":
        # Ensino Médio: 7 períodos com intervalo APÓS o 3º período
        horarios_em = {
            1: "07:00 - 07:50",
            2: "07:50 - 08:40", 
            3: "08:40 - 09:30",  # ÚLTIMO ANTES DO INTERVALO
            4: "09:50 - 10:40",  # PRIMEIRO APÓS INTERVALO
            5: "10:40 - 11:30",
            6: "11:30 - 12:20",
            7: "12:20 - 13:10"
        }
        return horarios_em.get(periodo, f"Período {periodo}")
    else:
        # EF II: 5 períodos com intervalo APÓS o 2º período
        horarios_efii = {
            1: "07:50 - 08:40",
            2: "08:40 - 09:30",  # ÚLTIMO ANTES DO INTERVALO
            3: "09:50 - 10:40",  # PRIMEIRO APÓS INTERVALO
            4: "10:40 - 11:30",
            5: "11:30 - 12:20"
        }
        return horarios_efii.get(periodo, f"Período {periodo}")

def obter_periodo_por_horario_real(turma_nome, horario_real):
    """Converte horário real para número do período baseado no segmento"""
    segmento = obter_segmento_turma(turma_nome)
    
    if segmento == "EM":
        # EM: 7 períodos
        horarios_em = {
            "07:00 - 07:50": 1,
            "07:50 - 08:40": 2,
            "08:40 - 09:30": 3,
            "09:50 - 10:40": 4,
            "10:40 - 11:30": 5,
            "11:30 - 12:20": 6,
            "12:20 - 13:10": 7
        }
        return horarios_em.get(horario_real, 0)
    else:
        # EF II: 5 períodos
        horarios_efii = {
            "07:50 - 08:40": 1,
            "08:40 - 09:30": 2,
            "09:50 - 10:40": 3,
            "10:40 - 11:30": 4,
            "11:30 - 12:20": 5
        }
        return horarios_efii.get(horario_real, 0)

def calcular_carga_maxima(serie):
    """Calcula a quantidade máxima de aulas semanais"""
    if not serie:
        return 25
    
    serie_lower = serie.lower()
    if 'em' in serie_lower or serie_lower in ['1em', '2em', '3em']:
        return 35  # EM: 7 aulas × 5 dias
    else:
        return 25  # EF II: 5 aulas × 5 dias

def converter_dia_para_semana(dia):
    """Converte dia do formato completo para abreviado"""
    if dia == "segunda": return "seg"
    elif dia == "terca": return "ter"
    elif dia == "quarta": return "qua"
    elif dia == "quinta": return "qui"
    elif dia == "sexta": return "sex"
    else: return dia

def converter_dia_para_completo(dia):
    """Converte dia do formato abreviado para completo"""
    if dia == "seg": return "segunda"
    elif dia == "ter": return "terca"
    elif dia == "qua": return "quarta"
    elif dia == "qui": return "quinta"
    elif dia == "sex": return "sexta"
    else: return dia

def converter_disponibilidade_para_semana(disponibilidade):
    """Converte conjunto de disponibilidade para formato DIAS_SEMANA"""
    convertido = []
    for dia in disponibilidade:
        dia_convertido = converter_dia_para_semana(dia)
        if dia_convertido in DIAS_SEMANA:
            convertido.append(dia_convertido)
    return convertido

def converter_disponibilidade_para_completo(disponibilidade):
    """Converte conjunto de disponibilidade para formato completo"""
    convertido = []
    for dia in disponibilidade:
        convertido.append(converter_dia_para_completo(dia))
    return convertido

# ============================================
# FUNÇões DE ACESSO SEGURO A AULAS (ATUALIZADAS)
# ============================================

def obter_turma_aula(aula):
    """Obtém a turma de uma aula de forma segura"""
    if isinstance(aula, Aula):
        return aula.turma
    elif isinstance(aula, dict) and 'turma' in aula:
        return aula['turma']
    elif hasattr(aula, 'turma'):
        return aula.turma
    return None

def obter_disciplina_aula(aula):
    """Obtém a disciplina de uma aula de forma segura"""
    if isinstance(aula, Aula):
        return aula.disciplina
    elif isinstance(aula, dict) and 'disciplina' in aula:
        return aula['disciplina']
    elif hasattr(aula, 'disciplina'):
        return aula.disciplina
    return None

def obter_professor_aula(aula):
    """Obtém o professor de uma aula de forma segura"""
    if isinstance(aula, Aula):
        return aula.professor
    elif isinstance(aula, dict) and 'professor' in aula:
        return aula['professor']
    elif hasattr(aula, 'professor'):
        return aula.professor
    return None

def obter_dia_aula(aula):
    """Obtém o dia de uma aula de forma segura"""
    if isinstance(aula, Aula):
        return aula.dia
    elif isinstance(aula, dict) and 'dia' in aula:
        return aula['dia']
    elif hasattr(aula, 'dia'):
        return aula.dia
    return None

def obter_horario_aula(aula):
    """Obtém o número do horário de uma aula de forma segura"""
    if isinstance(aula, Aula):
        return aula.horario
    elif isinstance(aula, dict) and 'horario' in aula:
        return aula['horario']
    elif hasattr(aula, 'horario'):
        return aula.horario
    return None

def obter_horario_real_aula(aula):
    """Obtém o horário REAL de uma aula"""
    turma = obter_turma_aula(aula)
    horario_num = obter_horario_aula(aula)
    
    if turma and horario_num:
        return obter_horario_real(turma, horario_num)
    return None

def obter_segmento_aula(aula):
    """Obtém o segmento de uma aula de forma segura"""
    if isinstance(aula, Aula):
        return aula.segmento if hasattr(aula, 'segmento') else None
    elif isinstance(aula, dict) and 'segmento' in aula:
        return aula['segmento']
    elif hasattr(aula, 'segmento'):
        return aula.segmento
    return None

# ============================================
# FUNÇÕES PARA PROFESSORES POR DISCIPLINA
# ============================================

def obter_professores_para_disciplina(disciplina_nome, grupo=None):
    """Retorna lista de professores que podem ministrar uma disciplina"""
    professores_disponiveis = []
    
    for professor in st.session_state.professores:
        if disciplina_nome in professor.disciplinas:
            # Verificar se o grupo do professor é compatível
            if grupo:
                prof_grupo = obter_grupo_seguro(professor)
                if prof_grupo in [grupo, "AMBOS"]:
                    professores_disponiveis.append(professor)
            else:
                professores_disponiveis.append(professor)
    
    return professores_disponiveis

def calcular_disponibilidade_professor(professor):
    """Calcula disponibilidade semanal do professor em horas"""
    dias_disponiveis = len(professor.disponibilidade) if hasattr(professor, 'disponibilidade') else 0
    horarios_indisponiveis = len(professor.horarios_indisponiveis) if hasattr(professor, 'horarios_indisponiveis') else 0
    
    # Cada dia tem 7 períodos possíveis
    total_periodos = dias_disponiveis * 7
    periodos_disponiveis = total_periodos - horarios_indisponiveis
    
    return periodos_disponiveis

def verificar_professor_comprometido(professor, disciplina_nome, grupo):
    """Verifica se um professor está comprometido com outras disciplinas"""
    # Obter todas as disciplinas que o professor ministra
    disciplinas_prof = professor.disciplinas
    
    if disciplina_nome not in disciplinas_prof:
        return False  # Não ministra esta disciplina
    
    # Verificar se há outras disciplinas no mesmo grupo
    outras_disciplinas = [d for d in disciplinas_prof if d != disciplina_nome]
    
    if not outras_disciplinas:
        return False  # Só ministra esta disciplina
    
    # Verificar se outras disciplinas são do mesmo grupo
    for outra_disc_nome in outras_disciplinas:
        # Encontrar a disciplina
        for disc in st.session_state.disciplinas:
            if disc.nome == outra_disc_nome:
                disc_grupo = obter_grupo_seguro(disc)
                if disc_grupo == grupo:
                    return True  # Está comprometido com outra disciplina do mesmo grupo
    
    return False

# ============================================
# FUNÇÕES PARA VERIFICAÇÃO E CORREÇÃO DE CONFLITOS (CORRIGIDAS)
# ============================================

def verificar_conflitos_horarios(aulas):
    """Verifica se há horários sobrepostos na mesma turma considerando horários REAIS"""
    conflitos = []
    horarios_por_turma = {}
    aulas_por_disciplina_turma = {}
    
    for aula in aulas:
        turma = obter_turma_aula(aula)
        dia = obter_dia_aula(aula)
        horario_num = obter_horario_aula(aula)
        disciplina = obter_disciplina_aula(aula)
        
        if not turma or not dia or not horario_num or not disciplina:
            continue
        
        # Obter horário REAL
        hora_real = obter_horario_real(turma, horario_num)
        segmento = obter_segmento_turma(turma)
        
        # Chave baseada em horário REAL
        chave_horario = f"{turma}|{dia}|{hora_real}"
        
        if chave_horario not in horarios_por_turma:
            horarios_por_turma[chave_horario] = []
        
        # VERIFICAÇÃO 1: Conflito no mesmo horário REAL
        disciplinas_no_horario = [obter_disciplina_aula(a) for a in horarios_por_turma[chave_horario]]
        if disciplina in disciplinas_no_horario:
            # AULA REPETIDA - mesma disciplina já alocada neste horário REAL
            conflitos.append({
                'tipo': 'repeticao_mesmo_horario',
                'turma': turma,
                'dia': dia,
                'horario_real': hora_real,
                'horario_num': horario_num,
                'disciplina': disciplina,
                'chave': chave_horario,
                'segmento': segmento
            })
        else:
            horarios_por_turma[chave_horario].append(aula)
            
            if len(horarios_por_turma[chave_horario]) > 1:
                # CONFLITO DETECTADO! Horário sobreposto com disciplinas diferentes
                conflitos.append({
                    'tipo': 'sobreposicao',
                    'turma': turma,
                    'dia': dia,
                    'horario_real': hora_real,
                    'horario_num': horario_num,
                    'aulas': horarios_por_turma[chave_horario].copy(),
                    'disciplinas': [obter_disciplina_aula(a) for a in horarios_por_turma[chave_horario]],
                    'chave': chave_horario,
                    'segmento': segmento
                })
        
        # VERIFICAÇÃO 2: Aulas repetidas em excesso
        chave_disc_turma = f"{turma}|{disciplina}"
        
        if chave_disc_turma not in aulas_por_disciplina_turma:
            aulas_por_disciplina_turma[chave_disc_turma] = []
        
        aulas_por_disciplina_turma[chave_disc_turma].append(aula)
        
        # Obter carga semanal necessária
        carga_necessaria = 0
        for disc in st.session_state.disciplinas:
            if disc.nome == disciplina and turma in disc.turmas:
                carga_necessaria = disc.carga_semanal
                break
        
        if len(aulas_por_disciplina_turma[chave_disc_turma]) > carga_necessaria:
            conflitos.append({
                'tipo': 'excesso_aulas',
                'turma': turma,
                'disciplina': disciplina,
                'quantidade': len(aulas_por_disciplina_turma[chave_disc_turma]),
                'necessario': carga_necessaria,
                'chave': chave_disc_turma,
                'segmento': segmento
            })
    
    return conflitos

def verificar_professor_superposto(aulas):
    """Verifica se o mesmo professor tem aulas em horários REAIS sobrepostos"""
    superposicoes = []
    horarios_por_professor = {}
    
    for aula in aulas:
        professor = obter_professor_aula(aula)
        dia = obter_dia_aula(aula)
        horario_num = obter_horario_aula(aula)
        turma = obter_turma_aula(aula)
        
        if not professor or not dia or not horario_num or not turma:
            continue
        
        # Obter horário REAL
        hora_real = obter_horario_real(turma, horario_num)
        segmento = obter_segmento_turma(turma)
        
        # Chave baseada em horário REAL
        chave = f"{professor}|{dia}|{hora_real}"
        
        if chave not in horarios_por_professor:
            horarios_por_professor[chave] = []
        
        horarios_por_professor[chave].append(aula)
        
        if len(horarios_por_professor[chave]) > 1:
            # SUPERPOSIÇÃO DETECTADA! Professor no mesmo horário REAL
            superposicoes.append({
                'professor': professor,
                'dia': dia,
                'horario_real': hora_real,
                'horario_num': horario_num,
                'aulas': horarios_por_professor[chave].copy(),
                'turmas': [obter_turma_aula(a) for a in horarios_por_professor[chave]],
                'disciplinas': [obter_disciplina_aula(a) for a in horarios_por_professor[chave]],
                'segmentos': [obter_segmento_turma(obter_turma_aula(a)) for a in horarios_por_professor[chave]],
                'chave': chave
            })
    
    return superposicoes

def analisar_superposicoes_por_horario_real(aulas):
    """Analisa superposições agrupando por horário REAL (para diagnóstico)"""
    analise = {}
    
    for aula in aulas:
        professor = obter_professor_aula(aula)
        dia = obter_dia_aula(aula)
        horario_num = obter_horario_aula(aula)
        turma = obter_turma_aula(aula)
        
        if not all([professor, dia, horario_num, turma]):
            continue
        
        # Obter horário REAL
        hora_real = obter_horario_real(turma, horario_num)
        segmento = obter_segmento_turma(turma)
        
        chave = f"{professor}|{dia}|{hora_real}"
        
        if chave not in analise:
            analise[chave] = {
                'professor': professor,
                'dia': dia,
                'horario_real': hora_real,
                'aulas': [],
                'turmas': [],
                'segmentos': [],
                'horarios_numericos': []
            }
        
        analise[chave]['aulas'].append(aula)
        analise[chave]['turmas'].append(turma)
        analise[chave]['segmentos'].append(segmento)
        analise[chave]['horarios_numericos'].append(horario_num)
    
    # Filtrar apenas os que têm superposição
    superposicoes = {k: v for k, v in analise.items() if len(v['aulas']) > 1}
    
    return superposicoes

def verificar_limites_professores(aulas):
    """Verifica se algum professor excedeu o limite de horas"""
    problemas = []
    
    for professor in st.session_state.professores:
        horas_atual = calcular_horas_professor(professor, aulas)
        limite = obter_limite_horas_professor(professor)
        
        if horas_atual > limite:
            problemas.append({
                'professor': professor.nome,
                'horas_atual': horas_atual,
                'limite': limite,
                'segmento': obter_segmento_professor(professor)
            })
    
    return problemas

# ============================================
# FUNÇÃO: REMOVER AULAS REPETIDAS
# ============================================

def remover_aulas_repetidas(aulas):
    """Remove aulas repetidas da mesma disciplina para a mesma turma"""
    if not aulas:
        return aulas
    
    aulas_filtradas = []
    contador = {}
    
    for aula in aulas:
        turma = obter_turma_aula(aula)
        disciplina = obter_disciplina_aula(aula)
        
        if not turma or not disciplina:
            aulas_filtradas.append(aula)  # Mantém se não puder identificar
            continue
            
        chave = f"{turma}|{disciplina}"
        
        # Obter carga semanal necessária
        carga_necessaria = 0
        for disc in st.session_state.disciplinas:
            if disc.nome == disciplina and turma in disc.turmas:
                carga_necessaria = disc.carga_semanal
                break
        
        # Inicializar contador se não existir
        if chave not in contador:
            contador[chave] = 0
        
        # Adicionar apenas se não exceder a carga necessária
        if contador[chave] < carga_necessaria:
            aulas_filtradas.append(aula)
            contador[chave] += 1
        else:
            # Aula repetida - não adicionar
            continue
    
    return aulas_filtradas

# ============================================
# FUNÇÃO: CORRIGIR SUPERPOSIÇÕES DE PROFESSOR (ATUALIZADA)
# ============================================

def corrigir_superposicoes_professor(aulas, superposicoes):
    """Corrige superposições onde o mesmo professor tem aulas no mesmo horário REAL"""
    if not superposicoes:
        return aulas
    
    # Converter para lista de dicionários para facilitar manipulação
    aulas_dict = []
    for aula in aulas:
        turma = obter_turma_aula(aula)
        horario_num = obter_horario_aula(aula)
        
        aulas_dict.append({
            'turma': turma,
            'disciplina': obter_disciplina_aula(aula),
            'professor': obter_professor_aula(aula),
            'dia': obter_dia_aula(aula),
            'horario': horario_num,
            'horario_real': obter_horario_real(turma, horario_num) if turma and horario_num else None,
            'segmento': obter_segmento_aula(aula) or obter_segmento_turma(turma),
            'id_temporario': len(aulas_dict)
        })
    
    # Para cada superposição, tentar encontrar horário livre
    for superposicao in superposicoes:
        professor = superposicao['professor']
        dia = superposicao['dia']
        horario_real_superposto = superposicao['horario_real']
        
        # Encontrar todas as aulas deste professor neste dia/horário REAL
        aulas_superpostas = []
        for i, aula in enumerate(aulas_dict):
            if (aula['professor'] == professor and 
                aula['dia'] == dia and 
                aula['horario_real'] == horario_real_superposto):
                aulas_superpostas.append((i, aula))
        
        # Se tiver mais de uma aula no mesmo horário REAL, mover as extras
        if len(aulas_superpostas) > 1:
            st.info(f"Corrigindo superposição: Professor {professor} tem {len(aulas_superpostas)} aulas às {dia}, {horario_real_superposto}")
            
            # Manter a primeira, mover as outras
            manter_idx, manter_aula = aulas_superpostas[0]
            
            for idx, aula in aulas_superpostas[1:]:
                turma = aula['turma']
                segmento = aula['segmento']
                
                # Encontrar horários possíveis para esta turma
                if segmento == "EM":
                    horarios_possiveis = list(range(1, 8))
                else:
                    horarios_possiveis = list(range(1, 6))
                
                # Encontrar horários já ocupados nesta turma/dia (horários REAIS)
                horarios_ocupados_turma = set()
                horarios_ocupados_prof = set()
                
                for a in aulas_dict:
                    if a['turma'] == turma and a['dia'] == dia:
                        horarios_ocupados_turma.add(a['horario'])
                    
                    if a['professor'] == professor and a['dia'] == dia:
                        horarios_ocupados_prof.add(a['horario'])
                
                # Prioridade 1: Encontrar horário livre no MESMO DIA
                horario_livre = None
                for h in horarios_possiveis:
                    if h not in horarios_ocupados_turma and h not in horarios_ocupados_prof:
                        horario_livre = h
                        break
                
                # Se encontrou horário livre no mesmo dia, mover a aula
                if horario_livre:
                    aulas_dict[idx]['horario'] = horario_livre
                    aulas_dict[idx]['horario_real'] = obter_horario_real(turma, horario_livre)
                    st.success(f"  • Movida aula de {aula['disciplina']} (Turma {turma}) para horário {horario_livre}º ({aulas_dict[idx]['horario_real']})")
                
                else:
                    # Prioridade 2: Tentar outro dia
                    dias_semana = ['segunda', 'terca', 'quarta', 'quinta', 'sexta']
                    dias_semana.remove(dia)  # Remover o dia atual
                    
                    encontrou_novo_dia = False
                    for novo_dia in dias_semana:
                        # Verificar se turma tem horário livre neste novo dia
                        turma_horarios_livres = []
                        for h in horarios_possiveis:
                            turma_ocupada = False
                            prof_ocupado = False
                            
                            for a in aulas_dict:
                                if a['turma'] == turma and a['dia'] == novo_dia and a['horario'] == h:
                                    turma_ocupada = True
                                if a['professor'] == professor and a['dia'] == novo_dia and a['horario'] == h:
                                    prof_ocupado = True
                            
                            if not turma_ocupada and not prof_ocupado:
                                turma_horarios_livres.append(h)
                        
                        if turma_horarios_livres:
                            # Escolher o primeiro horário livre
                            novo_horario = turma_horarios_livres[0]
                            aulas_dict[idx]['dia'] = novo_dia
                            aulas_dict[idx]['horario'] = novo_horario
                            aulas_dict[idx]['horario_real'] = obter_horario_real(turma, novo_horario)
                            encontrou_novo_dia = True
                            st.success(f"  • Movida aula de {aula['disciplina']} (Turma {turma}) para {novo_dia}, {novo_horario}º ({aulas_dict[idx]['horario_real']})")
                            break
                    
                    if not encontrou_novo_dia:
                        st.warning(f"  ⚠️ Não foi possível realocar aula de {aula['disciplina']} (Turma {turma}). Mantendo no horário original.")
    
    # Remover ID temporário
    for aula in aulas_dict:
        if 'id_temporario' in aula:
            del aula['id_temporario']
        if 'horario_real' in aula:
            del aula['horario_real']  # Não necessário no objeto final
    
    # Converter de volta para objetos Aula
    aulas_corrigidas = []
    for aula_dict in aulas_dict:
        aulas_corrigidas.append(Aula(
            turma=aula_dict['turma'],
            disciplina=aula_dict['disciplina'],
            professor=aula_dict['professor'],
            dia=aula_dict['dia'],
            horario=aula_dict['horario'],
            segmento=aula_dict['segmento']
        ))
    
    return aulas_corrigidas

def corrigir_conflitos_automaticamente(aulas, conflitos):
    """Tenta corrigir conflitos de horário automaticamente considerando horários REAIS"""
    if not conflitos:
        return aulas
    
    # Primeiro, remover aulas repetidas da mesma disciplina
    aulas_sem_repetidas = []
    aulas_por_disciplina_turma = {}
    
    for aula in aulas:
        turma = obter_turma_aula(aula)
        disciplina = obter_disciplina_aula(aula)
        
        if not turma or not disciplina:
            aulas_sem_repetidas.append(aula)
            continue
            
        # Chave única para disciplina+turma
        chave = f"{turma}|{disciplina}"
        
        # Contar quantas vezes esta disciplina já aparece para esta turma
        if chave not in aulas_por_disciplina_turma:
            aulas_por_disciplina_turma[chave] = []
        
        # Obter carga semanal necessária para esta disciplina+turma
        carga_necessaria = 0
        for disc in st.session_state.disciplinas:
            if disc.nome == disciplina and turma in disc.turmas:
                carga_necessaria = disc.carga_semanal
                break
        
        # Se já tem todas as aulas necessárias, não adicionar mais
        if len(aulas_por_disciplina_turma[chave]) >= carga_necessaria:
            continue  # Pular esta aula - já tem o suficiente
        
        # Adicionar aula
        aulas_por_disciplina_turma[chave].append(aula)
        aulas_sem_repetidas.append(aula)
    
    # Converter para lista de dicionários para facilitar manipulação
    aulas_dict = []
    for aula in aulas_sem_repetidas:
        turma = obter_turma_aula(aula)
        horario_num = obter_horario_aula(aula)
        
        aulas_dict.append({
            'turma': turma,
            'disciplina': obter_disciplina_aula(aula),
            'professor': obter_professor_aula(aula),
            'dia': obter_dia_aula(aula),
            'horario': horario_num,
            'segmento': obter_segmento_aula(aula) or obter_segmento_turma(turma),
            'horario_real': obter_horario_real(turma, horario_num) if turma and horario_num else None
        })
    
    # Para cada conflito, tentar encontrar horário livre
    for conflito in conflitos:
        if conflito.get('tipo') in ['repeticao_mesmo_horario', 'excesso_aulas']:
            # Aula repetida - já removemos acima
            continue
            
        # Processar conflitos de sobreposição
        if conflito.get('tipo') == 'sobreposicao':
            turma = conflito['turma']
            dia = conflito['dia']
            horario_real_conflito = conflito.get('horario_real')
            
            if not horario_real_conflito:
                continue
            
            # Encontrar aulas conflitantes
            aulas_conflitantes = []
            for i, aula in enumerate(aulas_dict):
                if (aula['turma'] == turma and 
                    aula['dia'] == dia and 
                    aula['horario_real'] == horario_real_conflito):
                    aulas_conflitantes.append((i, aula))
            
            # Se tiver mais de uma aula no mesmo horário REAL, mover as extras
            if len(aulas_conflitantes) > 1:
                # Manter a primeira, mover as outras
                for idx, aula in aulas_conflitantes[1:]:
                    # Encontrar horários possíveis para esta turma
                    segmento = obter_segmento_turma(turma)
                    if segmento == "EM":
                        horarios_possiveis = list(range(1, 8))
                    else:
                        horarios_possiveis = list(range(1, 6))
                    
                    # Encontrar horários já ocupados nesta turma/dia
                    horarios_ocupados = set()
                    for a in aulas_dict:
                        if a['turma'] == turma and a['dia'] == dia:
                            horarios_ocupados.add(a['horario'])
                    
                    # Encontrar horário livre
                    horario_livre = None
                    for h in horarios_possiveis:
                        if h not in horarios_ocupados:
                            horario_livre = h
                            break
                    
                    # Se encontrou horário livre, mover a aula
                    if horario_livre:
                        aulas_dict[idx]['horario'] = horario_livre
                        aulas_dict[idx]['horario_real'] = obter_horario_real(turma, horario_livre)
    
    # Remover campo auxiliar
    for aula in aulas_dict:
        if 'horario_real' in aula:
            del aula['horario_real']
    
    # Converter de volta para objetos Aula
    aulas_corrigidas = []
    for aula_dict in aulas_dict:
        aulas_corrigidas.append(Aula(
            turma=aula_dict['turma'],
            disciplina=aula_dict['disciplina'],
            professor=aula_dict['professor'],
            dia=aula_dict['dia'],
            horario=aula_dict['horario'],
            segmento=aula_dict['segmento']
        ))
    
    return aulas_corrigidas

def corrigir_csv_export(df):
    """Corrige problemas de formatação no CSV exportado"""
    # Remover coluna de índice se existir
    if '' in df.columns or df.columns[0] == '':
        if '' in df.columns:
            df = df.drop(columns=[''])
        elif df.columns[0] == '':
            df = df.drop(columns=[df.columns[0]])
    
    # Ordenar por dia e horário
    ordem_dias = {"Segunda": 1, "Terca": 2, "Quarta": 3, "Quinta": 4, "Sexta": 5}
    
    # Extrair número do período do horário para ordenação
    def extrair_periodo(horario):
        try:
            if isinstance(horario, str) and 'º' in horario:
                return int(horario.split('º')[0])
            return 0
        except:
            return 0
    
    if 'Horário' in df.columns:
        df['Periodo'] = df['Horário'].apply(extrair_periodo)
    else:
        df['Periodo'] = 0
    
    if 'Dia' in df.columns:
        df['Dia_Ordem'] = df['Dia'].map(ordem_dias)
        df = df.sort_values(['Dia_Ordem', 'Periodo'])
        df = df.drop(['Dia_Ordem', 'Periodo'], axis=1)
    else:
        df = df.sort_values(['Periodo'])
        df = df.drop(['Periodo'], axis=1)
    
    return df

# ============================================
# SISTEMA DE DIAGNÓSTICO DE GRADE (ATUALIZADO)
# ============================================

def diagnosticar_grade(turmas, professores, disciplinas, aulas_alocadas):
    """Diagnóstico completo do que impede a grade de ficar 100% completa"""
    diagnostico = {
        'status': '❌ INCOMPLETA',
        'completude': 0,
        'problemas': [],
        'sugestoes': [],
        'estatisticas': {},
        'detalhes_por_turma': {},
        'professores_saturados': [],
        'horarios_conflitantes': [],
        'conflitos_detectados': [],
        'professores_limite_excedido': [],
        'aulas_repetidas': [],
        'professores_superpostos': []
    }
    
    if not aulas_alocadas:
        return diagnostico
    
    # Verificar conflitos de horário primeiro
    conflitos = verificar_conflitos_horarios(aulas_alocadas)
    diagnostico['conflitos_detectados'] = conflitos
    
    # Verificar limites de horas dos professores
    problemas_limites = verificar_limites_professores(aulas_alocadas)
    diagnostico['professores_limite_excedido'] = problemas_limites
    
    # Verificar superposições de professor (CRÍTICO!)
    superposicoes = verificar_professor_superposto(aulas_alocadas)
    diagnostico['professores_superpostos'] = superposicoes
    
    # Analisar superposições por horário REAL para diagnóstico detalhado
    analise_superposicoes = analisar_superposicoes_por_horario_real(aulas_alocadas)
    
    # Verificar aulas repetidas
    aulas_por_disciplina_turma = {}
    for aula in aulas_alocadas:
        turma = obter_turma_aula(aula)
        disciplina = obter_disciplina_aula(aula)
        
        if not turma or not disciplina:
            continue
            
        chave = f"{turma}|{disciplina}"
        
        if chave not in aulas_por_disciplina_turma:
            aulas_por_disciplina_turma[chave] = []
        
        aulas_por_disciplina_turma[chave].append(aula)
        
        # Obter carga semanal necessária
        carga_necessaria = 0
        for disc in disciplinas:
            if disc.nome == disciplina and turma in disc.turmas:
                carga_necessaria = disc.carga_semanal
                break
        
        # Se tem mais aulas do que o necessário
        if len(aulas_por_disciplina_turma[chave]) > carga_necessaria:
            # Adicionar à lista de repetidas
            diagnostico['aulas_repetidas'].append({
                'turma': turma,
                'disciplina': disciplina,
                'quantidade': len(aulas_por_disciplina_turma[chave]),
                'necessario': carga_necessaria,
                'aulas': aulas_por_disciplina_turma[chave]
            })
    
    # Adicionar problemas de aulas repetidas
    if diagnostico['aulas_repetidas']:
        for repetida in diagnostico['aulas_repetidas'][:3]:
            diagnostico['problemas'].append(
                f"❌ **AULA REPETIDA**: {repetida['disciplina']} na turma {repetida['turma']} "
                f"tem {repetida['quantidade']} aulas (necessário: {repetida['necessario']})"
            )
        diagnostico['sugestoes'].append(
            "👉 Use o botão 'Remover Aulas Repetidas' para remover aulas extras"
        )
    
    # Converter todas as aulas para formato consistente
    aulas_consistente = []
    for aula in aulas_alocadas:
        turma = obter_turma_aula(aula)
        horario_num = obter_horario_aula(aula)
        
        aulas_consistente.append({
            'turma': turma,
            'disciplina': obter_disciplina_aula(aula),
            'professor': obter_professor_aula(aula),
            'dia': obter_dia_aula(aula),
            'horario_num': horario_num,
            'horario_real': obter_horario_real(turma, horario_num) if turma and horario_num else None,
            'segmento': obter_segmento_aula(aula) or obter_segmento_turma(turma)
        })
    
    # 1. ANÁLISE POR TURMA
    total_aulas_necessarias = 0
    total_aulas_alocadas = len(aulas_consistente)
    
    for turma in turmas:
        turma_nome = turma.nome
        grupo_turma = turma.grupo
        segmento = obter_segmento_turma(turma_nome)
        
        # Calcular aulas necessárias para esta turma
        aulas_necessarias_turma = 0
        disciplinas_da_turma = []
        
        for disc in disciplinas:
            if turma_nome in disc.turmas and obter_grupo_seguro(disc) == grupo_turma:
                aulas_necessarias_turma += disc.carga_semanal
                disciplinas_da_turma.append(disc)
        
        total_aulas_necessarias += aulas_necessarias_turma
        
        # Contar aulas alocadas para esta turma
        aulas_turma = [a for a in aulas_consistente if a['turma'] == turma_nome]
        aulas_alocadas_turma = len(aulas_turma)
        
        # Calcular completude da turma
        completude_turma = (aulas_alocadas_turma / aulas_necessarias_turma * 100) if aulas_necessarias_turma > 0 else 0
        
        # Detalhar por disciplina
        faltas_disciplinas = []
        for disc in disciplinas_da_turma:
            aulas_disc = len([a for a in aulas_turma if a['disciplina'] == disc.nome])
            if aulas_disc < disc.carga_semanal:
                faltas = disc.carga_semanal - aulas_disc
                faltas_disciplinas.append(f"{disc.nome} ({aulas_disc}/{disc.carga_semanal})")
        
        diagnostico['detalhes_por_turma'][turma_nome] = {
            'necessarias': aulas_necessarias_turma,
            'alocadas': aulas_alocadas_turma,
            'completude': completude_turma,
            'faltas_disciplinas': faltas_disciplinas,
            'segmento': segmento,
            'grupo': grupo_turma
        }
    
    # 2. CALCULAR COMPLETUDE GERAL
    if total_aulas_necessarias > 0:
        completude_geral = (total_aulas_alocadas / total_aulas_necessarias * 100)
        diagnostico['completude'] = round(completude_geral, 1)
        diagnostico['estatisticas']['total_necessario'] = total_aulas_necessarias
        diagnostico['estatisticas']['total_alocado'] = total_aulas_alocadas
        diagnostico['estatisticas']['faltam'] = total_aulas_necessarias - total_aulas_alocadas
    
    # 3. ANÁLISE DE PROFESSORES
    for professor in professores:
        # Contar aulas do professor
        aulas_professor = len([a for a in aulas_consistente if a['professor'] == professor.nome])
        
        # Verificar disponibilidade
        dias_disponiveis = len(professor.disponibilidade) if hasattr(professor, 'disponibilidade') else 0
        horarios_indisponiveis = len(professor.horarios_indisponiveis) if hasattr(professor, 'horarios_indisponiveis') else 0
        
        # Calcular capacidade máxima baseada em disponibilidade
        capacidade_maxima = dias_disponiveis * 7 - horarios_indisponiveis
        
        # Calcular limite baseado no segmento
        limite_segmento = obter_limite_horas_professor(professor)
        capacidade_maxima = min(capacidade_maxima, limite_segmento)
        
        if capacidade_maxima <= aulas_professor:
            diagnostico['professores_saturados'].append({
                'nome': professor.nome,
                'aulas': aulas_professor,
                'capacidade': capacidade_maxima,
                'dias_disponiveis': dias_disponiveis,
                'horarios_bloqueados': horarios_indisponiveis,
                'limite_segmento': limite_segmento,
                'segmento': obter_segmento_professor(professor)
            })
    
    # 4. IDENTIFICAR PROBLEMAS PRINCIPAIS
    for turma_nome, info in diagnostico['detalhes_por_turma'].items():
        if info['faltas_disciplinas']:
            turma_obj = next((t for t in turmas if t.nome == turma_nome), None)
            grupo_turma = turma_obj.grupo if turma_obj else 'A'
            
            for falta in info['faltas_disciplinas']:
                disc_nome = falta.split(' (')[0]
                
                # Verificar professores para esta disciplina
                professores_disc = obter_professores_para_disciplina(disc_nome, grupo_turma)
                
                if not professores_disc:
                    diagnostico['problemas'].append(f"❌ **{turma_nome}**: Nenhum professor para **{disc_nome}**")
                    diagnostico['sugestoes'].append(f"👉 Adicione um professor que ministre **{disc_nome}** no grupo **{grupo_turma}**")
                else:
                    # Verificar comprometimento dos professores
                    professores_livres = []
                    professores_comprometidos = []
                    
                    for prof in professores_disc:
                        if verificar_professor_comprometido(prof, disc_nome, grupo_turma):
                            professores_comprometidos.append(prof.nome)
                        else:
                            professores_livres.append(prof.nome)
                    
                    if not professores_livres:
                        diagnostico['problemas'].append(f"⚠️ **{turma_nome}**: Todos professores para **{disc_nome}** estão comprometidos com outras disciplinas")
                        diagnostico['sugestoes'].append(f"👉 Adicione mais professores para **{disc_nome}** ou libere professores comprometidos")
                    elif len(professores_livres) == 1:
                        diagnostico['problemas'].append(f"⚠️ **{turma_nome}**: Apenas 1 professor livre para **{disc_nome}** ({professores_livres[0]})")
                        diagnostico['sugestoes'].append(f"👉 Adicione um segundo professor para **{disc_nome}** ou aumente a disponibilidade de **{professores_livres[0]}**")
    
    # 5. Conflitos de horário REAL
    horarios_turma = {}
    for aula in aulas_consistente:
        if aula['horario_real']:
            chave = f"{aula['turma']}|{aula['dia']}|{aula['horario_real']}"
            if chave not in horarios_turma:
                horarios_turma[chave] = []
            horarios_turma[chave].append(aula)
    
    for chave, aulas_conflito in horarios_turma.items():
        if len(aulas_conflito) > 1:
            turma = aulas_conflito[0]['turma']
            dia = aulas_conflito[0]['dia']
            horario_real = aulas_conflito[0]['horario_real']
            disciplinas = [a['disciplina'] for a in aulas_conflito]
            professores = [a['professor'] for a in aulas_conflito]
            diagnostico['horarios_conflitantes'].append({
                'turma': turma,
                'dia': dia,
                'horario_real': horario_real,
                'disciplinas': disciplinas,
                'professores': professores
            })
    
    # 6. Superposições de professor (CRÍTICO!) - com horários REAIS
    if superposicoes:
        for sup in superposicoes[:3]:
            turmas_str = ", ".join(sup['turmas'][:2])
            segmentos_str = "/".join(set(sup['segmentos']))
            
            if len(sup['turmas']) > 2:
                turmas_str += f" (+{len(sup['turmas'])-2} mais)"
            
            diagnostico['problemas'].append(
                f"❌ **SUPERPOSIÇÃO CRÍTICA**: Professor **{sup['professor']}** tem {len(sup['aulas'])} aulas "
                f"no mesmo horário REAL ({sup['dia']}, {sup['horario_real']}) nas turmas: {turmas_str} ({segmentos_str})"
            )
        
        diagnostico['sugestoes'].append(
            "👉 **CORRIJA IMEDIATAMENTE** usando o botão 'Corrigir Superposições de Professor'"
        )
    
    # 7. Análise detalhada de superposições por horário REAL
    if analise_superposicoes:
        diagnostico['analise_superposicoes_detalhada'] = analise_superposicoes
    
    # 8. DEFINIR STATUS FINAL
    status_critico = len(superposicoes) > 0
    status_incompleto = diagnostico['completude'] < 100
    status_problemas = len(conflitos) > 0 or len(problemas_limites) > 0 or len(diagnostico['aulas_repetidas']) > 0
    
    if status_critico:
        diagnostico['status'] = '❌ CRÍTICO (Professor sobreposto)'
    elif not status_incompleto and not status_problemas:
        diagnostico['status'] = '✅ COMPLETA'
    elif diagnostico['completude'] >= 90:
        diagnostico['status'] = '⚠️ QUASE COMPLETA'
    elif diagnostico['completude'] >= 70:
        diagnostico['status'] = '⚠️ PARCIAL'
    else:
        diagnostico['status'] = '❌ INCOMPLETA'
    
    # 9. SUGESTÕES AUTOMÁTICAS
    if conflitos:
        diagnostico['problemas'].insert(0, f"❌ **CONFLITOS DETECTADOS**: {len(conflitos)} horários sobrepostos")
        diagnostico['sugestoes'].insert(0, "👉 Use o botão 'Corrigir Conflitos Automaticamente' para resolver")
    
    if problemas_limites:
        for problema in problemas_limites[:2]:
            diagnostico['problemas'].append(f"❌ **LIMITE EXCEDIDO**: Professor **{problema['professor']}** tem {problema['horas_atual']}h (limite: {problema['limite']}h para {problema['segmento']})")
            diagnostico['sugestoes'].append(f"👉 Reduza carga do professor **{problema['professor']}** ou redistribua aulas")
    
    if diagnostico['professores_saturados']:
        for prof in diagnostico['professores_saturados'][:3]:
            diagnostico['sugestoes'].append(f"👉 Professor **{prof['nome']}** está com {prof['aulas']}/{prof['capacidade']} aulas. Aumente disponibilidade ou reduza carga.")
    
    if total_aulas_necessarias > total_aulas_alocadas:
        faltam = total_aulas_necessarias - total_aulas_alocadas
        diagnostico['sugestoes'].append(f"👉 **Faltam {faltam} aulas no total**. Verifique disponibilidade de professores.")
    
    return diagnostico

# ============================================
# ALGORITMO AVANÇADO PARA COMPLETAR GRADES
# ============================================

class CompletadorDeGradeAvancado:
    """Algoritmo avançado para completar grades incompletas"""
    
    def __init__(self, turmas, professores, disciplinas):
        self.turmas = turmas
        self.professores = professores
        self.disciplinas = disciplinas
        self.dias = ['segunda', 'terca', 'quarta', 'quinta', 'sexta']
        self.max_iteracoes = 500
    
    def completar_grade(self, aulas_atuais):
        """Tenta completar uma grade existente"""
        if not aulas_atuais:
            return self._gerar_grade_do_zero()
        
        # Remover aulas repetidas primeiro
        aulas_atuais = remover_aulas_repetidas(aulas_atuais)
        
        # Corrigir superposições de professor
        superposicoes = verificar_professor_superposto(aulas_atuais)
        if superposicoes:
            aulas_atuais = corrigir_superposicoes_professor(aulas_atuais, superposicoes)
        
        # Converter para formato consistente
        aulas = self._converter_para_dict(aulas_atuais)
        
        # Verificar e corrigir conflitos primeiro
        conflitos = self._verificar_conflitos(aulas)
        if conflitos:
            aulas = self._corrigir_conflitos_internos(aulas, conflitos)
        
        # Verificar limites de professores
        limites_excedidos = self._verificar_limites_professores(aulas)
        if limites_excedidos:
            aulas = self._corrigir_limites_professores(aulas, limites_excedidos)
        
        # Analisar estado atual
        analise = self._analisar_estado(aulas)
        
        # Se já está completa, retornar
        if analise['completude'] == 100:
            return self._converter_para_aulas(aulas)
        
        # Tentar múltiplas estratégias
        estrategias = [
            self._estrategia_preencher_buracos,
            self._estrategia_rebalancear_professores,
            self._estrategia_permutar_horarios,
            self._estrategia_busca_local
        ]
        
        for estrategia in estrategias:
            st.info(f"Tentando estratégia: {estrategia.__name__}")
            nova_aulas = estrategia(aulas, analise)
            nova_analise = self._analisar_estado(nova_aulas)
            
            if nova_analise['completude'] > analise['completude']:
                aulas = nova_aulas
                analise = nova_analise
                
                if analise['completude'] == 100:
                    break
        
        # Converter de volta para objetos Aula
        return self._converter_para_aulas(aulas)
    
    def _converter_para_dict(self, aulas):
        """Converte aulas para formato dicionário"""
        aulas_dict = []
        for aula in aulas:
            aulas_dict.append({
                'turma': obter_turma_aula(aula),
                'disciplina': obter_disciplina_aula(aula),
                'professor': obter_professor_aula(aula),
                'dia': obter_dia_aula(aula),
                'horario': obter_horario_aula(aula),
                'segmento': obter_segmento_aula(aula) or obter_segmento_turma(obter_turma_aula(aula))
            })
        return aulas_dict
    
    def _converter_para_aulas(self, aulas_dict):
        """Converte dicionários para objetos Aula"""
        aulas_objetos = []
        for aula in aulas_dict:
            aulas_objetos.append(Aula(
                turma=aula['turma'],
                disciplina=aula['disciplina'],
                professor=aula['professor'],
                dia=aula['dia'],
                horario=aula['horario'],
                segmento=aula['segmento']
            ))
        return aulas_objetos
    
    def _verificar_conflitos(self, aulas):
        """Verifica conflitos internos"""
        conflitos = []
        horarios_por_turma = {}
        
        for aula in aulas:
            chave = f"{aula['turma']}|{aula['dia']}|{aula['horario']}"
            if chave not in horarios_por_turma:
                horarios_por_turma[chave] = []
            horarios_por_turma[chave].append(aula)
            
            if len(horarios_por_turma[chave]) > 1:
                conflitos.append({
                    'chave': chave,
                    'aulas': horarios_por_turma[chave].copy()
                })
        
        return conflitos
    
    def _verificar_limites_professores(self, aulas):
        """Verifica se professores excederam limites"""
        problemas = []
        
        for professor in self.professores:
            # Contar aulas do professor
            aulas_prof = len([a for a in aulas if a['professor'] == professor.nome])
            
            # Obter limite
            limite = obter_limite_horas_professor(professor)
            
            if aulas_prof > limite:
                problemas.append({
                    'professor': professor,
                    'aulas_atual': aulas_prof,
                    'limite': limite
                })
        
        return problemas
    
    def _corrigir_conflitos_internos(self, aulas, conflitos):
        """Corrige conflitos internos no algoritmo"""
        aulas_corrigidas = aulas.copy()
        
        for conflito in conflitos:
            turma = conflito['aulas'][0]['turma']
            dia = conflito['aulas'][0]['dia']
            horario_conflito = conflito['aulas'][0]['horario']
            
            # Encontrar horários possíveis
            segmento = obter_segmento_turma(turma)
            if segmento == "EM":
                horarios_possiveis = list(range(1, 8))
            else:
                horarios_possiveis = list(range(1, 6))
            
            # Encontrar horários ocupados
            horarios_ocupados = set()
            for aula in aulas_corrigidas:
                if aula['turma'] == turma and aula['dia'] == dia:
                    horarios_ocupados.add(aula['horario'])
            
            # Para cada aula conflitante (exceto a primeira)
            for i, aula in enumerate(aulas_corrigidas):
                if aula['turma'] == turma and aula['dia'] == dia and aula['horario'] == horario_conflito:
                    # Se não for a primeira ocorrência, tentar mover
                    encontrou_primeira = False
                    for j, a in enumerate(aulas_corrigidas):
                        if a['turma'] == turma and a['dia'] == dia and a['horario'] == horario_conflito:
                            if j == i:
                                encontrou_primeira = True
                            elif encontrou_primeira:
                                # Encontrar horário livre
                                for h in horarios_possiveis:
                                    if h not in horarios_ocupados:
                                        aulas_corrigidas[i]['horario'] = h
                                        horarios_ocupados.add(h)
                                        break
        
        return aulas_corrigidas
    
    def _corrigir_limites_professores(self, aulas, limites_excedidos):
        """Corrige professores que excederam limites"""
        aulas_corrigidas = aulas.copy()
        
        for problema in limites_excedidos:
            professor = problema['professor']
            limite = problema['limite']
            aulas_atual = problema['aulas_atual']
            
            # Encontrar aulas deste professor
            aulas_prof = [a for a in aulas_corrigidas if a['professor'] == professor.nome]
            
            # Se excedeu limite, remover aulas mais recentes
            if aulas_atual > limite:
                # Ordenar aulas por turma/disciplina menos crítica
                aulas_para_remover = aulas_atual - limite
                
                # Remover as últimas aulas alocadas
                for i in range(len(aulas_corrigidas)-1, -1, -1):
                    if aulas_corrigidas[i]['professor'] == professor.nome and aulas_para_remover > 0:
                        aulas_corrigidas.pop(i)
                        aulas_para_remover -= 1
        
        return aulas_corrigidas
    
    def _analisar_estado(self, aulas):
        """Analisa o estado atual da grade"""
        analise = {
            'completude': 0,
            'total_necessario': 0,
            'total_alocado': len(aulas),
            'faltas_por_turma': {},
            'horarios_livres_por_turma': {},
            'professores_carga': {},
            'professores_limite': {}
        }
        
        # Calcular total necessário
        for turma in self.turmas:
            turma_nome = turma.nome
            grupo_turma = turma.grupo
            
            aulas_necessarias = 0
            for disc in self.disciplinas:
                if turma_nome in disc.turmas and obter_grupo_seguro(disc) == grupo_turma:
                    aulas_necessarias += disc.carga_semanal
            
            analise['total_necessario'] += aulas_necessarias
            
            # Contar aulas alocadas
            aulas_turma = [a for a in aulas if a['turma'] == turma_nome]
            
            # Calcular horários livres
            horarios_turma = obter_horarios_turma(turma_nome)
            horarios_ocupados = set()
            for aula in aulas_turma:
                horarios_ocupados.add((aula['dia'], aula['horario']))
            
            horarios_livres = []
            for dia in self.dias:
                for horario in horarios_turma:
                    if (dia, horario) not in horarios_ocupados:
                        horarios_livres.append((dia, horario))
            
            analise['horarios_livres_por_turma'][turma_nome] = horarios_livres
            
            # Calcular faltas
            faltas = []
            for disc in self.disciplinas:
                if turma_nome in disc.turmas and obter_grupo_seguro(disc) == grupo_turma:
                    aulas_disc = len([a for a in aulas_turma if a['disciplina'] == disc.nome])
                    if aulas_disc < disc.carga_semanal:
                        faltas.append({
                            'disciplina': disc.nome,
                            'faltam': disc.carga_semanal - aulas_disc,
                            'prioridade': self._calcular_prioridade(disc.nome, grupo_turma)
                        })
            
            analise['faltas_por_turma'][turma_nome] = faltas
        
        # Calcular completude
        if analise['total_necessario'] > 0:
            analise['completude'] = (analise['total_alocado'] / analise['total_necessario']) * 100
        
        # Calcular carga e limite dos professores
        for professor in self.professores:
            aulas_prof = len([a for a in aulas if a['professor'] == professor.nome])
            analise['professores_carga'][professor.nome] = aulas_prof
            analise['professores_limite'][professor.nome] = obter_limite_horas_professor(professor)
        
        return analise
    
    def _calcular_prioridade(self, disciplina, grupo):
        """Calcula prioridade para alocação"""
        # Contar professores disponíveis
        professores_disponiveis = 0
        professores_livres = 0
        
        for prof in self.professores:
            if disciplina in prof.disciplinas:
                if prof.grupo in [grupo, "AMBOS"]:
                    professores_disponiveis += 1
                    # Verificar se não está comprometido
                    if not verificar_professor_comprometido(prof, disciplina, grupo):
                        professores_livres += 1
        
        # Quanto menos professores livres, maior a prioridade
        return (10 - professores_livres) * 2 + (5 - professores_disponiveis)
    
    def _estrategia_preencher_buracos(self, aulas, analise):
        """Preenche buracos óbvios na grade"""
        nova_grade = aulas.copy()
        
        # Ordenar turmas por número de faltas
        turmas_ordenadas = []
        for turma_nome, faltas in analise['faltas_por_turma'].items():
            if faltas:
                turmas_ordenadas.append((turma_nome, len(faltas)))
        
        turmas_ordenadas.sort(key=lambda x: x[1], reverse=True)
        
        for turma_nome, _ in turmas_ordenadas:
            faltas = analise['faltas_por_turma'].get(turma_nome, [])
            horarios_livres = analise['horarios_livres_por_turma'].get(turma_nome, [])
            
            # Ordenar faltas por prioridade
            faltas_ordenadas = sorted(faltas, key=lambda x: x['prioridade'])
            
            for falta in faltas_ordenadas:
                disciplina = falta['disciplina']
                
                # Encontrar professores LIVRES (não comprometidos)
                professores_candidatos = []
                turma_obj = next((t for t in self.turmas if t.nome == turma_nome), None)
                grupo_turma = turma_obj.grupo if turma_obj else 'A'
                
                for prof in self.professores:
                    if disciplina in prof.disciplinas:
                        if prof.grupo in [grupo_turma, "AMBOS"]:
                            # Verificar se não está comprometido
                            if not verificar_professor_comprometido(prof, disciplina, grupo_turma):
                                # Verificar limite do professor
                                carga_atual = analise['professores_carga'].get(prof.nome, 0)
                                limite = analise['professores_limite'].get(prof.nome, 35)
                                
                                if carga_atual < limite:
                                    professores_candidatos.append(prof)
                
                # Ordenar professores por carga (menos carregado primeiro)
                professores_candidatos.sort(key=lambda p: analise['professores_carga'].get(p.nome, 0))
                
                # Tentar cada horário livre
                for dia, horario in horarios_livres:
                    # Verificar se já alocou todas as faltas desta disciplina
                    if falta['faltam'] <= 0:
                        break
                    
                    # Tentar cada professor
                    for professor in professores_candidatos:
                        # Verificar disponibilidade do professor
                        if self._professor_disponivel(nova_grade, professor.nome, dia, horario):
                            # Verificar se não está bloqueado
                            if f"{dia}_{horario}" in professor.horarios_indisponiveis:
                                continue
                            
                            # Verificar limite do professor
                            carga_atual = analise['professores_carga'].get(professor.nome, 0)
                            limite = analise['professores_limite'].get(professor.nome, 35)
                            
                            if carga_atual >= limite:
                                continue  # Professor já atingiu limite
                            
                            # Alocar aula
                            nova_grade.append({
                                'turma': turma_nome,
                                'disciplina': disciplina,
                                'professor': professor.nome,
                                'dia': dia,
                                'horario': horario,
                                'segmento': obter_segmento_turma(turma_nome)
                            })
                            
                            # Atualizar contadores
                            falta['faltam'] -= 1
                            horarios_livres.remove((dia, horario))
                            analise['professores_carga'][professor.nome] = analise['professores_carga'].get(professor.nome, 0) + 1
                            break
                    
                    if falta['faltam'] <= 0:
                        break
        
        return nova_grade
    
    def _estrategia_rebalancear_professores(self, aulas, analise):
        """Rebalanceia carga entre professores"""
        nova_grade = aulas.copy()
        
        # Encontrar professores sobrecarregados
        professores_sobrecarregados = []
        for nome, carga in analise['professores_carga'].items():
            professor_obj = next((p for p in self.professores if p.nome == nome), None)
            if professor_obj:
                limite = analise['professores_limite'].get(nome, 35)
                
                if carga > limite * 0.9:  # Mais de 90% do limite
                    professores_sobrecarregados.append((nome, carga, limite))
        
        # Ordenar por sobrecarga
        professores_sobrecarregados.sort(key=lambda x: x[1] / x[2] if x[2] > 0 else 0, reverse=True)
        
        for prof_nome, carga, limite in professores_sobrecarregados[:3]:  # Apenas os 3 mais sobrecarregados
            # Encontrar aulas deste professor
            aulas_prof = [a for a in nova_grade if a['professor'] == prof_nome]
            
            for aula in aulas_prof:
                disciplina = aula['disciplina']
                turma_nome = aula['turma']
                
                # Encontrar professores alternativos LIVRES
                professores_alternativos = []
                turma_obj = next((t for t in self.turmas if t.nome == turma_nome), None)
                grupo_turma = turma_obj.grupo if turma_obj else 'A'
                
                for prof in self.professores:
                    if prof.nome != prof_nome and disciplina in prof.disciplinas:
                        if prof.grupo in [grupo_turma, "AMBOS"]:
                            # Verificar se não está comprometido
                            if not verificar_professor_comprometido(prof, disciplina, grupo_turma):
                                # Verificar disponibilidade no mesmo horário
                                if self._professor_disponivel(nova_grade, prof.nome, aula['dia'], aula['horario']):
                                    if f"{aula['dia']}_{aula['horario']}" not in prof.horarios_indisponiveis:
                                        # Verificar limite do professor
                                        carga_alternativo = analise['professores_carga'].get(prof.nome, 0)
                                        limite_alternativo = analise['professores_limite'].get(prof.nome, 35)
                                        
                                        if carga_alternativo < limite_alternativo:
                                            professores_alternativos.append(prof)
                
                # Se encontrou alternativo, transferir
                if professores_alternativos:
                    # Escolher o menos carregado
                    professores_alternativos.sort(key=lambda p: analise['professores_carga'].get(p.nome, 0))
                    novo_professor = professores_alternativos[0]
                    
                    # Atualizar aula
                    for i, a in enumerate(nova_grade):
                        if (a['turma'] == turma_nome and a['disciplina'] == disciplina and 
                            a['dia'] == aula['dia'] and a['horario'] == aula['horario']):
                            nova_grade[i]['professor'] = novo_professor.nome
                            break
                    
                    # Atualizar cargas
                    analise['professores_carga'][prof_nome] -= 1
                    analise['professores_carga'][novo_professor.nome] = analise['professores_carga'].get(novo_professor.nome, 0) + 1
                    break
        
        return nova_grade
    
    def _estrategia_permutar_horarios(self, aulas, analise):
        """Permuta horários para criar espaços"""
        nova_grade = aulas.copy()
        
        # Para cada turma com faltas
        for turma_nome, faltas in analise['faltas_por_turma'].items():
            if not faltas:
                continue
            
            # Encontrar aulas desta turma
            aulas_turma = [a for a in nova_grade if a['turma'] == turma_nome]
            
            # Tentar permutar com outras turmas
            for aula in aulas_turma:
                # Encontrar outra aula em horário diferente
                for outra_aula in nova_grade:
                    if outra_aula['turma'] != turma_nome:
                        # Tentar trocar horários
                        if self._permutacao_valida(nova_grade, aula, outra_aula):
                            # Realizar troca
                            dia_temp = aula['dia']
                            horario_temp = aula['horario']
                            
                            aula['dia'] = outra_aula['dia']
                            aula['horario'] = outra_aula['horario']
                            
                            outra_aula['dia'] = dia_temp
                            outra_aula['horario'] = horario_temp
        
        return nova_grade
    
    def _estrategia_busca_local(self, aulas, analise):
        """Busca local por melhorias"""
        melhor_grade = aulas.copy()
        melhor_completude = analise['completude']
        
        for _ in range(50):  # 50 iterações
            grade_tentativa = melhor_grade.copy()
            
            # Aplicar operação aleatória
            operacao = random.choice(['mover', 'trocar', 'realocar'])
            
            if operacao == 'mover' and len(grade_tentativa) > 0:
                # Mover uma aula para horário livre
                aula_idx = random.randrange(len(grade_tentativa))
                aula = grade_tentativa[aula_idx]
                
                turma_nome = aula['turma']
                horarios_livres = analise['horarios_livres_por_turma'].get(turma_nome, [])
                
                if horarios_livres:
                    novo_dia, novo_horario = random.choice(horarios_livres)
                    
                    # Verificar se professor está disponível
                    if self._professor_disponivel(grade_tentativa, aula['professor'], novo_dia, novo_horario):
                        grade_tentativa[aula_idx]['dia'] = novo_dia
                        grade_tentativa[aula_idx]['horario'] = novo_horario
            
            elif operacao == 'trocar' and len(grade_tentativa) >= 2:
                # Trocar duas aulas de lugar
                idx1, idx2 = random.sample(range(len(grade_tentativa)), 2)
                aula1 = grade_tentativa[idx1]
                aula2 = grade_tentativa[idx2]
                
                # Verificar se troca é válida
                if (self._professor_disponivel(grade_tentativa, aula1['professor'], aula2['dia'], aula2['horario']) and
                    self._professor_disponivel(grade_tentativa, aula2['professor'], aula1['dia'], aula1['horario'])):
                    
                    # Trocar horários
                    dia_temp = aula1['dia']
                    horario_temp = aula1['horario']
                    
                    grade_tentativa[idx1]['dia'] = aula2['dia']
                    grade_tentativa[idx1]['horario'] = aula2['horario']
                    
                    grade_tentativa[idx2]['dia'] = dia_temp
                    grade_tentativa[idx2]['horario'] = horario_temp
            
            # Evaluar nova grade
            nova_analise = self._analisar_estado(grade_tentativa)
            
            if nova_analise['completude'] > melhor_completude:
                melhor_grade = grade_tentativa
                melhor_completude = nova_analise['completude']
        
        return melhor_grade
    
    def _professor_disponivel(self, grade, professor_nome, dia, horario):
        """Verifica se professor está disponível em determinado horário"""
        for aula in grade:
            if aula['professor'] == professor_nome:
                if aula['dia'] == dia and aula['horario'] == horario:
                    return False
        return True
    
    def _permutacao_valida(self, grade, aula1, aula2):
        """Verifica se permutação entre duas aulas é válida"""
        # Verificar disponibilidade dos professores nos novos horários
        prof1_livre = self._professor_disponivel(grade, aula1['professor'], aula2['dia'], aula2['horario'])
        prof2_livre = self._professor_disponivel(grade, aula2['professor'], aula1['dia'], aula1['horario'])
        
        # Verificar se turmas estão livres nos novos horários
        turma1_livre = True
        turma2_livre = True
        
        for aula in grade:
            if aula['turma'] == aula1['turma']:
                if aula['dia'] == aula2['dia'] and aula['horario'] == aula2['horario']:
                    turma1_livre = False
            
            if aula['turma'] == aula2['turma']:
                if aula['dia'] == aula1['dia'] and aula['horario'] == aula1['horario']:
                    turma2_livre = False
        
        return prof1_livre and prof2_livre and turma1_livre and turma2_livre
    
    def _gerar_grade_do_zero(self):
        """Gera uma grade completa do zero"""
        try:
            simple_grade = SimpleGradeHoraria(
                turmas=self.turmas,
                professores=self.professores,
                disciplinas=self.disciplinas,
                salas=[]
            )
            
            return simple_grade.gerar_grade()
        except:
            return []

# ============================================
# FUNÇÕES ADICIONAIS
# ============================================

def salvar_grade_como(nome, aulas, config):
    """Salva uma grade com um nome específico"""
    if not hasattr(st.session_state, 'grades_salvas'):
        st.session_state.grades_salvas = {}
    
    # Converter para dicionários
    aulas_dict = []
    for aula in aulas:
        if isinstance(aula, Aula):
            aulas_dict.append({
                'turma': aula.turma,
                'disciplina': aula.disciplina,
                'professor': aula.professor,
                'dia': aula.dia,
                'horario': aula.horario,
                'segmento': aula.segmento if hasattr(aula, 'segmento') else obter_segmento_turma(aula.turma)
            })
        elif isinstance(aula, dict):
            aulas_dict.append(aula)
        else:
            aulas_dict.append({
                'turma': obter_turma_aula(aula),
                'disciplina': obter_disciplina_aula(aula),
                'professor': obter_professor_aula(aula),
                'dia': obter_dia_aula(aula),
                'horario': obter_horario_aula(aula),
                'segmento': obter_segmento_aula(aula)
            })
    
    st.session_state.grades_salvas[nome] = {
        'aulas': aulas_dict,
        'config': config,
        'data': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'total_aulas': len(aulas_dict)
    }
    
    return True
