import tkinter as tk
from tkinter import ttk
from CRUD_Produtos import create_produto, read_produto, update_produto, delete_produto
from CRUD_Fornecedores import create_fornecedor, read_fornecedor, update_fornecedor, delete_fornecedor
from CRUD_Funcionarios import create_funcionario, read_funcionario, update_funcionario, delete_funcionario

class TelaAbas_ADM:
    def __init__(self, root):
        self.root = root
        self.root.title("Tela Principal - Abas")
        self.root.configure(background="white")

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
        labels_produto = ["Tipo", "Marca", "Modelo", "Capacidade de Injeção", "Força de Fechamento", 
                        "Tipo de Controle", "Preço Médio (USD)", "Preço Médio (BRL)", "Fornecedor", "Observação"]
        self.create_entries(self.produto_frame, labels_produto)
        
        # Definindo as entradas específicas da aba produto
        self.tipo_entry = self.entries["Tipo"]
        self.marca_entry = self.entries["Marca"]
        self.modelo_entry = self.entries["Modelo"]
        self.capacidade_entry = self.entries["Capacidade de Injeção"]
        self.forca_fechar_entry = self.entries["Força de Fechamento"]
        self.tipo_controle_entry = self.entries["Tipo de Controle"]
        self.preco_usd_entry = self.entries["Preço Médio (USD)"]
        self.preco_brl_entry = self.entries["Preço Médio (BRL)"]
        self.fornecedor_produto_entry = self.entries["Fornecedor"]
        self.observacao_entry = self.entries["Observação"]

        # Botões CRUD separados para Produto
        self.create_crud_widgets_produto(self.produto_frame)

        # Tabela para Produtos
        self.create_produto_table(self.produto_frame)

    def criar_produto(self):
        create_produto(self)

    def listar_produtos(self):
        read_produto(self)

    def atualizar_produto(self):
        update_produto(self)

    def deletetar_produto(self):
        delete_produto(self)

    # Métodos para a aba fornecedor
    def create_fornecedor_widgets(self):
        labels_fornecedor = ["Nome do Fornecedor", "CNPJ", "Email", "Endereço", "Telefone", "Contato Principal", "Website"]
        self.create_entries(self.fornecedor_frame, labels_fornecedor)
        
        # Botões CRUD separados para Fornecedor
        self.create_crud_widgets_fornecedor(self.fornecedor_frame)

        # Definindo as entradas específicas da aba fornecedor
        self.nome_fornecedor_entry = self.entries["Nome do Fornecedor"]
        self.cnpj_entry = self.entries["CNPJ"]
        self.email_entry = self.entries["Email"]
        self.endereco_entry = self.entries["Endereço"]
        self.telefone_entry = self.entries["Telefone"]
        self.contato_principal_entry = self.entries["Contato Principal"]
        self.website_entry = self.entries["Website"]
        self.id_fornecedor_entry = ttk.Entry(self.fornecedor_frame, width=50)

        # Tabela para Fornecedores
        self.create_fornecedor_table(self.fornecedor_frame)

    def criar_fornecedor(self):
        create_fornecedor(self)

    def listar_fornecedor(self):
        read_fornecedor(self)

    def atualizar_fornecedor(self):
        update_fornecedor(self)

    def deletetar_fornecedor(self):
        delete_fornecedor(self)

    def clear_fornecedor_entries(self):
        self.nome_fornecedor_entry.delete(0, tk.END)
        self.cnpj_entry.delete(0, tk.END)
        self.email_entry.delete(0, tk.END)
        self.endereco_entry.delete(0, tk.END)
        self.telefone_entry.delete(0, tk.END)
        self.contato_principal_entry.delete(0, tk.END)
        self.website_entry.delete(0, tk.END)
        self.id_fornecedor_entry.delete(0, tk.END)

    # Métodos para a aba funcionario
    def create_funcionario_widgets(self):
        labels_funcionario = ["Nome", "Cargo", "Telefone", "Email", "Data de Admissão", "Situação", "Permissão", 
                            "Usuário", "Senha"]
        self.create_entries(self.funcionario_frame, labels_funcionario)
        
        # Botões CRUD separados para Funcionario
        self.create_crud_widgets_funcionario(self.funcionario_frame)

        # Definindo as entradas específicas da aba funcionario
        self.nome_funcionario_entry = self.entries["Nome"]
        self.cargo_entry = self.entries["Cargo"]
        self.telefone_funcionario_entry = self.entries["Telefone"]
        self.email_funcionario_entry = self.entries["Email"]
        self.data_admissao_entry = self.entries["Data de Admissão"]
        self.situacao_entry = self.entries["Situação"]
        self.permissao_entry = self.entries["Permissão"]
        self.usuario_entry = self.entries["Usuário"]
        self.senha_entry = self.entries["Senha"]

        # Tabela para Funcionários
        self.create_funcionario_table(self.funcionario_frame)

    def criar_funcionario(self):
        create_funcionario(self)

    def listar_funcionarios(self):
        read_funcionario(self)

    def atualizar_funcionario(self):
        update_funcionario(self)

    def deletetar_funcionario(self):
        delete_funcionario(self)

    # Método para criar os Entry widgets para uma aba específica
    def create_entries(self, frame, labels):
        """Cria os widgets Entry para os labels fornecidos"""
        self.entries = {}
        for i, label in enumerate(labels):
            # Criar o label
            tk.Label(frame, text=f"{label}: ", font=("Century Gothic", 15), fg="black").grid(row=i, column=0, padx=10, pady=5, sticky="w")
            # Criar a entrada (Entry)
            self.entries[label] = ttk.Entry(frame, width=50)  # Tamanho ajustado para entradas
            self.entries[label].grid(row=i, column=1, padx=10, pady=5, sticky="w")

    # Métodos para os botões CRUD nas diferentes abas

    def create_crud_widgets_produto(self, frame):
        search_frame = ttk.Frame(frame)
        search_frame.grid(row=10, column=0, columnspan=2, pady=10, sticky="w")

        ttk.Button(search_frame, text="CRIAR PRODUTO", command=self.criar_produto, style='TButton').pack(side="left", padx=5, pady=5)
        ttk.Button(search_frame, text="LISTAR PRODUTO", command=self.listar_produtos, style='TButton').pack(side="left", padx=5, pady=5)
        ttk.Button(search_frame, text="ATUALIZAR PRODUTO", command=self.atualizar_produto, style='TButton').pack(side="left", padx=5, pady=5)
        ttk.Button(search_frame, text="EXCLUIR PRODUTO", command=self.deletetar_produto, style='TButton').pack(side="left", padx=5, pady=5)

    def create_crud_widgets_fornecedor(self, frame):
        search_frame = ttk.Frame(frame)
        search_frame.grid(row=10, column=0, columnspan=2, pady=10, sticky="w")

        ttk.Button(search_frame, text="CRIAR FORNECEDOR", command=self.criar_fornecedor, style='TButton').pack(side="left", padx=5, pady=5)
        ttk.Button(search_frame, text="LISTAR FORNECEDOR", command=self.listar_fornecedor, style='TButton').pack(side="left", padx=5, pady=5)
        ttk.Button(search_frame, text="ATUALIZAR FORNECEDOR", command=self.atualizar_fornecedor, style='TButton').pack(side="left", padx=5, pady=5)
        ttk.Button(search_frame, text="EXCLUIR FORNECEDOR", command=self.deletetar_fornecedor, style='TButton').pack(side="left", padx=5, pady=5)

    def create_crud_widgets_funcionario(self, frame):
        search_frame = ttk.Frame(frame)
        search_frame.grid(row=10, column=0, columnspan=2, pady=10, sticky="w")

        ttk.Button(search_frame, text="CRIAR FUNCIONÁRIO", command=self.criar_funcionario, style='TButton').pack(side="left", padx=5, pady=5)
        ttk.Button(search_frame, text="LISTAR FUNCIONÁRIO", command=self.listar_funcionarios, style='TButton').pack(side="left", padx=5, pady=5)
        ttk.Button(search_frame, text="ATUALIZAR FUNCIONÁRIO", command=self.atualizar_funcionario, style='TButton').pack(side="left", padx=5, pady=5)
        ttk.Button(search_frame, text="EXCLUIR FUNCIONÁRIO", command=self.deletetar_funcionario, style='TButton').pack(side="left", padx=5, pady=5)

    # Métodos para as tabelas de cada aba

    def create_produto_table(self, frame):
        columns = ["ID", "Tipo", "Marca", "Modelo", "Capacidade de Injeção", "Força de Fechamento", 
                   "Tipo de Controle", "Preço Médio (USD)", "Preço Médio (BRL)", "Fornecedor", "Observação"]
        self.produto_table = ttk.Treeview(frame, columns=columns, show="headings")
        for col in columns:
            self.produto_table.heading(col, text=col)
            self.produto_table.column(col, width=120)
        self.produto_table.grid(row=11, column=0, columnspan=2, pady=10, sticky="w")

        # Vincula a função de clique para selecionar uma linha
        self.produto_table.bind("<ButtonRelease-1>", self.on_table_select_produto)

    def create_fornecedor_table(self, frame):
        columns = ["ID", "Nome", "CNPJ", "Email", "Endereço", "Telefone", "Contato Principal", "Website"]
        self.fornecedor_table = ttk.Treeview(frame, columns=columns, show="headings")
        for col in columns:
            self.fornecedor_table.heading(col, text=col)
            self.fornecedor_table.column(col, width=120)
        self.fornecedor_table.grid(row=11, column=0, columnspan=2, pady=10, sticky="w")

        # Vincula a função de clique para selecionar uma linha
        self.fornecedor_table.bind("<ButtonRelease-1>", self.on_table_select_fornecedor)

    def create_funcionario_table(self, frame):
        columns = ["ID", "Nome", "Cargo", "Telefone", "Email", "Data de Admissão", "Situação", "Permissão", 
                   "Usuário", "Senha"]
        self.funcionario_table = ttk.Treeview(frame, columns=columns, show="headings")
        for col in columns:
            self.funcionario_table.heading(col, text=col)
            self.funcionario_table.column(col, width=120)
        self.funcionario_table.grid(row=11, column=0, columnspan=2, pady=10, sticky="w")

        # Vincula a função de clique para selecionar uma linha
        self.funcionario_table.bind("<ButtonRelease-1>", self.on_table_select_funcionario)

    def on_table_select_produto(self, event):
        selected_item = self.produto_table.selection()
        if selected_item:
            item_values = self.produto_table.item(selected_item)['values']
            # Preenche os campos de entrada com os dados da linha selecionada
            self.tipo_entry.delete(0, tk.END)
            self.tipo_entry.insert(0, item_values[1])
            self.marca_entry.delete(0, tk.END)
            self.marca_entry.insert(0, item_values[2])
            self.modelo_entry.delete(0, tk.END)
            self.modelo_entry.insert(0, item_values[3])
            self.capacidade_entry.delete(0, tk.END)
            self.capacidade_entry.insert(0, item_values[4])
            self.forca_fechar_entry.delete(0, tk.END)
            self.forca_fechar_entry.insert(0, item_values[5])
            self.tipo_controle_entry.delete(0, tk.END)
            self.tipo_controle_entry.insert(0, item_values[6])
            self.preco_usd_entry.delete(0, tk.END)
            self.preco_usd_entry.insert(0, item_values[7])
            self.preco_brl_entry.delete(0, tk.END)
            self.preco_brl_entry.insert(0, item_values[8])
            self.fornecedor_produto_entry.delete(0, tk.END)
            self.fornecedor_produto_entry.insert(0, item_values[9])
            self.observacao_entry.delete(0, tk.END)
            self.observacao_entry.insert(0, item_values[10])

    def on_table_select_fornecedor(self, event):
        selected_item = self.fornecedor_table.selection()
        if selected_item:
            item_values = self.fornecedor_table.item(selected_item)['values']
            # Preenche os campos de entrada com os dados da linha selecionada
            self.nome_fornecedor_entry.delete(0, tk.END)
            self.nome_fornecedor_entry.insert(0, item_values[1])
            self.cnpj_entry.delete(0, tk.END)
            self.cnpj_entry.insert(0, item_values[2])
            self.email_entry.delete(0, tk.END)
            self.email_entry.insert(0, item_values[3])
            self.endereco_entry.delete(0, tk.END)
            self.endereco_entry.insert(0, item_values[4])
            self.telefone_entry.delete(0, tk.END)
            self.telefone_entry.insert(0, item_values[5])
            self.contato_principal_entry.delete(0, tk.END)
            self.contato_principal_entry.insert(0, item_values[6])
            self.website_entry.delete(0, tk.END)
            self.website_entry.insert(0, item_values[7])

    def on_table_select_funcionario(self, event):
        selected_item = self.funcionario_table.selection()
        if selected_item:
            item_values = self.funcionario_table.item(selected_item)['values']
            # Preenche os campos de entrada com os dados da linha selecionada
            self.nome_funcionario_entry.delete(0, tk.END)
            self.nome_funcionario_entry.insert(0, item_values[1])
            self.cargo_entry.delete(0, tk.END)
            self.cargo_entry.insert(0, item_values[2])
            self.telefone_funcionario_entry.delete(0, tk.END)
            self.telefone_funcionario_entry.insert(0, item_values[3])
            self.email_funcionario_entry.delete(0, tk.END)
            self.email_funcionario_entry.insert(0, item_values[4])
            self.data_admissao_entry.delete(0, tk.END)
            self.data_admissao_entry.insert(0, item_values[5])
            self.situacao_entry.delete(0, tk.END)
            self.situacao_entry.insert(0, item_values[6])
            self.permissao_entry.delete(0, tk.END)
            self.permissao_entry.insert(0, item_values[7])
            self.usuario_entry.delete(0, tk.END)
            self.usuario_entry.insert(0, item_values[8])
            self.senha_entry.delete(0, tk.END)
            self.senha_entry.insert(0, item_values[9])
