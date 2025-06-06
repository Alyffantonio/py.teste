import pandas as pd
import os

def constructors_data(file_path):
    print(f"Transformando dados de: {file_path}")
    try:
        df = pd.read_csv(file_path)

        colunas = ['constructorId', 'name']

        transform = df[colunas].copy()

        transform.rename(columns={
            'constructorId': 'constructor_id'
        }, inplace=True)

        transform['constructor_id'] = transform['constructor_id'].astype(int)
        transform['name'] = transform['name'].astype(str)

        print(f"Transformação de 'constructors.csv' concluída. {len(transform)} linhas processadas.")
        return transform

    except FileNotFoundError:
        print(f"ERRO: Arquivo '{file_path}' não encontrado.")
        return None
    except KeyError as e:
        print(f"ERRO: Coluna esperada não encontrada no arquivo '{file_path}': {e}. Verifique se as colunas 'constructorId' e 'name' existem.")
        return None
    except pd.errors.EmptyDataError:
        print(f"ERRO: O arquivo '{file_path}' está vazio.")
        return None
    except Exception as e:
        print(f"ERRO inesperado ao transformar '{file_path}': {e}")
        return None

def drivers_data(file_path):
    print(f"Transformando dados de: {file_path}")
    try:
        df = pd.read_csv(file_path)

        df['fullname'] = df['forename'].fillna('') + ' ' + df['surname'].fillna('')
        df['fullname'] = df['fullname'].str.strip()

        colunas = ['driverId', 'fullname']

        transform = df[colunas].copy()

        transform.rename(columns={
            'driverId': 'driver_id',
            'fullname': 'full_name'
        }, inplace=True)

        transform['driver_id'] = transform['driver_id'].astype(int)
        transform['full_name'] = transform['full_name'].astype(str)

        print(f"Transformação de 'drivers.csv' concluída. {len(transform)} linhas processadas.")
        return transform

    except FileNotFoundError:
        print(f"ERRO: Arquivo '{file_path}' não encontrado.")
        return None
    except KeyError as e:
        print(f"ERRO: Coluna esperada não encontrada no arquivo '{file_path}': {e}. Verifique se as colunas 'driverId', 'forename' e 'surname' existem.")
        return None
    except pd.errors.EmptyDataError:
        print(f"ERRO: O arquivo '{file_path}' está vazio.")
        return None
    except Exception as e:
        print(f"ERRO ao transformar '{file_path}': {e}")
        return None

def races_data(file_path):
    print(f"Transformando dados de: {file_path}")
    try:
        df = pd.read_csv(file_path, parse_dates=['date'])

        colunas = ['raceId', 'year', 'name', 'date']
        transform = df[colunas].copy()

        transform.rename(columns={'raceId': 'race_id'}, inplace=True)

        transform['race_id'] = transform['race_id'].astype(int)
        transform['year'] = transform['year'].astype(int)
        transform['name'] = transform['name'].astype(str)
        transform['date'] = pd.to_datetime(transform['date'], format='%Y-%m-%d').dt.date

        print(f"Transformação de 'races.csv' concluída. {len(transform)} linhas processadas.")
        return transform

    except FileNotFoundError:
        print(f"ERRO: Arquivo '{file_path}' não encontrado.")
        return None
    except KeyError as e:
        print(f"ERRO: Coluna esperada não encontrada no arquivo '{file_path}': {e}. Verifique se as colunas 'raceId', 'year', 'name' e 'date' existem.")
        return None
    except pd.errors.EmptyDataError:
        print(f"ERRO: O arquivo '{file_path}' está vazio.")
        return None
    except Exception as e:
        print(f"ERRO inesperado ao transformar '{file_path}': {e}")
        return None

def results_data(file_path):
    print(f"Transformando dados de: {file_path}")
    try:
        df = pd.read_csv(file_path)

        colunas = ['resultId', 'raceId', 'driverId', 'constructorId', 'positionOrder', 'points', 'fastestLapTime']
        transform = df[colunas].copy()

        transform.rename(columns={
            'resultId': 'result_id',
            'raceId': 'race_id',
            'driverId': 'driver_id',
            'constructorId': 'constructor_id',
            'positionOrder': 'position_order',
            'fastestLapTime': 'fastest_lap_time'
        }, inplace=True)

        transform['result_id'] = transform['result_id'].astype(int)
        transform['race_id'] = transform['race_id'].astype(int)
        transform['driver_id'] = transform['driver_id'].astype(int)
        transform['constructor_id'] = transform['constructor_id'].astype(int)
        transform['position_order'] = transform['position_order'].astype(int)
        transform['points'] = transform['points'].astype(int)

        transform['fastest_lap_time'] = transform['fastest_lap_time'].apply(convert_lap_time)
        transform['fastest_lap_time'] = pd.to_timedelta(transform['fastest_lap_time'], errors='coerce')

        transform['fastest_lap_time'] = transform['fastest_lap_time'].astype(str).str.extract(r'(\d{2}:\d{2}:\d{2})')

        print(f"Transformação de 'results.csv' concluída. {len(transform)} linhas processadas.")
        return transform

    except FileNotFoundError:
        print(f"ERRO: Arquivo '{file_path}' não encontrado.")
        return None
    except KeyError as e:
        print(f"ERRO: Coluna esperada não encontrada no arquivo '{file_path}': {e}.")
        return None
    except pd.errors.EmptyDataError:
        print(f"ERRO: O arquivo '{file_path}' está vazio.")
        return None
    except Exception as e:
        print(f"ERRO inesperado ao transformar '{file_path}': {e}")
        return None

def convert_lap_time(lap_time):
    if pd.notna(lap_time) and isinstance(lap_time, str):
        try:
            minutos, segundos = lap_time.split(":")
            return f"00:{minutos}:{segundos.split('.')[0]}"
        except ValueError:
            return None
    return None
