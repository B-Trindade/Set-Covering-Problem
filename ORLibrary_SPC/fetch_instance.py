import requests
from pathlib import Path

def get_data(instance_url: str):
    """
    Recebe um URL para uma instância na OR-Lib e armazena os dados localmente.
    """

    # Extrai o nome da instancia do URL
    instance_name = instance_url.split('/')[-1]

    try:
        file_path = f'Instancias/{instance_name}'

        with open(file_path, 'r') as file:
            print(f'{instance_name} already found at: {file_path}')
            return
    except Exception as e:
        print(f"Error: {e}")
        print(f'Could not find {instance_name}, fetching from source...')

    # Envia uma requisição HTTP GET para pegar os dados 
    response = requests.get(instance_url)
    
    if response.status_code == 200:
        # Cria diretório para instâncias caso não exista
        Path("Instancias").mkdir(parents=True, exist_ok=True)

        # Escreve o conteúdo recebido em um .txt local usando o nome da instancia
        with open(f'Instancias/{instance_name}', 'w') as file:
            file.write(response.text)
        print(f"Data saved to {instance_name}")
    else:
        print(f"Failed to fetch data from {instance_url}. Status code: {response.status_code}")

if __name__ == "__main__":
    instance_name = 'scp41' # input("Unit test for fetching instance data. Input the instance code:")
    
    url = f"http://people.brunel.ac.uk/~mastjjb/jeb/orlib/files/{instance_name}.txt"
    get_data(instance_url=url)