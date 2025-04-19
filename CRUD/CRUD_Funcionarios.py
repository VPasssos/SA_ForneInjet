import mysql.connector
from Config import get_connection
from tkinter import messagebox
import tkinter as tk
from tkinter import ttk

def criar_funcionario(nome_funcionario, cargo, telefone, email, data_admissao, situacao, permissao, usuario, senha):
    conn = get_connection()
    cursor = conn.cursor()
    query = """
    INSERT INTO Funcionario (nome_funcionario, cargo, telefone, email, data_admissao, situacao, permissao, usuario, senha) 
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
    """
    cursor.execute(query, (nome_funcionario, cargo, telefone, email, data_admissao, situacao, permissao, usuario, senha))
    conn.commit()
    cursor.close()
    conn.close()

def listar_funcionario():
    conn = get_connection()
    cursor = conn.cursor()
    query = "SELECT * FROM Funcionario"
    cursor.execute(query)
    result = cursor.fetchall()
    cursor.close()
    conn.close()
    return result

def atualizar_funcionario(idFuncionario, nome_funcionario, cargo, telefone, email, data_admissao, situacao, permissao, usuario, senha):
    conn = get_connection()
    cursor = conn.cursor()
    query = """
    UPDATE Funcionario 
    SET nome_funcionario=%s, cargo=%s, telefone=%s, email=%s, data_admissao=%s, situacao=%s, permissao=%s, usuario=%s, senha=%s
    WHERE idFuncionario=%s
    """
    cursor.execute(query, (nome_funcionario, cargo, telefone, email, data_admissao, situacao, permissao, usuario, senha, idFuncionario))
    conn.commit()
    cursor.close()
    conn.close()

def deletar_funcionario(idFuncionario):
    conn = get_connection()
    cursor = conn.cursor()
    query = "DELETE FROM Funcionario WHERE idFuncionario = %s"
    cursor.execute(query, (idFuncionario,))
    conn.commit()
    cursor.close()
    conn.close()

# Métodos para a aba Funcionario
def create_funcionario(self):
    nome_funcionario = self.nome_funcionario_entry.get()
    cargo = self.cargo_entry.get()
    telefone = self.telefone_entry.get()
    email = self.email_entry.get()
    data_admissao = self.data_admissao_entry.get()
    situacao = self.situacao_entry.get()
    permissao = self.permissao_entry.get()
    usuario = self.usuario_entry.get()
    senha = self.senha_entry.get()

    if nome_funcionario and cargo and telefone and email and data_admissao and situacao and permissao and usuario and senha:
        criar_funcionario(nome_funcionario, cargo, telefone, email, data_admissao, situacao, permissao, usuario, senha)
        messagebox.showinfo("Sucesso", "Funcionário cadastrado com sucesso!")
        self.clear_funcionario_entries()
        self.read_funcionario()  # Atualizar a tabela
    else:
        messagebox.showerror("Erro", "Todos os campos são obrigatórios")

def read_funcionario(self):
    # Chama a função de listagem de funcionários e armazena os dados retornados
    funcionarios = listar_funcionario()  # Função que retorna uma lista de dados de funcionários
    
    # Limpa a tabela de funcionários antes de adicionar novos dados
    for row in self.funcionario_table.get_children():
        self.fornecedor_table.insert("", "end", values=funcionario)  # Inserir os dados na tabela

    # Insere cada funcionário na tabela
    for funcionario in funcionarios:
        self.funcionario_table.insert("", "end", values=funcionario)  # Insere cada linha na tabela


def update_funcionario(self):
    id_funcionario = self.id_funcionario_entry.get()
    nome_funcionario = self.nome_funcionario_entry.get()
    cargo = self.cargo_entry.get()
    telefone = self.telefone_entry.get()
    email = self.email_entry.get()
    data_admissao = self.data_admissao_entry.get()
    situacao = self.situacao_entry.get()
    permissao = self.permissao_entry.get()
    usuario = self.usuario_entry.get()
    senha = self.senha_entry.get()

    if id_funcionario and nome_funcionario and cargo and telefone and email and data_admissao and situacao and permissao and usuario and senha:
        atualizar_funcionario(id_funcionario, nome_funcionario, cargo, telefone, email, data_admissao, situacao, permissao, usuario, senha)
        messagebox.showinfo("Sucesso", "Funcionário atualizado com sucesso!")
        self.clear_funcionario_entries()
        self.read_funcionario()  # Atualizar a tabela
    else:
        messagebox.showerror("Erro", "Todos os campos são obrigatórios")

def delete_funcionario(self):
    id_funcionario = self.id_funcionario_entry.get()
    if id_funcionario:
        deletar_funcionario(id_funcionario)
        messagebox.showinfo("Sucesso", "Funcionário excluído com sucesso!")
        self.id_funcionario_entry.delete(0, tk.END)
        self.read_funcionario()  # Atualizar a tabela
    else:
        messagebox.showerror("Erro", "Digite um ID válido para exclusão")

def clear_funcionario_entries(self):
    self.nome_funcionario_entry.delete(0, tk.END)
    self.cargo_entry.delete(0, tk.END)
    self.telefone_entry.delete(0, tk.END)
    self.email_entry.delete(0, tk.END)
    self.data_admissao_entry.delete(0, tk.END)
    self.situacao_entry.delete(0, tk.END)
    self.permissao_entry.delete(0, tk.END)
    self.usuario_entry.delete(0, tk.END)
    self.senha_entry.delete(0, tk.END)
    self.id_funcionario_entry.delete(0, tk.END)

class Database:
    def __init__(self):
        # Conecta ao banco de dados MySQL com as credenciais fornecidas
        self.conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="ForneInjet_SA"
        )
        self.cursor = self.conn.cursor()  # Cria um cursor para executar comandos SQL
        
        # Criação da tabela "funcionario", se ela não existir
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS funcionario (
                                idFuncionario INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
                                nome_funcionario TEXT,
                                email TEXT,
                                telefone TEXT,
                                cargo TEXT,
                                data_admissao DATE,  # Ou altere para DATE, se necessário
                                situacao TEXT,
                                permissao TEXT,
                                usuario TEXT,
                                senha TEXT
                            );''')
        self.conn.commit()  # Confirma criação da tabela
        print("Conectado ao banco de dados")

    # Método chamado quando a instância da classe é destruída
    def close_connection(self):
        self.conn.close()  # Fecha a conexão com o banco de dados