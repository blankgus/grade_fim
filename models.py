from dataclasses import dataclass, field
from typing import List, Dict
import uuid

DIAS_SEMANA = ["seg", "ter", "qua", "qui", "sex"]

@dataclass
class Turma:
    nome: str
    serie: str
    turno: str
    grupo: str
    segmento: str = ""
    id: str = field(default_factory=lambda: str(uuid.uuid4()))

@dataclass
class Professor:
    nome: str
    disciplinas: List[str]
    disponibilidade: List[str]
    grupo: str
    horarios_indisponiveis: List[str] = field(default_factory=list)
    carga_horaria_maxima: int = 35  # Carga individual do professor (padrão 35h)
    observacoes: str = ""  # Restrições especiais (ex: "Análises bater com 1º e 2º EM B")
    id: str = field(default_factory=lambda: str(uuid.uuid4()))

@dataclass
class Disciplina:
    nome: str
    carga_semanal: int  # DEPRECATED: mantido para compatibilidade, usar carga_por_turma
    tipo: str
    turmas: List[str]
    grupo: str
    cor_fundo: str = "#4A90E2"
    cor_fonte: str = "#FFFFFF"
    carga_por_turma: Dict[str, int] = field(default_factory=dict)  # {"6ºA": 5, "7ºA": 4, ...}
    professor_por_turma: Dict[str, str] = field(default_factory=dict)  # NOVO: {"6ºA": "Santiago", "7ºA": "Cesar", ...}
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    
    def obter_carga_turma(self, turma_nome: str) -> int:
        """Obtém a carga semanal para uma turma específica"""
        # PRIORIDADE 1: Usar carga específica se disponível
        if self.carga_por_turma and turma_nome in self.carga_por_turma:
            return self.carga_por_turma[turma_nome]
        # PRIORIDADE 2: Fallback para carga genérica (compatibilidade)
        return self.carga_semanal
    
    def obter_professor_turma(self, turma_nome: str) -> str:
        """Obtém o professor atribuído para uma turma específica"""
        if self.professor_por_turma and turma_nome in self.professor_por_turma:
            return self.professor_por_turma[turma_nome]
        return None  # Nenhum professor definido (será escolhido pelo algoritmo)

@dataclass
class Sala:
    nome: str
    capacidade: int
    tipo: str
    id: str = field(default_factory=lambda: str(uuid.uuid4()))

@dataclass
class Aula:
    turma: str
    disciplina: str
    professor: str
    dia: str
    horario: int
    segmento: str = ""
    id: str = field(default_factory=lambda: str(uuid.uuid4()))