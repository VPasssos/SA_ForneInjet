from tkinter import ttk
from CRUDS.CRUD_INJETORA import *
from CRUDS.CRUD_FORNECEDOR import *
from CRUDS.CRUD_FUNCIONARIO import *
from CRUDS.CRUD_CLIENTE import *
from CRUDS.CRUD_VENDA import *
class TELA_ADM:
    def __init__(self, root, id_funcionario):
        self.root = root
        self.root.title("Sistema ForneInjet - Gestão Completa - ADM")
        self.root.geometry("1200x800")
        self.funcionario_logado_id = id_funcionario
        self.fornecedores_disponiveis = {}
        self.CRIAR_WIDGETS()

    def CRIAR_WIDGETS(self):
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill="both", expand=True)
        
        self.ABA_VENDA()
        # self.ABA_CLIENTE()
        self.ABA_INJETORAS()
        self.ABA_FORNECEDORES()
        self.ABA_FUNCIONARIOS()
        
    def ABA_INJETORAS(self):
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="INJETORA")
        form_frame = ttk.LabelFrame(frame, text="Dados da Injetora", padding=10)
        form_frame.pack(fill="x", padx=10, pady=5)

        campos = [
            ("Marca", 0, 0), ("Modelo", 0, 2), 
            ("Tipo de Controle", 1, 0), ("Capacidade de Injeção (g)", 1, 2),
            ("Força de Fechamento (ton)", 2, 0), ("Preço Médio (USD)", 2, 2),
            ("Preço Médio (BRL)", 3, 0), ("Quantidade", 3, 2),
            ("Observações", 4, 0), ("Fornecedor", 4, 2)
        ]
        self.entries_injetora = {}
        for campo, row, col in campos:
            lbl = ttk.Label(form_frame, text=f"{campo}:")
            lbl.grid(row=row, column=col, padx=5, pady=5, sticky="e")
            
            if campo == "Fornecedor":
                entry = ttk.Combobox(form_frame, width=30)
                self.fornecedor_cb_injetora = entry
            else:
                entry = ttk.Entry(form_frame, width=30)
            
            entry.grid(row=row, column=col+1, padx=5, pady=5, sticky="w")
            self.entries_injetora[campo] = entry
        self.injetora_id = ttk.Entry(form_frame)
        self.injetora_id.grid(row=0, column=4)
        self.injetora_id.grid_remove()

        btn_frame = ttk.Frame(frame)
        btn_frame.pack(fill="x", padx=10, pady=5)

        botoes = [
            ("Novo", lambda: ADD_INJETORA(self.entries_injetora, self.fornecedor_id , self.tree_injetoras)),
            ("Salvar", lambda: UPD_INJETORA(self.entries_injetora, self.fornecedor_cb_injetora, self.injetora_id, self.tree_injetoras)),
            ("Excluir", lambda: DEL_INJETORA(self.injetora_id, self.tree_injetoras))
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

        self.search_entry_injetora = ttk.Entry(search_frame, width=30)
        self.search_entry_injetora.pack(side="left", fill="x", expand=True)
        self.search_entry_injetora.bind("<KeyRelease>", self.filtrar_itens_injetoras)

        cols = ["ID","Marca", "Modelo", "Tipo", "Capacidade", "Força", "Preço USD", "Preço BRL", "Qtd", "Fornecedor","Observações"]
        self.tree_injetoras = ttk.Treeview(table_frame, columns=cols, show="headings", height=15)

        for col in cols:
            width = 100  # Largura padrão
            if col == "ID":
                width = 50  # Largura menor para ID
            elif col in ["Observações", "Endereço"]:
                width = 150  # Largura maior para campos longos
            elif col == "Fornecedor":
                width = 120  # Largura intermediária para fornecedor
                
            self.tree_injetoras.heading(col, text=col)
            self.tree_injetoras.column(col, width=width, anchor='w' if col in ["Observações", "Endereço"] else 'center')
        
        scroll = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree_injetoras.yview)
        scroll.pack(side="right", fill="y")
        self.tree_injetoras.configure(yscrollcommand=scroll.set)
        
        self.tree_injetoras.pack(fill="both", expand=True)
        UPD_TABELA_IJETORA(self.tree_injetoras)
        self.tree_injetoras.bind("<ButtonRelease-1>", self.SELECIONAR_INJETORA)

    def filtrar_itens_injetoras(self, event=None):
        termo = self.search_entry_injetora.get().lower()

        if termo == "":
            UPD_TABELA_IJETORA(self.tree_injetoras)
        else: 
            if not termo:
                for child in self.tree_injetoras.get_children(""):
                    self.tree_injetoras.reattach(child, "", "end")
                return
            
            for child in self.tree_injetoras.get_children(""):
                valores = self.tree_injetoras.item(child)["values"]
                texto = " ".join(str(v) for v in valores).lower()
                if termo in texto:
                    self.tree_injetoras.reattach(child, "", "end")
                else:
                    self.tree_injetoras.detach(child)

    def SELECIONAR_INJETORA(self, event):
        item = self.tree_injetoras.selection()
        if item:
            id_inj = self.tree_injetoras.item(item[0])["values"][0]
            UPD_CAMPOS_INJETORA(self.entries_injetora, self.fornecedor_cb_injetora, self.injetora_id, id_inj, self.fornecedores_disponiveis)
        
    def ABA_FORNECEDORES(self):
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="FORNECEDORES")
        form_frame = ttk.LabelFrame(frame, text="Dados da fornecedor", padding=10)
        form_frame.pack(fill="x", padx=10, pady=5)

        campos = [
            ("Nome", 0, 0), ("CNPJ", 0, 2),
            ("Telefone", 1, 0), ("E-mail", 1, 2),
            ("Website", 2, 0), ("Rua", 2, 2),
            ("Número", 3, 0), ("Bairro", 3, 2),
            ("Cidade", 4, 0), ("Estado", 4, 2),
            ("CEP", 5, 0)
        ]
        
        self.entries_fornecedor = {}
        for campo, row, col in campos:
            lbl = ttk.Label(form_frame, text=f"{campo}:")
            lbl.grid(row=row, column=col, padx=5, pady=5, sticky="e")
            
            if campo == "Fornecedor":
                entry = ttk.Combobox(form_frame, width=30)
                self.fornecedor_cb_fornecedor = entry
            else:
                entry = ttk.Entry(form_frame, width=30)
            
            entry.grid(row=row, column=col+1, padx=5, pady=5, sticky="w")
            self.entries_fornecedor[campo] = entry
        self.fornecedor_id = ttk.Entry(form_frame)
        self.fornecedor_id.grid(row=0, column=4)
        self.fornecedor_id.grid_remove()

        btn_frame = ttk.Frame(frame)
        btn_frame.pack(fill="x", padx=10, pady=5)

        botoes = [
            ("Novo", lambda: ADD_FORNECEDOR(self.entries_fornecedor, self.tree_fornecedor)),
            ("Salvar", lambda: UPD_FORNECEDOR(self.entries_fornecedor, self.fornecedor_id, self.tree_fornecedor, self.funcionario_logado_id)),
            ("Excluir", lambda: DEL_FORNECEDOR(self.fornecedor_id, self.tree_fornecedor))
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

        self.search_entry_fornecedor = ttk.Entry(search_frame, width=30)
        self.search_entry_fornecedor.pack(side="left", fill="x", expand=True)
        self.search_entry_fornecedor.bind("<KeyRelease>", self.filtrar_itens_fornecedor)

        cols = ["ID","Nome", "CNPJ", "Telefone", "E-mail", "Website", "Endereço"]
        self.tree_fornecedor = ttk.Treeview(table_frame, columns=cols, show="headings", height=15)

        for col in cols:
            width = 100  # Largura padrão
            if col == "ID":
                width = 50
            elif col == "Endereço":
                width = 180  # Largura maior para endereço completo
            elif col == "CNPJ":
                width = 120  # Largura maior para CNPJ
                
            self.tree_fornecedor.heading(col, text=col)
            self.tree_fornecedor.column(col, width=width, anchor='w' if col == "Endereço" else 'center')
        
        scroll = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree_fornecedor.yview)
        scroll.pack(side="right", fill="y")
        self.tree_fornecedor.configure(yscrollcommand=scroll.set)
        
        self.tree_fornecedor.pack(fill="both", expand=True)
        UPD_TABELA_FORNECEDOR(self.tree_fornecedor)
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
            ("Novo", lambda: ADD_CLIENTE(self.entries_cliente, self.tree_cliente)),
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

        cols = ["ID","Nome", "CNPJ", "Telefone", "E-mail", "Website", "Endereço"]
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
                                values=["admin", "usuario"] if campo == "Permissão" else ["ativo", "inativo"])
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
            ("Novo", lambda: ADD_FUNCIONARIO(self.entries_funcionario, self.funcionario_id, self.tree_funcionarios)),
            ("Salvar", lambda: UPD_FUNCIONARIO(self.entries_funcionario, self.funcionario_id, self.tree_funcionarios)),
            ("Excluir", lambda: DEL_FUNCIONARIO(self.funcionario_id, self.tree_funcionarios))
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

        campos = [
            ("Cliente", 0, 0), ("Produto", 0, 2),
            ("Quantidade", 1, 0), ("Cadastrante", 1, 2),
            ("Preço Unitário (BRL)", 2, 0), ("Preço Unitário (USA)", 2, 2),
            ("Data Venda", 3, 0), ("Forma Pagamento", 3, 2),
            ("Status Aprovação", 4, 0), ("Observações", 4, 2)
        ]
        
        self.entries_venda = {}
        for campo, row, col in campos:
            lbl = ttk.Label(form_frame, text=f"{campo}:")
            lbl.grid(row=row, column=col, padx=5, pady=5, sticky="e")
            
         
            if campo == "Cliente":
                entry = ttk.Combobox(form_frame, width=30) 
                self.cliente_cb_venda = entry
            elif campo == "Produto":
                entry = ttk.Combobox(form_frame, width=30) 
                self.produto_cb_venda = entry
            elif campo == "Data da Venda":
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
            ("Novo", lambda: ADD_VENDA(self.entries_venda, self.cliente_cb_venda, self.produto_cb_venda, self.tree_vendas, self.funcionario_id)),
            ("Salvar", lambda: UPD_VENDA(self.entries_venda, self.cliente_cb_venda, self.venda_id, self.tree_vendas, self.funcionario_id)),
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
        cols = ["ID", "Cliente", "Produto", "Quantidade", "Preço Unitário (BRL)", "Preço Unitário (USA)", "Data da Venda", "Forma Pagamento", "Status Aprovação", "Cadastrante", "Observações"]
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