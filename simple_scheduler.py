import streamlit as st
import random
from datetime import datetime
from collections import defaultdict

class SimpleGradeHoraria:
    """Algoritmo otimizado para geração de grade horária com compactação máxima"""
    
    def __init__(self, turmas, professores, disciplinas, salas):
        self.turmas = turmas
        self.professores = professores
        self.disciplinas = disciplinas
        self.salas = salas
        self.dias = ['segunda', 'terca', 'quarta', 'quinta', 'sexta']
        self.max_iteracoes = 1000
    
    def _obter_horario_real(self, turma_nome, periodo):
        """Converte período da turma para horário real (hh:mm)"""
        if 'em' in turma_nome.lower():
            # Ensino Médio: 07:00-13:10
            horarios_em = {
                1: "07:00", 2: "07:50", 3: "08:40",
                4: "09:50", 5: "10:40", 6: "11:30", 7: "12:20"
            }
            return horarios_em.get(periodo, "00:00")
        else:
            # EF II: 07:50-12:20
            horarios_efii = {
                1: "07:50", 2: "08:40", 3: "09:50",
                4: "10:40", 5: "11:30"
            }
            return horarios_efii.get(periodo, "00:00")
    
    def gerar_grade(self):
        """Gera grade horária otimizada com compactação máxima e distribuição uniforme"""
        try:
            st.info("🎯 Iniciando geração de grade horária otimizada (v4 - compactação máxima)...")
            
            # Inicializar estruturas
            aulas = []
            # Rastrear ocupação de professores por (dia, horario_real)
            # para evitar que um professor esteja em 2 lugares ao mesmo tempo
            professores_ocupacao = {prof.nome: set() for prof in self.professores}
            
            # Estatísticas para monitoramento
            tentativas_por_turma = {}
            
            # Ordenar turmas: EM primeiro (mais restritivo), depois EF
            turmas_ordenadas = sorted(self.turmas, 
                                     key=lambda t: (0 if 'em' in t.nome.lower() else 1, t.nome))
            
            st.write(f"📚 Processando {len(turmas_ordenadas)} turmas...")
            
            # Para cada turma
            for idx_turma, turma in enumerate(turmas_ordenadas):
                turma_nome = turma.nome
                
                # Determinar períodos disponíveis
                if 'em' in turma_nome.lower():
                    periodos = list(range(1, 8))  # 7 períodos
                    limite_turma = 35
                else:
                    periodos = list(range(1, 6))  # 5 períodos
                    limite_turma = 25
                
                # Obter disciplinas com carga específica
                disciplinas_turma = []
                for disc in self.disciplinas:
                    if turma_nome in disc.turmas:
                        carga = disc.obter_carga_turma(turma_nome)
                        
                        # Obter professor pré-atribuído
                        professor_atribuido = None
                        if hasattr(disc, 'professor_por_turma') and turma_nome in disc.professor_por_turma:
                            professor_atribuido = disc.professor_por_turma[turma_nome]
                        
                        for _ in range(carga):
                            disciplinas_turma.append({
                                'disciplina': disc,
                                'professor_atribuido': professor_atribuido
                            })
                
                if not disciplinas_turma:
                    st.warning(f"⚠️ Turma {turma_nome} não tem disciplinas!")
                    continue
                
                # ESTRATÉGIA 1: Agrupar disciplinas por professor para facilitar compactação
                disciplinas_por_professor = defaultdict(list)
                disciplinas_sem_professor = []
                
                for item in disciplinas_turma:
                    if item['professor_atribuido']:
                        disciplinas_por_professor[item['professor_atribuido']].append(item)
                    else:
                        disciplinas_sem_professor.append(item)
                
                # ESTRATÉGIA 2: Distribuir uniformemente pelos dias
                # Calcular quantas aulas por dia em média
                total_aulas = len(disciplinas_turma)
                aulas_por_dia_ideal = total_aulas / len(self.dias)
                
                # Criar grid de ocupação da turma
                horarios_turma = {dia: set() for dia in self.dias}
                
                # ESTRATÉGIA 3: Alocar por professor (para compactar)
                aulas_alocadas_turma = 0
                tentativas = 0
                max_tentativas = 1000
                
                # Ordenar professores por quantidade de aulas (maior primeiro)
                professores_ordenados = sorted(
                    disciplinas_por_professor.items(),
                    key=lambda x: len(x[1]),
                    reverse=True
                )
                
                # Alocar disciplinas com professor atribuído
                for professor_nome, items_prof in professores_ordenados:
                    # Encontrar objeto professor
                    prof_obj = next((p for p in self.professores if p.nome == professor_nome), None)
                    
                    if not prof_obj:
                        st.warning(f"⚠️ Professor {professor_nome} não encontrado!")
                        continue
                    
                    # Alocar todas as aulas deste professor de uma vez
                    for item in items_prof:
                        alocada = False
                        
                        # Estratégia: tentar dias com menos aulas primeiro (distribuição uniforme)
                        dias_ordenados = sorted(self.dias, 
                                               key=lambda d: len(horarios_turma[d]))
                        
                        # Para cada dia
                        for dia in dias_ordenados:
                            # Verificar disponibilidade do professor no dia
                            if dia not in prof_obj.disponibilidade:
                                continue
                            
                            # Verificar se dia não está cheio
                            if len(horarios_turma[dia]) >= len(periodos):
                                continue
                            
                            # Tentar períodos em sequência (compactação)
                            for periodo in periodos:
                                if periodo in horarios_turma[dia]:
                                    continue
                                
                                # Converter para horário real
                                horario_real = self._obter_horario_real(turma_nome, periodo)
                                
                                # Verificar se professor já está ocupado neste horário
                                if (dia, horario_real) in professores_ocupacao[professor_nome]:
                                    continue
                                
                                # Verificar limite do professor
                                carga_atual = self._contar_aulas_professor(professor_nome, aulas)
                                limite_prof = self._obter_limite_professor(prof_obj)
                                
                                if carga_atual >= limite_prof:
                                    break  # Professor está no limite
                                
                                # ALOCAR AULA
                                aula = type('Aula', (), {})()
                                aula.turma = turma_nome
                                aula.disciplina = item['disciplina'].nome
                                aula.professor = professor_nome
                                aula.dia = dia
                                aula.horario = periodo
                                aula.segmento = 'EM' if 'em' in turma_nome.lower() else 'EF_II'
                                
                                aulas.append(aula)
                                horarios_turma[dia].add(periodo)
                                professores_ocupacao[professor_nome].add((dia, horario_real))
                                
                                alocada = True
                                aulas_alocadas_turma += 1
                                break
                            
                            if alocada:
                                break
                        
                        if not alocada:
                            st.warning(f"⚠️ Não foi possível alocar {item['disciplina'].nome} para {turma_nome} (professor {professor_nome})")
                
                # Alocar disciplinas sem professor atribuído
                for item in disciplinas_sem_professor:
                    alocada = False
                    disc = item['disciplina']
                    
                    # Dias ordenados por ocupação
                    dias_ordenados = sorted(self.dias, key=lambda d: len(horarios_turma[d]))
                    
                    for dia in dias_ordenados:
                        if len(horarios_turma[dia]) >= len(periodos):
                            continue
                        
                        for periodo in periodos:
                            if periodo in horarios_turma[dia]:
                                continue
                            
                            # Converter para horário real
                            horario_real = self._obter_horario_real(turma_nome, periodo)
                            
                            # Buscar professores disponíveis
                            professores_disponiveis = []
                            
                            for prof in self.professores:
                                if disc.nome in prof.disciplinas:
                                    if dia in prof.disponibilidade:
                                        # Verificar se professor não está ocupado neste horário
                                        if (dia, horario_real) not in professores_ocupacao[prof.nome]:
                                            carga_atual = self._contar_aulas_professor(prof.nome, aulas)
                                            limite_prof = self._obter_limite_professor(prof)
                                            
                                            if carga_atual < limite_prof:
                                                # Contar aulas do professor neste dia (para compactação)
                                                aulas_prof_dia = sum(1 for a in aulas 
                                                                   if hasattr(a, 'professor') and a.professor == prof.nome 
                                                                   and hasattr(a, 'dia') and a.dia == dia)
                                                professores_disponiveis.append((prof, aulas_prof_dia))
                            
                            if not professores_disponiveis:
                                continue
                            
                            # Priorizar professores que já têm aulas no dia (compactação)
                            professores_ordenados = sorted(
                                professores_disponiveis,
                                key=lambda x: (-x[1], self._contar_aulas_professor(x[0].nome, aulas))
                            )
                            
                            prof_selecionado = professores_ordenados[0][0]
                            
                            # ALOCAR AULA
                            aula = type('Aula', (), {})()
                            aula.turma = turma_nome
                            aula.disciplina = disc.nome
                            aula.professor = prof_selecionado.nome
                            aula.dia = dia
                            aula.horario = periodo
                            aula.segmento = 'EM' if 'em' in turma_nome.lower() else 'EF_II'
                            
                            aulas.append(aula)
                            horarios_turma[dia].add(periodo)
                            professores_ocupacao[prof_selecionado.nome].add((dia, horario_real))
                            
                            alocada = True
                            aulas_alocadas_turma += 1
                            break
                        
                        if alocada:
                            break
                    
                    if not alocada:
                        st.warning(f"⚠️ Não foi possível alocar {disc.nome} para {turma_nome}")
                
                # Verificar se turma foi completa
                if aulas_alocadas_turma < total_aulas:
                    st.warning(f"⚠️ Turma {turma_nome}: {aulas_alocadas_turma}/{total_aulas} aulas alocadas (faltam {total_aulas - aulas_alocadas_turma})")
                else:
                    # Verificar distribuição pelos dias
                    distribuicao = {dia: len(periodos_dia) for dia, periodos_dia in horarios_turma.items()}
                    dias_vazios = [dia for dia, count in distribuicao.items() if count == 0]
                    
                    if dias_vazios:
                        st.warning(f"⚠️ Turma {turma_nome}: dias vazios - {', '.join(dias_vazios)}")
            
            # VERIFICAÇÃO FINAL
            conflitos_finais = self._verificar_conflitos_professores(aulas)
            limites_excedidos = self._verificar_limites_excedidos(aulas)
            aulas_isoladas = self._analisar_aulas_isoladas(aulas)
            
            # Relatório final
            if conflitos_finais:
                st.error(f"❌ ATENÇÃO: {len(conflitos_finais)} conflitos de professores detectados!")
                for conflito in conflitos_finais[:5]:
                    st.write(f"  - {conflito}")
            
            if limites_excedidos:
                st.error(f"❌ ATENÇÃO: {len(limites_excedidos)} professores excederam limite de horas!")
                for exc in limites_excedidos[:5]:
                    st.write(f"  - {exc}")
            
            if aulas_isoladas:
                st.warning(f"⚠️ COMPACTAÇÃO: {len(aulas_isoladas)} professores com aulas isoladas (1 aula/dia)")
                for alerta in aulas_isoladas[:5]:
                    dias_str = ", ".join(alerta['dias_isolados'])
                    st.write(f"  - **{alerta['professor']}**: 1 aula isolada em {dias_str}")
            
            if not conflitos_finais and not limites_excedidos:
                if aulas_isoladas:
                    st.success(f"✅ Grade gerada com {len(aulas)} aulas SEM CONFLITOS e dentro dos LIMITES!")
                else:
                    st.success(f"✅ Grade PERFEITA com {len(aulas)} aulas: SEM CONFLITOS, LIMITES OK e TOTALMENTE COMPACTADA!")
            
            return aulas
            
        except Exception as e:
            st.error(f"❌ Erro ao gerar grade: {str(e)}")
            import traceback
            st.code(traceback.format_exc())
            return []
    
    def _obter_grupo(self, objeto):
        """DEPRECATED: Compatibilidade"""
        return None
    
    def _contar_aulas_professor(self, professor_nome, aulas):
        """Conta quantas aulas um professor já tem"""
        return sum(1 for aula in aulas if hasattr(aula, 'professor') and aula.professor == professor_nome)
    
    def _obter_limite_professor(self, professor):
        """Retorna o limite de horas do professor"""
        # Usar carga_horaria (que foi sincronizada do PDF)
        if hasattr(professor, 'carga_horaria') and professor.carga_horaria:
            return professor.carga_horaria
        
        # Fallback: calcular por segmento
        tem_em = any('em' in turma.lower() 
                    for disc_nome in professor.disciplinas 
                    for disc in self.disciplinas if disc.nome == disc_nome 
                    for turma in disc.turmas)
        
        return 35 if tem_em else 25
    
    def _verificar_conflitos_professores(self, aulas):
        """Verifica se há professores em dois lugares ao mesmo tempo"""
        conflitos = []
        professores_por_horario = defaultdict(list)
        
        for aula in aulas:
            if not all(hasattr(aula, attr) for attr in ['professor', 'dia', 'horario', 'turma']):
                continue
            
            horario_real = self._obter_horario_real(aula.turma, aula.horario)
            chave = f"{aula.professor}|{aula.dia}|{horario_real}"
            
            professores_por_horario[chave].append({
                'turma': aula.turma,
                'disciplina': aula.disciplina if hasattr(aula, 'disciplina') else '?',
                'periodo': aula.horario
            })
        
        for chave, aulas_info in professores_por_horario.items():
            if len(aulas_info) > 1:
                professor, dia, horario_real = chave.split('|')
                detalhes = [f"{info['turma']} ({info['disciplina']})" for info in aulas_info]
                conflitos.append(f"Professor {professor} em {' E '.join(detalhes)} no {dia} às {horario_real}")
        
        return conflitos
    
    def _verificar_limites_excedidos(self, aulas):
        """Verifica se algum professor excedeu o limite de horas"""
        excedidos = []
        
        for prof in self.professores:
            carga_atual = self._contar_aulas_professor(prof.nome, aulas)
            limite = self._obter_limite_professor(prof)
            
            if carga_atual > limite:
                excedidos.append(
                    f"Professor {prof.nome}: {carga_atual}h alocadas (limite: {limite}h) - EXCESSO: {carga_atual - limite}h"
                )
        
        return excedidos
    
    def _analisar_aulas_isoladas(self, aulas):
        """Analisa professores com aulas isoladas (1 aula/dia)"""
        aulas_por_prof_dia = defaultdict(lambda: defaultdict(int))
        
        for aula in aulas:
            if hasattr(aula, 'professor') and hasattr(aula, 'dia'):
                aulas_por_prof_dia[aula.professor][aula.dia] += 1
        
        alertas = []
        for prof_nome, dias_dict in aulas_por_prof_dia.items():
            dias_com_1_aula = [dia for dia, count in dias_dict.items() if count == 1]
            
            if dias_com_1_aula:
                total_aulas = sum(dias_dict.values())
                total_dias = len([d for d, c in dias_dict.items() if c > 0])
                
                alertas.append({
                    'professor': prof_nome,
                    'dias_isolados': dias_com_1_aula,
                    'total_aulas': total_aulas,
                    'total_dias': total_dias
                })
        
        return alertas
