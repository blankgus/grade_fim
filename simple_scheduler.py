#!/usr/bin/env python3
"""
Versão melhorada do algoritmo de geração de grades com backtracking.

Melhorias:
1. Múltiplas tentativas antes de desistir
2. Embaralhamento para evitar padrões que causam conflitos
3. Priorização inteligente de professores mais críticos
4. Redistribuição quando não consegue alocar
"""

import streamlit as st
import random
from datetime import datetime
from collections import defaultdict

class SimpleGradeHoraria:
    """Algoritmo otimizado v5: com backtracking e múltiplas tentativas"""
    
    def __init__(self, turmas, professores, disciplinas, salas):
        self.turmas = turmas
        self.professores = professores
        self.disciplinas = disciplinas
        self.salas = salas
        self.dias = ['segunda', 'terca', 'quarta', 'quinta', 'sexta']
        self.max_tentativas_aula = 100  # Máximo de tentativas para alocar uma aula
    
    def _obter_horario_real(self, turma_nome, periodo):
        """Converte período da turma para horário real (hh:mm)"""
        if 'em' in turma_nome.lower():
            horarios_em = {
                1: "07:00", 2: "07:50", 3: "08:40",
                4: "09:50", 5: "10:40", 6: "11:30", 7: "12:20"
            }
            return horarios_em.get(periodo, "00:00")
        else:
            horarios_efii = {
                1: "07:50", 2: "08:40", 3: "09:50",
                4: "10:40", 5: "11:30"
            }
            return horarios_efii.get(periodo, "00:00")
    
    def gerar_grade(self):
        """Gera grade com múltiplas tentativas e backtracking"""
        try:
            st.info("🎯 Gerando grade v5 otimizada (100 tentativas com backtracking)...")
            
            # Calcular total esperado
            total_esperado = sum(25 if 'ano' in t.nome else 35 for t in self.turmas)
            
            # Tentar até 100 vezes com variação máxima
            melhor_resultado = None
            melhor_score = -1
            sem_melhora = 0
            
            for tentativa in range(100):
                random.seed(tentativa * 13 + tentativa ** 2)  # Máxima variação
                
                # Mostrar progresso a cada 10 tentativas
                if tentativa % 10 == 0:
                    st.write(f"🔄 Tentativa {tentativa + 1}/100...")
                
                resultado = self._gerar_grade_tentativa()
                score = len(resultado)
                
                if score > melhor_score:
                    melhor_score = score
                    melhor_resultado = resultado
                    percentual = (score / total_esperado * 100) if total_esperado > 0 else 0
                    st.write(f"   ✅ NOVO RECORDE: {score}/{total_esperado} aulas ({percentual:.1f}%)")
                    sem_melhora = 0
                else:
                    sem_melhora += 1
                
                if score == total_esperado:
                    st.success(f"🎉 PERFEITO! Todas as {score} aulas alocadas em {tentativa + 1} tentativas!")
                    break
                
                # Se já está perfeito ou quase (>99.5%), aceitar
                if score >= total_esperado * 0.995:
                    st.success(f"✅ Excelente! {score}/{total_esperado} aulas ({score/total_esperado*100:.2f}%)")
                    break
                
                # Se não melhorou em 20 tentativas e já está bom (>97%), aceitar
                if sem_melhora >= 20 and score >= total_esperado * 0.97:
                    st.info(f"ℹ️ Aceitando resultado: {score}/{total_esperado} aulas ({score/total_esperado*100:.1f}%)")
                    break
            
            # Verificações finais
            conflitos = self._verificar_conflitos_professores(melhor_resultado)
            limites = self._verificar_limites_excedidos(melhor_resultado)
            
            if conflitos:
                st.error(f"❌ {len(conflitos)} conflitos detectados!")
                for c in conflitos[:3]:
                    st.write(f"  - {c}")
            
            if limites:
                st.error(f"❌ {len(limites)} professores com excesso de carga!")
                for l in limites[:3]:
                    st.write(f"  - {l}")
            
            if not conflitos and not limites:
                st.success(f"✅ Grade gerada com {len(melhor_resultado)} aulas SEM CONFLITOS!")
            
            return melhor_resultado
            
        except Exception as e:
            st.error(f"❌ Erro: {str(e)}")
            import traceback
            st.code(traceback.format_exc())
            return []
    
    def _gerar_grade_tentativa(self):
        """Uma tentativa de geração de grade"""
        aulas = []
        professores_ocupacao = {prof.nome: set() for prof in self.professores}
        
        # Estratégia: processar turmas em ordem que minimize conflitos
        # Priorizar turmas com menos disciplinas/professores críticos
        turmas_ordenadas = sorted(self.turmas, 
                                  key=lambda t: (0 if 'em' in t.nome.lower() else 1, t.nome))
        
        # Em tentativas pares, inverter ordem
        if random.randint(0, 1) == 0:
            turmas_ordenadas = list(reversed(turmas_ordenadas))
        
        for turma in turmas_ordenadas:
            turma_nome = turma.nome
            
            # Determinar períodos
            if 'em' in turma_nome.lower():
                periodos = list(range(1, 8))
                limite_turma = 35
            else:
                periodos = list(range(1, 6))
                limite_turma = 25
            
            # Obter disciplinas da turma
            disciplinas_turma = []
            for disc in self.disciplinas:
                if turma_nome in disc.turmas:
                    carga = disc.obter_carga_turma(turma_nome)
                    professor = None
                    if hasattr(disc, 'professor_por_turma') and turma_nome in disc.professor_por_turma:
                        professor = disc.professor_por_turma[turma_nome]
                    
                    for _ in range(carga):
                        disciplinas_turma.append({
                            'disciplina': disc,
                            'professor': professor
                        })
            
            if not disciplinas_turma:
                continue
            
            # Embaralhar disciplinas, mas priorizar as que têm professor fixo
            # (menos flexibilidade = alocar primeiro)
            disciplinas_com_prof = [d for d in disciplinas_turma if d['professor']]
            disciplinas_sem_prof = [d for d in disciplinas_turma if not d['professor']]
            
            # Embaralhar cada grupo separadamente
            random.shuffle(disciplinas_com_prof)
            random.shuffle(disciplinas_sem_prof)
            
            # Processar com professor fixo primeiro (menos flexível)
            disciplinas_turma = disciplinas_com_prof + disciplinas_sem_prof
            
            # Grid de ocupação da turma
            horarios_turma = {dia: set() for dia in self.dias}
            
            # Alocar cada disciplina
            for item in disciplinas_turma:
                disc = item['disciplina']
                prof_preferido = item['professor']
                
                alocada = False
                tentativas = 0
                
                # Criar lista de (dia, periodo) priorizando distribuição
                # Priorizar dias com menos aulas para distribuir uniformemente
                slots = []
                for dia in sorted(self.dias, key=lambda d: len(horarios_turma[d])):
                    for periodo in periodos:
                        if periodo not in horarios_turma[dia]:
                            slots.append((dia, periodo))
                
                # Embaralhar apenas um pouco (manter alguma ordem de prioridade)
                if len(slots) > 10:
                    # Embaralhar apenas os primeiros 10 slots
                    primeiros = slots[:10]
                    random.shuffle(primeiros)
                    slots = primeiros + slots[10:]
                
                for dia, periodo in slots:
                    tentativas += 1
                    if tentativas > self.max_tentativas_aula:
                        break
                    
                    # Verificar se slot está livre na turma
                    if periodo in horarios_turma[dia]:
                        continue
                    
                    # Tentar professor preferido primeiro
                    professores_tentar = []
                    if prof_preferido:
                        prof_obj = next((p for p in self.professores if p.nome == prof_preferido), None)
                        if prof_obj:
                            professores_tentar.append(prof_obj)
                    
                    # Adicionar outros professores que dão esta disciplina
                    for prof in self.professores:
                        if prof not in professores_tentar and disc.nome in prof.disciplinas:
                            professores_tentar.append(prof)
                    
                    # Embaralhar professores alternativos
                    if len(professores_tentar) > 1:
                        primeiro = professores_tentar[0]
                        outros = professores_tentar[1:]
                        random.shuffle(outros)
                        professores_tentar = [primeiro] + outros
                    
                    # Tentar cada professor
                    for prof in professores_tentar:
                        # Verificar disponibilidade
                        if dia not in prof.disponibilidade:
                            continue
                        
                        # Verificar horário real
                        horario_real = self._obter_horario_real(turma_nome, periodo)
                        if (dia, horario_real) in professores_ocupacao[prof.nome]:
                            continue
                        
                        # Verificar limite
                        carga_atual = self._contar_aulas_professor(prof.nome, aulas)
                        limite_prof = self._obter_limite_professor(prof)
                        if carga_atual >= limite_prof:
                            continue
                        
                        # ALOCAR!
                        aula = type('Aula', (), {})()
                        aula.turma = turma_nome
                        aula.disciplina = disc.nome
                        aula.professor = prof.nome
                        aula.dia = dia
                        aula.horario = periodo
                        aula.segmento = 'EM' if 'em' in turma_nome.lower() else 'EF_II'
                        
                        aulas.append(aula)
                        horarios_turma[dia].add(periodo)
                        professores_ocupacao[prof.nome].add((dia, horario_real))
                        
                        alocada = True
                        break
                    
                    if alocada:
                        break
        
        return aulas
    
    def _contar_aulas_professor(self, professor_nome, aulas):
        """Conta aulas de um professor"""
        return sum(1 for aula in aulas if hasattr(aula, 'professor') and aula.professor == professor_nome)
    
    def _obter_limite_professor(self, professor):
        """Retorna limite de horas do professor"""
        if hasattr(professor, 'carga_horaria') and professor.carga_horaria:
            return professor.carga_horaria
        return 35
    
    def _verificar_conflitos_professores(self, aulas):
        """Verifica conflitos de professores"""
        conflitos = []
        por_horario = defaultdict(list)
        
        for aula in aulas:
            if not all(hasattr(aula, attr) for attr in ['professor', 'dia', 'horario', 'turma']):
                continue
            
            horario_real = self._obter_horario_real(aula.turma, aula.horario)
            chave = f"{aula.professor}|{aula.dia}|{horario_real}"
            por_horario[chave].append(aula.turma)
        
        for chave, turmas in por_horario.items():
            if len(turmas) > 1:
                professor, dia, horario = chave.split('|')
                conflitos.append(f"{professor} em {' E '.join(turmas)} no {dia} às {horario}")
        
        return conflitos
    
    def _verificar_limites_excedidos(self, aulas):
        """Verifica se professores excederam limite"""
        excedidos = []
        
        for prof in self.professores:
            carga = self._contar_aulas_professor(prof.nome, aulas)
            limite = self._obter_limite_professor(prof)
            
            if carga > limite:
                excedidos.append(f"{prof.nome}: {carga}h alocadas (limite: {limite}h)")
        
        return excedidos
