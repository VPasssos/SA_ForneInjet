from Config import get_connection

def create_produto(tipo, marca, modelo, capacidade_de_injeçao, força_de_fechamento, tipo_de_controle, preço_medio_USD,preço_medio_BRL, 
fornecedor, observacao):

    conn = get_connection()
    cursor = conn.cursor()
    query = "INCERT INTO  produto(tipo, marca, modelo, capacidade_de_injecao,força_de_fechamento, tipo_de_controle, preço_medio_USD,preço_medio_BRL, fornecedor, observacao) VALUES( %s, %s, %s, %s, %s, %s ,%s, %s, %s,%s)"
    cursor.execute(query, (tipo, marca, modelo, capacidade_de_injeçao, força_de_fechamento, tipo_de_controle, preço_medio_USD,preço_medio_BRL, fornecedor, observacao))
    conn.commit()
    cursor.close()
    conn.close()

def read_produto():

    conn = get_connection()
    cursor = conn.cursor()
    query = "SELECT * FROM produto"
    cursor.execute(query)
    result = cursor.fetchall()
    cursor.close()
    conn.close()
    return result

def update_produto(tipo, marca, modelo, capacidade_de_injeçao, força_de_fechamento, tipo_de_controle, preço_medio_USD,preço_medio_BRL, fornecedor, observacao, idMaquinas):

    conn = get_connection()
    cursor = conn.cursor()
    query = "UPDATE produto SET tipo = %s, marca = %s, modelo = %s, capacidade_de_injecao = %s , força_de_fechamento = %s, tipo_de_controle = %s, observaçoes = %s WHERE idMaquinas = %s"
    cursor.execute(query, (tipo, marca, modelo, capacidade_de_injeçao, força_de_fechamento, tipo_de_controle, preço_medio_USD,preço_medio_BRL, fornecedor, observacao, idMaquinas))
    conn.commit()
    cursor.close()
    conn.close()

def delete_produto(idMaquinas):

    conn = get_connection()
    cursor = conn.cursor()
    query = "DELETE FROM produto WHERE idMaquinas = %s"
    cursor.execute(query, (idMaquinas,))
    conn.commit()
    cursor.close()
    conn.close()