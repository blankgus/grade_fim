# simple_scheduler_corrigido.py
import random
from models import Aula

class SimpleGradeHorariaCorrigida:
    """Versão corrigida do algoritmo que evita conflitos de professores"""
    
    def __init__(self, turmas, professores, disciplinas, salas):
        self.turmas = turmas
        self.professores = professores
        self.disciplinas = disciplinas
        self.salas = salas
        self.dias_semana = ['segunda', 'terca', 'quarta', 'quinta', 'sexta']
        
    def obter_horario_real_completo(self, segmento, periodo):
        """Retorna horário real como tupla (inicio, fim)"""
        if segmento == "EM":
            horarios = {
                1: ("07:00", "07:50"),
                2: ("07:50", "08:40"), 
                3: ("08:40", "09:30"),
                4: ("09:50", "10:40"),
                5: ("10:40", "11:30"),
                6: ("11:30", "12:20"),
                7: ("12:20", "13:10")
            }
        else:  # EF_II
            horarios = {
                1: ("07:50", "08:40"),
                2: ("08:40", "09:30"),
                3: ("09:50", "10:40"),
                4: ("10:40", "11:30"),
                5: ("11:30", "12:20")
            }
        
        return horarios.get(periodo, ("00:00", "00:00"))
    
    def obter_segmento_turma(self, turma_nome):
        """Determina o segmento da turma"""
        if not turma_nome:
            return "EF_II"
        
        turma_nome_lower = turma_nome.lower()
        
        if 'em' in turma_nome_lower:
            return "EM"
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
    
    def obter_grupo_seguro(self, objeto):
        """Obtém o grupo de um objeto de forma segura"""
        try:
            if hasattr(objeto, 'grupo'):
                grupo = objeto.grupo
                if grupo in ["A", "B", "AMBOS"]:
                    return grupo
            return "A"
        except:
            return "A"
    
    def gerar_grade(self):
        """Gera grade evitando conflitos de professores"""
        aulas = []
        
        # Para cada turma
        for turma in self.turmas:
            turma_nome = turma.nome
            segmento = self.obter_segmento_turma(turma_nome)
            grupo_turma = turma.grupo if hasattr(turma, 'grupo') else "A"
            
            # Determinar períodos disponíveis
            if segmento == "EM":
                periodos_disponiveis = list(range(1, 8))
            else:
                periodos_disponiveis = list(range(1, 6))
            
            # Obter disciplinas desta turma
            disciplinas_turma = []
            for disc in self.disciplinas:
                if turma_nome in disc.turmas and self.obter_grupo_seguro(disc) == grupo_turma:
                    for _ in range(disc.carga_semanal):
                        disciplinas_turma.append(disc)
            
            # Embaralhar disciplinas para distribuição aleatória
            random.shuffle(disciplinas_turma)
            
            # Tentativa de alocação
            tentativas_maximas = len(disciplinas_turma) * 20
            tentativas = 0
            
            while disciplinas_turma and tentativas < tentativas_maximas:
                disciplina = disciplinas_turma[0]
                
                # Encontrar professores disponíveis para esta disciplina
                professores_candidatos = []
                for prof in self.professores:
                    if disciplina.nome in prof.disciplinas:
                        prof_grupo = self.obter_grupo_seguro(prof)
                        if prof_grupo in [grupo_turma, "AMBOS"]:
                            professores_candidatos.append(prof)
                
                if not professores_candidatos:
                    disciplinas_turma.pop(0)
                    continue
                
                # Embaralhar professores
                random.shuffle(professores_candidatos)
                
                # Tentar encontrar horário
                horario_encontrado = False
                
                for professor in professores_candidatos:
                    if horario_encontrado:
                        break
                    
                    # Dias disponíveis do professor
                    dias_disponiveis_prof = professor.disponibilidade if hasattr(professor, 'disponibilidade') else self.dias_semana
                    
                    for _ in range(10):  # Tentar 10 combinações aleatórias
                        # Escolher dia e período aleatório
                        dia = random.choice([d for d in self.dias_semana if d in dias_disponiveis_prof])
                        periodo = random.choice(periodos_disponiveis)
                        
                        # Verificar horário indisponível do professor
                        if hasattr(professor, 'horarios_indisponiveis'):
                            if f"{dia}_{periodo}" in professor.horarios_indisponiveis:
                                continue
                        
                        # Verificar horário real
                        inicio, fim = self.obter_horario_real_completo(segmento, periodo)
                        
                        # 1. Verificar se turma já tem aula neste horário
                        turma_ocupada = False
                        for aula_existente in aulas:
                            if (aula_existente.turma == turma_nome and 
                                aula_existente.dia == dia and
                                aula_existente.horario == periodo):
                                turma_ocupada = True
                                break
                        
                        if turma_ocupada:
                            continue
                        
                        # 2. Verificar se professor já tem aula neste horário REAL
                        professor_ocupado = False
                        for aula_existente in aulas:
                            if (aula_existente.professor == professor.nome and 
                                aula_existente.dia == dia):
                                
                                # Comparar horários REAIS
                                seg_existente = self.obter_segmento_turma(aula_existente.turma)
                                inicio_existente, fim_existente = self.obter_horario_real_completo(seg_existente, aula_existente.horario)
                                
                                if (inicio < fim_existente and inicio_existente < fim):
                                    professor_ocupado = True
                                    break
                        
                        if professor_ocupado:
                            continue
                        
                        # 3. Verificar limite do professor
                        aulas_professor = [a for a in aulas if a.professor == professor.nome]
                        limite_professor = 35  # Default
                        
                        # Calcular limite baseado em segmento
                        tem_efii = False
                        tem_em = False
                        for disc_nome in professor.disciplinas:
                            for disc in self.disciplinas:
                                if disc.nome == disc_nome:
                                    for turma_disc_nome in disc.turmas:
                                        seg = self.obter_segmento_turma(turma_disc_nome)
                                        if seg == "EF_II":
                                            tem_efii = True
                                        elif seg == "EM":
                                            tem_em = True
                        
                        if tem_efii and not tem_em:
                            limite_professor = 25
                        elif tem_em and not tem_efii:
                            limite_professor = 35
                        else:
                            limite_professor = 35
                        
                        if len(aulas_professor) >= limite_professor:
                            continue
                        
                        # TODAS AS VERIFICAÇÕES PASSARAM! Criar aula
                        nova_aula = Aula(
                            turma=turma_nome,
                            disciplina=disciplina.nome,
                            professor=professor.nome,
                            dia=dia,
                            horario=periodo,
                            segmento=segmento
                        )
                        aulas.append(nova_aula)
                        disciplinas_turma.pop(0)
                        horario_encontrado = True
                        break
                
                tentativas += 1
                
                # Se não encontrou após muitas tentativas, remover esta disciplina
                if not horario_encontrado and tentativas > tentativas_maximas / 2:
                    disciplinas_turma.pop(0)
        
        return aulas