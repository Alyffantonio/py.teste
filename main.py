import os
import sys
from src.extraction import *
from src.setup_db import *
from src.transformation import *
from src.loading import *

sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'src'))


def run_etl_process():
    print("Iniciando processo ETL...")


    print("\n--- SETUP DO BANCO DE DADOS: Criação de Tabelas ---")
    execute_sql_script('create_table.sql')


    print("\n--- LIMPANDO DADOS EXISTENTES (TRUNCATE) ---")
    if not truncate_all_tables():
        print("Falha ao truncar tabelas. Abortando o processo ETL.")
        return

    data_extraction()


    extracao_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'extraction')


    constructors_file_path = os.path.join(extracao_folder, 'constructors.csv')
    df_constructors = constructors_data(constructors_file_path)
    if df_constructors is not None:
        data_db(df_constructors, 'constructors', exists_table='append')
    else:
        print("Transformação de 'constructors.csv' falhou. Carga para 'constructors' pulada.")


    drivers_file_path = os.path.join(extracao_folder, 'drivers.csv')
    df_drivers = drivers_data(drivers_file_path)
    if df_drivers is not None:
        data_db(df_drivers, 'drivers', exists_table='append')
    else:
        print("Transformação de 'drivers.csv' falhou. Carga para 'drivers' pulada.")


    races_file_path = os.path.join(extracao_folder, 'races.csv')
    df_races = races_data(races_file_path)
    if df_races is not None:
        data_db(df_races, 'races', exists_table='append')
    else:
        print("Transformação de 'races.csv' falhou. Carga para 'races' pulada.")

    results_file_path = os.path.join(extracao_folder, 'results.csv')
    df_results = results_data(results_file_path)
    if df_results is not None:
        data_db(df_results, 'results', exists_table='append')
    else:
        print("Transformação de 'results.csv' falhou. Carga para 'results' pulada.")


    execute_sql_script('create_views.sql')

    print("\n" + "=" * 80)
    execute_select_query('query_race_perform.sql')

    print("\n" + "=" * 80)
    execute_select_query('query_fast_lap.sql')

if __name__ == "__main__":
    run_etl_process()