import requests
import os

csv_urls = [
    "https://github.com/CaioSobreira/dti_arquivos/raw/main/constructors.csv",
    "https://github.com/CaioSobreira/dti_arquivos/raw/main/drivers.csv",
    "https://github.com/CaioSobreira/dti_arquivos/raw/main/races.csv",
    "https://github.com/CaioSobreira/dti_arquivos/raw/main/results.csv"
]

output_folder = "extraction"


def data_extraction():
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
        print(f"Pasta '{output_folder}' criada com sucesso.")
    else:
        print(f"Pasta '{output_folder}' já existe.")

    for url in csv_urls:
        file_name = url.split('/')[-1]
        file_path = os.path.join(output_folder, file_name)

        print(f"Baixando {file_name}... Por favor aguarde!!!")

        if os.path.exists(file_path):
            print(f"Arquivo '{file_name}' já existe em '{output_folder}'. Pulando download.")
            continue

        try:
            response = requests.get(url, stream=True)

            with open(file_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)

            print(f"'{file_name}' baixado com sucesso em '{output_folder}'.")

        except requests.exceptions.RequestException as e_request:
            print(f"Erro  na Requisição '{file_name}': {e_request}")

        except FileNotFoundError as e_file:
            print(f"Erro no arquivo '{file_name}': {e_file}")

        except Exception as error:
            print(f"Ocorreu um erro inesperado: {error}")
