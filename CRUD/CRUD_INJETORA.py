from Config import get_connection
from tkinter import messagebox
import tkinter as tk
from tkinter import ttk

def criar_injetora(quantidade, marca, modelo, capacidade_de_injecao, forca_de_fechamento, tipo_de_controle, preco_medio_USD, preco_medio_BRL, fornecedor, observacao):
    conn = get_connection()
    cursor = conn.cursor()
    query = """
        INSERT INTO Injetora (
            quantidade, marca, modelo, capacidade_de_injecao,
            forca_de_fechamento, tipo_de_controle, preco_medio_USD,
            preco_medio_BRL, fornecedor, observacao
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """
    cursor.execute(query, (quantidade, marca, modelo, capacidade_de_injecao, forca_de_fechamento,
                           tipo_de_controle, preco_medio_USD, preco_medio_BRL, fornecedor, observacao))
    conn.commit()
    cursor.close()
    conn.close()

def listar_injetora():
    conn = get_connection()
    cursor = conn.cursor()
    query = "SELECT * FROM Injetora"
    cursor.execute(query)
    result = cursor.fetchall()
    cursor.close()
    conn.close()
    return result

def atualizar_injetora(idMaquinas, quantidade, marca, modelo, capacidade_de_injecao, forca_de_fechamento,
                       tipo_de_controle, preco_medio_USD, preco_medio_BRL, fornecedor, observacao):
    conn = get_connection()
    cursor = conn.cursor()
    query = """
        UPDATE Injetora SET
            quantidade = %s,
            marca = %s,
            modelo = %s,
            capacidade_de_injecao = %s,
            forca_de_fechamento = %s,
            tipo_de_controle = %s,
            preco_medio_USD = %s,
            preco_medio_BRL = %s,
            fornecedor = %s,
            observacao = %s
        WHERE idMaquinas = %s
    """
    cursor.execute(query, (quantidade, marca, modelo, capacidade_de_injecao, forca_de_fechamento,
                           tipo_de_controle, preco_medio_USD, preco_medio_BRL, fornecedor, observacao, idMaquinas))
    conn.commit()
    cursor.close()
    conn.close()

def deletar_injetora(idMaquinas):
    conn = get_connection()
    cursor = conn.cursor()
    query = "DELETE FROM Injetora WHERE idMaquinas = %s"
    cursor.execute(query, (idMaquinas,))
    conn.commit()
    cursor.close()
    conn.close()

# Métodos para a aba Injetora
def create_injetora(self):
    quantidade = self.quantidade_entry.get()
    marca = self.marca_entry.get()
    modelo = self.modelo_entry.get()
    capacidade_de_injecao = self.capacidade_entry.get()
    forca_de_fechamento = self.forca_fechar_entry.get()
    tipo_de_controle = self.tipo_controle_entry.get()
    preco_medio_usd = self.preco_usd_entry.get()
    preco_medio_brl = self.preco_brl_entry.get()
    fornecedor = self.fornecedor_injetora_entry.get()
    observacao = self.observacao_entry.get()

    if quantidade and marca and modelo and capacidade_de_injecao and forca_de_fechamento and tipo_de_controle and preco_medio_usd and preco_medio_brl and fornecedor and observacao:
        criar_injetora(quantidade, marca, modelo, capacidade_de_injecao, forca_de_fechamento,
                       tipo_de_controle, preco_medio_usd, preco_medio_brl, fornecedor, observacao)
        messagebox.showinfo("Sucesso", "Injetora cadastrada com sucesso!")
        clear_injetora_entries(self)
    else:
        messagebox.showerror("Erro", "Todos os campos são obrigatórios")

def read_injetora(self):
    injetoras = listar_injetora()
    for row in self.injetora_table.get_children():
        self.injetora_table.delete(row)
    for injetora in injetoras:
        self.injetora_table.insert("", "end", values=injetora)

def update_injetora(self):
    id_maquinas = self.id_maquinas_entry.get()
    quantidade = self.quantidade_entry.get()
    marca = self.marca_entry.get()
    modelo = self.modelo_entry.get()
    capacidade_de_injecao = self.capacidade_entry.get()
    forca_de_fechamento = self.forca_fechar_entry.get()
    tipo_de_controle = self.tipo_controle_entry.get()
    preco_medio_usd = self.preco_usd_entry.get()
    preco_medio_brl = self.preco_brl_entry.get()
    fornecedor = self.fornecedor_injetora_entry.get()
    observacao = self.observacao_entry.get()

    clear_injetora_entries(self)

    if id_maquinas and quantidade and marca and modelo and capacidade_de_injecao and forca_de_fechamento and tipo_de_controle and preco_medio_usd and preco_medio_brl and fornecedor and observacao:
        atualizar_injetora(id_maquinas, quantidade, marca, modelo, capacidade_de_injecao, forca_de_fechamento,
                           tipo_de_controle, preco_medio_usd, preco_medio_brl, fornecedor, observacao)
        messagebox.showinfo("Sucesso", "Injetora atualizada com sucesso!")
    else:
        messagebox.showerror("Erro", "Todos os campos são obrigatórios")

def delete_injetora(self):
    id_maquinas = self.id_maquinas_entry.get()
    if id_maquinas:
        deletar_injetora(id_maquinas)
        messagebox.showinfo("Sucesso", "Injetora excluída com sucesso!")
        self.id_maquinas_entry.delete(0, tk.END)
    else:
        messagebox.showerror("Erro", "Digite um ID válido para exclusão")

def clear_injetora_entries(self):
    self.quantidade_entry.delete(0, tk.END)
    self.marca_entry.delete(0, tk.END)
    self.modelo_entry.delete(0, tk.END)
    self.capacidade_entry.delete(0, tk.END)
    self.forca_fechar_entry.delete(0, tk.END)
    self.tipo_controle_entry.delete(0, tk.END)
    self.preco_usd_entry.delete(0, tk.END)
    self.preco_brl_entry.delete(0, tk.END)
    self.fornecedor_injetora_entry.delete(0, tk.END)
    self.observacao_entry.delete(0, tk.END)
    self.id_maquinas_entry.delete(0, tk.END)
