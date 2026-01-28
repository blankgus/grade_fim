import json
import os
from models import Turma, Professor, Disciplina, Sala, Aula

# Arquivo de database
DB_FILE = "escola_database.json"

def criar_dados_iniciais():
    """Cria dados iniciais para teste"""
    
    # Professores sem campo grupo
    professores = [
        Professor("Heliana", ["Português"], {"segunda", "terca", "quarta", "quinta", "sexta"}),
        Professor("Deise", ["Português"], {"segunda", "terca", "quarta", "quinta", "sexta"}),
        Professor("Loide", ["Português"], {"segunda", "terca", "quarta", "quinta", "sexta"}),
        Professor("Tatiane", ["Matemática"], {"segunda", "terca", "quarta", "quinta", "sexta"}),
        Professor("Ricardo", ["Matemática"], {"segunda", "terca", "quarta", "quinta", "sexta"}),
        Professor("Laís", ["História"], {"segunda", "terca", "quarta", "quinta", "sexta"}),
        Professor("Waldemar", ["História"], {"segunda", "terca", "quarta", "quinta", "sexta"}),
        Professor("Rene", ["Geografia"], {"segunda", "terca", "quarta", "quinta", "sexta"}),
        Professor("Vladmir", ["Química"], {"segunda", "terca", "quarta", "quinta", "sexta"}),
        Professor("Zabuor", ["Química"], {"segunda", "terca", "quarta", "quinta", "sexta"}),
        Professor("Gisele", ["Geografia"], {"segunda", "terca", "quarta", "quinta", "sexta"}),
        Professor("Marina", ["Biologia", "Ciências"], {"segunda", "terca", "quarta", "quinta", "sexta"}),
        Professor("Santiago", ["Matemática"], {"segunda", "terca", "quarta", "quinta", "sexta"}),
        Professor("Andréia Lucia", ["Matemática"], {"segunda", "terca", "quarta", "quinta", "sexta"}),
        Professor("César", ["Informática", "Física"], {"segunda", "terca", "quarta", "quinta", "sexta"}),
        Professor("Anna Maria", ["Filosofia", "Sociologia"], {"segunda", "terca", "quarta", "quinta", "sexta"}),
        Professor("Marcão", ["Educação Física"], {"segunda", "terca", "quarta", "quinta", "sexta"}),
        Professor("Andréia", ["Educação Física"], {"segunda", "terca", "quarta", "quinta", "sexta"}),
        Professor("Vanessa", ["Arte"], {"segunda", "terca", "quarta", "quinta", "sexta"}),
        Professor("Maria Luiza", ["Inglês"], {"segunda", "terca", "quarta", "quinta", "sexta"}),
        Professor("Andréia Barreto", ["Dinâmica", "Vida Pratica"], {"segunda", "terca", "quarta", "quinta", "sexta"}),
    ]
    
    # Turmas sem campo grupo (grupo já está no nome: 6anoA, 6anoB, etc)
    turmas = [
        Turma("6anoA", "6ano", "manha", "EF_II"),
        Turma("7anoA", "7ano", "manha", "EF_II"),
        Turma("8anoA", "8ano", "manha", "EF_II"),
        Turma("9anoA", "9ano", "manha", "EF_II"),
        Turma("1emA", "1em", "manha", "EM"),
        Turma("2emA", "2em", "manha", "EM"),
        Turma("3emA", "3em", "manha", "EM"),
        Turma("6anoB", "6ano", "manha", "EF_II"),
        Turma("7anoB", "7ano", "manha", "EF_II"),
        Turma("8anoB", "8ano", "manha", "EF_II"),
        Turma("9anoB", "9ano", "manha", "EF_II"),
        Turma("1emB", "1em", "manha", "EM"),
        Turma("2emB", "2em", "manha", "EM"),
        Turma("3emB", "3em", "manha", "EM"),
    ]
    
    # Disciplinas sem campo grupo (aplicam a todas as turmas especificadas)
    disciplinas = [
        # Turmas A
        Disciplina("Português", 4, "pesada", ["6anoA", "7anoA", "8anoA", "9anoA", "1emA", "2emA", "3emA"]),
        Disciplina("Matemática", 5, "pesada", ["6anoA", "7anoA", "8anoA", "9anoA", "1emA", "2emA", "3emA"]),
        Disciplina("História", 2, "media", ["6anoA", "7anoA", "8anoA", "9anoA", "1emA", "2emA", "3emA"]),
        Disciplina("Geografia", 2, "media", ["6anoA", "7anoA", "8anoA", "9anoA", "1emA", "2emA", "3emA"]),
        Disciplina("Ciências", 2, "media", ["6anoA", "7anoA", "8anoA", "9anoA"]),
        Disciplina("Biologia", 2, "media", ["1emA", "2emA", "3emA"]),
        Disciplina("Física", 2, "pesada", ["1emA", "2emA", "3emA"]),
        Disciplina("Química", 2, "pesada", ["1emA", "2emA", "3emA"]),
        Disciplina("Inglês", 2, "leve", ["6anoA", "7anoA", "8anoA", "9anoA", "1emA", "2emA", "3emA"]),
        Disciplina("Arte", 2, "leve", ["6anoA", "7anoA", "8anoA", "9anoA", "1emA", "2emA", "3emA"]),
        Disciplina("Educação Física", 2, "pratica", ["6anoA", "7anoA", "8anoA", "9anoA", "1emA", "2emA", "3emA"]),
        Disciplina("Filosofia", 2, "media", ["1emA", "2emA", "3emA"]),
        Disciplina("Sociologia", 2, "media", ["1emA", "2emA", "3emA"]),
        Disciplina("Informática", 2, "leve", ["6anoA", "7anoA", "8anoA", "9anoA", "1emA", "2emA", "3emA"]),
        Disciplina("Dinâmica", 2, "leve", ["6anoA", "7anoA", "8anoA", "9anoA"]),
        
        # Turmas B  
        Disciplina("Português", 4, "pesada", ["6anoB", "7anoB", "8anoB", "9anoB", "1emB", "2emB", "3emB"]),
        Disciplina("Matemática", 5, "pesada", ["6anoB", "7anoB", "8anoB", "9anoB", "1emB", "2emB", "3emB"]),
        Disciplina("História", 2, "media", ["6anoB", "7anoB", "8anoB", "9anoB", "1emB", "2emB", "3emB"]),
        Disciplina("Geografia", 2, "media", ["6anoB", "7anoB", "8anoB", "9anoB", "1emB", "2emB", "3emB"]),
        Disciplina("Ciências", 2, "media", ["6anoB", "7anoB", "8anoB", "9anoB"]),
        Disciplina("Biologia", 2, "media", ["1emB", "2emB", "3emB"]),
        Disciplina("Física", 2, "pesada", ["1emB", "2emB", "3emB"]),
        Disciplina("Química", 2, "pesada", ["1emB", "2emB", "3emB"]),
        Disciplina("Inglês", 2, "leve", ["6anoB", "7anoB", "8anoB", "9anoB", "1emB", "2emB", "3emB"]),
        Disciplina("Arte", 2, "leve", ["6anoB", "7anoB", "8anoB", "9anoB", "1emB", "2emB", "3emB"]),
        Disciplina("Educação Física", 2, "pratica", ["6anoB", "7anoB", "8anoB", "9anoB", "1emB", "2emB", "3emB"]),
        Disciplina("Filosofia", 2, "media", ["1emB", "2emB", "3emB"]),
        Disciplina("Sociologia", 2, "media", ["1emB", "2emB", "3emB"]),
        Disciplina("Informática", 2, "leve", ["6anoB", "7anoB", "8anoB", "9anoB", "1emB", "2emB", "3emB"]),
        Disciplina("Dinâmica", 1, "leve", ["6anoB", "7anoB", "8anoB", "9anoB"]),
    ]

    
    salas = [
        Sala("Sala 1", 30, "normal"),
        Sala("Sala 2", 30, "normal"),
        Sala("Sala 3", 30, "normal"),
        Sala("Sala 4", 30, "normal"),
        Sala("Sala 5", 30, "normal"),
        Sala("Sala 6", 30, "normal"),
        Sala("Sala 7", 30, "normal"),
        Sala("Sala 8", 30, "normal"),
        Sala("Sala 9", 30, "normal"),
        Sala("Sala 10", 30, "normal"),
        Sala("Sala 11", 30, "normal"),
        Sala("Sala 12", 30, "normal"),
        Sala("Sala 13", 30, "normal"),
        Sala("Sala 14", 30, "normal"),
        Sala("Laboratório de Ciências", 25, "laboratório"),
        Sala("Auditório", 100, "auditório"),
    ]
    
    return {
        "professores": [p.__dict__ for p in professores],
        "disciplinas": [d.__dict__ for d in disciplinas],
        "turmas": [t.__dict__ for t in turmas],
        "salas": [s.__dict__ for s in salas],
        "aulas": [],
        "feriados": [],
        "periodos": []
    }

def init_db():
    """Inicializa o banco de dados com dados padrão se não existir"""
    if not os.path.exists(DB_FILE):
        dados_iniciais = criar_dados_iniciais()
        salvar_tudo(dados_iniciais)

def carregar_tudo():
    """Carrega todos os dados do banco"""
    if not os.path.exists(DB_FILE):
        init_db()
    
    try:
        with open(DB_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except:
        return criar_dados_iniciais()

def salvar_tudo(dados):
    """Salva todos os dados no banco"""
    try:
        with open(DB_FILE, 'w', encoding='utf-8') as f:
            json.dump(dados, f, indent=2, ensure_ascii=False)
        return True
    except Exception as e:
        print(f"Erro ao salvar: {e}")
        return False

# Funções de carregamento
def carregar_turmas():
    dados = carregar_tudo()
    turmas = dados.get("turmas", [])
    resultado = []
    
    for item in turmas:
        if isinstance(item, dict):
            resultado.append(Turma(**item))
        elif hasattr(item, 'nome') and hasattr(item, 'serie'):
            resultado.append(item)
        else:
            print(f"Item inválido em turmas: {item}")
    
    return resultado

def carregar_professores():
    dados = carregar_tudo()
    professores = dados.get("professores", [])
    resultado = []
    
    for item in professores:
        if isinstance(item, dict):
            # Converter disponibilidade conforme o tipo no banco
            if 'disponibilidade' in item:
                disp = item['disponibilidade']
                
                # Se for dicionário (formato novo), extrair apenas os dias disponíveis
                if isinstance(disp, dict):
                    item['disponibilidade'] = [dia for dia, disponivel in disp.items() if disponivel]
                # Se for lista (formato antigo), manter como está
                elif isinstance(disp, list):
                    pass  # Já está no formato correto
            
            # Garantir que carga_horaria existe
            if 'carga_horaria' not in item:
                item['carga_horaria'] = 0
            
            # Converter horarios_indisponiveis de lista para set/lista (manter como lista)
            resultado.append(Professor(**item))
        elif hasattr(item, 'nome') and hasattr(item, 'disciplinas'):
            resultado.append(item)
        else:
            print(f"Item inválido em professores: {item}")
    
    return resultado

def carregar_disciplinas():
    dados = carregar_tudo()
    disciplinas = dados.get("disciplinas", [])
    resultado = []
    
    for item in disciplinas:
        if isinstance(item, dict):
            # Compatibilidade: renomear carga_turmas para carga_por_turma
            if 'carga_turmas' in item:
                item['carga_por_turma'] = item.pop('carga_turmas')
            
            resultado.append(Disciplina(**item))
        elif hasattr(item, 'nome') and hasattr(item, 'carga_semanal'):
            resultado.append(item)
        else:
            print(f"Item inválido em disciplinas: {item}")
    
    return resultado

def carregar_salas():
    dados = carregar_tudo()
    salas = dados.get("salas", [])
    resultado = []
    
    for item in salas:
        if isinstance(item, dict):
            resultado.append(Sala(**item))
        elif hasattr(item, 'nome') and hasattr(item, 'capacidade'):
            resultado.append(item)
        else:
            print(f"Item inválido em salas: {item}")
    
    return resultado

def carregar_grade():
    dados = carregar_tudo()
    aulas = dados.get("aulas", [])
    resultado = []
    
    for item in aulas:
        if isinstance(item, dict):
            resultado.append(Aula(**item))
        elif hasattr(item, 'turma') and hasattr(item, 'disciplina'):
            resultado.append(item)
        else:
            print(f"Item inválido em aulas: {item}")
    
    return resultado

def carregar_feriados():
    dados = carregar_tudo()
    return dados.get("feriados", [])

def carregar_periodos():
    dados = carregar_tudo()
    return dados.get("periodos", [])

# Funções de salvamento
def _converter_para_dict(obj):
    """Converte objeto para dicionário se for um objeto models, convertendo sets para listas"""
    if hasattr(obj, '__dict__'):
        obj_dict = obj.__dict__.copy()
        # Converter sets para listas (JSON não suporta sets)
        for key, value in obj_dict.items():
            if isinstance(value, set):
                obj_dict[key] = list(value)
        return obj_dict
    return obj

def salvar_turmas(turmas):
    dados = carregar_tudo()
    dados["turmas"] = [_converter_para_dict(t) for t in turmas]
    return salvar_tudo(dados)

def salvar_professores(professores):
    dados = carregar_tudo()
    dados["professores"] = [_converter_para_dict(p) for p in professores]
    return salvar_tudo(dados)

def salvar_disciplinas(disciplinas):
    dados = carregar_tudo()
    dados["disciplinas"] = [_converter_para_dict(d) for d in disciplinas]
    return salvar_tudo(dados)

def salvar_salas(salas):
    dados = carregar_tudo()
    dados["salas"] = [_converter_para_dict(s) for s in salas]
    return salvar_tudo(dados)

def salvar_grade(aulas):
    dados = carregar_tudo()
    dados["aulas"] = [_converter_para_dict(a) for a in aulas]
    return salvar_tudo(dados)

def salvar_feriados(feriados):
    dados = carregar_tudo()
    dados["feriados"] = feriados
    return salvar_tudo(dados)

def salvar_periodos(periodos):
    dados = carregar_tudo()
    dados["periodos"] = periodos
    return salvar_tudo(dados)

def resetar_banco():
    """Reseta o banco de dados para os valores iniciais"""
    if os.path.exists(DB_FILE):
        os.remove(DB_FILE)
    init_db()
    return True