from Config import get_connection

def create_fornecedor(nome_fornecedor, cnpj, email, endereco, telefone , contato_principal, website):
    conn = get_connection()
    cursor = conn.cursor()
    query = "insert Fornecedor (nome_fornecedor, cnpj, email, endereco, telefone, contato_principal, website) VALUES(%s,%s,%s,%s,%s,%s,%s)"
    cursor.execute(query,(nome_fornecedor, cnpj, email, endereco, telefone, contato_principal, website))
    conn.commit()
    cursor.close()
    conn.close()

def read_fornecedor():
    conn = get_connection()
    cursor = conn.cursor()
    query = "SELECT * FROM Fornecedor"
    cursor.execute(query)
    result = cursor.fetchall()
    cursor.close()
    conn.close()
    return result

def update_fornecedor(idFornecedor, nome_fornecedor, cnpj, email, endereco, telefone, contato_principal, website):
    conn = get_connection()
    cursor = conn.cursor()
    query = "UPDATE Fornecedor SET nome=%s, cnpj=%s, email=%s, endereco=%s, telefone=%s, contato_principal=%s, website=%s WHERE idFornecedor=%s"
    cursor.execute(query,(idFornecedor, nome_fornecedor, cnpj, email, endereco, telefone, contato_principal, website))
    conn.commit()
    cursor.close()
    conn.close()

def delete_fornecedor(idFornecedor):
    conn = get_connection()
    cursor = conn.cursor()
    query = "DELETE FROM Fornecedor WHERE idFornecedor = %s"
    cursor.execute(query,(idFornecedor,))
    conn.commit()
    cursor.close()
    conn.close()