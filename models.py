from dataclasses import dataclass, field
from typing import List
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
    id: str = field(default_factory=lambda: str(uuid.uuid4()))

@dataclass
class Disciplina:
    nome: str
    carga_semanal: int
    tipo: str
    turmas: List[str]
    grupo: str
    cor_fundo: str = "#4A90E2"
    cor_fonte: str = "#FFFFFF"
    id: str = field(default_factory=lambda: str(uuid.uuid4()))

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