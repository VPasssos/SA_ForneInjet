from Config import get_connection

def criar_produto(tipo, marca, modelo, capacidade_de_injeçao, força_de_fechamento, tipo_de_controle, preço_medio_USD, preço_medio_BRL, fornecedor, observacao):
    conn = get_connection()
    cursor = conn.cursor()
    query = "INSERT INTO Produto (tipo, marca, modelo, capacidade_de_injeçao, força_de_fechamento, tipo_de_controle, preço_medio_USD, preço_medio_BRL, fornecedor, observacao) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    cursor.execute(query, (tipo, marca, modelo, capacidade_de_injeçao, força_de_fechamento, tipo_de_controle, preço_medio_USD, preço_medio_BRL, fornecedor, observacao))
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

def atualizar_produto(tipo, marca, modelo, capacidade_de_injeçao, força_de_fechamento, tipo_de_controle, preço_medio_USD, preço_medio_BRL, fornecedor, observacao, idMaquinas):
    conn = get_connection()
    cursor = conn.cursor()
    query = "UPDATE Produto SET tipo = %s, marca = %s, modelo = %s, capacidade_de_injeçao = %s, força_de_fechamento = %s, tipo_de_controle = %s, preço_medio_USD = %s, preço_medio_BRL = %s, fornecedor = %s, observacao = %s WHERE idMaquinas = %s"
    cursor.execute(query, (tipo, marca, modelo, capacidade_de_injeçao, força_de_fechamento, tipo_de_controle, preço_medio_USD, preço_medio_BRL, fornecedor, observacao, idMaquinas))
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


def read_produtos(self):
    produtos = listar_produto()
    for row in self.func_table.get_children():
        self.func_table.delete(row)  # Limpar a tabela antes de adicionar novos dados

    for produto in produtos:
        self.func_table.insert("", "end", values=produto)  # Inserir os dados na tabela

def update_produtos(self):
    idMaquinas = self.idMaquinas_entry.get()
    tipo = self.func_tipo_entry.get()
    marca = self.func_marca_entry.get()
    modelo = self.func_modelo_entry.get()
    capacidade_de_injeçao = self.func_capacidade_de_injeçao_entry.get()
    força_de_fechamento = self.func_força_de_fechamento_entry.get()
    tipo_de_controle = self.func_tipo_de_controle_entry.get()
    preço_medio_USD = self.func_preço_medio_USD_entry.get()
    preço_medio_BRL = self.func_preço_medio_BRL_entry.get()
    fornecedor = self.func_fornecedor_entry.get()
    observacao = self.func_observacao_entry.get()

    if tipo and marca and modelo and capacidade_de_injeçao and  força_de_fechamento and tipo_de_controle and preço_medio_USD and preço_medio_BRL and fornecedor and observacao and idMaquinas:
        atualizar_produto(idMaquinas,tipo, marca, modelo, capacidade_de_injeçao, força_de_fechamento, tipo_de_controle, preço_medio_USD, preço_medio_BRL, fornecedor, observacao)
        messagebox.showinfo("Sucesso", "Produto atualizado com sucesso!")
        self.clear_produto_entries()
        self.read_produtos()  # Atualizar a tabela
    else:
        messagebox.showerror("Erro", "Todos os campos são obrigatórios")

def delete_produtos(self):
    idMaquinas = self.idMaquinas_entry.get()
    if idMaquinas:
        deletar_produto(idMaquinas)
        messagebox.showinfo("Sucesso", "Funcionário excluído com sucesso!")
        self.idMaquinas_entry.delete(0, tk.END)
        self.read_produto()  # Atualizar a tabela
    else:
        messagebox.showerror("Erro", "Digite um ID válido para exclusão")

def clear_produtos_entries(self):
    self.func_tipo_entry.delete(0, Tk.END)
    self..delete(0, tk.END)
    self..delete(0, tk.END)
    self..delete(0, tk.END)
    self..delete(0, tk.END)
    self..delete(0, tk.END)
    self..delete(0, tk.END)
    self..delete(0, tk.END)
    self..delete(0, tk.END)
    self..delete(0, tk.END)
    self..delete(0, tk.END)
