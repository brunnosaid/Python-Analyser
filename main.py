import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from ttkthemes import ThemedTk
import os
from unidecode import unidecode
import time
import getpass

# Variável global para controlar o estado da busca
busca_em_andamento = False


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


def find(nome_arquivo, diretorio_atual):
    try:
        global busca_em_andamento

        # Verifica se o botão "Cancelar" foi pressionado
        if not busca_em_andamento:
            return False

        if os.path.isdir(diretorio_atual) and unidecode(os.path.basename(diretorio_atual).lower()) == unidecode(
                nome_arquivo.lower()):
            messagebox.showinfo("Diretório Encontrado!", f"Local Encontrado: {diretorio_atual}")
            return True

        # Processamento de Busca
        if os.path.isdir(diretorio_atual):
            for item in os.listdir(diretorio_atual):

                # Verifica se o botão "Cancelar" foi pressionado
                if not busca_em_andamento:
                    return False

                full_path = os.path.join(diretorio_atual, item)

                # Ignora pastas que começam com um ponto
                if os.path.isdir(full_path) and not item.startswith("."):
                    processamento.insert(tk.END, f"Verificando: {full_path}\n")
                    processamento.see(tk.END)
                    processamento.update()

                    if find(nome_arquivo, full_path):
                        return True
                elif os.path.isfile(full_path) and item.lower() == nome_arquivo.lower():
                    processamento.insert(tk.END, f"Arquivo encontrado: {full_path}\n")
                    processamento.see(tk.END)
                    processamento.update()

                    # Exibe uma nova janela sem widgets
                    janela_detalhes = ThemedTk(theme="arc")
                    janela_detalhes.title("Detalhes do Arquivo")
                    janela_detalhes.geometry("400x300")

                    # TELA PARA OS DETALHES DO ARQUIVO
                    detalhes = obter_detalhes_arquivo(full_path)

                    frame = ttk.Frame(janela_detalhes)
                    frame.pack(pady=10)

                    for i, (nome, valor) in enumerate(detalhes.items()):
                        label_nome = ttk.Label(frame, text=nome)
                        label_nome.grid(row=i, column=0, sticky="e", padx=5, pady=5)

                        label_valor = ttk.Label(frame, text=valor)
                        label_valor.grid(row=i, column=1, sticky="w", padx=5, pady=5)

                    janela_detalhes.mainloop()

                    return True

        # Caso não encontre nada
        return False

    except PermissionError:
        # Lidar com o erro de permissão negada
        processamento.insert(tk.END, "Erro de permissão negada ao acessar a pasta.\n")
        processamento.see(tk.END)
        processamento.update()
        return False


def search_selected_drives(nome_arquivo, drives):
    try:
        encontrado = False
        for drive in drives:
            if os.path.isdir(drive):
                if find(nome_arquivo, drive):
                    encontrado = True
                    break

        return encontrado

    except PermissionError:
        # Lidar com o erro de permissão negada
        messagebox.showwarning("Erro de Permissão", "Erro de permissão negada ao acessar o drive.")
        return False


def name_file():
    global busca_em_andamento

    # Verifica se uma busca já está em andamento
    if busca_em_andamento:
        messagebox.showinfo("Busca em Andamento", "A busca já está em andamento.")
        return

    nome_arquivo = entrada.get()
    if nome_arquivo:
        selected_drives = [drive_labels[i]['text'] for i in range(len(drive_labels)) if drive_var[i].get()]
        if not selected_drives:
            messagebox.showinfo("Nenhum drive selecionado", "Selecione pelo menos um drive para realizar a busca.")
            return

        # Define o estado da busca como em andamento
        busca_em_andamento = True

        encontrado = search_selected_drives(nome_arquivo, selected_drives)
        if not encontrado:
            messagebox.showinfo("Arquivo/Diretório não encontrado", "O arquivo/diretório especificado não foi encontrado.")

        # Redefine o estado da busca
        busca_em_andamento = False


def cancel_search():
    global busca_em_andamento

    # Define o estado da busca como cancelado
    busca_em_andamento = False

    # Limpa o widget de processamento (opcional)
    processamento.delete("1.0", tk.END)


# Cria a janela principal
janela = ThemedTk(theme="arc")

# Configurações da janela
janela.title("Search and Detail")
janela.geometry("600x400")

# Criação dos widgets
label = ttk.Label(janela, text="Digite o nome do arquivo/diretório:")
label.pack()

entrada = ttk.Entry(janela, width=40)
entrada.pack(pady=10)

# Criação de um frame para os botões Buscar e Cancelar
frame_botoes = ttk.Frame(janela)
frame_botoes.pack(pady=10)

btn_buscar = ttk.Button(frame_botoes, text="Buscar", command=name_file)
btn_buscar.pack(side=tk.LEFT, padx=5)

btn_cancelar = ttk.Button(frame_botoes, text="Cancelar", command=cancel_search)
btn_cancelar.pack(side=tk.LEFT, padx=5)

processamento = tk.Text(janela, height=10, width=60)
processamento.pack()

# Definição dos drives disponíveis
drives = ["C:/", "D:/", "E:/"]  # Adicione aqui os drives desejados

# Criação dos checkboxes para selecionar os drives
drive_labels = []
drive_var = []
for drive in drives:
    var = tk.StringVar(value="1")
    drive_var.append(var)
    label = ttk.Checkbutton(janela, text=drive, variable=var, onvalue="1", offvalue="")
    label.pack(anchor=tk.W)
    drive_labels.append(label)

# Define a pasta raiz como "Este Computador" (ou "This PC")
selected_drives = [drive_labels[i]['text'] for i in range(len(drive_labels)) if drive_var[i].get()]
selected_drives.append("This PC")

janela.mainloop()
