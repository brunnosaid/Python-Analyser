import tkinter as tk
from tkinter import ttk
import os
import pickle


def import_cache():
    diretorio = "Cache"
    path = os.path.join(diretorio, "Cache.dat")

    with open(path, "rb") as file:
        dados = pickle.load(file)

    return dados


def exibir_cache():
    dados = import_cache()

    # Criação da janela
    janela = tk.Tk()
    janela.title("Cache Memory")
    janela.geometry("400x300")

    # Criação da treeview
    tree = ttk.Treeview(janela)
    tree["columns"] = ("Valor")
    tree.column("#0", width=150, minwidth=150)
    tree.column("Valor", width=250, minwidth=250)
    tree.heading("#0", text="Chave")
    tree.heading("Valor", text="Valor")

    # Preenchimento da treeview com os dados do cache
    for chave, valor in dados.items():
        tree.insert("", tk.END, text=chave, values=(valor,))

    tree.pack(expand=True, fill=tk.BOTH)

    janela.mainloop()


if __name__ == "__main__":
    exibir_cache()
