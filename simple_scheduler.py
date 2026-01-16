import streamlit as st
import random
from datetime import datetime

class SimpleGradeHoraria:
    """Algoritmo simples para geração de grade horária"""
    
    def __init__(self, turmas, professores, disciplinas, salas):
        self.turmas = turmas
        self.professores = professores
        self.disciplinas = disciplinas
        self.salas = salas
        self.dias = ['segunda', 'terca', 'quarta', 'quinta', 'sexta']
        self.max_iteracoes = 1000
    
    def _obter_horario_real(self, turma_nome, periodo):
        """Converte período da turma para horário real (hh:mm)"""
        # Mapear períodos para horários reais
        if 'em' in turma_nome.lower():
            # Ensino Médio: 07:00-13:10
            horarios_em = {
                1: "07:00",
                2: "07:50",
                3: "08:40",
                4: "09:50",  # Após intervalo
                5: "10:40",
                6: "11:30",
                7: "12:20"
            }
            return horarios_em.get(periodo, "00:00")
        else:
            # EF II: 07:50-12:20
            horarios_efii = {
                1: "07:50",
                2: "08:40",
                3: "09:50",  # Após intervalo
                4: "10:40",
                5: "11:30"
            }
            return horarios_efii.get(periodo, "00:00")
    
    def gerar_grade(self):
        """Gera uma grade horária simples SEM CONFLITOS de professores"""
        try:
            st.info("🎯 Iniciando geração de grade horária (algoritmo corrigido v2)...")
            
            # Inicializar lista de aulas
            aulas = []
            
            # Dicionário para rastrear ocupação de professores por HORÁRIO REAL
            # {professor_nome: {(dia, "HH:MM")}}
            professores_ocupacao = {}
            for prof in self.professores:
                professores_ocupacao[prof.nome] = set()
            
            # Ordenar turmas por dificuldade (EM primeiro - tem mais períodos e é mais restritivo)
            turmas_ordenadas = sorted(self.turmas, key=lambda t: 1 if 'em' in t.nome.lower() else 0)
            
            # Para cada turma
            for turma in turmas_ordenadas:
                turma_nome = turma.nome
                grupo_turma = turma.grupo
                
                # Determinar horários disponíveis para esta turma
                if 'em' in turma_nome.lower():
                    periodos = list(range(1, 8))  # 7 períodos para EM
                else:
                    periodos = list(range(1, 6))  # 5 períodos para EF II
                
                # Obter disciplinas desta turma
                disciplinas_turma = []
                for disc in self.disciplinas:
                    if turma_nome in disc.turmas and self._obter_grupo(disc) == grupo_turma:
                        for _ in range(disc.carga_semanal):
                            disciplinas_turma.append(disc)
                
                if not disciplinas_turma:
                    st.warning(f"⚠️ Turma {turma_nome} não tem disciplinas!")
                    continue
                
                # Embaralhar disciplinas para distribuição
                random.shuffle(disciplinas_turma)
                
                # Criar grid de horários disponíveis para esta turma
                horarios_turma_ocupados = set()
                
                # Tentar alocar cada disciplina
                for disciplina in disciplinas_turma:
                    alocada = False
                    
                    # Criar lista de todos os horários possíveis e embaralhar
                    todos_horarios = [(dia, periodo) for dia in self.dias for periodo in periodos]
                    random.shuffle(todos_horarios)
                    
                    # Tentar cada horário possível
                    for dia, horario in todos_horarios:
                        # 1. Verificar se turma já tem aula neste horário
                        if (dia, horario) in horarios_turma_ocupados:
                            continue
                        
                        # CONVERTER PERÍODO PARA HORÁRIO REAL
                        horario_real = self._obter_horario_real(turma_nome, horario)
                        
                        # 2. Encontrar professores DISPONÍVEIS para esta disciplina
                        professores_candidatos = []
                        for prof in self.professores:
                            if disciplina.nome in prof.disciplinas:
                                if prof.grupo in [grupo_turma, "AMBOS"]:
                                    # Verificar disponibilidade do dia
                                    if dia in prof.disponibilidade:
                                        # VERIFICAÇÃO CRÍTICA: Professor não pode estar ocupado neste HORÁRIO REAL
                                        if (dia, horario_real) not in professores_ocupacao[prof.nome]:
                                            # Verificar horários indisponíveis
                                            horario_str = f"{dia}_{horario}"
                                            if hasattr(prof, 'horarios_indisponiveis'):
                                                if horario_str in prof.horarios_indisponiveis:
                                                    continue
                                            
                                            # Verificar limite de horas do professor
                                            carga_atual = self._contar_aulas_professor(prof.nome, aulas)
                                            limite = self._obter_limite_professor(prof)
                                            
                                            if carga_atual < limite:
                                                professores_candidatos.append(prof)
                        
                        if not professores_candidatos:
                            continue
                        
                        # Ordenar professores por carga atual (menos carregado primeiro)
                        professores_candidatos.sort(key=lambda p: self._contar_aulas_professor(p.nome, aulas))
                        
                        # Selecionar o melhor professor
                        professor_selecionado = professores_candidatos[0]
                        
                        # Criar aula
                        aula = type('Aula', (), {})()
                        aula.turma = turma_nome
                        aula.disciplina = disciplina.nome
                        aula.professor = professor_selecionado.nome
                        aula.dia = dia
                        aula.horario = horario
                        aula.segmento = 'EM' if 'em' in turma_nome.lower() else 'EF_II'
                        
                        # Adicionar aula
                        aulas.append(aula)
                        
                        # Marcar horário como ocupado
                        # Para turma: usar período relativo
                        horarios_turma_ocupados.add((dia, horario))
                        # Para professor: usar HORÁRIO REAL
                        professores_ocupacao[professor_selecionado.nome].add((dia, horario_real))
                        
                        alocada = True
                        break
                    
                    if not alocada:
                        st.warning(f"⚠️ Não foi possível alocar {disciplina.nome} para {turma_nome}")
            
            # VERIFICAÇÃO FINAL: Detectar conflitos residuais
            conflitos_finais = self._verificar_conflitos_professores(aulas)
            
            if conflitos_finais:
                st.error(f"❌ ATENÇÃO: {len(conflitos_finais)} conflitos de professores detectados!")
                for conflito in conflitos_finais[:3]:
                    st.write(f"  - {conflito}")
            else:
                st.success(f"✅ Grade gerada com {len(aulas)} aulas SEM CONFLITOS!")
            
            return aulas
            
        except Exception as e:
            st.error(f"❌ Erro ao gerar grade: {str(e)}")
            import traceback
            st.code(traceback.format_exc())
            return []
    
    def _obter_grupo(self, objeto):
        """Obtém o grupo de um objeto de forma segura"""
        try:
            if hasattr(objeto, 'grupo'):
                grupo = objeto.grupo
                if grupo in ["A", "B", "AMBOS"]:
                    return grupo
            return "A"
        except:
            return "A"
    
    def _contar_aulas_professor(self, professor_nome, aulas):
        """Conta quantas aulas um professor já tem"""
        count = 0
        for aula in aulas:
            if hasattr(aula, 'professor') and aula.professor == professor_nome:
                count += 1
        return count
    
    def _obter_limite_professor(self, professor):
        """Retorna o limite de horas do professor baseado no segmento"""
        # Determinar segmento do professor
        tem_efii = False
        tem_em = False
        
        for disc_nome in professor.disciplinas:
            for disc in self.disciplinas:
                if disc.nome == disc_nome:
                    for turma_nome in disc.turmas:
                        if 'em' in turma_nome.lower():
                            tem_em = True
                        else:
                            tem_efii = True
        
        # Limites
        LIMITE_HORAS_EFII = 25
        LIMITE_HORAS_EM = 35
        
        if tem_efii and not tem_em:
            return LIMITE_HORAS_EFII
        elif tem_em and not tem_efii:
            return LIMITE_HORAS_EM
        else:
            return LIMITE_HORAS_EM  # Usar limite maior para professores de ambos
    
    def _verificar_conflitos_professores(self, aulas):
        """Verifica se há professores em dois lugares ao mesmo tempo (usando horário real)"""
        conflitos = []
        
        # Criar dicionário de professores por horário REAL
        professores_por_horario = {}
        
        for aula in aulas:
            if not hasattr(aula, 'professor') or not hasattr(aula, 'dia') or not hasattr(aula, 'horario'):
                continue
            
            if not hasattr(aula, 'turma'):
                continue
            
            # Converter período para horário real
            horario_real = self._obter_horario_real(aula.turma, aula.horario)
            
            # Usar horário real na chave
            chave = f"{aula.professor}|{aula.dia}|{horario_real}"
            
            if chave not in professores_por_horario:
                professores_por_horario[chave] = []
            
            professores_por_horario[chave].append({
                'turma': aula.turma,
                'disciplina': aula.disciplina if hasattr(aula, 'disciplina') else '?',
                'periodo': aula.horario,
                'segmento': aula.segmento if hasattr(aula, 'segmento') else '?'
            })
        
        # Detectar conflitos
        for chave, aulas_info in professores_por_horario.items():
            if len(aulas_info) > 1:
                partes = chave.split('|')
                professor = partes[0]
                dia = partes[1]
                horario_real = partes[2]
                
                detalhes = []
                for info in aulas_info:
                    detalhes.append(f"{info['turma']}({info['segmento']}-{info['periodo']}º)")
                
                conflitos.append(
                    f"Professor {professor} em {' E '.join(detalhes)} no {dia} às {horario_real}"
                )
        
        return conflitos