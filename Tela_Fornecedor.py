import tkinter as tk
from tkinter import messagebox
from CRUD_Fornecedores import create_fornecedor,read_fornecedor,update_fornecedor,delete_fornecedor

class CRUDApp:
    def __init__(self,root):
        self.root = root
        self.root.title("CRUD FORNECEDORES")

        #Criaçao de WIDGETS
        self.create_widgets()

    def create_widgets(self):
        #Labels
        tk.Label(self.root,text="Nome: ").grid(row=0,column=0)
        tk.Label(self.root,text="CNPJ: ").grid(row=1,column=0)
        tk.Label(self.root,text="Endereço: ").grid(row=2,column=0)
        tk.Label(self.root,text="Telefone: ").grid(row=3,column=0)
        tk.Label(self.root,text="Email: ").grid(row=4,column=0)
        tk.Label(self.root,text="Contato Principal: ").grid(row=5,column=0)
        tk.Label(self.root,text="Website: ").grid(row=6,column=0)

        tk.Label(self.root,text="ID Fornecedor(for update/delete): ").grid(row=7,column=0)

        # Criar as caixas para digitar os valores
        self.nome_fornecedor_entry = tk.Entry(self.root)
        self.cnpj_entry = tk.Entry(self.root)
        self.endereco_entry = tk.Entry(self.root)
        self.telefone_entry = tk.Entry(self.root)
        self.email_entry = tk.Entry(self.root)
        self.contato_principal_entry = tk.Entry(self.root)
        self.website_entry = tk.Entry(self.root)
        self.idFornecedor_entry = tk.Entry(self.root)

        self.nome_fornecedor_entry.grid(row=0,column=1)
        self.cnpj_entry.grid(row=1,column=1)
        self.endereco_entry.grid(row=2,column=1)
        self.telefone_entry.grid(row=3,column=1)
        self.email_entry.grid(row=4,column=1)
        self.contato_principal_entry.grid(row=5,column=1)
        self.website_entry.grid(row=6,column=1)

        self.idFornecedor_entry.grid(row=7,column=1)

        #Botoes do CRUD
        tk.Button(self.root,text="Criar Fornecedor",command=self.create_fornecedor).grid(row=6,column=0,columnspan=1)
        tk.Button(self.root,text="Listar Fornecedor",command=self.read_fornecedor).grid(row=6,column=1,columnspan=1)
        tk.Button(self.root,text="Alterar Fornecedor",command=self.update_fornecedor).grid(row=7,column=0,columnspan=1)
        tk.Button(self.root,text="Excluir Fornecedor",command=self.delete_fornecedor).grid(row=7,column=1,columnspan=1)
        
        self.text_area = tk.Text(self.root,height=10,width=80)
        self.text_area.grid(row=10,column=0,columnspan=4)

    def create_fornecedor(self):
        nome_fornecedor = self.nome_fornecedor_entry.get()
        cnpj = self.cnpj_entry.get()
        endereco = self.endereco_entry.get()
        telefone = self.telefone_entry.get()
        email = self.email_entry.get()
        contato_principal = self.contato_principal_entry.get()
        website = self.website_entry.get()

        if nome_fornecedor and cnpj and endereco and telefone and email and contato_principal and website:
            create_fornecedor(nome_fornecedor,cnpj,endereco,telefone,email,contato_principal,website)
            self.nome_fornecedor_entry.delete(0,tk.END)
            self.cnpj_entry.delete(0,tk.END)
            self.endereco_entry.delete(0,tk.END)
            self.telefone_entry.delete(0,tk.END)
            self.email_entry.delete(0,tk.END)
            self.contato_principal_entry.delete(0,tk.END)
            self.website_entry.delete(0,tk.END)
            messagebox.showerror("Success","Fornecedor criado com sucesso")
        else:
            messagebox.showerror("Error","Todos os campos são obrigatórios")
    def read_fornecedor(self):
        users =read_fornecedor()
        self.text_area.delete(1.0,tk.END)
        for user in users:
            self.text_area.insert(tk.END,f"ID: {user[0]}, Nome: {user[1]}, Telefone: {user[2]}, Email: {user[3]}\n")
            
    def update_fornecedor(self):
        idFornecedor = self.idFornecedor_entry.get()
        nome_fornecedor = self.nome_fornecedor_entry.get()
        endereco = self.endereco_entry.get()
        telefone = self.telefone_entry.get()
        email = self.email_entry.get()
        contato_principal = self.contato_principal_entry.get()
        website = self.website_entry.get()

        if idFornecedor and nome_fornecedor and endereco and telefone and email and contato_principal and website:
            update_fornecedor(idFornecedor,nome_fornecedor,endereco,telefone,email,contato_principal,website)
            self.nome_fornecedor_entry.delete(0,tk.END)
            self.endereco_entry.delete(0,tk.END)
            self.telefone_entry.delete(0,tk.END)
            self.email_entry.delete(0,tk.END)
            self.contato_principal_entry.delete(0,tk.END)
            self.website_entry.delete(0,tk.END)

            messagebox.showerror("Success","Fornecedor alterado com sucesso")
        else:
            messagebox.showerror("Error","Todos os campos são obrigatórios")

    def delete_fornecedor(self):
        idFornecedor = self.idFornecedor_entry.get()
        if idFornecedor:
            delete_fornecedor(idFornecedor)
            self.idFornecedor_entry.delete(0,tk.END)
            messagebox.showerror("Success","Fornecedor excluido com sucesso!")
        else:
            messagebox.showerror("Error","ID do Fornecedor é obrigatorio")
    
if __name__=="__main__":
    root = tk.Tk()
    app = CRUDApp(root)
    root.mainloop()