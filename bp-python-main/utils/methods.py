import requests
import os
import json
import time
import matplotlib.pyplot as plt
from datetime import datetime

def timer(seconds : int) -> None:
    """
    Temporizador em segundos.

    Args:
        seconds (int): A quantidade de segundos para o temporizador.

    Returns:
        None
    """
    while seconds:
        minutos, remaining_seconds = divmod(seconds, 60)
        print(f"\033[33mUma tentativa de reconexão será feita em: {minutos:02}:{remaining_seconds:02}, sem isso, a aplicação não funcionará da maneira correta\033[0m", end='\r')
        time.sleep(1)
        seconds -= 1


def plot_data(filepath="data/data.json") -> None:
    """
    Função para gerar um gráfico com base nos dados fornecidos/gerados do arquivo.json
    """
    with open(filepath, "r") as file:
        data : dict = json.load(file)

    timestamps : list = []
    east_values : list = []
    west_values : list = []
    efficiency_values : list = []

    for timestamp, values in sorted(data.items()):
        # Verifica se o TIMESTAMP está no formato correto para a coleta dos horários/datas
        try:
            timestamps.append(datetime.fromisoformat(timestamp))
        except ValueError:
            error_message("ERRO: Os valores do arquivo JSON não estão no formato adequado de timestamp! Verifique e tente novamente")
            return None # Caso o formato esteja incorreto, o programa retorna None (nada) e não causa uma exceção acabando com o uso do programa pelo usuário
        east_values.append(values["east"])
        west_values.append(values["west"])
        efficiency_values.append(values["efficiency"])

    plt.figure(figsize=(10, 6))

    plt.plot(timestamps, east_values, label="Leste", marker="o")
    plt.plot(timestamps, west_values, label="Oeste", marker="o")
    plt.plot(timestamps, efficiency_values, label="Eficiencia", marker="x")
    
    plt.title("Valores da placa Leste & Oeste e Eficiência energética em função do tempo")
    plt.xlabel("Timestamp")
    plt.ylabel("Valores")
    plt.legend()
    plt.grid(True)
    plt.xticks(rotation=45)
    
    plt.tight_layout()
    plt.show()


def save_data(east, west, efficiency, filepath="data/data.json") -> None:
    """
    Essa função deve salvar os dados em um arquivo JSON
    """
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    
    timestamp = datetime.now().isoformat()
    
    new_entry : dict = {
        timestamp: {
            "east": east,
            "west": west,
            "efficiency": efficiency
        }
    }

    if os.path.exists(filepath):
        with open(filepath, "r") as file:
            data : dict = json.load(file)  
    else:
        data : dict = {}
    
    data.update(new_entry)
    
    with open(filepath, "w") as file:
        json.dump(data, file, indent=4)


def check_connection(ip : str) -> bool:
    """
    Função para melhorar a experiência do usuário com o programa, se a conexão for estabelecida com sucesso, a função retorna True, caso contrário, False
    """
    try:
        url : str = f"http://{ip}:4041/iot/about"

        payload : dict = {}
        headers : dict = {}
        response : dict = requests.request("GET", url, headers=headers, data=payload)
    except:
        return False

    if "libVersion" in response.text:
        return True


def request_info(ip : str, param : str) -> str:
    """
    Essa função deve requisitar ao servidor informações dos parametros de placa leste, oeste e eficiencia energetica
    """
    url : str = f"http://{ip}:1026/v2/entities/urn:ngsi-ld:Iot:001/attrs/{param}"

    payload : str = ""
    headers : dict = {
    'fiware-service': 'smart',
    'fiware-servicepath': '/',
    'accept': 'application/json'
    }

    response : dict = requests.request("GET", url, headers=headers, data=payload)
    response_json : dict = response.json()

    return response_json["value"]


def print_info(ip : str, param : str) -> None:
    """
    Essa função deve requisitar ao servidor informações de acordo com o que for solicitado pelo usuario e devolver um print em amarelo com esse dado
    """
    url : str = f"http://{ip}:1026/v2/entities/urn:ngsi-ld:Iot:001/attrs/{param}"

    payload : str = ""
    headers : dict = {
    'fiware-service': 'smart',
    'fiware-servicepath': '/',
    'accept': 'application/json'
    }

    response : dict = requests.request("GET", url, headers=headers, data=payload)
    response_json : dict = response.json()

    if param == "east":
        device = "da Placa Leste"
    if param == "west":
        device = "da Placa Oeste"
    if param == "efficiency":
        device = "de Eficiência energética (a média das duas placas)"

    print(f"\033[35mO valor {device} é de {response_json["value"]}% de sua capacidade máxima\n\033[0m")


def error_message(message : str) -> None:
    """
    Função que utiliza o código Ansi para deixar o texto em vermelho

    Código ANSI é uma sequência de escape iniciada por '\ 033[' seguida por um código de cor, e terminada por m. Para resetar o estilo (voltar ao padrão), usa-se o código '\ 033[0m'
    """
    print(f"\033[31m{message}\n \033[0m")


def return_message(message : str) -> None:
    """
    Função que utiliza o código Ansi para deixar o texto em vermelho

    Código ANSI é uma sequência de escape iniciada por '\ 033[' seguida por um código de cor, e terminada por m. Para resetar o estilo (voltar ao padrão), usa-se o código '\ 033[0m'
    """
    print(f"\033[32m{message}\n \033[0m")


def bright_message(message : str) -> None:
    """
    Função que utiliza o código Ansi para deixar o texto em amarelo

    Código ANSI é uma sequência de escape iniciada por '\ 033[' seguida por um código de cor, e terminada por m. Para resetar o estilo (voltar ao padrão), usa-se o código '\ 033[0m'
    """
    print(f"\033[33m{message}\n \033[0m")


def copy_values(ip : str) -> list:
    """
    Função para realizar a leitura dos valores do STH Comet e gerar uma lista para que os valores possam ser armazenados e se necessários manipulados

    :return: list
    """
    valueList : list = [1,2,3]
    return valueList


def check_efficiency(values : list) -> int:
    """
    Função para checar a eficiência da coleta de energia dos paineis solares

    :return: int
    """
    number : int = 1
    return number


def user_guide() -> str:
    return "Olá usuário! Seja bem-vindo(a) ao programa da Bright Path. Somos uma empresa dedicada ao avanço em tecnologias sustentáveis!\nNosso projeto foi desenvolvido para conscientização da população sobre como utilizar a energia elética de maneira sustentável."
