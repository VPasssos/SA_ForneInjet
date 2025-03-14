import mysql.connector
from Config import get_connection
from tkinter import messagebox
import tkinter as tk


def criar_funcionario(nome_funcionario, telefone, email, cargo, data_admissao, situacao, permissao, usuario, senha):
    conn = get_connection()
    cursor = conn.cursor()
    query = """INSERT INTO funcionario (nome_funcionario, telefone, email, cargo, data_admissao, situacao, permissao, usuario, senha)
               VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"""
    cursor.execute(query, (nome_funcionario, telefone, email, cargo, data_admissao, situacao, permissao, usuario, senha))
    conn.commit()
    cursor.close()
    conn.close()

def listar_funcionario():  
    conn = get_connection()
    cursor = conn.cursor()
    query = "SELECT * FROM funcionario"
    cursor.execute(query)
    result = cursor.fetchall()
    cursor.close()
    conn.close()
    return result 

def atualizar_funcionario(idfuncionario, nome_funcionario, telefone, email, cargo, data_admissao, situacao, permissao, usuario, senha):
    conn = get_connection()
    cursor = conn.cursor()
    query = """UPDATE funcionario
               SET nome_funcionario=%s, telefone=%s, email=%s, cargo=%s, data_admissao=%s, situacao=%s, permissao=%s,usuario=%s,senha=%s
               WHERE idfuncionario=%s"""
    cursor.execute(query, (nome_funcionario, telefone, email, cargo, data_admissao, situacao, permissao, usuario, senha, idfuncionario))
    conn.commit()
    cursor.close()
    conn.close()

def deletar_funcionario(idfuncionario):
    conn = get_connection()
    cursor = conn.cursor()
    query = "DELETE FROM funcionario WHERE idfuncionario = %s"
    cursor.execute(query, (idfuncionario,))
    conn.commit()
    cursor.close()
    conn.close()

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
        criar_funcionario(nome_funcionario, cargo, telefone, email, data_admissao, situacao, permissao, usuario, senha)
        messagebox.showinfo("Sucesso", "Funcionário criado com sucesso!")
        self.clear_funcionario_entries()
        self.read_funcionarios()  # Atualizar a tabela
    else:
        messagebox.showerror("Erro", "Todos os campos são obrigatórios")

def read_funcionarios(self):
    funcionarios = listar_funcionario()
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
        atualizar_funcionario(func_id, nome, email, telefone, cargo, data_admissao, situacao, permissao, usuario, senha)
        messagebox.showinfo("Sucesso", "Funcionário atualizado com sucesso!")
        self.clear_funcionario_entries()
        self.read_funcionarios()  # Atualizar a tabela
    else:
        messagebox.showerror("Erro", "Todos os campos são obrigatórios")

def delete_funcionario(self):
    func_id = self.func_id_entry.get()
    if func_id:
        deletar_funcionario(func_id)
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
