import pandas as pd
import psycopg2
import os
from dotenv import load_dotenv
import pathlib
from tabulate import tabulate


load_dotenv()


def execute_sql_script(script_name):
    conn = None
    script_path = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        '..',
        'scripts_db',
        script_name
    )

    print(f"--- Executando script SQL: {script_name} ---")
    print(f"DEBUG: Caminho completo gerado para o script: {script_path}")  # <-- ADICIONE ESTA LINHA DE DEBUG

    try:
        conn = psycopg2.connect(
            host=os.getenv("DB_HOST"),
            port=os.getenv("DB_PORT"),
            database=os.getenv("DB_NAME"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD")
        )
        cursor = conn.cursor()

        with open(script_path, 'r') as f:
            sql_script_content = f.read()

        commands = sql_script_content.split(';')
        for command in commands:
            command = command.strip()
            if command:
                cursor.execute(command)

        conn.commit()

        print(f"Script '{script_name}' executado com sucesso no banco de dados.")

    except FileNotFoundError:
        print(f"ERRO: Script SQL '{script_path}' não encontrado. Verifique o caminho.")
    except psycopg2.Error as e:
        print(f"ERRO de banco de dados ao executar '{script_name}': {e}")
        if conn:
            conn.rollback()
    except Exception as e:
        print(f"Ocorreu um erro inesperado ao executar '{script_name}': {e}")
    finally:
        if conn:
            cursor.close()
            conn.close()
            print("Conexão com o banco de dados fechada.")


def execute_select_query(script_name):
    conn = None
    script_path = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        '..',
        'scripts_db',
        script_name
    )

    try:
        conn = psycopg2.connect(
            host=os.getenv("DB_HOST"),
            port=os.getenv("DB_PORT"),
            database=os.getenv("DB_NAME"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD")
        )
        cursor = conn.cursor()

        with open(script_path, 'r') as f:
            sql_query = f.read()

        if sql_query.strip().upper().startswith('SELECT'):
            cursor.execute(sql_query)

            col_names = [desc[0] for desc in cursor.description]
            results = cursor.fetchall()

            if not results:
                print("⚠️ A consulta não retornou nenhum resultado.")
            else:
                df = pd.DataFrame(results, columns=col_names)

                if df.empty:
                    print("⚠️ DataFrame está vazio, nada a exibir.")
                else:
                    print(tabulate(df, headers="keys", tablefmt="grid"))
        else:
            print(f"❌ ERRO: O script '{script_name}' não é uma consulta SELECT.")

    except FileNotFoundError:
        print(f"❌ ERRO: Script SQL '{script_path}' não encontrado.")
    except psycopg2.Error as e:
        print(f"❌ ERRO de banco de dados ao executar '{script_name}': {e}")
    finally:
        if conn:
            cursor.close()
            conn.close()


if __name__ == "__main__":
    execute_sql_script('create_table.sql')
