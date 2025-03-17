import tkinter as tk
from tkinter import ttk

# from CRUD_Produtos import create_produto, update_produto, delete_produto, read_produtos
# from CRUD_Fornecedores import create_fornecedor, update_fornecedor, delete_fornecedor, read_fornecedores
# from CRUD_Funcionarios import create_funcionario, update_funcionario, delete_funcionario, read_funcionarios

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
        labels_produto = ["Tipo", "Marca", "Modelo", "Capacidade de Injeção", "Força de Fechamento", "Tipo de Controle", "Preço Médio (USD)", "Preço Médio (BRL)", "Fornecedor", "Observação"]
        self.create_crud_widgets(self.produto_frame, labels_produto, self.criar_produto, self.listar_produtos, self.atualizar_produto, self.deletetar_produto)

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
        labels_fornecedor = ["Nome do Fornecedor", "Endereço", "Telefone", "Email", "Contato Principal", "Website"]
        self.create_crud_widgets(self.fornecedor_frame, labels_fornecedor, self.criar_fornecedor, self.listar_fornecedores, self.atualizar_fornecedor, self.deletetar_fornecedor)

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
        labels_funcionario = ["Nome", "Cargo", "Telefone", "Email", "Data de Admissão", "Situação", "Permissão", "Usuário", "Senha"]
        self.create_crud_widgets(self.funcionario_frame, labels_funcionario, self.criar_funcionario, self.listar_funcionarios, self.atualizar_funcionario, self.deletetar_funcionario)

    def criar_funcionario(self):
        create_funcionario(self)

    def listar_funcionarios(self):
        read_funcionarios(self)

    def atualizar_funcionario(self):
        update_funcionario(self)

    def deletetar_funcionario(self):
        delete_funcionario(self)

    # Método genérico para criar os widgets CRUD em qualquer aba
    def create_crud_widgets(self, frame, labels, criar_command, listar_command, atualizar_command, deletar_command):
        # Entradas
        self.entries = {}
        for i, label in enumerate(labels):
            # Criar o label
            tk.Label(frame, text=f"{label}: ", font=("Century Gothic", 15), fg="black").grid(row=i, column=0, padx=10, pady=5, sticky="w")
            # Criar a entrada (Entry)
            self.entries[label] = ttk.Entry(frame, width=50)  # Tamanho ajustado para entradas
            self.entries[label].grid(row=i, column=1, padx=10, pady=5, sticky="w")  # Mantém a diferença de espaçamento entre os campos

        # Barra de pesquisa (filtro por nome) e botões na linha horizontal
        search_frame = ttk.Frame(frame)
        search_frame.grid(row=len(labels), column=0, columnspan=2, pady=10, sticky="w")

        # Barra de pesquisa
        tk.Label(search_frame, text="Pesquisa:", font=("Century Gothic", 15), fg="black").pack(side="left", padx=10)
        self.search_entry = ttk.Entry(search_frame, width=50)

        # Adicionar o texto de placeholder "Insira um nome"
        self.search_entry.insert(0, "Insira um nome")
        self.search_entry.bind("<FocusIn>", self.on_entry_click)  # Quando o campo receber foco
        self.search_entry.bind("<FocusOut>", self.on_focusout)  # Quando o campo perder o foco
        self.search_entry.pack(side="left", padx=10)

        # Criar o estilo para os botões
        style = ttk.Style()
        style.configure('TButton', 
                        font=("Century Gothic", 8, "bold"),  # Font em negrito
                        foreground="black", 
                        padding=(2))  # Ajuste de padding, um pouco maior que o Entry

        # Botões de CRUD e Filtro (em linha horizontal, ao lado da barra de pesquisa)
        ttk.Button(search_frame, text="FILTRAR", command=self.filtrar_tabela, style='TButton').pack(side="left", padx=5, pady=5)
        ttk.Button(search_frame, text="CRIAR", command=criar_command, style='TButton').pack(side="left", padx=5, pady=5)
        ttk.Button(search_frame, text="LISTAR", command=listar_command, style='TButton').pack(side="left", padx=5, pady=5)
        ttk.Button(search_frame, text="ATUALIZAR", command=atualizar_command, style='TButton').pack(side="left", padx=5, pady=5)
        ttk.Button(search_frame, text="EXCLUIR", command=deletar_command, style='TButton').pack(side="left", padx=5, pady=5)

        # Tabela para exibir dados
        self.table = ttk.Treeview(frame, columns=("ID", "Nome", "Email", "Telefone", "Cargo", "Data Admissao", "Situacao", "Permissao", "Usuario", "Senha"), show="headings")
        self.table.grid(row=len(labels)+1, column=0, columnspan=3, padx=15, pady=15, sticky="nsew")
        
        # Definindo as colunas
        for col in self.table["columns"]:
            self.table.heading(col, text=col)
        
        # Ajustando a largura das colunas específicas (ID e Permissao)
        self.table.column("ID", width=60, anchor="center")  # Diminuir a largura da coluna "ID"
        self.table.column("Permissao", width=80, anchor="center")  # Diminuir a largura da coluna "Permissao"

        # Adicionar uma barra de rolagem
        scrollbar = ttk.Scrollbar(frame, orient="vertical", command=self.table.yview)
        scrollbar.grid(row=len(labels)+1, column=2, sticky="ns")
        self.table.configure(yscrollcommand=scrollbar.set)

        # Configurar o comportamento de redimensionamento para preencher o espaço
        frame.grid_rowconfigure(len(labels)+1, weight=1)
        frame.grid_columnconfigure(1, weight=1)

        # Configurar a centralização do espaço restante
        frame.grid_columnconfigure(2, weight=1)

        # Ajuste na tabela para ter a largura correta com a barra de rolagem
        self.table.grid(row=len(labels)+1, column=0, columnspan=2, padx=15, pady=15, sticky="nsew")
        scrollbar.grid(row=len(labels)+1, column=2, sticky="ns")

    # Função de filtro para a tabela
    def filtrar_tabela(self):
        nome_filtro = self.search_entry.get().lower()  # Obtém o nome digitado para pesquisa
        for row in self.table.get_children():
            values = self.table.item(row, "values")
            nome = values[1].lower()  # Coluna "Nome" (índice 1)
            
            if nome_filtro in nome:
                self.table.item(row, tags="match")  # Marcar a linha como "match"
                self.table.selection_add(row)  # Selecionar a linha que corresponde ao filtro
            else:
                self.table.item(row, tags="no_match")  # Marcar a linha como "no_match"
                self.table.selection_remove(row)  # Remover a seleção da linha que não corresponde ao filtro

    # Função para limpar o texto de placeholder quando o campo recebe foco
    def on_entry_click(self, event):
        if self.search_entry.get() == "Insira um nome":
            self.search_entry.delete(0, tk.END)  # Limpa o texto de placeholder

    # Função para restaurar o texto de placeholder se o campo estiver vazio
    def on_focusout(self, event):
        if self.search_entry.get() == "":
            self.search_entry.insert(0, "Insira um nome")  # Restaura o texto de placeholder
