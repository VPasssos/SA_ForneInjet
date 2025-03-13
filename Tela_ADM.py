import tkinter as tk
from tkinter import ttk, messagebox
from CRUD_Fornecedores import create_fornecedor, read_fornecedor, update_fornecedor, delete_fornecedor
from CRUD_Funcionarios import create_funcionario, read_funcionario, update_funcionario, delete_funcionario
from CRUD_Produtos import create_produto, read_produto, update_produto, delete_produto

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

        # Aba produtos
        self.produtos_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.produtos_frame, text="produtos")
        self.create_produtos_widgets()

        # Aba fornecedores
        self.fornecedores_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.fornecedores_frame, text="fornecedores")



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
        tk.Button(self.funcionario_frame, text="Criar Funcionario", command=self.create_funcionario).grid(row=10, column=0)
        tk.Button(self.funcionario_frame, text="Listar Funcionarios", command=self.read_funcionarios).grid(row=10, column=1)
        tk.Button(self.funcionario_frame, text="Atualizar Funcionario", command=self.update_funcionario).grid(row=11, column=0)
        tk.Button(self.funcionario_frame, text="Excluir Funcionario", command=self.delete_funcionario).grid(row=11, column=1)

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

    def create_funcionario(self):
        nome_funcionario = self.func_nome_funcionario_entry.get()
        cargo = self.func_cargo_entry.get()
        telefone = self.func_telefone_entry.get()
        email = self.func_email_entry.get()
        data_admissao = self.func_data_admissao_entry.get()
        situacao = self.func_situacao_entry.get()
        permissao = self.func_permissao_entry.get()
        usuario = self.func_usuario_entry.get()
        senha = self.func_senha_entry.get()

        if nome_funcionario and cargo and telefone and email and data_admissao and situacao and permissao and usuario and senha:
            create_funcionario(nome_funcionario, cargo, telefone, email, data_admissao, situacao, permissao, usuario, senha)
            messagebox.showinfo("Sucesso", "Funcionário criado com sucesso!")
            self.clear_funcionario_entries()
            self.read_funcionarios()  # Atualizar a tabela
        else:
            messagebox.showerror("Erro", "Todos os campos são obrigatórios")

    def read_funcionarios(self):
        funcionarios = read_funcionario()
        for row in self.func_table.get_children():
            self.func_table.delete(row)  # Limpar a tabela antes de adicionar novos dados

        for funcionario in funcionarios:
            self.func_table.insert("", "end", values=funcionario)  # Inserir os dados na tabela

    def update_funcionario(self):
        func_id = self.func_id_entry.get()
        nome = self.func_nome_funcionario_entry.get()
        email = self.func_email_entry.get()
        telefone = self.func_telefone_entry.get()
        cargo = self.func_cargo_entry.get()
        data_admissao = self.func_data_admissao_entry.get()
        situacao = self.func_situacao_entry.get()
        permissao = self.func_permissao_entry.get()
        usuario = self.func_usuario_entry.get()
        senha = self.func_senha_entry.get()

        if func_id and nome and email and telefone and cargo and data_admissao and situacao and permissao and usuario and senha:
            update_funcionario(func_id, nome, email, telefone, cargo, data_admissao, situacao, permissao, usuario, senha)
            messagebox.showinfo("Sucesso", "Funcionário atualizado com sucesso!")
            self.clear_funcionario_entries()
            self.read_funcionarios()  # Atualizar a tabela
        else:
            messagebox.showerror("Erro", "Todos os campos são obrigatórios")

    def delete_funcionario(self):
        func_id = self.func_id_entry.get()
        if func_id:
            delete_funcionario(func_id)
            messagebox.showinfo("Sucesso", "Funcionário excluído com sucesso!")
            self.func_id_entry.delete(0, tk.END)
            self.read_funcionarios()  # Atualizar a tabela
        else:
            messagebox.showerror("Erro", "Digite um ID válido para exclusão")

    def clear_funcionario_entries(self):
        self.func_nome_funcionario_entry.delete(0, tk.END)
        self.func_email_entry.delete(0, tk.END)
        self.func_telefone_entry.delete(0, tk.END)
        self.func_cargo_entry.delete(0, tk.END)
        self.func_data_admissao_entry.delete(0, tk.END)
        self.func_situacao_entry.delete(0, tk.END)
        self.func_permissao_entry.delete(0, tk.END)
        self.func_usuario_entry.delete(0, tk.END)
        self.func_senha_entry.delete(0, tk.END)

    def create_produtos_widgets (self):



         # Labels
        tk.Label(self.produtos_frame, text="Tipo: ").grid(row=0, column=0)
        tk.Label(self.produtos_frame, text="Marca: ").grid(row=1, column=0)
        tk.Label(self.produtos_frame, text="Modelo: ").grid(row=2, column=0)
        tk.Label(self.produtos_frame, text="Capacidade de injeçao: ").grid(row=3, column=0)
        tk.Label(self.produtos_frame, text="Força de fechamento: ").grid(row=4, column=0)
        tk.Label(self.produtos_frame, text="Tipo de controle: ").grid(row=5, column=0)
        tk.Label(self.produtos_frame, text="Preço medio em USD: ").grid(row=6, column=0)
        tk.Label(self.produtos_frame, text="Preço medio em BRL: ").grid(row=7, column=0)
        tk.Label(self.produtos_frame, text="Fornecedor: ").grid(row=8, column=0)
        tk.Label(self.produtos_frame, text="Observaçao: ").grid(row=9, column=0)
        tk.Label(self.produtos_frame, text="ID (para atualizar/excluir): ").grid(row=10, column=0)

        # Entradas
        self.prod_tipo_entry = tk.Entry(self.produtos_frame)
        self.prod_marca_entry = tk.Entry(self.produtos_frame)
        self.prod_modelo_entry = tk.Entry(self.produtos_frame)
        self.prod_capacidade_de_injecao_entry = tk.Entry(self.produtos_frame)
        self.prod_forca_de_fechamento_entry = tk.Entry(self.produtos_frame)
        self.prod_tipo_de_controle_entry = tk.Entry(self.produtos_frame)
        self.prod_preco_usd_entry = tk.Entry(self.produtos_frame)
        self.prod_preco_brl_entry = tk.Entry(self.produtos_frame)
        self.prod_fornecedor_entry = tk.Entry(self.produtos_frame)
        self.prod_observacao_entry = tk.Entry(self.produtos_frame)
        self.prod_id_entry = tk.Entry(self.produtos_frame)

        # Posicionamento
        self.prod_tipo_entry.grid(row=0, column=1)
        self.prod_marca_entry.grid(row=1, column=1)
        self.prod_modelo_entry.grid(row=2, column=1)
        self.prod_capacidade_de_injecao_entry.grid(row=3, column=1)
        self.prod_forca_de_fechamento_entry.grid(row=4, column=1)
        self.prod_tipo_de_controle_entry.grid(row=5, column=1)
        self.prod_preco_usd_entry.grid(row=6, column=1)
        self.prod_preco_brl_entry.grid(row=7, column=1)
        self.prod_fornecedor_entry.grid(row=8, column=1)
        self.prod_observacao_entry.grid(row=9, column=1)
        self.prod_id_entry.grid(row=10, column=1)

        # Botões
        tk.Button(self.produtos_frame, text="Criar Produtos", command=self.create_produtos).grid(row=11, column=0)
        tk.Button(self.produtos_frame, text="Listar Produtos", command=self.read_produtos).grid(row=11, column=1)
        tk.Button(self.produtos_frame, text="Atualizar Produtos", command=self.update_produtos).grid(row=12, column=0)
        tk.Button(self.produtos_frame, text="Excluir Produtos", command=self.delete_produtos).grid(row=12, column=1)

        # Tabela para exibir dados
        self.prod_table = ttk.Treeview(self.produtos_frame, columns=("ID", "tipo", "marca", "modelo", "Capacidade de injecao", "força de fechamento", "tipo de controle", "Preço medio em UDS", "preço medio em BRL", "fornecedor","observaçao"), show="headings")
        self.prod_table.grid(row=13, column=0, columnspan=2)
        
        # Definindo as colunas
        for col in self.prod_table["columns"]:
            self.prod_table.heading(col, text=col)
        
        # Adicionar uma barra de rolagem
        self.scrollbar = ttk.Scrollbar(self.produtos_frame, orient="vertical", command=self.prod_table.yview)
        self.scrollbar.grid(row=12, column=2, sticky="ns")
        self.prod_table.configure(yscrollcommand=self.scrollbar.set)

        # Vincular o evento de clique na linha
        self.prod_table.bind("<ButtonRelease-1>", self.row_selected_produto)
    
    def create_produtos (self):
        tipo = self.prod_tipo_entry.get()
        marca = self.prod_marca_entry.get()
        modelo = self.prod_modelo_entry.get()
        capacidade_de_injecao = self.prod_capacidade_de_injecao_entry.get()
        força_de_fechamento = self.prod_forca_de_fechamento_entry.get()
        tipo_de_controle = self.prod_tipo_de_controle_entry.get()
        preco_medio_USD = self.prod_preco_usd_entry.get()
        preco_medio_BRL= self.prod_preco_brl_entry.get()
        fornecedor = self.prod_fornecedor_entry.get()
        observacao = self.prod_observacao_entry.get()


        if tipo and marca and modelo and capacidade_de_injecao and força_de_fechamento and tipo_de_controle  and preco_medio_USD and preco_medio_BRL and fornecedor and observacao:
            create_produto(tipo, marca, modelo, capacidade_de_injecao, força_de_fechamento, tipo_de_controle, preco_medio_USD, preco_medio_BRL, fornecedor, observacao)
            messagebox.showinfo("Sucesso", "Produto criado com sucesso!")
            self.clear_produto_entries()
            self.read_produto()  # Atualizar a tabela
        else:
            messagebox.showerror("Erro", "Todos os campos são obrigatórios")
    
    def read_produtos(self):
        produtos = read_produtos()
        for row in self.prod_table.get_children():
            self.prod_table.delete(row)  # Limpar a tabela antes de adicionar novos dados

        for produto in produtos:
            self.prod_table.insert("", "end", values=produto)  # Inserir os dados na tabela

    def update_produtos(self):
        prod_id = self.prod_id_entry.get()
        tipo = self.prod_tipo_entry.get()
        marca = self.prod_marca_entry.get()
        modelo = self.prod_modelo_entry.get()
        capacidade_de_injecao = self.prod_capacidade_de_injecao_entry.get()
        força_de_fechamento = self.prod_forca_de_fechamento_entry.get()
        tipo_de_controle = self.prod_tipo_de_controle_entry.get()
        preco_medio_USD = self.prod_preco_usd_entry.get()
        preco_medio_BRL = self.prod_preco_brl_entry.get()
        fornecedor = self.prod_fornecedor_entry.get()
        observacao = self.prod_observacao_entry.get()

    def delete_produtos(self):
        prod_id = self.prod_id_entry.get()
        if prod_id:
            delete_funcionario(prod_id)
            messagebox.showinfo("Sucesso", "produto excluído com sucesso!")
            self.prod_id_entry.delete(0, tk.END)
            self.read_produtos()  # Atualizar a tabela
        else:
            messagebox.showerror("Erro", "Digite um ID válido para exclusão")

    def row_selected_produto(self,event):
        selected_item = self.prod_table.selection()[0]
        values = self.prod_table.item(selected_item, "values")
        
        # Preencher os campos com os dados da linha
        self.prod_tipo_entry.delete(0, tk.END)
        self.prod_tipo_entry.insert(0, values[1])  # Nome
        self.prod_marca_entry.delete(0, tk.END)
        self.prod_marca_entry.insert(0, values[2])  # Email
        self.prod_modelo_entry.delete(0, tk.END)
        self.prod_modelo_entry.insert(0, values[3])  # Telefone
        self.prod_capacidade_de_injecao_entry.delete(0, tk.END)
        self.prod_capacidade_de_injecao_entry.insert(0, values[4])  # Cargo
        self.prod_forca_de_fechamento_entry.delete(0, tk.END)
        self.prod_forca_de_fechamento_entry.insert(0, values[5])  # Data Admissão
        self.prod_tipo_de_controle_entry.delete(0, tk.END)
        self.prod_tipo_de_controle_entry.insert(0, values[6])  # Situação
        self.prod_preco_usd_entry.delete(0, tk.END)
        self.prod_preco_usd_entry.insert(0, values[7])  # Permissão
        self.prod_preco_brl_entry.delete(0, tk.END)
        self.prod_preco_brl_entry.insert(0, values[8])  # Usuario
        self.prod_fornecedor_entry.delete(0, tk.END)
        self.prod_fornecedor_entry.insert(0, values[9])  # Senha
        self.prod_id_entry.delete(0, tk.END)
        self.prod_id_entry.insert(0, values[0])  # ID