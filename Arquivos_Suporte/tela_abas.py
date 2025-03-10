import tkinter as tk
from tkinter import ttk

class TelaAbas:
    def __init__(self, root):
        self.root = root
        self.root.title("Tela Principal - Abas")

        # Criação do notebook
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill="both", expand=True)
        
        # Aba Inicial
        self.inicio_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.inicio_frame, text="Inicio")
        self.create_inicio_widgets()

        # Aba 2 (Exemplo)
        self.outra_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.outra_frame, text="Outra Aba")
        self.create_outra_widgets()

    def create_inicio_widgets(self):
        label = tk.Label(self.inicio_frame, text="Bem-vindo à Aba Inicial", font=("Arial", 16))
        label.pack(padx=10, pady=10)

    def create_outra_widgets(self):
        label = tk.Label(self.outra_frame, text="Conteúdo da Outra Aba", font=("Arial", 16))
        label.pack(padx=10, pady=10)
