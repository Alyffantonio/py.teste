import pandas as pd
import psycopg2
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine

load_dotenv()

def get_db_connect():

    try:
        conn = psycopg2.connect(
            host=os.getenv("DB_HOST"),
            port=os.getenv("DB_PORT"),
            database=os.getenv("DB_NAME"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD")
        )
        print("Conexão com o banco de dados PostgreSQL estabelecida com sucesso para carga.")
        return conn
    except psycopg2.Error as e:
        print(f"Erro ao conectar ao banco de dados PostgreSQL para carga: {e}")
        return None


def close_db_connect(conn):

    if conn:
        conn.close()
        print("Conexão com o banco de dados PostgreSQL fechada após carga.")


def truncate_all_tables():
    conn = get_db_connect()
    if conn:
        try:
            cursor = conn.cursor()
            tables_to_truncate = ['constructors', 'drivers', 'races', 'results']

            print("\n--- Truncando tabelas para evitar duplicatas ---")
            for table_name in tables_to_truncate:
                try:
                    cursor.execute(f"TRUNCATE TABLE {table_name} RESTART IDENTITY;")
                    conn.commit()
                    print(f"Tabela '{table_name}' truncada com sucesso.")
                except psycopg2.errors.UndefinedTable:
                    print(f"Aviso: Tabela '{table_name}' não existe ainda, TRUNCATE ignorado.")
                    conn.rollback()
                except psycopg2.Error as e_truncate:
                    print(f"ERRO ao truncar a tabela '{table_name}': {e_truncate}. Revertendo transação.")
                    conn.rollback()
                    return False
            print("Todas as tabelas foram truncadas com sucesso.")
            return True
        except Exception as e:
            print(f"ERRO inesperado durante o truncamento de tabelas: {e}")
            if conn: conn.rollback()
            return False
        finally:
            close_db_connect(conn)
    return False


def data_db(df: pd.DataFrame, table_name: str, exists_table: str = 'append'):
    db_connection_str = f"postgresql+psycopg2://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"

    engine = None
    try:
        engine = create_engine(db_connection_str)
        print(f"Iniciando carga de dados para a tabela '{table_name}' usando SQLAlchemy...")

        df.to_sql(table_name, engine, if_exists=exists_table, index=False)
        print(f"Dados carregados com sucesso na tabela '{table_name}'. Total de {len(df)} linhas.")

    except Exception as e:
        print(f"Ocorreu um ERRO inesperado ao carregar dados na tabela '{table_name}': {e}")
    finally:
        if engine:
            engine.dispose()


if __name__ == "__main__":
    print("Módulo de carga de dados. Não deve ser executado diretamente em produção.")
    print("Execute via main.py para o fluxo completo do ETL.")