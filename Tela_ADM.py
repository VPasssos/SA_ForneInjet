import tkinter as tk
from tkinter import ttk, messagebox
from CRUD_Fornecedores import create_fornecedor, read_fornecedor, update_fornecedor, delete_fornecedor

class CRUDApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema ForneInjet SA")

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
        tk.Label(self.funcionario_frame, text="Cargo: ").grid(row=1, column=0)
        tk.Label(self.funcionario_frame, text="Departamento: ").grid(row=2, column=0)
        tk.Label(self.funcionario_frame, text="Telefone: ").grid(row=3, column=0)
        tk.Label(self.funcionario_frame, text="Email: ").grid(row=4, column=0)
        tk.Label(self.funcionario_frame, text="Data Admissão: ").grid(row=5, column=0)
        tk.Label(self.funcionario_frame, text="Situação: ").grid(row=6, column=0)
        tk.Label(self.funcionario_frame, text="Permissão: ").grid(row=7, column=0)
        tk.Label(self.funcionario_frame, text="ID (para atualizar/excluir): ").grid(row=8, column=0)

        # Entradas
        self.func_nome_entry = tk.Entry(self.funcionario_frame)
        self.func_cargo_entry = tk.Entry(self.funcionario_frame)
        self.func_departamento_entry = tk.Entry(self.funcionario_frame)
        self.func_telefone_entry = tk.Entry(self.funcionario_frame)
        self.func_email_entry = tk.Entry(self.funcionario_frame)
        self.func_data_admissao_entry = tk.Entry(self.funcionario_frame)
        self.func_situacao_entry = tk.Entry(self.funcionario_frame)
        self.func_permissao_entry = tk.Entry(self.funcionario_frame)
        self.func_id_entry = tk.Entry(self.funcionario_frame)

        # Posicionamento
        self.func_nome_entry.grid(row=0, column=1)
        self.func_cargo_entry.grid(row=1, column=1)
        self.func_departamento_entry.grid(row=2, column=1)
        self.func_telefone_entry.grid(row=3, column=1)
        self.func_email_entry.grid(row=4, column=1)
        self.func_data_admissao_entry.grid(row=5, column=1)
        self.func_situacao_entry.grid(row=6, column=1)
        self.func_permissao_entry.grid(row=7, column=1)
        self.func_id_entry.grid(row=8, column=1)

        # Botões
        tk.Button(self.funcionario_frame, text="Criar Funcionario", command=self.create_funcionario).grid(row=9, column=0)
        tk.Button(self.funcionario_frame, text="Listar Funcionarios", command=self.read_funcionarios).grid(row=9, column=1)
        tk.Button(self.funcionario_frame, text="Atualizar Funcionario", command=self.update_funcionario).grid(row=10, column=0)
        tk.Button(self.funcionario_frame, text="Excluir Funcionario", command=self.delete_funcionario).grid(row=10, column=1)

        # Área de texto para exibir dados
        self.func_text_area = tk.Text(self.funcionario_frame, height=10, width=80)
        self.func_text_area.grid(row=11, column=0, columnspan=2)
    def create_funcionario(self):
        # Lógica para criar um funcionário
        nome = self.func_nome_entry.get()
        cargo = self.func_cargo_entry.get()
        departamento = self.func_departamento_entry.get()
        telefone = self.func_telefone_entry.get()
        email = self.func_email_entry.get()
        data_admissao = self.func_data_admissao_entry.get()
        situacao = self.func_situacao_entry.get()
        permissao = self.func_permissao_entry.get()
    def read_funcionarios(self):
        # Exemplo de listagem de funcionários (simulação)
        self.func_text_area.delete(1.0, tk.END)
        # Simula listagem de funcionários
        funcionarios = ["Funcionário 1", "Funcionário 2", "Funcionário 3"]
        for func in funcionarios:
            self.func_text_area.insert(tk.END, f"{func}\n")
    def update_funcionario(self):
        # Lógica para atualizar um funcionário (usando ID)
        func_id = self.func_id_entry.get()
        messagebox.showinfo("Info", f"Funcionário com ID {func_id} atualizado!")
    def delete_funcionario(self):
        # Lógica para excluir um funcionário (usando ID)
        func_id = self.func_id_entry.get()
        messagebox.showinfo("Info", f"Funcionário com ID {func_id} excluído!")
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

        # Salvar dados do produto
        produto = {
            "Nome": nome,
            "Categoria": categoria,
            "Preço": preco,
            "Quantidade": quantidade,
            "Fornecedor": fornecedor
        }

        messagebox.showinfo("Info", f"Produto {nome} criado com sucesso!")
    def read_produtos(self):
        self.produto_text_area.delete(1.0, tk.END)
        produtos = ["Produto 1", "Produto 2", "Produto 3"]
        for produto in produtos:
            self.produto_text_area.insert(tk.END, f"{produto}\n")
    def update_produto(self):
        produto_id = self.produto_id_entry.get()
        messagebox.showinfo("Info", f"Produto com ID {produto_id} atualizado!")
    def delete_produto(self):
        produto_id = self.produto_id_entry.get()
        messagebox.showinfo("Info", f"Produto com ID {produto_id} excluído!")
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
            self.fornecedor_nome_entry.delete(0, tk.END)
            self.fornecedor_cnpj_entry.delete(0, tk.END)
            self.fornecedor_telefone_entry.delete(0, tk.END)
            self.fornecedor_email_entry.delete(0, tk.END)
            self.fornecedor_endereco_entry.delete(0, tk.END)
            messagebox.showinfo("Sucesso", "Fornecedor criado com sucesso!")
        else:
            messagebox.showerror("Erro", "Todos os campos são obrigatórios")
    def read_fornecedores(self):
        fornecedores = read_fornecedor()
        self.fornecedor_text_area.delete(1.0, tk.END)
        for fornecedor in fornecedores:
            self.fornecedor_text_area.insert(tk.END, f"ID: {fornecedor[0]}, Nome: {fornecedor[1]}, Telefone: {fornecedor[2]}, Email: {fornecedor[3]}\n")
    def update_fornecedor(self):
        idFornecedor = self.fornecedor_id_entry.get()
        nome = self.fornecedor_nome_entry.get()
        cnpj = self.fornecedor_cnpj_entry.get()
        telefone = self.fornecedor_telefone_entry.get()
        email = self.fornecedor_email_entry.get()
        endereco = self.fornecedor_endereco_entry.get()

        if idFornecedor and nome and cnpj and telefone and email and endereco:
            update_fornecedor(idFornecedor, nome, cnpj, endereco, telefone, email)
            self.fornecedor_id_entry.delete(0, tk.END)
            self.fornecedor_nome_entry.delete(0, tk.END)
            self.fornecedor_cnpj_entry.delete(0, tk.END)
            self.fornecedor_telefone_entry.delete(0, tk.END)
            self.fornecedor_email_entry.delete(0, tk.END)
            self.fornecedor_endereco_entry.delete(0, tk.END)
            messagebox.showinfo("Sucesso", "Fornecedor atualizado com sucesso!")
        else:
            messagebox.showerror("Erro", "Todos os campos são obrigatórios")
    def delete_fornecedor(self):
        idFornecedor = self.fornecedor_id_entry.get()
        if idFornecedor:
            delete_fornecedor(idFornecedor)
            self.fornecedor_id_entry.delete(0, tk.END)
            messagebox.showinfo("Sucesso", "Fornecedor excluído com sucesso!")
        else:
            messagebox.showerror("Erro", "Digite um ID válido para exclusão")

if __name__ == "__main__":
    root = tk.Tk()
    app = CRUDApp(root)
    root.mainloop()