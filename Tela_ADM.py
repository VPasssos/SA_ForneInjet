import tkinter as tk
from tkinter import ttk, messagebox
from CRUD_Fornecedores import create_fornecedor, read_fornecedor, update_fornecedor, delete_fornecedor
from CRUD_Funcionarios import create_funcionario, read_funcionario, update_funcionario, delete_funcionario
from CRUD_Produtos import create_produto, read_produto, update_produto, delete_produto

class TelaAbas_ADM:
    def __init__(self,root):
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

        # Aba Produto
        self.produto_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.produto_frame, text="Produto")
        self.create_produto_widgets()

        # Aba Fornecedor
        self.fornecedor_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.fornecedor_frame, text="Fornecedor")
        self.create_fornecedor_widgets()
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

        # Área de texto para exibir dados
        self.func_text_area = tk.Text(self.funcionario_frame, height=10, width=80)
        self.func_text_area.grid(row=12, column=0, columnspan=2)
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
        else:
            messagebox.showerror("Erro", "Todos os campos são obrigatórios")

    def read_funcionarios(self):
        funcionarios = read_funcionario()
        self.func_text_area.delete(1.0, tk.END)
        for funcionario in funcionarios:
            self.func_text_area.insert(tk.END, f"ID: {funcionario[0]}, Nome: {funcionario[1]}, Email: {funcionario[2]},telefone{funcionario[3]},Cargo:{funcionario[4]},\n")

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
        else:
            messagebox.showerror("Erro", "Todos os campos são obrigatórios")

    def delete_funcionario(self):
        func_id = self.func_id_entry.get()
        if func_id:
            delete_funcionario(func_id)
            messagebox.showinfo("Sucesso", "Funcionário excluído com sucesso!")
            self.func_id_entry.delete(0, tk.END)
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

    # Métodos para a aba Produto
    def create_produto_widgets(self):
        # Labels
        tk.Label(self.produto_frame, text="Nome: ").grid(row=0, column=0)
        tk.Label(self.produto_frame, text="Categoria: ").grid(row=1, column=0)
        tk.Label(self.produto_frame, text="Preço: ").grid(row=2, column=0)
        tk.Label(self.produto_frame, text="Quantidade: ").grid(row=3, column=0)
        tk.Label(self.produto_frame, text="Fornecedor: ").grid(row=4, column=0)
        tk.Label(self.produto_frame, text="ID (para atualizar/excluir): ").grid(row=5, column=0)

        # Entradas
        self.produto_nome_entry = tk.Entry(self.produto_frame)
        self.produto_categoria_entry = tk.Entry(self.produto_frame)
        self.produto_preco_entry = tk.Entry(self.produto_frame)
        self.produto_quantidade_entry = tk.Entry(self.produto_frame)
        self.produto_fornecedor_entry = tk.Entry(self.produto_frame)
        self.produto_id_entry = tk.Entry(self.produto_frame)

        # Posicionamento
        self.produto_nome_entry.grid(row=0, column=1)
        self.produto_categoria_entry.grid(row=1, column=1)
        self.produto_preco_entry.grid(row=2, column=1)
        self.produto_quantidade_entry.grid(row=3, column=1)
        self.produto_fornecedor_entry.grid(row=4, column=1)
        self.produto_id_entry.grid(row=5, column=1)

        # Botões
        tk.Button(self.produto_frame, text="Criar Produto", command=self.create_produto).grid(row=6, column=0)
        tk.Button(self.produto_frame, text="Listar Produtos", command=self.read_produtos).grid(row=6, column=1)
        tk.Button(self.produto_frame, text="Atualizar Produto", command=self.update_produto).grid(row=7, column=0)
        tk.Button(self.produto_frame, text="Excluir Produto", command=self.delete_produto).grid(row=7, column=1)

        # Área de texto para exibir dados
        self.produto_text_area = tk.Text(self.produto_frame, height=10, width=80)
        self.produto_text_area.grid(row=8, column=0, columnspan=2)

    def create_produto(self):
        nome = self.produto_nome_entry.get()
        categoria = self.produto_categoria_entry.get()
        preco = self.produto_preco_entry.get()
        quantidade = self.produto_quantidade_entry.get()
        fornecedor = self.produto_fornecedor_entry.get()

        if nome and categoria and preco and quantidade and fornecedor:
            create_produto(nome, categoria, preco, quantidade, fornecedor)
            messagebox.showinfo("Sucesso", "Produto criado com sucesso!")
            self.clear_produto_entries()
        else:
            messagebox.showerror("Erro", "Todos os campos são obrigatórios")

    def read_produtos(self):
        produtos = read_produto()
        self.produto_text_area.delete(1.0, tk.END)
        for produto in produtos:
            self.produto_text_area.insert(tk.END, f"ID: {produto[0]}, Nome: {produto[1]}, Preço: {produto[2]}\n")

    def update_produto(self):
        produto_id = self.produto_id_entry.get()
        nome = self.produto_nome_entry.get()
        categoria = self.produto_categoria_entry.get()
        preco = self.produto_preco_entry.get()
        quantidade = self.produto_quantidade_entry.get()
        fornecedor = self.produto_fornecedor_entry.get()

        if produto_id and nome and categoria and preco and quantidade and fornecedor:
            update_produto(produto_id, nome, categoria, preco, quantidade, fornecedor)
            messagebox.showinfo("Sucesso", "Produto atualizado com sucesso!")
            self.clear_produto_entries()
        else:
            messagebox.showerror("Erro", "Todos os campos são obrigatórios")

    def delete_produto(self):
        produto_id = self.produto_id_entry.get()
        if produto_id:
            delete_produto(produto_id)
            messagebox.showinfo("Sucesso", "Produto excluído com sucesso!")
            self.produto_id_entry.delete(0, tk.END)
        else:
            messagebox.showerror("Erro", "Digite um ID válido para exclusão")

    def clear_produto_entries(self):
        self.produto_nome_entry.delete(0, tk.END)
        self.produto_categoria_entry.delete(0, tk.END)
        self.produto_preco_entry.delete(0, tk.END)
        self.produto_quantidade_entry.delete(0, tk.END)
        self.produto_fornecedor_entry.delete(0, tk.END)

    # Métodos para a aba Fornecedor
    def create_fornecedor_widgets(self):
        # Labels
        tk.Label(self.fornecedor_frame, text="Nome: ").grid(row=0, column=0)
        tk.Label(self.fornecedor_frame, text="CNPJ: ").grid(row=1, column=0)
        tk.Label(self.fornecedor_frame, text="Telefone: ").grid(row=2, column=0)
        tk.Label(self.fornecedor_frame, text="Email: ").grid(row=3, column=0)
        tk.Label(self.fornecedor_frame, text="Endereço: ").grid(row=4, column=0)
        tk.Label(self.fornecedor_frame, text="ID (para atualizar/excluir): ").grid(row=5, column=0)

        # Entradas
        self.fornecedor_nome_entry = tk.Entry(self.fornecedor_frame)
        self.fornecedor_cnpj_entry = tk.Entry(self.fornecedor_frame)
        self.fornecedor_telefone_entry = tk.Entry(self.fornecedor_frame)
        self.fornecedor_email_entry = tk.Entry(self.fornecedor_frame)
        self.fornecedor_endereco_entry = tk.Entry(self.fornecedor_frame)
        self.fornecedor_id_entry = tk.Entry(self.fornecedor_frame)

        # Posicionamento
        self.fornecedor_nome_entry.grid(row=0, column=1)
        self.fornecedor_cnpj_entry.grid(row=1, column=1)
        self.fornecedor_telefone_entry.grid(row=2, column=1)
        self.fornecedor_email_entry.grid(row=3, column=1)
        self.fornecedor_endereco_entry.grid(row=4, column=1)
        self.fornecedor_id_entry.grid(row=5, column=1)

        # Botões
        tk.Button(self.fornecedor_frame, text="Criar Fornecedor", command=self.create_fornecedor).grid(row=6, column=0)
        tk.Button(self.fornecedor_frame, text="Listar Fornecedores", command=self.read_fornecedores).grid(row=6, column=1)
        tk.Button(self.fornecedor_frame, text="Atualizar Fornecedor", command=self.update_fornecedor).grid(row=7, column=0)
        tk.Button(self.fornecedor_frame, text="Excluir Fornecedor", command=self.delete_fornecedor).grid(row=7, column=1)

        # Área de texto para exibir dados
        self.fornecedor_text_area = tk.Text(self.fornecedor_frame, height=10, width=80)
        self.fornecedor_text_area.grid(row=8, column=0, columnspan=2)

    def create_fornecedor(self):
        nome = self.fornecedor_nome_entry.get()
        cnpj = self.fornecedor_cnpj_entry.get()
        telefone = self.fornecedor_telefone_entry.get()
        email = self.fornecedor_email_entry.get()
        endereco = self.fornecedor_endereco_entry.get()

        if nome and cnpj and telefone and email and endereco:
            create_fornecedor(nome, cnpj, endereco, telefone, email)
            messagebox.showinfo("Sucesso", "Fornecedor criado com sucesso!")
            self.clear_fornecedor_entries()
        else:
            messagebox.showerror("Erro", "Todos os campos são obrigatórios")

    def read_fornecedores(self):
        fornecedores = read_fornecedor()
        self.fornecedor_text_area.delete(1.0, tk.END)
        for fornecedor in fornecedores:
            self.fornecedor_text_area.insert(tk.END, f"ID: {fornecedor[0]}, Nome: {fornecedor[1]}, Telefone: {fornecedor[2]}, Email: {fornecedor[3]}\n")

    def update_fornecedor(self):
        id_fornecedor = self.fornecedor_id_entry.get()
        nome = self.fornecedor_nome_entry.get()
        cnpj = self.fornecedor_cnpj_entry.get()
        telefone = self.fornecedor_telefone_entry.get()
        email = self.fornecedor_email_entry.get()
        endereco = self.fornecedor_endereco_entry.get()

        if id_fornecedor and nome and cnpj and telefone and email and endereco:
            update_fornecedor(id_fornecedor, nome, cnpj, endereco, telefone, email)
            messagebox.showinfo("Sucesso", "Fornecedor atualizado com sucesso!")
            self.clear_fornecedor_entries()
        else:
            messagebox.showerror("Erro", "Todos os campos são obrigatórios")

    def delete_fornecedor(self):
        id_fornecedor = self.fornecedor_id_entry.get()
        if id_fornecedor:
            delete_fornecedor(id_fornecedor)
            messagebox.showinfo("Sucesso", "Fornecedor excluído com sucesso!")
            self.fornecedor_id_entry.delete(0, tk.END)
        else:
            messagebox.showerror("Erro", "Digite um ID válido para exclusão")

    def clear_fornecedor_entries(self):
        self.fornecedor_nome_entry.delete(0, tk.END)
        self.fornecedor_cnpj_entry.delete(0, tk.END)
        self.fornecedor_telefone_entry.delete(0, tk.END)
        self.fornecedor_email_entry.delete(0, tk.END)
        self.fornecedor_endereco_entry.delete(0, tk.END)
