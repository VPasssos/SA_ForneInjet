import tkinter as tk
from tkinter import ttk
from CRUD_Produtos import create_produto, update_produto, delete_produto
from CRUD_Fornecedores import create_fornecedor, update_fornecedor, delete_fornecedor
from CRUD_Funcionarios import create_funcionario, update_funcionario, delete_funcionario, read_funcionarios

class TelaAbas_ADM:
    def __init__(self, root):
        self.root = root
        self.root.title("Tela Principal - Abas")
        
        # Criar um Notebook (abas) para alternar entre Funcionario, Produto e Fornecedor
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill="both", expand=True)

        # Aba Inicial
        self.inicio_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.inicio_frame, text="Inicio")
        self.create_inicio_widgets()

        # Aba produtos
        self.produto_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.produto_frame, text="Produto")
        self.create_produto_widgets()
        
        # Aba fornecedor
        self.fornecedor_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.fornecedor_frame, text="Fornecedor")
        self.create_fornecedor_widgets()

        # Aba Funcionario
        self.funcionario_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.funcionario_frame, text="Funcionario")
        self.create_funcionario_widgets()

    # Métodos para a aba inicial
    def create_inicio_widgets(self):
        print("Tela Inicial")

    # Métodos para a aba produto
    def create_produto_widgets(self):
        self.create_crud_widgets(self.produto_frame, self.criar_produto, self.listar_produtos, self.atualizar_produto, self.deletetar_produto)

    def criar_produto(self):
        create_produto(self)

    def listar_produtos(self):
        read_produtos(self)

    def atualizar_produto(self):
        update_produto(self)

    def deletetar_produto(self):
        delete_produto(self)

    # Métodos para a aba fornecedor
    def create_fornecedor_widgets(self):
        self.create_crud_widgets(self.fornecedor_frame, self.criar_fornecedor, self.listar_fornecedores, self.atualizar_fornecedor, self.deletetar_fornecedor)

    def criar_fornecedor(self):
        create_fornecedor(self)

    def listar_fornecedores(self):
        read_fornecedores(self)

    def atualizar_fornecedor(self):
        update_fornecedor(self)

    def deletetar_fornecedor(self):
        delete_fornecedor(self)

    # Métodos para a aba funcionario
    def create_funcionario_widgets(self):
        self.create_crud_widgets(self.funcionario_frame, self.criar_funcionario, self.listar_funcionarios, self.atualizar_funcionario, self.deletetar_funcionario)

    def criar_funcionario(self):
        create_funcionario(self)

    def listar_funcionarios(self):
        read_funcionarios(self)

    def atualizar_funcionario(self):
        update_funcionario(self)

    def deletetar_funcionario(self):
        delete_funcionario(self)

    # Método para criar os widgets CRUD em qualquer aba
    def create_crud_widgets(self, frame, criar_command, listar_command, atualizar_command, deletar_command):
        # Labels
        labels = ["Nome", "Email", "Telefone", "Cargo", "Data Admissão", "Situação", "Permissão", "Usuario", "Senha", "ID (para atualizar/excluir)"]
        for i, label in enumerate(labels):
            tk.Label(frame, text=f"{label}: ").grid(row=i, column=0)

        # Entradas
        self.entries = {}
        for i, label in enumerate(labels):
            self.entries[label] = tk.Entry(frame)
            self.entries[label].grid(row=i, column=1)

        # Botões
        tk.Button(frame, text="Criar", command=criar_command).grid(row=10, column=0)
        tk.Button(frame, text="Listar", command=listar_command).grid(row=10, column=1)
        tk.Button(frame, text="Atualizar", command=atualizar_command).grid(row=11, column=0)
        tk.Button(frame, text="Excluir", command=deletar_command).grid(row=11, column=1)

        # Tabela para exibir dados
        self.table = ttk.Treeview(frame, columns=("ID", "Nome", "Email", "Telefone", "Cargo", "Data Admissao", "Situacao", "Permissao", "Usuario", "Senha"), show="headings")
        self.table.grid(row=12, column=0, columnspan=2)
        
        # Definindo as colunas
        for col in self.table["columns"]:
            self.table.heading(col, text=col)
        
        # Adicionar uma barra de rolagem
        scrollbar = ttk.Scrollbar(frame, orient="vertical", command=self.table.yview)
        scrollbar.grid(row=12, column=2, sticky="ns")
        self.table.configure(yscrollcommand=scrollbar.set)

        # Vincular o evento de clique na linha
        self.table.bind("<ButtonRelease-1>", self.row_selected)

    def row_selected(self, event):
        selected_item = self.table.selection()[0]
        values = self.table.item(selected_item, "values")
        
        # Preencher os campos com os dados da linha
        labels = ["Nome", "Email", "Telefone", "Cargo", "Data Admissao", "Situacao", "Permissao", "Usuario", "Senha", "ID"]
        for i, label in enumerate(labels):
            entry = self.entries[label]
            entry.delete(0, tk.END)
            entry.insert(0, values[i])  # Preenche cada entrada com o valor correspondente
