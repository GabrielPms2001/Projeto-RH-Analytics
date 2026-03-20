# 📊 Projeto RH Analytics - Engenharia de Dados + Power BI

## 📌 Visão Geral

Este projeto simula um ambiente real de **Departamento Pessoal (RH)** utilizando **engenharia de dados**, **modelagem dimensional (Star Schema)** e **dados sintéticos** para análise em ferramentas como o Power BI.

O objetivo é reproduzir o cenário de uma empresa terceirizada de RH que presta serviços para múltiplos clientes, permitindo análises estratégicas como:

* Taxa de turnover
* Admissões vs demissões
* Headcount
* Custo por setor
* Tempo médio de permanência

---

## 🏢 Empresas Simuladas

O ambiente contempla três clientes:

* PicPay
* Grupo Autoglass
* ArcelorMittal

---

## 🧠 Arquitetura de Dados

O modelo segue o padrão **Star Schema**, amplamente utilizado em BI e Data Warehousing.

### 🔹 Tabelas Fato

* **fato_funcionarios**

  * Snapshot atual dos funcionários
* **fato_admissao**

  * Eventos de entrada na empresa
* **fato_demissao**

  * Eventos de saída da empresa

### 🔹 Tabelas Dimensão

* **dim_empresa**
* **dim_setor**
* **dim_cargo**

---

## 📅 Período dos Dados

Os dados foram gerados com base no seguinte intervalo:

* Início: Janeiro de 2024
* Fim: Março de 2026

Isso permite análises temporais como:

* Comparação anual (2024 vs 2025)
* Tendência de turnover
* Sazonalidade de demissões

---

## ⚙️ Tecnologias Utilizadas

* Python
* Pandas
* Faker (geração de dados sintéticos)
* SQLAlchemy
* SQL Server
* Power BI (para visualização)

---

## 🔄 Pipeline de Dados

1. Geração de dados sintéticos via Python
2. Aplicação de regras de negócio (datas, salários, demissões)
3. Estruturação em modelo dimensional
4. Carga no SQL Server
5. Consumo via Power BI

---

## 📊 Possibilidades de Análise

Com essa base é possível construir dashboards com:

* 📉 Taxa de Turnover
* 📈 Evolução de admissões e demissões
* 🏢 Comparativo entre empresas
* 🧑‍💼 Distribuição por cargos
* 💰 Custo por setor
* ⏳ Tempo médio de empresa

---

## 🚀 Como Executar o Projeto

### 1. Criar ambiente virtual

```bash
python -m venv .venv
```

### 2. Ativar o ambiente

```bash
.\.venv\Scripts\activate
```

### 3. Instalar dependências

```bash
pip install pandas faker sqlalchemy pyodbc
```

### 4. Configurar conexão com SQL Server

Edite no script:

```python
server = 'localhost'
database = 'RH_Analytics'
```

### 5. Executar o script

```bash
python main.py
```

---

## 🧱 Estrutura Sugerida do Projeto

```
Projeto-RH-Analytics/
│
├── main.py
├── requirements.txt
├── README.md
└── powerbi/
    └── dashboard.pbix
```

---

## 🧠 Diferenciais do Projeto

* Modelagem dimensional aplicada (Star Schema)
* Simulação de cenário real de RH terceirizado
* Multi-empresa (multi-tenant)
* Dados consistentes com regras de negócio
* Pronto para integração com BI

---

## 🔥 Próximos Passos (Evolução)

* Criar dimensão de tempo (dim_tempo)
* Implementar histórico de funcionários (SCD Tipo 2)
* Automatizar pipeline (Airflow / Prefect)
* Criar dashboard completo no Power BI
* Publicar como portfólio profissional

---

## 👨‍💻 Autor

Projeto desenvolvido para fins de estudo, prática em engenharia de dados e construção de portfólio profissional.

---

## 📌 Observação

Os dados são **100% fictícios**, gerados apenas para simulação e não representam nenhuma empresa real.

---
