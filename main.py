import pandas as pd
import random
from faker import Faker
from datetime import datetime, timedelta
from sqlalchemy import create_engine

fake = Faker('pt_BR')

# ==============================
# PERÍODO
# ==============================
DATA_INICIO = datetime(2024, 1, 1)
DATA_FIM = datetime(2026, 3, 31)

# ==============================
# CONEXÃO SQL SERVER
# ==============================
SERVER = 'localhost'
DATABASE = 'RH_Analytics'

engine = create_engine(
    f"mssql+pyodbc://@{SERVER}/{DATABASE}?driver=ODBC+Driver+17+for+SQL+Server&trusted_connection=yes"
)

# ==============================
# DIMENSÕES
# ==============================

dim_setor = pd.DataFrame({
    'id_setor': range(1, 8),
    'nome_setor': [
        'Contabilidade', 'TI', 'RH',
        'Logistica', 'Comercial',
        'Marketing', 'Financeiro'
    ]
})

dim_empresa = pd.DataFrame({
    'id_empresa': [1, 2, 3],
    'nome_empresa': ['PicPay', 'Grupo Autoglass', 'ArcelorMittal']
})

dim_cargo = pd.DataFrame({
    'id_cargo': [1, 2, 3, 4, 5],
    'nome_cargo': [
        'Auxiliar',
        'Assistente',
        'Analista',
        'Coordenador',
        'Gerente'
    ]
})

# ==============================
# FUNÇÕES
# ==============================

def gerar_nome_limpo():
    return f"{fake.first_name()} {fake.last_name()}"

def gerar_genero(nome):
    # heurística simples baseada no primeiro nome
    primeiro_nome = nome.split()[0]
    if primeiro_nome[-1] in ['a', 'e']:
        return 'Feminino'
    return 'Masculino'

def gerar_idade():
    return random.randint(18, 65)

def gerar_senioridade(id_cargo):
    mapa = {
        1: 'Júnior',
        2: 'Pleno',
        3: 'Sênior',
        4: 'Liderança',
        5: 'Liderança'
    }
    return mapa[id_cargo]

def gerar_data_admissao():
    delta = DATA_FIM - DATA_INICIO
    return DATA_INICIO + timedelta(days=random.randint(0, delta.days))

def gerar_data_demissao(data_admissao):
    limite_final = min(DATA_FIM, data_admissao + timedelta(days=900))
    delta = (limite_final - data_admissao).days

    if delta < 30:
        return None

    return data_admissao + timedelta(days=random.randint(30, delta))

def gerar_salario(id_cargo):
    base = {
        1: (1600, 1975),
        2: (1900, 2350),
        3: (3500, 5500),
        4: (10000, 15000),
        5: (15000, 30000)
    }
    return round(random.uniform(*base[id_cargo]), 2)

# ==============================
# GERAÇÃO DE DADOS
# ==============================

qtd_funcionarios = 500

fato_funcionarios = []
fato_admissao = []
fato_demissao = []

for i in range(1, qtd_funcionarios + 1):
    nome = gerar_nome_limpo()
    genero = gerar_genero(nome)
    idade = gerar_idade()

    id_setor = random.choice(dim_setor['id_setor'])
    id_cargo = random.choice(dim_cargo['id_cargo'])
    id_empresa = random.choice(dim_empresa['id_empresa'])

    senioridade = gerar_senioridade(id_cargo)

    data_admissao = gerar_data_admissao()
    salario = gerar_salario(id_cargo)

    tempo_empresa = (datetime.now() - data_admissao).days // 30

    demitido = random.random() < 0.3
    data_demissao = None

    if demitido:
        data_demissao = gerar_data_demissao(data_admissao)
        if data_demissao is None:
            demitido = False

    # FATO FUNCIONÁRIOS
    fato_funcionarios.append({
        'id_funcionario': i,
        'nome_funcionario': nome,
        'genero': genero,
        'idade': idade,
        'senioridade': senioridade,
        'id_setor': id_setor,
        'id_cargo': id_cargo,
        'id_empresa': id_empresa,
        'tempo_empresa': tempo_empresa,
        'salario': salario
    })

    # FATO ADMISSÃO
    fato_admissao.append({
        'id_funcionario': i,
        'nome_funcionario': nome,
        'genero': genero,
        'idade': idade,
        'senioridade': senioridade,
        'id_cargo': id_cargo,
        'id_setor': id_setor,
        'id_empresa': id_empresa,
        'data_admissao': data_admissao,
        'salario': salario
    })

    # FATO DEMISSÃO
    if demitido:
        fato_demissao.append({
            'id_funcionario': i,
            'nome_funcionario': nome,
            'genero': genero,
            'idade': idade,
            'senioridade': senioridade,
            'id_cargo': id_cargo,
            'id_setor': id_setor,
            'id_empresa': id_empresa,
            'data_demissao': data_demissao,
            'salario': salario
        })

# ==============================
# DATAFRAMES
# ==============================

df_funcionarios = pd.DataFrame(fato_funcionarios)
df_admissao = pd.DataFrame(fato_admissao)
df_demissao = pd.DataFrame(fato_demissao)

# ==============================
# CARGA SQL SERVER
# ==============================

print("Subindo dados para o SQL Server...")

dim_setor.to_sql('dim_setor', engine, if_exists='replace', index=False)
dim_empresa.to_sql('dim_empresa', engine, if_exists='replace', index=False)
dim_cargo.to_sql('dim_cargo', engine, if_exists='replace', index=False)

df_funcionarios.to_sql('fato_funcionarios', engine, if_exists='replace', index=False)
df_admissao.to_sql('fato_admissao', engine, if_exists='replace', index=False)
df_demissao.to_sql('fato_demissao', engine, if_exists='replace', index=False)

print("Carga finalizada com sucesso!")