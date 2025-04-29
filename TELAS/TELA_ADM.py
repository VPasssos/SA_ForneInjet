import tkinter as tk
from tkinter import ttk, messagebox
from CRUD.CRUD_INJETORA import *
from CRUD.CRUD_FORNECEDOR import *
from CRUD.CRUD_FUNCIONARIO import *
import re

class TelaPrincipal:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema ForneInjet - Gestão Completa")
        self.root.geometry("1200x800")
        
        # Variáveis de controle
        self.funcionario_logado_id = 1
        self.fornecedores_disponiveis = {}
        
        self.criar_widgets()
        self.carregar_fornecedores_combobox()
    
    def criar_widgets(self):
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill="both", expand=True)
        
        self.criar_aba_inicio()
        self.criar_aba_injetoras()
        self.criar_aba_fornecedores()
        self.criar_aba_funcionarios()
    
    def criar_aba_inicio(self):
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="Início")
        
        lbl = tk.Label(frame, text="Bem-vindo ao Sistema ForneInjet", 
                      font=("Arial", 18), pady=20)
        lbl.pack()
    
    def criar_aba_injetoras(self):
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="Injetoras")
        
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
            ("Novo", lambda: limpar_campos_injetora(self.entries_injetora, self.fornecedor_cb_injetora, self.injetora_id)),
            ("Salvar", lambda: salvar_injetora_gui(self.entries_injetora, self.fornecedor_cb_injetora, self.injetora_id, self.tree_injetoras)),
            ("Excluir", lambda: excluir_injetora_gui(self.injetora_id, self.tree_injetoras))
        ]
        
        for i, (texto, cmd) in enumerate(botoes):
            btn = ttk.Button(btn_frame, text=texto, command=cmd)
            btn.grid(row=0, column=i, padx=5)
        
        table_frame = ttk.Frame(frame)
        table_frame.pack(fill="both", expand=True, padx=10, pady=5)
        
        cols = ["ID", "Marca", "Modelo", "Tipo", "Capacidade", "Força", "Preço USD", "Preço BRL", "Qtd", "Fornecedor"]
        self.tree_injetoras = ttk.Treeview(table_frame, columns=cols, show="headings", height=15)
        
        for col in cols:
            self.tree_injetoras.heading(col, text=col)
            self.tree_injetoras.column(col, width=100)
        
        scroll = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree_injetoras.yview)
        scroll.pack(side="right", fill="y")
        self.tree_injetoras.configure(yscrollcommand=scroll.set)
        
        self.tree_injetoras.pack(fill="both", expand=True)
        carregar_injetoras_na_tabela(self.tree_injetoras)
        self.tree_injetoras.bind("<ButtonRelease-1>", self.selecionar_injetora)
    
    def criar_aba_fornecedores(self):
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="Fornecedores")
        
        form_frame = ttk.LabelFrame(frame, text="Dados do Fornecedor", padding=10)
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
            lbl.grid(row=row, column=col, padx=5, pady=2, sticky="e")
            
            entry = ttk.Entry(form_frame, width=30)
            entry.grid(row=row, column=col+1, padx=5, pady=2, sticky="w")
            self.entries_fornecedor[campo] = entry
        
        self.fornecedor_id = ttk.Entry(form_frame)
        self.fornecedor_id.grid(row=0, column=4)
        self.fornecedor_id.grid_remove()
        
        btn_frame = ttk.Frame(frame)
        btn_frame.pack(fill="x", padx=10, pady=5)
        
        botoes = [
            ("Novo", lambda: limpar_campos_fornecedor(self.entries_fornecedor, self.fornecedor_id)),
            ("Salvar", lambda: salvar_fornecedor_gui(self.entries_fornecedor, self.fornecedor_id, self.tree_fornecedores, self.funcionario_logado_id)),
            ("Excluir", lambda: excluir_fornecedor_gui(self.fornecedor_id, self.tree_fornecedores))
        ]
        
        for i, (texto, cmd) in enumerate(botoes):
            btn = ttk.Button(btn_frame, text=texto, command=cmd)
            btn.grid(row=0, column=i, padx=5)
        
        table_frame = ttk.Frame(frame)
        table_frame.pack(fill="both", expand=True, padx=10, pady=5)
        
        cols = ["ID", "Nome", "CNPJ", "Telefone", "E-mail", "Website", "Endereço"]
        self.tree_fornecedores = ttk.Treeview(table_frame, columns=cols, show="headings", height=15)
        
        for col in cols:
            self.tree_fornecedores.heading(col, text=col)
            self.tree_fornecedores.column(col, width=100)
        
        scroll = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree_fornecedores.yview)
        scroll.pack(side="right", fill="y")
        self.tree_fornecedores.configure(yscrollcommand=scroll.set)
        
        self.tree_fornecedores.pack(fill="both", expand=True)
        carregar_fornecedores_na_tabela(self.tree_fornecedores)
        self.tree_fornecedores.bind("<ButtonRelease-1>", self.selecionar_fornecedor)
    
    def criar_aba_funcionarios(self):
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="Funcionários")
        
        form_frame = ttk.LabelFrame(frame, text="Dados do Funcionário", padding=10)
        form_frame.pack(fill="x", padx=10, pady=5)
        
        campos_principais = [
            ("Nome", 0, 0), ("Cargo", 0, 2),
            ("Telefone", 1, 0), ("E-mail", 1, 2),
            ("Usuário", 2, 0), ("Senha", 2, 2),
            ("Permissão", 3, 0), ("Situação", 3, 2),
            ("Data Admissão", 4, 0)
        ]
        
        campos_endereco = [
            ("Rua", 5, 0), ("Número", 5, 2),
            ("Bairro", 6, 0), ("Cidade", 6, 2),
            ("Estado", 7, 0), ("CEP", 7, 2)
        ]
        
        self.entries_funcionario = {}
        for campo, row, col in campos_principais:
            lbl = ttk.Label(form_frame, text=f"{campo}:")
            lbl.grid(row=row, column=col, padx=5, pady=2, sticky="e")
            
            if campo == "Senha":
                entry = ttk.Entry(form_frame, width=30, show="*")
            elif campo in ["Permissão", "Situação"]:
                entry = ttk.Combobox(form_frame, width=27, values=["admin", "usuario"] if campo == "Permissão" else ["ativo", "inativo"])
            else:
                entry = ttk.Entry(form_frame, width=30)
            
            entry.grid(row=row, column=col+1, padx=5, pady=2, sticky="w")
            self.entries_funcionario[campo] = entry
        
        self.entries_endereco_funcionario = {}
        for campo, row, col in campos_endereco:
            lbl = ttk.Label(form_frame, text=f"{campo}:")
            lbl.grid(row=row, column=col, padx=5, pady=2, sticky="e")
            
            entry = ttk.Entry(form_frame, width=30)
            entry.grid(row=row, column=col+1, padx=5, pady=2, sticky="w")
            self.entries_endereco_funcionario[campo] = entry
        
        self.funcionario_id = ttk.Entry(form_frame)
        self.funcionario_id.grid(row=0, column=4)
        self.funcionario_id.grid_remove()
        
        btn_frame = ttk.Frame(frame)
        btn_frame.pack(fill="x", padx=10, pady=5)
        
        botoes = [
            ("Novo", lambda: limpar_campos_funcionario(self.entries_funcionario, self.funcionario_id)),
            ("Salvar", lambda: salvar_funcionario_gui(self.entries_funcionario, self.funcionario_id, self.tree_funcionarios)),
            ("Excluir", lambda: excluir_funcionario_gui(self.funcionario_id, self.tree_funcionarios))
        ]
        
        for i, (texto, cmd) in enumerate(botoes):
            btn = ttk.Button(btn_frame, text=texto, command=cmd)
            btn.grid(row=0, column=i, padx=5)
        
        table_frame = ttk.Frame(frame)
        table_frame.pack(fill="both", expand=True, padx=10, pady=5)
        
        cols = ["ID", "Nome", "Cargo", "Telefone", "E-mail", "Usuário", "Senha", "Permissão", "Situação", "Admissão"]
        self.tree_funcionarios = ttk.Treeview(table_frame, columns=cols, show="headings", height=15)
        
        for col in cols:
            self.tree_funcionarios.heading(col, text=col)
            self.tree_funcionarios.column(col, width=100)
        
        scroll = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree_funcionarios.yview)
        scroll.pack(side="right", fill="y")
        self.tree_funcionarios.configure(yscrollcommand=scroll.set)
        
        self.tree_funcionarios.pack(fill="both", expand=True)
        carregar_funcionarios_na_tabela(self.tree_funcionarios)
        self.tree_funcionarios.bind("<ButtonRelease-1>", self.selecionar_funcionario)
    
    def selecionar_injetora(self, event):
        item = self.tree_injetoras.selection()
        if item:
            id_inj = self.tree_injetoras.item(item[0])["values"][0]
            preencher_campos_injetora(self.entries_injetora, self.fornecedor_cb_injetora, self.injetora_id, id_inj, self.fornecedores_disponiveis)
    
    def selecionar_fornecedor(self, event):
        """Preenche os campos quando seleciona um fornecedor na tabela"""
        try:
            item = self.tree_fornecedores.selection()
            if item:
                # Obtém todos os valores da linha selecionada
                valores = self.tree_fornecedores.item(item[0])["values"]
                
                # O ID deve ser o primeiro valor (índice 0)
                id_forn = valores[0] if valores else None
                
                if id_forn:
                    # Chama a função com TODOS os parâmetros necessários
                    preencher_campos_fornecedor(
                    self.entries_fornecedor,  # Todos os campos (incluindo endereço)
                    None,                     # Placeholder para endereco_entries
                    self.fornecedor_id,
                    int(id_forn)
                )
        except Exception as e:
            messagebox.showerror("Erro", f"Falha ao selecionar fornecedor: {str(e)}")


    def selecionar_funcionario(self, event):
        item = self.tree_funcionarios.selection()
        if item:
            id_func = self.tree_funcionarios.item(item[0])["values"][0]
            preencher_campos_funcionario(self.entries_funcionario, self.funcionario_id, id_func)
    
    def carregar_fornecedores_combobox(self):
        fornecedores = listar_fornecedores()
        self.fornecedores_disponiveis = {f['ID_Fornecedor']: f['NM_Fornecedor'] for f in fornecedores}
        nomes_fornecedores = [f"{f['NM_Fornecedor']} (ID: {f['ID_Fornecedor']})" for f in fornecedores]
        self.fornecedor_cb_injetora["values"] = nomes_fornecedores
