import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from ttkthemes import ThemedTk
import os
from unidecode import unidecode
import time
import getpass


class FileDetailsWindow(tk.Toplevel):
    def __init__(self, file_path):
        super().__init__()
        self.title("Detalhes do Arquivo")
        self.geometry("300x150")
        self.resizable(False, False)

        self.file_path = file_path
        self.file_details = self._obter_detalhes_arquivo()

        self._criar_widgets()

    def _obter_detalhes_arquivo(self):
        nome_arquivo = os.path.basename(self.file_path)
        tamanho_arquivo = os.path.getsize(self.file_path)
        if tamanho_arquivo >= 1024 * 1024:
            tamanho_arquivo = f"{tamanho_arquivo / (1024 * 1024):.2f} MB"
        elif tamanho_arquivo >= 1024:
            tamanho_arquivo = f"{tamanho_arquivo / 1024:.2f} KB"
        else:
            tamanho_arquivo = f"{tamanho_arquivo} bytes"
        data_criacao = time.ctime(os.path.getctime(self.file_path))
        data_modificacao = time.ctime(os.path.getmtime(self.file_path))
        usuario = getpass.getuser()

        return {
            "Nome": nome_arquivo,
            "Tamanho": tamanho_arquivo,
            "Data de Criação": data_criacao,
            "Data de Última Modificação": data_modificacao,
            "Usuário": usuario
        }

    def _criar_widgets(self):
        frame = ttk.Frame(self)
        frame.pack(pady=10)

        for i, (nome, valor) in enumerate(self.file_details.items()):
            label_nome = ttk.Label(frame, text=nome)
            label_nome.grid(row=i, column=0, sticky="e", padx=5, pady=5)

            label_valor = ttk.Label(frame, text=valor)
            label_valor.grid(row=i, column=1, sticky="w", padx=5, pady=5)


class FileSearchApp:
    def __init__(self):
        self.busca_em_andamento = False
        self.janela = ThemedTk(theme="arc")
        self._configurar_janela()
        self._criar_widgets()
        self._configurar_bindings()
        self._iniciar_app()

    def _configurar_janela(self):
        self.janela.title("Python Explorer")
        self.janela.geometry("600x400")
        self.janela.resizable(False, False)

    def _criar_widgets(self):
        self.label = ttk.Label(self.janela, text="Digite o nome do arquivo/diretório:")
        self.label.pack()

        self.entrada = ttk.Entry(self.janela, width=40)
        self.entrada.pack(pady=10)

        self.frame_botoes = ttk.Frame(self.janela)
        self.frame_botoes.pack(pady=10)

        self.btn_buscar = ttk.Button(self.frame_botoes, text="Buscar", command=self.name_file)
        self.btn_buscar.pack(side=tk.LEFT, padx=5)

        self.btn_cancelar = ttk.Button(self.frame_botoes, text="Cancelar", command=self.cancel_search)
        self.btn_cancelar.pack(side=tk.LEFT, padx=5)

        self.processamento = tk.Text(self.janela, height=10, width=60)
        self.processamento.pack()

        self.drive_labels = []
        self.drive_var = []
        self.drives = ["C:/", "D:/", "E:/", "F:/", "G:/"]

        for drive in self.drives:
            var = tk.StringVar(value="1")
            self.drive_var.append(var)
            label = ttk.Checkbutton(self.janela, text=drive, variable=var, onvalue="1", offvalue="")
            label.pack(anchor=tk.W)
            self.drive_labels.append(label)

    def _configurar_bindings(self):
        self.janela.bind("<Return>", lambda event: self.name_file())

    def _iniciar_app(self):
        self.janela.mainloop()

    def obter_detalhes_arquivo(self, caminho_arquivo):
        nome_arquivo = os.path.basename(caminho_arquivo)
        tamanho_arquivo = os.path.getsize(caminho_arquivo)
        if tamanho_arquivo >= 1024 * 1024:
            tamanho_arquivo = f"{tamanho_arquivo / (1024 * 1024):.2f} MB"
        elif tamanho_arquivo >= 1024:
            tamanho_arquivo = f"{tamanho_arquivo / 1024:.2f} KB"
        else:
            tamanho_arquivo = f"{tamanho_arquivo} bytes"
        data_criacao = time.ctime(os.path.getctime(caminho_arquivo))
        data_modificacao = time.ctime(os.path.getmtime(caminho_arquivo))
        usuario = getpass.getuser()

        return {
            "Nome": nome_arquivo,
            "Tamanho": tamanho_arquivo,
            "Data de Criação": data_criacao,
            "Data de Última Modificação": data_modificacao,
            "Usuário": usuario
        }

    def find(self, nome_arquivo, diretorio_atual):
        try:
            if not self.busca_em_andamento:
                return False

            if os.path.isdir(diretorio_atual) and unidecode(os.path.basename(diretorio_atual).lower()) == unidecode(
                    nome_arquivo.lower()):
                messagebox.showinfo("Diretório Encontrado!", f"Local Encontrado: {diretorio_atual}")
                return True

            if os.path.isdir(diretorio_atual):
                for item in os.listdir(diretorio_atual):
                    if not self.busca_em_andamento:
                        return False

                    full_path = os.path.join(diretorio_atual, item)

                    if os.path.isdir(full_path) and not item.startswith("."):
                        self.processamento.insert(tk.END, f"Verificando: {full_path}\n")
                        self.processamento.see(tk.END)
                        self.processamento.update()

                        if self.find(nome_arquivo, full_path):
                            return True
                    elif os.path.isfile(full_path) and item.lower() == nome_arquivo.lower():
                        self.processamento.insert(tk.END, f"Arquivo encontrado: {full_path}\n")
                        self.processamento.see(tk.END)
                        self.processamento.update()

                        FileDetailsWindow(full_path)

                        return True

            return False

        except PermissionError:
            self.processamento.insert(tk.END, "Erro de permissão negada ao acessar a pasta.\n")
            self.processamento.see(tk.END)
            self.processamento.update()
            return False

    def search_selected_drives(self, nome_arquivo, drives):
        try:
            encontrado = False
            for drive in drives:
                if os.path.isdir(drive):
                    if self.find(nome_arquivo, drive):
                        encontrado = True
                        break

            return encontrado

        except PermissionError:
            messagebox.showwarning("Erro de Permissão", "Erro de permissão negada ao acessar o drive.")
            return False

    def name_file(self):
        if self.busca_em_andamento:
            messagebox.showinfo("Busca em Andamento", "A busca já está em andamento.")
            return

        nome_arquivo = self.entrada.get()
        if nome_arquivo:
            selected_drives = [self.drive_labels[i]['text'] for i in range(len(self.drive_labels)) if self.drive_var[i].get()]
            if not selected_drives:
                messagebox.showinfo("Nenhum drive selecionado", "Selecione pelo menos um drive para realizar a busca.")
                return

            self.busca_em_andamento = True

            encontrado = self.search_selected_drives(nome_arquivo, selected_drives)
            if not encontrado:
                messagebox.showinfo("Arquivo/Diretório não encontrado", "O arquivo/diretório especificado não foi encontrado.")

            self.busca_em_andamento = False

    def cancel_search(self):
        self.busca_em_andamento = False
        self.processamento.delete("1.0", tk.END)

    def _create_widgets(self):
        self.label = ttk.Label(self.janela, text="Digite o nome do arquivo/diretório:")
        self.label.pack()

        self.entrada = ttk.Entry(self.janela, width=40)
        self.entrada.pack(pady=10)

        self.frame_botoes = ttk.Frame(self.janela)
        self.frame_botoes.pack(pady=10)

        self.btn_buscar = ttk.Button(self.frame_botoes, text="Buscar", command=self.name_file)
        self.btn_buscar.pack(side=tk.LEFT, padx=5)

        self.btn_cancelar = ttk.Button(self.frame_botoes, text="Cancelar", command=self.cancel_search)
        self.btn_cancelar.pack(side=tk.LEFT, padx=5)

        self.processamento = tk.Text(self.janela, height=10, width=60)
        self.processamento.pack()

    def _create_drives_checkboxes(self):
        for drive in self.drives:
            var = tk.StringVar(value="1")
            self.drive_var.append(var)
            label = ttk.Checkbutton(self.janela, text=drive, variable=var, onvalue="1", offvalue="")
            label.pack(anchor=tk.W)
            self.drive_labels.append(label)

    def _get_selected_drives(self):
        selected_drives = [self.drive_labels[i]['text'] for i in range(len(self.drive_labels)) if self.drive_var[i].get()]
        selected_drives.append("This PC")
        return selected_drives

    def _configurar_bindings(self):
        self.janela.bind("<Return>", lambda event: self.name_file())

    def _iniciar_app(self):
        self.janela.mainloop()


class FileDetailsWindow:
    def __init__(self, file_path):
        self.file_path = file_path

        self.janela = ThemedTk(theme="arc")
        self.janela.title("Detalhes do Arquivo")
        self.janela.geometry("300x150")
        self.janela.resizable(False, False)

        self._create_widgets()

        self.janela.mainloop()

    def _create_widgets(self):
        detalhes = self.obter_detalhes_arquivo()

        frame = ttk.Frame(self.janela)
        frame.pack(pady=10)

        for i, (nome, valor) in enumerate(detalhes.items()):
            label_nome = ttk.Label(frame, text=nome)
            label_nome.grid(row=i, column=0, sticky="e", padx=5, pady=5)

            label_valor = ttk.Label(frame, text=valor)
            label_valor.grid(row=i, column=1, sticky="w", padx=5, pady=5)

    def obter_detalhes_arquivo(self):
        nome_arquivo = os.path.basename(self.file_path)
        tamanho_arquivo = os.path.getsize(self.file_path)
        if tamanho_arquivo >= 1024 * 1024:
            tamanho_arquivo = f"{tamanho_arquivo / (1024 * 1024):.2f} MB"
        elif tamanho_arquivo >= 1024:
            tamanho_arquivo = f"{tamanho_arquivo / 1024:.2f} KB"
        else:
            tamanho_arquivo = f"{tamanho_arquivo} bytes"
        data_criacao = time.ctime(os.path.getctime(self.file_path))
        data_modificacao = time.ctime(os.path.getmtime(self.file_path))
        usuario = getpass.getuser()

        return {
            "Nome": nome_arquivo,
            "Tamanho": tamanho_arquivo,
            "Data de Criação": data_criacao,
            "Data de Última Modificação": data_modificacao,
            "Usuário": usuario
        }


if __name__ == "__main__":
    app = FileSearchApp()
