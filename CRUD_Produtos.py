from Config import get_connection

def create_produto(tipo, marca, modelo, capacidade_de_injecao, força_de_fechamento, tipo_de_controle, preço_médio_dolar,preço_médio_real, 
Fornecedor, observaçoes):

    conn = get_connection()
    cursor = conn.cursor()
    query = "insert produto(tipo, marca, modelo, capacidade_de_injecao,força_de_fechamento, tipo_de_controle, preço_médio_dolar,preço_médio_real, Fornecedor, observaçoes) VALUES( %s, %s, %s, %s, %s, %s ,%s, %s, %s,%s)"
    cursor.execute(query, (tipo, marca, modelo, capacidade_de_injecao, força_de_fechamento, tipo_de_controle, preço_médio_dolar,preço_médio_real, Fornecedor, observaçoes))
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

def update_produto(tipo, marca, modelo, capacidade_de_injecao, força_de_fechamento, tipo_de_controle, preço_médio_dolar,preço_médio_real, Fornecedor, observaçoes , produtoID):

    conn = get_connection()
    cursor = conn.cursor()
    query = "UPDATE produto SET tipo = %s, marca = %s, modelo = %s, capacidade_de_injecao = %s , força_de_fechamento = %s, tipo_de_controle = %s, observaçoes = %s WHERE produtoID = %s"
    cursor.execute(query, (tipo, marca, modelo, capacidade_de_injecao, força_de_fechamento, tipo_de_controle, preço_médio_dolar,preço_médio_real, Fornecedor, observaçoes , produtoID))
    conn.commit()
    cursor.close()
    conn.close()

def delete_produto(produtoID):

    conn = get_connection()
    cursor = conn.cursor()
    query = "DELETE FROM produto WHERE produtoID = %s"
    cursor.execute(query, (produtoID,))
    conn.commit()
    cursor.close()
    conn.close()