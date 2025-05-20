from tkinter import ttk
from CRUDS.CRUD_INJETORA import *
from CRUDS.CRUD_FORNECEDOR import *
from CRUDS.CRUD_FUNCIONARIO import *
from CRUDS.CRUD_CLIENTE import *
from CRUDS.CRUD_VENDA import *

class TELA_ADM:
    # Inicializador da classe, onde são definidos os parâmetros iniciais
    def __init__(self, root, id_funcionario):
        self.root = root  # A janela principal (root)
        self.root.title("Sistema ForneInjet - Gestão Completa - ADM")  # Título da janela
        self.root.geometry("1200x800")  # Dimensões da janela
        self.funcionario_logado_id = id_funcionario  # ID do funcionário logado
        self.fornecedores_disponiveis = {}  # Dicionário para armazenar fornecedores
        self.funcionario_dados = UPD_DADOS_FUNCIONARIOS(self.funcionario_logado_id)  # Pega os dados do funcionário logado
        self.CRIAR_WIDGETS()  # Cria todos os widgets da interface

    # Função responsável por criar os widgets (componentes gráficos) da interface
    def CRIAR_WIDGETS(self):
        self.notebook = ttk.Notebook(self.root)  # Cria o widget Notebook para abas
        self.notebook.pack(fill="both", expand=True)  # Coloca o notebook na janela principal, ocupando todo o espaço disponível
        
        # Criação de abas para diferentes funcionalidades do sistema
        self.ABA_VENDA()
        self.ABA_CLIENTE()
        self.ABA_INJETORAS()
        self.ABA_FORNECEDORES()
        self.ABA_FUNCIONARIOS()
        self.ABA_CONFIGURACAO()

    # Função que cria a aba "INJETORAS"
    def ABA_INJETORAS(self):
        # Cria o frame para a aba Injetoras
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="INJETORA")  # Adiciona a aba ao notebook com o nome "INJETORA"
        
        # Criação do formulário de entrada de dados da injetora
        form_frame = ttk.LabelFrame(frame, text="Dados da Injetora", padding=10)
        form_frame.pack(fill="x", padx=10, pady=5)  # Formulário com padding (espaçamento)

        # Importa a função GET_FORNECEDOR para pegar os fornecedores disponíveis
        from CRUDS.CRUD_FORNECEDOR import GET_FORNECEDOR  
        fornecedores = GET_FORNECEDOR()  # Chama a função que retorna a lista de fornecedores
        nomes_fornecedores = [fornecedor[1] for fornecedor in fornecedores]  # Extrai os nomes dos fornecedores
        
        # Define os campos do formulário e suas posições na grade (linha, coluna)
        campos = [
            ("Marca", 0, 0), ("Modelo", 0, 2), 
            ("Tipo de Controle", 1, 0), ("Capacidade de Injeção (g)", 1, 2),
            ("Força de Fechamento (ton)", 2, 0),
            ("Preço Médio (BRL)", 3, 0), ("Quantidade", 3, 2),
            ("Observações", 4, 0), ("Fornecedor", 4, 2)
        ]
        
        # Dicionário para armazenar os campos de entrada (Entry ou Combobox)
        self.entries_injetora = {}
        
        # Criação dos widgets para cada campo do formulário
        for campo, row, col in campos:
            lbl = ttk.Label(form_frame, text=f"{campo}:")  # Cria o rótulo (label) para cada campo
            lbl.grid(row=row, column=col, padx=5, pady=5, sticky="e")  # Coloca o label na grade
            
            if campo == "Fornecedor":  # Se o campo for "Fornecedor", usamos um Combobox
                entry = ttk.Combobox(form_frame, width=30, values=nomes_fornecedores)  # Combobox com os fornecedores
                self.fornecedor_cb_injetora = entry  # Atribui o combobox à variável
            else:
                entry = ttk.Entry(form_frame, width=30)  # Se não, é um campo de texto (Entry)
            
            entry.grid(row=row, column=col+1, padx=5, pady=5, sticky="w")  # Coloca o campo na grade
            self.entries_injetora[campo] = entry  # Armazena o campo no dicionário

        # Campo invisível que será usado para armazenar o ID da injetora
        self.injetora_id = ttk.Entry(form_frame)
        self.injetora_id.grid(row=0, column=4)
        self.injetora_id.grid_remove()  # Remove esse campo da tela, ele é invisível
        
        # Criação do frame para os botões (Novo, Salvar, Excluir)
        btn_frame = ttk.Frame(frame)
        btn_frame.pack(fill="x", padx=10, pady=5)

        # Definição das funções dos botões
        botoes = [
            ("Novo", lambda: ADD_INJETORA(self.entries_injetora, self.fornecedor_cb_injetora , self.tree_injetoras)),
            ("Salvar", lambda: UPD_INJETORA(self.entries_injetora, self.fornecedor_cb_injetora, self.injetora_id, self.tree_injetoras)),
            ("Excluir", lambda: DEL_INJETORA(self.injetora_id, self.tree_injetoras))
        ]
        
        # Criação dos botões e ligação das funções a eles
        for i, (texto, cmd) in enumerate(botoes):
            btn = ttk.Button(btn_frame, text=texto, command=cmd)  # Cria o botão
            btn.grid(row=0, column=i, padx=5)  # Coloca o botão no frame

        # Criação do frame para a tabela de injetoras
        table_frame = ttk.Frame(frame)
        table_frame.pack(fill="both", expand=True, padx=10, pady=5)

        # Criação do campo de busca
        search_frame = ttk.Frame(table_frame)
        search_frame.pack(fill="x", pady=(0, 10))

        lbl_search = ttk.Label(search_frame, text="Pesquisar:")  # Rótulo para a pesquisa
        lbl_search.pack(side="left", padx=(0, 5))

        # Campo de texto para digitar o termo de pesquisa
        self.search_entry_injetora = ttk.Entry(search_frame, width=30)
        self.search_entry_injetora.pack(side="left", fill="x", expand=True)
        self.search_entry_injetora.bind("<KeyRelease>", self.filtrar_itens_injetoras)  # Evento de tecla pressionada para buscar

        # Definição das colunas da tabela de injetoras
        cols = ["ID","Marca", "Modelo", "Tipo", "Capacidade", "Força", "Preço BRL", "Qtd", "Fornecedor","Observações"]
        
        # Criação da árvore (Treeview) para exibir as injetoras
        self.tree_injetoras = ttk.Treeview(table_frame, columns=cols, show="headings", height=15)

        # Definindo a largura e o alinhamento das colunas
        for col in cols:
            width = 100  # Largura padrão das colunas
            if col == "ID":
                width = 50  # Coluna ID com largura menor
            elif col in ["Observações", "Endereço"]:
                width = 150  # Colunas com textos longos
            elif col == "Fornecedor":
                width = 120  # Coluna de fornecedor com largura intermediária

            self.tree_injetoras.heading(col, text=col)  # Definindo o cabeçalho das colunas
            self.tree_injetoras.column(col, width=width, anchor='w' if col in ["Observações", "Endereço"] else 'center')  # Alinhamento das colunas

        # Criação da barra de rolagem vertical para a tabela
        scroll = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree_injetoras.yview)
        scroll.pack(side="right", fill="y")
        self.tree_injetoras.configure(yscrollcommand=scroll.set)  # Conecta a barra de rolagem à árvore

        # Exibe a árvore (tabela) de injetoras
        self.tree_injetoras.pack(fill="both", expand=True)
        
        # Atualiza a tabela com os dados das injetoras
        UPD_TABELA_IJETORA(self.tree_injetoras)

        # Configura a seleção de uma injetora na tabela
        self.tree_injetoras.bind("<ButtonRelease-1>", self.SELECIONAR_INJETORA)


    def filtrar_itens_injetoras(self, event=None):
        termo = self.search_entry_injetora.get().lower()  # Pega o termo de busca digitado na caixa de texto e converte para minúsculo

        # Se o termo estiver vazio, atualiza a tabela sem filtros
        if termo == "":
            UPD_TABELA_IJETORA(self.tree_injetoras)  # Chama a função para atualizar a tabela com todas as injetoras
        else: 
            # Se o termo não estiver vazio, realiza a filtragem
            if not termo:
                for child in self.tree_injetoras.get_children(""):  # Percorre todos os filhos (linhas) na árvore
                    self.tree_injetoras.reattach(child, "", "end")  # Reanexa os itens na árvore (não filtra se o termo for vazio)
                return
            
            # Filtra as injetoras com base no termo de pesquisa
            for child in self.tree_injetoras.get_children(""):  # Percorre todos os itens da tabela
                valores = self.tree_injetoras.item(child)["values"]  # Obtém os valores (dados) do item
                texto = " ".join(str(v) for v in valores).lower()  # Junta os valores em uma string e converte para minúsculo
                if termo in texto:  # Se o termo de busca estiver no texto da injetora
                    self.tree_injetoras.reattach(child, "", "end")  # Mantém o item na tabela
                else:
                    self.tree_injetoras.detach(child)  # Remove o item da tabela


    def SELECIONAR_INJETORA(self, event):
        item = self.tree_injetoras.selection()  # Obtém o item selecionado na tabela
        if item:  # Se houver um item selecionado
            id_inj = self.tree_injetoras.item(item[0])["values"][0]  # Pega o ID da injetora selecionada
            UPD_CAMPOS_INJETORA(self.entries_injetora, self.fornecedor_cb_injetora, self.injetora_id, id_inj, self.fornecedores_disponiveis)
            # Atualiza os campos de dados da injetora com base no ID selecionado

        
    def ABA_FORNECEDORES(self):
        # Criação da aba de fornecedores
        frame = ttk.Frame(self.notebook)  # Cria o frame para a aba
        self.notebook.add(frame, text="FORNECEDORES")  # Adiciona a aba com o nome "FORNECEDORES"
        
        # Criação do formulário de entrada de dados do fornecedor
        form_frame = ttk.LabelFrame(frame, text="Dados da fornecedor", padding=10)  # LabelFrame para o formulário
        form_frame.pack(fill="x", padx=10, pady=5)

        # Definição dos campos do formulário
        campos = [
            ("Nome", 0, 0), ("CNPJ", 0, 2),
            ("Telefone", 1, 0), ("E-mail", 1, 2),
            ("Website", 2, 0), ("Rua", 2, 2),
            ("Número", 3, 0), ("Bairro", 3, 2),
            ("Cidade", 4, 0), ("Estado", 4, 2),
            ("CEP", 5, 0)
        ]
        
        self.entries_fornecedor = {}  # Dicionário para armazenar os campos de entrada
        for campo, row, col in campos:
            lbl = ttk.Label(form_frame, text=f"{campo}:")  # Criação do rótulo para o campo
            lbl.grid(row=row, column=col, padx=5, pady=5, sticky="e")  # Colocação do rótulo na grade
            
            # Condicional para verificar se o campo é "Fornecedor", então cria um combobox
            if campo == "Fornecedor":
                entry = ttk.Combobox(form_frame, width=30)  # Combobox para fornecedor
                self.fornecedor_cb_fornecedor = entry  # Atribui ao combobox para usar mais tarde
            else:
                entry = ttk.Entry(form_frame, width=30)  # Criação de um campo de entrada (Entry) para os demais campos
            
            entry.grid(row=row, column=col+1, padx=5, pady=5, sticky="w")  # Coloca o campo na grade
            self.entries_fornecedor[campo] = entry  # Armazena o campo no dicionário

        # Campo invisível para armazenar o ID do fornecedor
        self.fornecedor_id = ttk.Entry(form_frame)
        self.fornecedor_id.grid(row=0, column=4)
        self.fornecedor_id.grid_remove()  # Remove o campo da tela (não será exibido)

        # Criação do frame para os botões
        btn_frame = ttk.Frame(frame)
        btn_frame.pack(fill="x", padx=10, pady=5)

        # Definição das ações dos botões
        botoes = [
            ("Novo", lambda: ADD_FORNECEDOR(self.entries_fornecedor, self.tree_fornecedor, self.funcionario_logado_id)),
            ("Salvar", lambda: UPD_FORNECEDOR(self.entries_fornecedor, self.fornecedor_id, self.tree_fornecedor, self.funcionario_logado_id)),
            ("Excluir", lambda: DEL_FORNECEDOR(self.fornecedor_id, self.tree_fornecedor))
        ]
        
        # Criação dos botões e suas ações associadas
        for i, (texto, cmd) in enumerate(botoes):
            btn = ttk.Button(btn_frame, text=texto, command=cmd)  # Cria o botão
            btn.grid(row=0, column=i, padx=5)  # Coloca o botão na grade

        # Criação do frame para a tabela de fornecedores
        table_frame = ttk.Frame(frame)
        table_frame.pack(fill="both", expand=True, padx=10, pady=5)

        # Criação do campo de pesquisa para a tabela de fornecedores
        search_frame = ttk.Frame(table_frame)
        search_frame.pack(fill="x", pady=(0, 10))

        lbl_search = ttk.Label(search_frame, text="Pesquisar:")  # Rótulo da pesquisa
        lbl_search.pack(side="left", padx=(0, 5))

        # Caixa de texto para inserir o termo de busca
        self.search_entry_fornecedor = ttk.Entry(search_frame, width=30)
        self.search_entry_fornecedor.pack(side="left", fill="x", expand=True)
        self.search_entry_fornecedor.bind("<KeyRelease>", self.filtrar_itens_fornecedor)  # Associa evento de pesquisa

        # Definição das colunas da tabela de fornecedores
        cols = ["ID","Nome", "CNPJ", "Telefone", "E-mail", "Website", "Endereço"]
        
        # Criação da tabela (Treeview) para exibir os fornecedores
        self.tree_fornecedor = ttk.Treeview(table_frame, columns=cols, show="headings", height=15)

        # Definindo a largura e o alinhamento das colunas
        for col in cols:
            width = 100  # Largura padrão das colunas
            if col == "ID":
                width = 50  # Coluna ID com largura menor
            elif col == "Endereço":
                width = 180  # Largura maior para endereço completo
            elif col == "CNPJ":
                width = 120  # Largura maior para CNPJ

            self.tree_fornecedor.heading(col, text=col)  # Define o cabeçalho das colunas
            self.tree_fornecedor.column(col, width=width, anchor='w' if col == "Endereço" else 'center')  # Alinhamento das colunas

        # Criação da barra de rolagem vertical para a tabela
        scroll = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree_fornecedor.yview)
        scroll.pack(side="right", fill="y")
        self.tree_fornecedor.configure(yscrollcommand=scroll.set)  # Conecta a barra de rolagem à tabela
        
        # Exibe a tabela de fornecedores
        self.tree_fornecedor.pack(fill="both", expand=True)
        
        # Atualiza a tabela com os dados dos fornecedores
        UPD_TABELA_FORNECEDOR(self.tree_fornecedor)

        # Define a ação quando um fornecedor é selecionado na tabela
        self.tree_fornecedor.bind("<ButtonRelease-1>", self.SELECIONAR_FORNECEDOR)

    def filtrar_itens_fornecedor(self, event=None):
        termo = self.search_entry_fornecedor.get().lower()

        if termo == "":
            UPD_TABELA_FORNECEDOR(self.tree_fornecedor)
        else: 
            if not termo:
                for child in self.tree_fornecedor.get_children(""):
                    self.tree_fornecedor.reattach(child, "", "end")
                return
            
            for child in self.tree_fornecedor.get_children(""):
                valores = self.tree_fornecedor.item(child)["values"]
                texto = " ".join(str(v) for v in valores).lower()
                if termo in texto:
                    self.tree_fornecedor.reattach(child, "", "end")
                else:
                    self.tree_fornecedor.detach(child)

    def SELECIONAR_FORNECEDOR(self, event):
        item = self.tree_fornecedor.selection()
        if item:
            id_for = self.tree_fornecedor.item(item[0])["values"][0]
            UPD_CAMPOS_FORNECEDOR(self.entries_fornecedor, self.fornecedor_id, id_for)   

    def ABA_CLIENTE(self):
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="CLIENTE")
        form_frame = ttk.LabelFrame(frame, text="Dados da Cliente", padding=10)
        form_frame.pack(fill="x", padx=10, pady=5)

        campos = [
            ("Nome", 0, 0), ("CNPJ", 0, 2),
            ("Telefone", 1, 0), ("E-mail", 1, 2),
            ("Rua", 2, 0), ("Número", 2, 2),
            ("Bairro", 3, 0), ("Cidade", 3, 2),
            ("Estado", 4, 0), ("CEP", 4, 2)
        ]
        
        self.entries_cliente = {}
        for campo, row, col in campos:
            lbl = ttk.Label(form_frame, text=f"{campo}:")
            lbl.grid(row=row, column=col, padx=5, pady=5, sticky="e")
            
            if campo == "Cliente":
                entry = ttk.Combobox(form_frame, width=30)
                self.cliente_cb_cliente = entry
            else:
                entry = ttk.Entry(form_frame, width=30)
            
            entry.grid(row=row, column=col+1, padx=5, pady=5, sticky="w")
            self.entries_cliente[campo] = entry
        self.cliente_id = ttk.Entry(form_frame)
        self.cliente_id.grid(row=0, column=4)
        self.cliente_id.grid_remove()

        btn_frame = ttk.Frame(frame)
        btn_frame.pack(fill="x", padx=10, pady=5)

        botoes = [
            ("Novo", lambda: ADD_CLIENTE(self.entries_cliente, self.tree_cliente, self.funcionario_logado_id)),
            ("Salvar", lambda: UPD_CLIENTE(self.entries_cliente, self.cliente_id, self.tree_cliente, self.funcionario_logado_id)),
            ("Excluir", lambda: DEL_CLIENTE(self.cliente_id, self.tree_cliente))
        ]
        for i, (texto, cmd) in enumerate(botoes):
            btn = ttk.Button(btn_frame, text=texto, command=cmd)
            btn.grid(row=0, column=i, padx=5)

        table_frame = ttk.Frame(frame)
        table_frame.pack(fill="both", expand=True, padx=10, pady=5)

        search_frame = ttk.Frame(table_frame)
        search_frame.pack(fill="x", pady=(0, 10))

        lbl_search = ttk.Label(search_frame, text="Pesquisar:")
        lbl_search.pack(side="left", padx=(0, 5))

        self.search_entry_cliente = ttk.Entry(search_frame, width=30)
        self.search_entry_cliente.pack(side="left", fill="x", expand=True)
        self.search_entry_cliente.bind("<KeyRelease>", self.filtrar_itens_cliente)

        cols = ["ID","Nome", "CNPJ", "Telefone", "E-mail", "Endereço"]
        self.tree_cliente = ttk.Treeview(table_frame, columns=cols, show="headings", height=15)

        for col in cols:
            width = 100  # Largura padrão
            if col == "ID":
                width = 50
            elif col == "Endereço":
                width = 180  # Largura maior para endereço completo
            elif col == "CNPJ":
                width = 120  # Largura maior para CNPJ
                
            self.tree_cliente.heading(col, text=col)
            self.tree_cliente.column(col, width=width, anchor='w' if col == "Endereço" else 'center')
        
        scroll = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree_cliente.yview)
        scroll.pack(side="right", fill="y")
        self.tree_cliente.configure(yscrollcommand=scroll.set)
        
        self.tree_cliente.pack(fill="both", expand=True)
        UPD_TABELA_CLIENTE(self.tree_cliente)
        self.tree_cliente.bind("<ButtonRelease-1>", self.SELECIONAR_CLIENTE)

    def filtrar_itens_cliente(self, event=None):
        termo = self.search_entry_cliente.get().lower()

        if termo == "":
            UPD_TABELA_CLIENTE(self.tree_cliente)
        else: 
            if not termo:
                for child in self.tree_cliente.get_children(""):
                    self.tree_cliente.reattach(child, "", "end")
                return
            
            for child in self.tree_cliente.get_children(""):
                valores = self.tree_cliente.item(child)["values"]
                texto = " ".join(str(v) for v in valores).lower()
                if termo in texto:
                    self.tree_cliente.reattach(child, "", "end")
                else:
                    self.tree_cliente.detach(child)

    def SELECIONAR_CLIENTE(self, event):
        item = self.tree_cliente.selection()
        if item:
            id_for = self.tree_cliente.item(item[0])["values"][0]
            UPD_CAMPOS_CLIENTE(self.entries_cliente, self.cliente_id, id_for)   

    def ABA_FUNCIONARIOS(self):
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="FUNCIONARIOS")
        form_frame = ttk.LabelFrame(frame, text="Dados da funcionario", padding=10)
        form_frame.pack(fill="x", padx=10, pady=5)

        campos = [
            ("Nome", 0, 0), ("Cargo", 0, 2),
            ("Telefone", 1, 0), ("E-mail", 1, 2),
            ("Usuário", 2, 0), ("Senha", 2, 2),
            ("Permissão", 3, 0), ("Situação", 3, 2),
            ("Data Admissão", 4, 0),
            ("Rua", 5, 0), ("Número", 5, 2),
            ("Bairro", 6, 0), ("Cidade", 6, 2),
            ("Estado", 7, 0), ("CEP", 7, 2)
        ]
        
        self.entries_funcionario = {}
        for campo, row, col in campos:
            lbl = ttk.Label(form_frame, text=f"{campo}:")
            lbl.grid(row=row, column=col, padx=5, pady=2, sticky="e")
            if campo == "Senha":
                entry = ttk.Entry(form_frame, width=30, show="*") 
            elif campo in ["Permissão", "Situação"]:
                entry = ttk.Combobox(form_frame, width=27, 
                                values=["admin", "usuario", "gestor"] if campo == "Permissão" else ["ativo", "inativo"])
            else:
                entry = ttk.Entry(form_frame, width=30)
            
            entry.grid(row=row, column=col+1, padx=5, pady=5, sticky="w")
            self.entries_funcionario[campo] = entry

        self.funcionario_id = ttk.Entry(form_frame)
        self.funcionario_id.grid(row=0, column=4)
        self.funcionario_id.grid_remove()

        btn_frame = ttk.Frame(frame)
        btn_frame.pack(fill="x", padx=10, pady=5)

        botoes = [
            ("Novo", lambda: ADD_FUNCIONARIO(self.entries_funcionario, self.tree_funcionarios, self.funcionario_logado_id)),
            ("Salvar", lambda: UPD_FUNCIONARIO(self.entries_funcionario, self.funcionario_id, self.tree_funcionarios, self.funcionario_logado_id)),
            ("Excluir", lambda: DEL_FUNCIONARIO(self.funcionario_id, self.tree_funcionarios, self.funcionario_logado_id))
        ]
        for i, (texto, cmd) in enumerate(botoes):
            btn = ttk.Button(btn_frame, text=texto, command=cmd)
            btn.grid(row=0, column=i, padx=5)
        
        table_frame = ttk.Frame(frame)
        table_frame.pack(fill="both", expand=True, padx=10, pady=5)

        search_frame = ttk.Frame(table_frame)
        search_frame.pack(fill="x", pady=(0, 10))

        lbl_search = ttk.Label(search_frame, text="Pesquisar:")
        lbl_search.pack(side="left", padx=(0, 5))

        self.search_entry_funcionario = ttk.Entry(search_frame, width=30)
        self.search_entry_funcionario.pack(side="left", fill="x", expand=True)
        self.search_entry_funcionario.bind("<KeyRelease>", self.filtrar_itens_funcionario)

        cols = ["ID","Nome", "Cargo", "Telefone", "E-mail", "Usuário", "Senha", "Permissão", "Situação", "Admissão","Endereço"]
        self.tree_funcionarios = ttk.Treeview(table_frame, columns=cols, show="headings", height=15)

        for col in cols:
            width = 90  
            if col == "ID":
                width = 40
            elif col == "Endereço":
                width = 150
            elif col in ["Nome", "E-mail"]:
                width = 120
            elif col == "Data Admissão":
                width = 100
                
            self.tree_funcionarios.heading(col, text=col)
            self.tree_funcionarios.column(col, width=width, anchor='w' if col in ["Endereço", "Nome"] else 'center')

        scroll = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree_funcionarios.yview)
        scroll.pack(side="right", fill="y")
        self.tree_funcionarios.configure(yscrollcommand=scroll.set)
        
        self.tree_funcionarios.pack(fill="both", expand=True)
        UPD_TABELA_FUNCIONARIO(self.tree_funcionarios)
        self.tree_funcionarios.bind("<ButtonRelease-1>", self.SELECIONAR_FUNCIONARIO)

    def filtrar_itens_funcionario(self, event=None):
        termo = self.search_entry_funcionario.get().lower()

        if termo == "":
            UPD_TABELA_FUNCIONARIO(self.tree_funcionarios)
        else: 
            if not termo:
                for child in self.tree_funcionarios.get_children(""):
                    self.tree_funcionarios.reattach(child, "", "end")
                return
            
            for child in self.tree_funcionarios.get_children(""):
                valores = self.tree_funcionarios.item(child)["values"]
                texto = " ".join(str(v) for v in valores).lower()
                if termo in texto:
                    self.tree_funcionarios.reattach(child, "", "end")
                else:
                    self.tree_funcionarios.detach(child)

    def SELECIONAR_FUNCIONARIO(self, event):
        item = self.tree_funcionarios.selection()
        if item:
            id_func = self.tree_funcionarios.item(item[0])["values"][0]
            UPD_CAMPOS_FUNCIONARIO(self.entries_funcionario, self.funcionario_id, id_func)


    def ABA_VENDA(self):
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="VENDAS")
        
        form_frame = ttk.LabelFrame(frame, text="Dados da Venda", padding=10)
        form_frame.pack(fill="x", padx=10, pady=5)

        from CRUDS.CRUD_CLIENTE import GET_CLIENTES  
        from CRUDS.CRUD_INJETORA import GET_INJETORA  
        from CRUDS.CRUD_FUNCIONARIO import GET_FUNCIONARIO  
        clientes = GET_CLIENTES()
        injetoras = GET_INJETORA()
        funcionarios = GET_FUNCIONARIO()
        
        nomes_clientes = [cliente[1] for cliente in clientes]
        nomes_injetoras = [injetora[1] for injetora in injetoras]
        nomes_funcionarios = [funcionario[1] for funcionario in funcionarios]

        campos = [
            ("Cliente", 0, 0), ("Produto", 0, 2),
            ("Quantidade", 1, 0), ("Cadastrante", 1, 2),
            ("Preço Unitário (BRL)", 2, 0),
            ("Data Venda", 3, 0), ("Forma Pagamento", 3, 2),
            ("Status Aprovação", 4, 0), ("Observações", 4, 2)
        ]
        
        self.entries_venda = {}
        for campo, row, col in campos:
            lbl = ttk.Label(form_frame, text=f"{campo}:")
            lbl.grid(row=row, column=col, padx=5, pady=5, sticky="e")
            
            if campo == "Cliente":
                entry = ttk.Combobox(form_frame, width=30, values=nomes_clientes) 
                self.cliente_cb_venda = entry
            elif campo == "Produto":
                entry = ttk.Combobox(form_frame, width=30, values=nomes_injetoras) 
                self.produto_cb_venda = entry
            elif campo == "Cadastrante":
                entry = ttk.Combobox(form_frame, width=30, values=nomes_funcionarios) 
                self.funcionario_cb_venda = entry
            elif campo == "Status Aprovação":
                entry = ttk.Combobox(form_frame, width=27, 
                                    values=["Aprovado", "Reprovado", "Em análise"])
            elif campo == "Data Venda":
                entry = ttk.Entry(form_frame, width=30)  
            else:
                entry = ttk.Entry(form_frame, width=30)
            
            entry.grid(row=row, column=col+1, padx=5, pady=5, sticky="w")
            self.entries_venda[campo] = entry

        self.venda_id = ttk.Entry(form_frame)  
        self.venda_id.grid(row=0, column=4)
        self.venda_id.grid_remove()

        btn_frame = ttk.Frame(frame)
        btn_frame.pack(fill="x", padx=10, pady=5)
        botoes = [
            ("Novo", lambda: ADD_VENDA(self.entries_venda, self.cliente_cb_venda, self.produto_cb_venda, self.tree_vendas, self.funcionario_logado_id)),
            ("Salvar", lambda: UPD_VENDA(self.entries_venda, self.cliente_cb_venda, self.venda_id, self.tree_vendas, self.funcionario_logado_id)),
            ("Excluir", lambda: DEL_VENDA(self.venda_id, self.tree_vendas))
        ]
        for i, (texto, cmd) in enumerate(botoes):
            btn = ttk.Button(btn_frame, text=texto, command=cmd)
            btn.grid(row=0, column=i, padx=5)

        # Create a frame for the sales table
        table_frame = ttk.Frame(frame)
        table_frame.pack(fill="both", expand=True, padx=10, pady=5)

        search_frame = ttk.Frame(table_frame)
        search_frame.pack(fill="x", pady=(0, 10))

        lbl_search = ttk.Label(search_frame, text="Pesquisar:")
        lbl_search.pack(side="left", padx=(0, 5))

        self.search_entry_venda = ttk.Entry(search_frame, width=30)
        self.search_entry_venda.pack(side="left", fill="x", expand=True)
        self.search_entry_venda.bind("<KeyRelease>", self.filtrar_itens_vendas)

        # Define the columns for the sales table
        cols = ["ID", "Cliente", "Produto", "Quantidade", "Preço Unitário (BRL)", "Data da Venda", "Forma Pagamento", "Status Aprovação", "Cadastrante", "Observações"]
        self.tree_vendas = ttk.Treeview(table_frame, columns=cols, show="headings", height=15)

        for col in cols:
            width = 100  # Default width
            if col == "ID":
                width = 50  # Smaller width for ID
            elif col == "Observações":
                width = 150  # Wider width for observations
            elif col == "Data da Venda":
                width = 120  # Specific width for date

            self.tree_vendas.heading(col, text=col)
            self.tree_vendas.column(col, width=width, anchor='w' if col == "Observações" else 'center')

        # Add a scrollbar for the treeview
        scroll = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree_vendas.yview)
        scroll.pack(side="right", fill="y")
        self.tree_vendas.configure(yscrollcommand=scroll.set)

        self.tree_vendas.pack(fill="both", expand=True)
        UPD_TABELA_VENDAS(self.tree_vendas)
        self.tree_vendas.bind("<ButtonRelease-1>", self.SELECIONAR_VENDA)

    def filtrar_itens_vendas(self, event=None):
        termo = self.search_entry_venda.get().lower()

        if termo == "":
            UPD_TABELA_VENDAS(self.tree_vendas)
        else:
            if not termo:
                for child in self.tree_vendas.get_children(""):  # Reset view
                    self.tree_vendas.reattach(child, "", "end")
                return

            for child in self.tree_vendas.get_children(""):  # Filter sales based on search term
                valores = self.tree_vendas.item(child)["values"]
                texto = " ".join(str(v) for v in valores).lower()
                if termo in texto:
                    self.tree_vendas.reattach(child, "", "end")
                else:
                    self.tree_vendas.detach(child)

    def SELECIONAR_VENDA(self, event):
        item = self.tree_vendas.selection()
        if item:
            id_venda = self.tree_vendas.item(item[0])["values"][0]
            UPD_CAMPOS_VENDA(self.entries_venda, self.cliente_cb_venda, self.venda_id, id_venda)

    def ABA_CONFIGURACAO(self):
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="CONFIGURAÇÃO")

        info_frame = ttk.LabelFrame(frame, text="Dados do Funcionário")
        info_frame.pack(fill="x", padx=10, pady=10)

        dados = self.funcionario_dados

        # Labels com os dados do funcionário
        ttk.Label(info_frame, text=f"Nome: {dados.get('nome', '')}").pack(anchor="w", padx=10, pady=2)
        ttk.Label(info_frame, text=f"Cargo: {dados.get('cargo', '')}").pack(anchor="w", padx=10, pady=2)
        ttk.Label(info_frame, text=f"Telefone: {dados.get('telefone', '')}").pack(anchor="w", padx=10, pady=2)
        ttk.Label(info_frame, text=f"E-mail: {dados.get('email', '')}").pack(anchor="w", padx=10, pady=2)
        ttk.Label(info_frame, text=f"Usuário: {dados.get('usuario', '')}").pack(anchor="w", padx=10, pady=2)
        ttk.Label(info_frame, text=f"Permissão: {dados.get('permissao', '')}").pack(anchor="w", padx=10, pady=2)
        ttk.Label(info_frame, text=f"Situação: {dados.get('situacao', '')}").pack(anchor="w", padx=10, pady=2)
        ttk.Label(info_frame, text=f"Admissão: {dados.get('data_admissao', '')}").pack(anchor="w", padx=10, pady=2)

        endereco_str = f"{dados.get('rua', '')}, {dados.get('numero', '')}, {dados.get('bairro', '')}, {dados.get('cidade', '')} - {dados.get('estado', '')}, CEP: {dados.get('cep', '')}"
        ttk.Label(info_frame, text=f"Endereço: {endereco_str}").pack(anchor="w", padx=10, pady=2)

        # Botões
        btn_frame = ttk.Frame(frame)
        btn_frame.pack(fill="x", padx=10, pady=10)

        botoes = [("Sair", lambda: self.SAIR(self.funcionario_logado_id))]
        for i, (texto, cmd) in enumerate(botoes):
            btn = ttk.Button(btn_frame, text=texto, command=cmd)
            btn.grid(row=0, column=i, padx=5)

    
    def SAIR(self, funcionario_logado_id):
        import tkinter as tk
        from TELAS.TELA_LOGIN import TELA_LOGIN

        self.root.withdraw()
        novo_root = tk.Toplevel()
        TELA_LOGIN(novo_root)
        novo_root.mainloop()
        print(f"Funcionário ID {funcionario_logado_id} saiu e retornou ao login.")
