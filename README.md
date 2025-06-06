# Projeto de ETL de Dados da Fórmula 1

## Visão Geral

Este projeto implementa um pipeline de ETL (Extração, Transformação e Carga) para processar dados de corridas de Fórmula 1. Os dados são extraídos de arquivos CSV, transformados usando a biblioteca Pandas em Python e, em seguida, carregados em um banco de dados PostgreSQL. O ambiente do projeto é totalmente containerizado usando Docker e Docker Compose, facilitando a configuração e a execução.

## ⚙️ Funcionalidades

- **Extração**: Lê dados de construtores, pilotos, corridas e resultados a partir de arquivos CSV.
- **Transformação**: Realiza a limpeza e o pré-processamento dos dados, como a conversão de tipos de dados, tratamento de valores ausentes e a criação de novas colunas para análise.
- **Carga**: Insere os dados transformados em tabelas de um banco de dados PostgreSQL.
- **Configuração do Banco de Dados**: Cria automaticamente as tabelas e views necessárias para a análise dos dados.
- **Análise**: Fornece queries SQL prontas para análises, como o desempenho em corridas e as voltas mais rápidas.
- **Ambiente Dockerizado**: Utiliza Docker Compose para orquestrar os serviços da aplicação (aplicação Python e banco de dados PostgreSQL), garantindo um ambiente de desenvolvimento e produção consistente e de fácil configuração.

## 🛠  Tecnologias Utilizadas

- **Linguagem de Programação**: Python 3.12
- **Banco de Dados**: PostgreSQL
- **Bibliotecas Python**:
  - `pandas`: Para manipulação e análise de dados.
  - `SQLAlchemy`: Para o mapeamento objeto-relacional (ORM) e interação com o banco de dados.
  - `psycopg2-binary`: Driver PostgreSQL para Python.
  - `python-dotenv`: Para gerenciamento de variáveis de ambiente.
  - `python-slugify`, `unidecode`: Para manipulação de strings.
- **Containerização**: Docker & Docker Compose

## 🚀 Estrutura do Projeto

.
![image](https://github.com/user-attachments/assets/2fb2897c-3b2b-4073-b195-08e5583bcd27)


## Como Executar o Projeto

### Pré-requisitos

- [Docker](https://docs.docker.com/get-docker/)
- [Docker Compose](https://docs.docker.com/compose/install/)

### Configuração

1.  **Clone o repositório** (se aplicável):
    ```bash
    git clone <url-do-seu-repositorio>
    cd <nome-do-repositorio>
    ```

2.  **Variáveis de Ambiente**:
    Crie um arquivo `.env` na raiz do projeto, seguindo o exemplo do arquivo `.env_example` (não fornecido, mas inferido a partir do código). Este arquivo deve conter as credenciais e configurações do banco de dados.
    ```env
    POSTGRES_USER=admin
    POSTGRES_PASSWORD=admin
    POSTGRES_DB=formula_db
    DB_HOST=localhost #com docker ficaria local.docker.internal
    DB_PORT=5432
    ```

### Execução

1.  **Construir e iniciar os containers**:
    Na raiz do projeto, execute o seguinte comando para construir as imagens e iniciar os containers da aplicação Python e do banco de dados PostgreSQL em segundo plano.

    ```bash
    docker-compose up --build -d
    ```

2.  **Verificar a Execução**:
    O script `main.py` será executado automaticamente. Ele irá:
    - Configurar o banco de dados (`setup_db.py`).
    - Extrair os dados dos arquivos CSV (`extraction.py`).
    - Transformar os dados (`transformation.py`).
    - Carregar os dados para o PostgreSQL (`loading.py`).

    Você pode verificar os logs para acompanhar o processo:
    ```bash
    docker-compose logs -f python-app
    ```

3.  **Acessar o Banco de Dados**:
    Após a conclusão do pipeline, você pode se conectar ao banco de dados PostgreSQL para executar as queries de análise localizadas em `scripts_db/`.

## Descrição dos Scripts

- **`main.py`**: Orquestra todo o fluxo do pipeline ETL, chamando as funções de extração, transformação e carga em sequência.
- **`src/setup_db.py`**: Conecta-se ao banco de dados e executa os scripts `create_table.sql` e `create_views.sql` para preparar o esquema do banco.
- **`src/extraction.py`**: Contém a lógica para ler os arquivos CSV do diretório `extraction/` e carregá-los em DataFrames do Pandas.
- **`src/transformation.py`**: Responsável por limpar, transformar e enriquecer os dados brutos para prepará-los para a análise.
- **`src/loading.py`**: Carrega os DataFrames transformados nas tabelas correspondentes do banco de dados PostgreSQL.
- **`scripts_db/`**:
- **`create_table.sql`**: Define a estrutura das tabelas que armazenarão os dados.
- **`create_views.sql`**: Cria views SQL para simplificar consultas de análise complexas.
- **`query_*.sql`**: Contém exemplos de consultas para extrair insights dos dados, como identificar as voltas mais rápidas.


## Autor
- **Alyff antonio**
