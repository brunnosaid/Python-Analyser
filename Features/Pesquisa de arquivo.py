import os
import time
import getpass

def obter_detalhes_arquivo(caminho_arquivo):
    # Obter o nome do arquivo
    nome_arquivo = os.path.basename(caminho_arquivo)

    # Obter o tamanho do arquivo em bytes
    tamanho_arquivo = os.path.getsize(caminho_arquivo)

    # Converter o tamanho do arquivo para KB ou MB
    if tamanho_arquivo >= 1024 * 1024:
        tamanho_arquivo = f"{tamanho_arquivo / (1024 * 1024):.2f} MB"
    elif tamanho_arquivo >= 1024:
        tamanho_arquivo = f"{tamanho_arquivo / 1024:.2f} KB"
    else:
        tamanho_arquivo = f"{tamanho_arquivo} bytes"

    # Obter a data de criação do arquivo
    data_criacao = time.ctime(os.path.getctime(caminho_arquivo))

    # Obter a data de última modificação do arquivo
    data_modificacao = time.ctime(os.path.getmtime(caminho_arquivo))

    # Obter o usuário que criou/modificou o arquivo
    usuario = getpass.getuser()

    # Retornar os detalhes do arquivo como um dicionário
    detalhes_arquivo = {
        "Nome": nome_arquivo,
        "Tamanho": tamanho_arquivo,
        "Data de Criação": data_criacao,
        "Data de Última Modificação": data_modificacao,
        "Usuário": usuario
    }

    return detalhes_arquivo

# Exemplo de uso
caminho_arquivo = "E:\HxD\HxD.exe"
detalhes = obter_detalhes_arquivo(caminho_arquivo)
print(detalhes)
