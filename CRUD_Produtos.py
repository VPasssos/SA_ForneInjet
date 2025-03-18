from Config import get_connection
from tkinter import messagebox
import tkinter as tk
from tkinter import ttk

def criar_produto(quantidade, marca, modelo, capacidade_de_injeçao, força_de_fechamento, tipo_de_controle, preço_medio_USD, preço_medio_BRL, fornecedor, observacao):
    conn = get_connection()
    cursor = conn.cursor()
    query = "INSERT INTO Produto (quantidade, marca, modelo, capacidade_de_injeçao, força_de_fechamento, tipo_de_controle, preço_medio_USD, preço_medio_BRL, fornecedor, observacao) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    cursor.execute(query, (quantidade, marca, modelo, capacidade_de_injeçao, força_de_fechamento, tipo_de_controle, preço_medio_USD, preço_medio_BRL, fornecedor, observacao))
    conn.commit()
    cursor.close()
    conn.close()

def listar_produto():
    conn = get_connection()
    cursor = conn.cursor()
    query = "SELECT * FROM Produto"
    cursor.execute(query)
    result = cursor.fetchall()
    cursor.close()
    conn.close()
    return result

def atualizar_produto(quantidade, marca, modelo, capacidade_de_injeçao, força_de_fechamento, tipo_de_controle, preço_medio_USD, preço_medio_BRL, fornecedor, observacao, idMaquinas):
    conn = get_connection()
    cursor = conn.cursor()
    query = "UPDATE Produto SET quantidade = %s, marca = %s, modelo = %s, capacidade_de_injeçao = %s, força_de_fechamento = %s, tipo_de_controle = %s, preço_medio_USD = %s, preço_medio_BRL = %s, fornecedor = %s, observacao = %s WHERE idMaquinas = %s"
    cursor.execute(query, (quantidade, marca, modelo, capacidade_de_injeçao, força_de_fechamento, tipo_de_controle, preço_medio_USD, preço_medio_BRL, fornecedor, observacao, idMaquinas))
    conn.commit()
    cursor.close()
    conn.close()

def deletar_produto(idMaquinas):
    conn = get_connection()
    cursor = conn.cursor()
    query = "DELETE FROM Produto WHERE idMaquinas = %s"
    cursor.execute(query, (idMaquinas,))
    conn.commit()
    cursor.close()
    conn.close()

# Métodos para a aba Produto
def create_produto(self):
    quantidade = self.quantidade_entry.get()
    marca = self.marca_entry.get()
    modelo = self.modelo_entry.get()
    capacidade_de_injecao = self.capacidade_entry.get()
    forca_de_fechamento = self.forca_fechar_entry.get()
    tipo_de_controle = self.tipo_controle_entry.get()
    preco_medio_usd = self.preco_usd_entry.get()
    preco_medio_brl = self.preco_brl_entry.get()
    fornecedor = self.fornecedor_produto_entry.get()
    observacao = self.observacao_entry.get()

    if quantidade and marca and modelo and capacidade_de_injecao and forca_de_fechamento and tipo_de_controle and preco_medio_usd and preco_medio_brl and fornecedor and observacao:
        criar_produto(quantidade, marca, modelo, capacidade_de_injecao, forca_de_fechamento, tipo_de_controle, preco_medio_usd, preco_medio_brl, fornecedor, observacao)
        messagebox.showinfo("Sucesso", "Produto cadastrado com sucesso!")
        self.clear_produto_entries()

    else:
        messagebox.showerror("Erro", "Todos os campos são obrigatórios")

def read_produto(self):
    # Aqui você deve chamar a função para listar os produtos
    produtos = listar_produto()  # Lista de produtos retornada pela função listar_produto()

    # Limpar a tabela antes de adicionar novos dados
    for row in self.produto_table.get_children():
        self.produto_table.delete(row)

    # Inserir os dados na tabela
    for produto in produtos:
        # A função insert insere uma nova linha na tabela com os dados do produto
        # Supondo que 'produto' seja uma lista ou tupla de valores correspondentes às colunas da tabela
        self.produto_table.insert("", "end", values=produto)


def update_produto(self):
    # Usando a variável correta para ID do produto
    id_maquinas = self.id_maquinas_entry.get()
    quantidade = self.quantidade_entry.get()
    marca = self.marca_entry.get()
    modelo = self.modelo_entry.get()
    capacidade_de_injecao = self.capacidade_entry.get()
    forca_de_fechamento = self.forca_fechar_entry.get()
    tipo_de_controle = self.tipo_controle_entry.get()
    preco_medio_usd = self.preco_usd_entry.get()
    preco_medio_brl = self.preco_brl_entry.get()
    fornecedor = self.fornecedor_produto_entry.get()
    observacao = self.observacao_entry.get()

    # Verificando se todos os campos obrigatórios estão preenchidos
    if id_maquinas and quantidade and marca and modelo and capacidade_de_injecao and forca_de_fechamento and tipo_de_controle and preco_medio_usd and preco_medio_brl and fornecedor and observacao:
        atualizar_produto(id_maquinas, quantidade, marca, modelo, capacidade_de_injecao, forca_de_fechamento, tipo_de_controle, preco_medio_usd, preco_medio_brl, fornecedor, observacao)
        messagebox.showinfo("Sucesso", "Produto atualizado com sucesso!")
    else:
        messagebox.showerror("Erro", "Todos os campos são obrigatórios")

def delete_produto(self):
    # Usando a variável correta para ID do produto
    id_maquinas = self.id_maquinas_entry.get()
    if id_maquinas:
        deletar_produto(id_maquinas)
        messagebox.showinfo("Sucesso", "Produto excluído com sucesso!")
        self.id_maquinas_entry.delete(0, tk.END)  # Limpar o campo de ID após exclusão
    else:
        messagebox.showerror("Erro", "Digite um ID válido para exclusão")

def clear_produto_entries(self):
    # Limpando todos os campos da aba Produto
    self.quantidade_entry.delete(0, tk.END)
    self.marca_entry.delete(0, tk.END)
    self.modelo_entry.delete(0, tk.END)
    self.capacidade_entry.delete(0, tk.END)
    self.forca_fechar_entry.delete(0, tk.END)
    self.tipo_controle_entry.delete(0, tk.END)
    self.preco_usd_entry.delete(0, tk.END)
    self.preco_brl_entry.delete(0, tk.END)
    self.fornecedor_produto_entry.delete(0, tk.END)
    self.observacao_entry.delete(0, tk.END)
    self.id_maquinas.delete(0, tk.END)  # Limpar também o campo de ID
