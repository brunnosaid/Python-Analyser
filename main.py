import sys
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from ttkthemes import ThemedTk
import os
import shutil
import ctypes
from unidecode import unidecode


def find(nome_arquivo, diretorio_atual):
    try:
        # Verifica se o diretório atual corresponde ao nome do arquivo
        if os.path.isdir(diretorio_atual) and unidecode(os.path.basename(diretorio_atual).lower()) == unidecode(nome_arquivo.lower()):
            messagebox.showinfo("Diretório Encontrado!", f"Local Encontrado: {diretorio_atual}")
            return True

        # Processamento de Busca
        if os.path.isdir(diretorio_atual):
            for item in os.listdir(diretorio_atual):
                full_path = os.path.join(diretorio_atual, item)

                # Ignora pastas que começam com um ponto
                if os.path.isdir(full_path) and not item.startswith("."):
                    processamento.insert(tk.END, f"Verificando: {full_path}\n")
                    processamento.see(tk.END)
                    processamento.update()

                    if find(nome_arquivo, full_path):
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
    nome_arquivo = entrada.get()
    if nome_arquivo:
        selected_drives = [drive_labels[i]['text'][:-1] for i in range(len(drive_labels)) if drive_var[i].get()]
        if not selected_drives:
            messagebox.showinfo("Nenhum drive selecionado", "Selecione pelo menos um drive para realizar a busca.")
            return

        encontrado = search_selected_drives(nome_arquivo, selected_drives)
        if encontrado:
            resposta = messagebox.askyesno("Excluir Arquivo/Diretório", "Deseja excluir o arquivo/diretório encontrado?")
            if resposta:
                try:
                    # Verifica se o programa está sendo executado como administrador
                    if ctypes.windll.shell32.IsUserAnAdmin():
                        diretorio_atual = os.path.expanduser("~")
                        shutil.rmtree(diretorio_atual)
                        messagebox.showinfo("Exclusão Concluída", "Arquivo/Diretório excluído com sucesso.")
                    else:
                        # Se não estiver sendo executado como administrador, solicita privilégios elevados
                        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, __file__, None, 1)
                except PermissionError:
                    messagebox.showwarning("Erro de Permissão", "Erro de permissão negada ao excluir o arquivo/diretório.")
        else:
            messagebox.showinfo("Arquivo/Diretório não encontrado", "O arquivo/diretório especificado não foi encontrado.")


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

btn_buscar = ttk.Button(janela, text="Buscar", command=name_file)
btn_buscar.pack(pady=10)

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
selected_drives = [drive_labels[i]['text'][:-1] for i in range(len(drive_labels)) if drive_var[i].get()]
selected_drives.append("This PC")

janela.mainloop()
