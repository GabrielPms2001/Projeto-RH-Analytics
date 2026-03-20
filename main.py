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

# DIM SETOR
dim_setor = pd.DataFrame({
    'id_setor': range(1, 8),
    'nome_setor': [
        'Contabilidade',
        'TI',
        'RH',
        'Logistica',
        'Comercial',
        'Marketing',
        'Financeiro'
    ]
})

# DIM EMPRESA
dim_empresa = pd.DataFrame({
    'id_empresa': [1, 2, 3],
    'nome_empresa': ['PicPay', 'Grupo Autoglass', 'ArcelorMittal']
})

# DIM CARGO (melhor prática)
dim_cargo = pd.DataFrame({
    'id_cargo': [1, 2, 3, 4, 5],
    'nome_cargo': [
        'Analista Júnior',
        'Analista Pleno',
        'Analista Sênior',
        'Coordenador',
        'Gerente'
    ]
})

# ==============================
# FUNÇÕES
# ==============================

def gerar_data_admissao():
    delta = DATA_FIM - DATA_INICIO
    return DATA_INICIO + timedelta(days=random.randint(0, delta.days))

def gerar_data_demissao(data_admissao):
    limite_final = min(DATA_FIM, data_admissao + timedelta(days=900))

    # diferença entre datas
    delta = (limite_final - data_admissao).days

    # 🔥 REGRA PRINCIPAL
    if delta < 30:
        return None  # não dá pra gerar demissão válida

    return data_admissao + timedelta(days=random.randint(30, delta))

def gerar_salario(id_cargo):
    base = {
        1: (2500, 4000),
        2: (4000, 7000),
        3: (7000, 12000),
        4: (10000, 15000),
        5: (15000, 25000)
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
    nome = fake.name()
    
    id_setor = random.choice(dim_setor['id_setor'])
    id_cargo = random.choice(dim_cargo['id_cargo'])
    id_empresa = random.choice(dim_empresa['id_empresa'])

    data_admissao = gerar_data_admissao()
    salario = gerar_salario(id_cargo)

    tempo_empresa = (datetime.now() - data_admissao).days // 30

    demitido = random.random() < 0.3
    data_demissao = None

    if demitido:
        data_demissao = gerar_data_demissao(data_admissao)
        if data_demissao is None:
            demitido = False

    # ======================
    # FATO FUNCIONARIOS
    # ======================
    fato_funcionarios.append({
        'id_funcionario': i,
        'nome_funcionario': nome,
        'id_setor': id_setor,
        'id_cargo': id_cargo,
        'id_empresa': id_empresa,
        'tempo_empresa': tempo_empresa,
        'salario': salario
    })

    # ======================
    # FATO ADMISSAO
    # ======================
    fato_admissao.append({
        'id_funcionario': i,
        'nome_funcionario': nome,
        'id_cargo': id_cargo,
        'id_setor': id_setor,
        'id_empresa': id_empresa,
        'data_admissao': data_admissao,
        'salario': salario
    })

    # ======================
    # FATO DEMISSAO
    # ======================
    if demitido:
        fato_demissao.append({
            'id_funcionario': i,
            'nome_funcionario': nome,
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
# CARGA NO SQL SERVER
# ==============================

print("Subindo dados para o SQL Server...")

dim_setor.to_sql('dim_setor', engine, if_exists='replace', index=False)
dim_empresa.to_sql('dim_empresa', engine, if_exists='replace', index=False)
dim_cargo.to_sql('dim_cargo', engine, if_exists='replace', index=False)

df_funcionarios.to_sql('fato_funcionarios', engine, if_exists='replace', index=False)
df_admissao.to_sql('fato_admissao', engine, if_exists='replace', index=False)
df_demissao.to_sql('fato_demissao', engine, if_exists='replace', index=False)

print("Carga finalizada com modelo Star Schema correto!")