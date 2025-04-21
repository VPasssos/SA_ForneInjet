from Config import get_connection
from tkinter import messagebox
import tkinter as tk
from tkinter import ttk

def criar_fornecedor(nome_fornecedor, cnpj, email, endereco, telefone, contato_principal, website):
    conn = get_connection()
    cursor = conn.cursor()
    query = "INSERT INTO Fornecedor (nome_fornecedor, cnpj, email, endereco, telefone, contato_principal, website) VALUES (%s, %s, %s, %s, %s, %s, %s)"
    cursor.execute(query, (nome_fornecedor, cnpj, email, endereco, telefone, contato_principal, website))
    conn.commit()
    cursor.close()
    conn.close()

def listar_fornecedor():
    conn = get_connection()
    cursor = conn.cursor()
    query = "SELECT * FROM Fornecedor"
    cursor.execute(query)
    result = cursor.fetchall()
    cursor.close()
    conn.close()
    return result

def atualizar_fornecedor(idFornecedor, nome_fornecedor, cnpj, email, endereco, telefone, contato_principal, website):
    conn = get_connection()
    cursor = conn.cursor()
    query = "UPDATE Fornecedor SET nome_fornecedor=%s, cnpj=%s, email=%s, endereco=%s, telefone=%s, contato_principal=%s, website=%s WHERE idFornecedor=%s"
    cursor.execute(query, (nome_fornecedor, cnpj, email, endereco, telefone, contato_principal, website, idFornecedor))
    conn.commit()
    cursor.close()
    conn.close()

def deletar_fornecedor(idFornecedor):
    conn = get_connection()
    cursor = conn.cursor()
    query = "DELETE FROM Fornecedor WHERE idFornecedor = %s"
    cursor.execute(query, (idFornecedor,))
    conn.commit()
    cursor.close()
    conn.close()

# Métodos para a aba fornecedor
def create_fornecedor(self):
    nome_fornecedor = self.nome_fornecedor_entry.get()
    cnpj = self.cnpj_entry.get()
    email = self.email_fornecedor_entry.get()
    endereco = self.endereco_entry.get()
    telefone = self.telefone_fornecedor_entry.get()
    contato_principal = self.contato_principal_entry.get()
    website = self.website_entry.get()

    if nome_fornecedor and cnpj and email and endereco and telefone and contato_principal and website:
        criar_fornecedor(nome_fornecedor, cnpj, email, endereco, telefone, contato_principal, website)
        messagebox.showinfo("Sucesso", "Fornecedor cadastrado com sucesso!")
        self.clear_fornecedor_entries()
        read_fornecedor(self)  # Atualizar a tabela
    else:
        messagebox.showerror("Erro", "Todos os campos são obrigatórios")

def read_fornecedor(self):
    fornecedores = listar_fornecedor()  # Remover o 'self' aqui
    for row in self.fornecedor_table.get_children():
        self.fornecedor_table.delete(row)  # Limpar a tabela antes de adicionar novos dados
        
    for fornecedor in fornecedores:
        self.fornecedor_table.insert("", "end", values=fornecedor)  # Inserir os dados na tabela

def update_fornecedor(self):
    id_fornecedor = self.id_fornecedor_entry.get()
    nome_fornecedor = self.nome_fornecedor_entry.get()
    cnpj = self.cnpj_entry.get()
    email = self.email_fornecedor_entry.get()
    endereco = self.endereco_entry.get()
    telefone = self.telefone_fornecedor_entry.get()
    contato_principal = self.contato_principal_entry.get()
    website = self.website_entry.get()

    if id_fornecedor and nome_fornecedor and cnpj and email and endereco and telefone and contato_principal and website:
        atualizar_fornecedor(id_fornecedor, nome_fornecedor, cnpj, email, endereco, telefone, contato_principal, website)
        messagebox.showinfo("Sucesso", "Fornecedor atualizado com sucesso!")
        self.clear_fornecedor_entries()
        read_fornecedor(self)  # Atualizar a tabela
    else:
        messagebox.showerror("Erro", "Todos os campos são obrigatórios")

def delete_fornecedor(self):
    id_fornecedor = self.id_fornecedor_entry.get()
    if id_fornecedor:
        deletar_fornecedor(id_fornecedor)
        messagebox.showinfo("Sucesso", "Fornecedor excluído com sucesso!")
        self.id_fornecedor_entry.delete(0, tk.END)
        read_fornecedor(self)  # Atualizar a tabela
    else:
        messagebox.showerror("Erro", "Digite um ID válido para exclusão")

def clear_fornecedor_entries(self):
    self.nome_fornecedor_entry.delete(0, tk.END)
    self.cnpj_entry.delete(0, tk.END)
    self.email_fornecedor_entry.delete(0, tk.END)
    self.endereco_entry.delete(0, tk.END)
    self.telefone_fornecedor_entry.delete(0, tk.END)
    self.contato_principal_entry.delete(0, tk.END)
    self.website_entry.delete(0, tk.END)
    self.id_fornecedor_entry.delete(0, tk.END)