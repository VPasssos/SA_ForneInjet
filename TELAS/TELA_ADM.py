import tkinter as tk
from tkinter import ttk
from CRUD.CRUD_INJETORA import create_injetora, read_injetora, update_injetora, delete_injetora, clear_injetora_entries
from CRUD.CRUD_FORNECEDOR import create_fornecedor, read_fornecedor, update_fornecedor, delete_fornecedor, clear_fornecedor_entries
from CRUD.CRUD_FUNCIONARIO import create_funcionario, read_funcionario, update_funcionario, delete_funcionario, clear_funcionario_entries

class TELAABAS_ADM:
    def __init__(self, root):
        self.root = root
        self.root.title("Tela Principal - Abas")
        self.root.configure(background="white")

        # Criar um Notebook (abas) para alternar entre Funcionario, Injetora e Fornecedor
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill="both", expand=True)

        # Aba Inicial
        self.inicio_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.inicio_frame, text="Inicio")
        self.create_inicio_widgets()

        # Aba injetoras
        self.injetora_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.injetora_frame, text="Injetora")
        self.create_injetora_widgets()

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
        # Adicionando o texto de boas-vindas
        welcome_label = tk.Label(self.inicio_frame, text="Seja bem-vindo ao Forninet!", 
                                font=("Century Gothic", 20, "bold"), fg="black")
        welcome_label.pack(pady=20)

    # Métodos para a aba injetora
    def create_injetora_widgets(self):
        labels_injetora = ["Quantidade", "Marca", "Modelo", "Capacidade de Injeção", "Força de Fechamento", 
                        "Tipo de Controle", "Preço Médio (USD)", "Preço Médio (BRL)", "Fornecedor", "Observação"]
        self.entries_injetora = self.create_entries(self.injetora_frame, labels_injetora)
        
        # Adicionando o campo ID para injetora
        tk.Label(self.injetora_frame, text="ID:", font=("Century Gothic", 15), fg="black").grid(row=len(labels_injetora), column=0, padx=10, pady=5, sticky="w")
        self.id_maquinas_entry = ttk.Entry(self.injetora_frame, width=50)
        self.id_maquinas_entry.grid(row=len(labels_injetora), column=1, padx=10, pady=5, sticky="w")

        # Definindo as entradas específicas da aba injetora
        self.quantidade_entry = self.entries_injetora["Quantidade"]
        self.marca_entry = self.entries_injetora["Marca"]
        self.modelo_entry = self.entries_injetora["Modelo"]
        self.capacidade_entry = self.entries_injetora["Capacidade de Injeção"]
        self.forca_fechar_entry = self.entries_injetora["Força de Fechamento"]
        self.tipo_controle_entry = self.entries_injetora["Tipo de Controle"]
        self.preco_usd_entry = self.entries_injetora["Preço Médio (USD)"]
        self.preco_brl_entry = self.entries_injetora["Preço Médio (BRL)"]
        self.fornecedor_injetora_entry = self.entries_injetora["Fornecedor"]
        self.observacao_entry = self.entries_injetora["Observação"]

        # Botões CRUD separados para Injetora
        self.create_crud_widgets_injetora(self.injetora_frame)

        # Tabela para Injetoras
        self.create_injetora_table(self.injetora_frame)
        read_injetora(self)
        
        # Vincular evento de seleção na tabela
        self.injetora_table.bind("<ButtonRelease-1>", self.on_table_select_injetora)

    def criar_injetora(self):
        create_injetora(self)
        read_injetora(self)
        
    def listar_injetoras(self):
        read_injetora(self)

    def atualizar_injetora(self):
        update_injetora(self)
        read_injetora(self)

    def deletetar_injetora(self):
        delete_injetora(self)
        read_injetora(self)

    # Métodos para a aba fornecedor
    def create_fornecedor_widgets(self):
        labels_fornecedor = ["Nome do Fornecedor", "CNPJ", "Email Fornecedor", "Endereço", "Telefone Fornecedor", "Contato Principal", "Website"]
        self.entries_fornecedor = self.create_entries(self.fornecedor_frame, labels_fornecedor)
        
        # Adicionando o campo ID para fornecedor
        tk.Label(self.fornecedor_frame, text="ID:", font=("Century Gothic", 15), fg="black").grid(row=len(labels_fornecedor), column=0, padx=10, pady=5, sticky="w")
        self.id_fornecedor_entry = ttk.Entry(self.fornecedor_frame, width=50)
        self.id_fornecedor_entry.grid(row=len(labels_fornecedor), column=1, padx=10, pady=5, sticky="w")
        
        # Definindo as entradas específicas da aba fornecedor
        self.nome_fornecedor_entry = self.entries_fornecedor["Nome do Fornecedor"]
        self.cnpj_entry = self.entries_fornecedor["CNPJ"]
        self.email_fornecedor_entry = self.entries_fornecedor["Email Fornecedor"]
        self.endereco_entry = self.entries_fornecedor["Endereço"]
        self.telefone_fornecedor_entry = self.entries_fornecedor["Telefone Fornecedor"]
        self.contato_principal_entry = self.entries_fornecedor["Contato Principal"]
        self.website_entry = self.entries_fornecedor["Website"]

        # Botões CRUD separados para Fornecedor
        self.create_crud_widgets_fornecedor(self.fornecedor_frame)

        # Tabela para Fornecedores
        self.create_fornecedor_table(self.fornecedor_frame)
        read_fornecedor(self)
        
        # Vincular evento de seleção na tabela
        self.fornecedor_table.bind("<ButtonRelease-1>", self.on_table_select_fornecedor)

    def criar_fornecedor(self):
        create_fornecedor(self)
        read_fornecedor(self)

    def listar_fornecedor(self):
        read_fornecedor(self)

    def atualizar_fornecedor(self):
        update_fornecedor(self)
        read_fornecedor(self)

    def deletetar_fornecedor(self):
        delete_fornecedor(self)
        read_fornecedor(self)

    def clear_fornecedor_entries(self):
        self.nome_fornecedor_entry.delete(0, tk.END)
        self.cnpj_entry.delete(0, tk.END)
        self.email_fornecedor_entry.delete(0, tk.END)
        self.endereco_entry.delete(0, tk.END)
        self.telefone_fornecedor_entry.delete(0, tk.END)
        self.contato_principal_entry.delete(0, tk.END)
        self.website_entry.delete(0, tk.END)
        self.id_fornecedor_entry.delete(0, tk.END)

    # Métodos para a aba funcionario
    def create_funcionario_widgets(self):
        labels_funcionario = ["Nome", "Cargo", "Telefone Funcionário", "Email Funcionário", "Data de Admissão", "Situação", "Permissão", 
                            "Usuário", "Senha"]
        self.entries_funcionario = self.create_entries(self.funcionario_frame, labels_funcionario)
        
        # Adicionando o campo ID para funcionario
        tk.Label(self.funcionario_frame, text="ID:", font=("Century Gothic", 15), fg="black").grid(row=len(labels_funcionario), column=0, padx=10, pady=5, sticky="w")
        self.id_funcionario_entry = ttk.Entry(self.funcionario_frame, width=50)
        self.id_funcionario_entry.grid(row=len(labels_funcionario), column=1, padx=10, pady=5, sticky="w")
        
        # Definindo as entradas específicas da aba funcionario
        self.nome_funcionario_entry = self.entries_funcionario["Nome"]
        self.cargo_entry = self.entries_funcionario["Cargo"]
        self.telefone_funcionario_entry = self.entries_funcionario["Telefone Funcionário"]
        self.email_funcionario_entry = self.entries_funcionario["Email Funcionário"]
        self.data_admissao_entry = self.entries_funcionario["Data de Admissão"]
        self.situacao_entry = self.entries_funcionario["Situação"]
        self.permissao_entry = self.entries_funcionario["Permissão"]
        self.usuario_entry = self.entries_funcionario["Usuário"]
        self.senha_entry = self.entries_funcionario["Senha"]

        # Botões CRUD separados para Funcionario
        self.create_crud_widgets_funcionario(self.funcionario_frame)

        # Tabela para Funcionários
        self.create_funcionario_table(self.funcionario_frame)
        read_funcionario(self)
        
        # Vincular evento de seleção na tabela
        self.funcionario_table.bind("<ButtonRelease-1>", self.on_table_select_funcionario)

    def criar_funcionario(self):
        create_funcionario(self)
        read_funcionario(self)

    def listar_funcionarios(self):
        read_funcionario(self)

    def atualizar_funcionario(self):
        update_funcionario(self)
        read_funcionario(self)

    def deletetar_funcionario(self):
        delete_funcionario(self)
        read_funcionario(self)

    # Método para criar os Entry widgets para uma aba específica
    def create_entries(self, frame, labels):
        """Cria os widgets Entry para os labels fornecidos"""
        entries = {}
        for i, label in enumerate(labels):
            # Criar o label
            tk.Label(frame, text=f"{label}: ", font=("Century Gothic", 15), fg="black").grid(row=i, column=0, padx=10, pady=5, sticky="w")
            # Criar a entrada (Entry)
            entries[label] = ttk.Entry(frame, width=50)
            entries[label].grid(row=i, column=1, padx=10, pady=5, sticky="w")
        return entries

    # Métodos para os botões CRUD nas diferentes abas
    def create_crud_widgets_injetora(self, frame):
        search_frame = ttk.Frame(frame)
        search_frame.grid(row=10, column=0, columnspan=2, pady=10, sticky="w")

        ttk.Button(search_frame, text="CRIAR INJETORA", command=self.criar_injetora, style='TButton').pack(side="left", padx=5, pady=5)
        ttk.Button(search_frame, text="LISTAR INJETORA", command=self.listar_injetoras, style='TButton').pack(side="left", padx=5, pady=5)
        ttk.Button(search_frame, text="ATUALIZAR INJETORA", command=self.atualizar_injetora, style='TButton').pack(side="left", padx=5, pady=5)
        ttk.Button(search_frame, text="EXCLUIR INJETORA", command=self.deletetar_injetora, style='TButton').pack(side="left", padx=5, pady=5)

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
    def create_injetora_table(self, frame):
        columns = ["ID", "Quantidade", "Marca", "Modelo", "Capacidade de Injeção", "Força de Fechamento", 
                   "Tipo de Controle", "Preço Médio (USD)", "Preço Médio (BRL)", "Fornecedor", "Observação"]
        self.injetora_table = self.create_table(frame, columns)

    def create_fornecedor_table(self, frame):
        columns = ["ID", "Nome do Fornecedor", "CNPJ", "Email Fornecedor", "Endereço", "Telefone Fornecedor", "Contato Principal", "Website"]
        self.fornecedor_table = self.create_table(frame, columns)

    def create_funcionario_table(self, frame):
        columns = ["ID", "Nome", "Cargo", "Telefone Funcionário", "Email Funcionário", "Data de Admissão", "Situação", "Permissão", 
                   "Usuário", "Senha"]
        self.funcionario_table = self.create_table(frame, columns)

    def create_table(self, frame, columns):
        tree = ttk.Treeview(frame, columns=columns, show="headings")
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=150, anchor="center")
        tree.grid(row=11, column=0, columnspan=2, pady=10, sticky="nsew")
        
        # Adicionar scrollbar
        scrollbar = ttk.Scrollbar(frame, orient="vertical", command=tree.yview)
        scrollbar.grid(row=11, column=2, sticky="ns")
        tree.configure(yscrollcommand=scrollbar.set)
        
        return tree

    def on_table_select_injetora(self, event):
        selected_item = self.injetora_table.selection()
        if selected_item:
            item_values = self.injetora_table.item(selected_item[0])['values']
            
            # Limpar todos os campos primeiro
            clear_injetora_entries(self)
            
            # Preencher os campos com os valores da linha selecionada
            if len(item_values) >= 11:  # Verifica se há valores suficientes
                self.id_maquinas_entry.insert(0, item_values[0])
                self.quantidade_entry.insert(0, item_values[1])
                self.marca_entry.insert(0, item_values[2])
                self.modelo_entry.insert(0, item_values[3])
                self.capacidade_entry.insert(0, item_values[4])
                self.forca_fechar_entry.insert(0, item_values[5])
                self.tipo_controle_entry.insert(0, item_values[6])
                self.preco_usd_entry.insert(0, item_values[7])
                self.preco_brl_entry.insert(0, item_values[8])
                self.fornecedor_injetora_entry.insert(0, item_values[9])
                self.observacao_entry.insert(0, item_values[10])

    def on_table_select_fornecedor(self, event):
        selected_item = self.fornecedor_table.selection()
        if selected_item:
            item_values = self.fornecedor_table.item(selected_item[0])['values']
            
            # Limpar todos os campos primeiro
            clear_fornecedor_entries(self)
            
            # Preencher os campos com os valores da linha selecionada
            if len(item_values) >= 8:  # Verifica se há valores suficientes
                self.id_fornecedor_entry.insert(0, item_values[0])
                self.nome_fornecedor_entry.insert(0, item_values[1])
                self.cnpj_entry.insert(0, item_values[2])
                self.email_fornecedor_entry.insert(0, item_values[3])
                self.endereco_entry.insert(0, item_values[4])
                self.telefone_fornecedor_entry.insert(0, item_values[5])
                self.contato_principal_entry.insert(0, item_values[6])
                self.website_entry.insert(0, item_values[7])

    def on_table_select_funcionario(self, event):
        selected_item = self.funcionario_table.selection()
        if selected_item:
            item_values = self.funcionario_table.item(selected_item[0])['values']
            
            # Limpar todos os campos primeiro
            clear_funcionario_entries(self)
            
            # Preencher os campos com os valores da linha selecionada
            if len(item_values) >= 10:  # Verifica se há valores suficientes
                self.id_funcionario_entry.insert(0, item_values[0])
                self.nome_funcionario_entry.insert(0, item_values[1])
                self.cargo_entry.insert(0, item_values[2])
                self.telefone_funcionario_entry.insert(0, item_values[3])
                self.email_funcionario_entry.insert(0, item_values[4])
                self.data_admissao_entry.insert(0, item_values[5])
                self.situacao_entry.insert(0, item_values[6])
                self.permissao_entry.insert(0, item_values[7])
                self.usuario_entry.insert(0, item_values[8])
                self.senha_entry.insert(0, item_values[9])