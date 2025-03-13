import tkinter as tk
from tkinter import ttk, messagebox
from CRUD_Fornecedores import create_fornecedor, read_fornecedor, update_fornecedor, delete_fornecedor
from CRUD_Funcionarios import create_funcionario, read_funcionario, update_funcionario, delete_funcionario
from CRUD_Produtos import create_produto, read_produto, update_produto, delete_produto

class TelaAbas_NORM:
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

    # Métodos para a aba Inicial
    def create_inicio_widgets(self):
        label = tk.Label(self.inicio_frame, text="Bem-vindo(a) ao programa da ForneInjet", font=("Arial", 16))
        label.pack(padx=10, pady=10)

        self.inic_table = ttk.Treeview(self.inicio_frame, columns=("ID", "Tipo", "Marca", "Modelo", "Capacidade de Injeção", "Força de Fechamento", "Tipo de Controle", "Preço USD", "Preço BRL", "Fornecedor", "Observação"), show="headings")
        self.inic_table.pack(padx=10, pady=10, fill="both", expand=True)
        
        # Definindo as colunas
        for col in self.inic_table["columns"]:
            self.inic_table.heading(col, text=col)

        # Ajustar a largura das colunas automaticamente
        self.ajustar_largura_colunas()

        # Adicionar uma barra de rolagem
        self.scrollbar = ttk.Scrollbar(self.inicio_frame, orient="vertical", command=self.inic_table.yview)
        self.scrollbar.pack(side="right", fill="y")
        self.inic_table.configure(yscrollcommand=self.scrollbar.set)

    def ajustar_largura_colunas(self):
        for col in self.inic_table["columns"]:
            max_length = 0
            for item in self.inic_table.get_children():
                text = self.inic_table.item(item)["values"][self.inic_table["columns"].index(col)]
                max_length = max(max_length, len(str(text)))
            
                # Ajustar a largura da coluna com base no comprimento máximo do texto
                self.inic_table.column(col, width=max_length * 10)  # Multiplicar por 10 para ajustar

    # Métodos para a aba Funcionario
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