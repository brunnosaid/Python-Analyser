import pickle
import os


def create_cache(detalhes_arquivo):
    dados = detalhes_arquivo
    diretorio_cache = "Cache"
    path = os.path.join(diretorio_cache, "Cache.dat")

    # Cria o diretorio "Cache" caso ele não exista
    if not os.path.exists(diretorio_cache):
        os.makedirs(diretorio_cache)

    with open(path, "wb") as file:
        pickle.dump(dados, file)


# Dados Iniciais para criar o arquivo de cache
dados_iniciais = {

    "file1.txt": "C:/Path/To/file1.txt",
    "file2.dll": "D:/Path/To/file2.dll",
    "file3.exe": "E:/Path/To/file3.exe"

}

create_cache(dados_iniciais)
