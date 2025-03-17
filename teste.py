import tkinter as tk
from tkinter import ttk

class TelaAbas_ADM:
    def __init__(self, root):
        self.root = root
        self.root.title("Tela Principal - Abas")
        self.root.configure(background="white")

        # Criar um Notebook (abas) para alternar entre Funcionario, Produto e Fornecedor
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill="both", expand=True)

        # Aba Produto
        self.produto_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.produto_frame, text="Produto")
        self.create_crud_widgets(self.produto_frame, ["Nome do Produto", "Categoria", "Preço", "Quantidade em Estoque", "Código do Produto"])

        # Aba Fornecedor
        self.fornecedor_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.fornecedor_frame, text="Fornecedor")
        self.create_crud_widgets(self.fornecedor_frame, ["Nome do Fornecedor", "CNPJ", "Email", "Telefone", "Endereço"])

        # Aba Funcionario
        self.funcionario_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.funcionario_frame, text="Funcionario")
        self.create_crud_widgets(self.funcionario_frame, ["Nome do Funcionário", "Cargo", "Email", "Telefone", "Data de Admissão"])

    # Função genérica para criar widgets CRUD nas abas
    def create_crud_widgets(self, frame, labels):
        for i, label in enumerate(labels):
            # Criar o label
            tk.Label(frame, text=f"{label}: ", font=("Century Gothic", 15), fg="black").grid(row=i, column=0, padx=10, pady=5, sticky="w")
            # Criar a entrada (Entry)
            entry = ttk.Entry(frame, width=50)
            entry.grid(row=i, column=1, padx=10, pady=5, sticky="w")

# Inicializando a aplicação
if __name__ == "__main__":
    root = tk.Tk()
    app = TelaAbas_ADM(root)
    root.mainloop()
