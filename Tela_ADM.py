import tkinter as tk
from tkinter import ttk
from CRUD_Funcionarios import create_funcionario, update_funcionario, delete_funcionario

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

        # Aba Funcionario
        self.funcionario_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.funcionario_frame, text="Funcionario")
        self.create_funcionario_widgets()

    # Métodos para a aba Funcionario
    def create_inicio_widgets(self):
        print("Teste")
    
    def create_funcionario_widgets(self):
        # Labels
        tk.Label(self.funcionario_frame, text="Nome: ").grid(row=0, column=0)
        tk.Label(self.funcionario_frame, text="Email: ").grid(row=1, column=0)
        tk.Label(self.funcionario_frame, text="Telefone: ").grid(row=2, column=0)
        tk.Label(self.funcionario_frame, text="Cargo: ").grid(row=3, column=0)
        tk.Label(self.funcionario_frame, text="Data Admissão: ").grid(row=4, column=0)
        tk.Label(self.funcionario_frame, text="Situação: ").grid(row=5, column=0)
        tk.Label(self.funcionario_frame, text="Permissão: ").grid(row=6, column=0)
        tk.Label(self.funcionario_frame, text="Usuario: ").grid(row=7, column=0)
        tk.Label(self.funcionario_frame, text="Senha: ").grid(row=8, column=0)
        tk.Label(self.funcionario_frame, text="ID (para atualizar/excluir): ").grid(row=9, column=0)

        # Entradas
        self.func_nome_funcionario_entry = tk.Entry(self.funcionario_frame)
        self.func_email_entry = tk.Entry(self.funcionario_frame)
        self.func_telefone_entry = tk.Entry(self.funcionario_frame)
        self.func_cargo_entry = tk.Entry(self.funcionario_frame)
        self.func_data_admissao_entry = tk.Entry(self.funcionario_frame)
        self.func_situacao_entry = tk.Entry(self.funcionario_frame)
        self.func_permissao_entry = tk.Entry(self.funcionario_frame)
        self.func_usuario_entry = tk.Entry(self.funcionario_frame)
        self.func_senha_entry = tk.Entry(self.funcionario_frame, show="*")
        self.func_id_entry = tk.Entry(self.funcionario_frame)

        # Posicionamento
        self.func_nome_funcionario_entry.grid(row=0, column=1)
        self.func_email_entry.grid(row=1, column=1)
        self.func_telefone_entry.grid(row=2, column=1)
        self.func_cargo_entry.grid(row=3, column=1)
        self.func_data_admissao_entry.grid(row=4, column=1)
        self.func_situacao_entry.grid(row=5, column=1)
        self.func_permissao_entry.grid(row=6, column=1)
        self.func_usuario_entry.grid(row=7, column=1)
        self.func_senha_entry.grid(row=8, column=1)
        self.func_id_entry.grid(row=9, column=1)

        # Botões
        tk.Button(self.funcionario_frame, text="Criar Funcionario", command=self.criar_funcionarios).grid(row=10, column=0)
        tk.Button(self.funcionario_frame, text="Listar Funcionarios", command=self.listar_funcionarios).grid(row=10, column=1)
        tk.Button(self.funcionario_frame, text="Atualizar Funcionario", command=self.atualizar_funcionario).grid(row=11, column=0)
        tk.Button(self.funcionario_frame, text="Excluir Funcionario", command=self.deletetar_funcionario).grid(row=11, column=1)

        # Tabela para exibir dados
        self.func_table = ttk.Treeview(self.funcionario_frame, columns=("ID", "Nome", "Email", "Telefone", "Cargo", "Data Admissao", "Situacao", "Permissao", "Usuario", "Senha"), show="headings")
        self.func_table.grid(row=12, column=0, columnspan=2)
        
        # Definindo as colunas
        for col in self.func_table["columns"]:
            self.func_table.heading(col, text=col)
        
        # Adicionar uma barra de rolagem
        self.scrollbar = ttk.Scrollbar(self.funcionario_frame, orient="vertical", command=self.func_table.yview)
        self.scrollbar.grid(row=12, column=2, sticky="ns")
        self.func_table.configure(yscrollcommand=self.scrollbar.set)

        # Vincular o evento de clique na linha
        self.func_table.bind("<ButtonRelease-1>", self.row_selected_funcionario)

    def row_selected_funcionario(self, event):
        selected_item = self.func_table.selection()[0]
        values = self.func_table.item(selected_item, "values")
        
        # Preencher os campos com os dados da linha
        self.func_nome_funcionario_entry.delete(0, tk.END)
        self.func_nome_funcionario_entry.insert(0, values[1])  # Nome
        self.func_email_entry.delete(0, tk.END)
        self.func_email_entry.insert(0, values[2])  # Email
        self.func_telefone_entry.delete(0, tk.END)
        self.func_telefone_entry.insert(0, values[3])  # Telefone
        self.func_cargo_entry.delete(0, tk.END)
        self.func_cargo_entry.insert(0, values[4])  # Cargo
        self.func_data_admissao_entry.delete(0, tk.END)
        self.func_data_admissao_entry.insert(0, values[5])  # Data Admissão
        self.func_situacao_entry.delete(0, tk.END)
        self.func_situacao_entry.insert(0, values[6])  # Situação
        self.func_permissao_entry.delete(0, tk.END)
        self.func_permissao_entry.insert(0, values[7])  # Permissão
        self.func_usuario_entry.delete(0, tk.END)
        self.func_usuario_entry.insert(0, values[8])  # Usuario
        self.func_senha_entry.delete(0, tk.END)
        self.func_senha_entry.insert(0, values[9])  # Senha
        self.func_id_entry.delete(0, tk.END)
        self.func_id_entry.insert(0, values[0])  # ID

    def criar_funcionarios(self):
        create_funcionario(self)
    def listar_funcionarios(self):
        read_funcionario(self)
    def atualizar_funcionario(self):
        update_funcionario(self)
    def deletetar_funcionario(self):
        delete_funcionario(self)
