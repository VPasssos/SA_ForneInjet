import tkinter as tk
from tkinter import messagebox
from CRUD_Produtos import create_produto,read_produto,update_produto,delete_produto

class CRUDApp:
    def __init__(self,root):
        self.root = root
        self.root.title("CRUD produtos")

        #Criaçao de WIDGETS
        self.create_widgets()

    def create_widgets(self):
        #Labels
        tk.Label(self.root,text="Tipo: ").grid(row=0,column=0)
        tk.Label(self.root,text="Marca: ").grid(row=1,column=0)
        tk.Label(self.root,text="Modelo: ").grid(row=2,column=0)
        tk.Label(self.root,text="Capacidade de injeçao: ").grid(row=3,column=0)
        tk.Label(self.root,text="Força de fechamento: ").grid(row=4,column=0)
        tk.Label(self.root,text="Tipo de controle: ").grid(row=5,column=0)
        tk.Label(self.root,text="Preço médio(USD): ").grid(row=6,column=0)
        tk.Label(self.root,text="Preço médio(BRL): ").grid(row=7,column=0)
        tk.Label(self.root,text="Fornecedor: ").grid(row=8,column=0)
        tk.Label(self.root,text="Observaçoes: ").grid(row=9,column=0)

        tk.Label(self.root,text="produtoID(for update/delete): ").grid(row=10,column=0)

        # Criar as caixas para digitar os valores
        self.tipo_entry = tk.Entry(self.root)
        self.marca_entry = tk.Entry(self.root)
        self.modelo_entry = tk.Entry(self.root)
        self.capacidade_de_injecao_entry = tk.Entry(self.root)
        self.força_de_fechamento_entry = tk.Entry(self.root)
        self.tipo_de_controle_entry = tk.Entry(self.root)
        self.preço_médio_dolar_entry = tk.Entry(self.root)
        self.preço_médio_real_entry = tk.Entry(self.root)
        self.fornecedor_entry = tk.Entry(self.root)
        self.observaçoes_entry = tk.Entry(self.root)
        self.produto_ID_entry = tk.Entry(self.root)

        self.tipo_entry.grid(row=0,column=1)
        self.marca_entry.grid(row=1,column=1)
        self.modelo_entry.grid(row=2,column=1)
        self.capacidade_de_injecao_entry.grid(row=3,column=1)
        self.força_de_fechamento_entry.grid(row=4,column=1)
        self.tipo_de_controle_entry .grid(row=5,column=1)
        self.preço_médio_dolar_entry.grid(row=6,column=1)
        self.preço_médio_real_entry.grid(row=7,column=1)
        self.fornecedor_entry.grid(row=8,column=1)
        self.observaçoes_entry.grid(row=9,column=1)

        self.produto_ID_entry.grid(row=10,column=1)

        #Botoes do CRUD
        tk.Button(self.root,text="Criar Produto",command=self.create_produto).grid(row=6,column=0,columnspan=1)
        tk.Button(self.root,text="Listar Produto",command=self.read_produto).grid(row=6,column=1,columnspan=1)
        tk.Button(self.root,text="Alterar Produto",command=self.update_produto).grid(row=7,column=0,columnspan=1)
        tk.Button(self.root,text="Excluir Produto",command=self.delete_produto).grid(row=7,column=1,columnspan=1)
        
        self.text_area = tk.Text(self.root,height=10,width=80)
        self.text_area.grid(row=10,column=0,columnspan=4)

    def create_user(self):
        tipo = self.tipo_entry.get()
        marca = self.marca_entry.get()
        modelo = self.modelo_entry.get()
        capacidade_de_injecao = self.capacidade_de_injecao_entry.get()
        força_de_fechamento = self.força_de_fechamento_entry.get()
        tipo_de_controle = self.tipo_de_controle_entry.get()
        preço_médio_dolar = self.preço_médio_dolar_entry.get()
        preço_médio_real = self.preço_médio_real_entry.get()
        fornecedor = self.fornecedor_entry.get()
        observaçoes = self.observaçoes_entry.get()

        if tipo and marca and modelo and capacidade_de_injecao and força_de_fechamento and tipo_de_controle and preço_médio_dolar and preço_médio_real and fornecedor and observaçoes:
            create_produto(tipo, marca, modelo, capacidade_de_injecao, força_de_fechamento, tipo_de_controle, preço_médio_dolar,preço_médio_real,fornecedor, observaçoes)
            self.tipo_entry.delete(0,tk.END)
            self.marca_entry.delete(0,tk.END)
            self.modelo_entry.delete(0,tk.END)
            self.capacidade_de_injecao_entry.delete(0,tk.END)
            self.força_de_fechamento_entry.delete(0,tk.END)
            self.tipo_de_controle_entry.delete(0,tk.END)
            self.preço_médio_dolar_entry.delete(0,tk.END)
            self.preço_médio_real_entry.delete(0,tk.END)
            self.fornecedor_entry.delete(0,tk.END)
            self.observaçoes_entry.delete(0,tk.END)

            messagebox.showerror("Success","Produto criado com sucesso")
        else:
            messagebox.showerror("Error","Todos os campos são obrigatórios")

    def read_produto(self):
        produto =read_produto()
        self.text_area.delete(1.0,tk.END)
        for user in produto:
            self.text_area.insert(tk.END,f"ID: {user[0]}, Tipo: {user[1]}, Marca: {user[2]}, Modelo: {user[3]}, Capacidade de injecao: {user[4]},Força de fechamento : {user[5]}, Tipo de controle: {user[6]}, Preço médio(USD): {user[7]}, Preço médio(BRL): {user[8]},Fornecedor : {user[9]}, Observaçoes : {user[10]}\n")

    def update_produto(self):
        tipo = self.tipo_entry.get()
        marca = self.marca_entry.get()
        modelo = self.modelo_entry.get()
        capacidade_de_injecao = self.capacidade_de_injecao_entry.get()
        força_de_fechamento = self.força_de_fechamento_entry.get()
        tipo_de_controle = self.tipo_de_controle_entry.get()
        preço_médio_dolar = self.preço_médio_dolar_entry.get()
        preço_médio_real = self.preço_médio_real_entry.get()
        fornecedor = self.fornecedor_entry.get()
        observaçoes = self.observaçoes_entry.get()

        if  produtoID and tipo and marca and modelo and capacidade_de_injecao and força_de_fechamento and tipo_de_controle and preço_médio_dolar and preço_médio_real and fornecedor and observaçoes:
            update_produto(tipo, marca, modelo, capacidade_de_injecao, força_de_fechamento, tipo_de_controle, preço_médio_dolar,preço_médio_real,fornecedor, observaçoes)
            self.tipo_entry.delete(0,tk.END)
            self.marca_entry.delete(0,tk.END)
            self.modelo_entry.delete(0,tk.END)
            self.capacidade_de_injecao_entry.delete(0,tk.END)
            self.força_de_fechamento_entry.delete(0,tk.END)
            self.tipo_de_controle_entry.delete(0,tk.END)
            self.preço_médio_dolar_entry.delete(0,tk.END)
            self.preço_médio_real_entry.delete(0,tk.END)
            self.fornecedor_entry.delete(0,tk.END)
            self.observaçoes_entry.delete(0,tk.END)
            messagebox.showerror("Success","Produto alterado com sucesso")
        else:
            messagebox.showerror("Error","Todos os campos são obrigatórios")

    def delete_produto(self):
        produtoID = self.produtoID_entry.get()
        if produtoID:
            delete_produto(produtoID)
            self.produtoID_entry.delete(0,tk.END)
            messagebox.showerror("Success","Produto excluido com sucesso!")
        else:
            messagebox.showerror("Error","ID do produto é obrigatorio")
    
if __name__=="__main__":
    root = tk.Tk()
    app = CRUDApp(root)
    root.mainloop()