def create_user(nome, cnpj,email,endereco, telefone,cont_principal,site):
    conn = get_connection()
    cursor = conn.cursor()
    query = "insert usuario(nome, telefone, email, usuario, senha) VALUES(%s,%s,%s,%s,%s)"
    cursor.execute(query,(nome,cnpj,email, endereco, telefone, cont_principal, site))
    conn.commit()
    cursor.close()
    conn.close()

def read_users():
    conn = get_connection()
    cursor = conn.cursor()
    query = "SELECT * FROM usuario"
    cursor.execute(query)
    result = cursor.fetchall()
    cursor.close()
    conn.close()
    return result

def update_user(user_id,nome,cnpj,email,endereco,telefone,cont_principal,site):
    conn = get_connection()
    cursor = conn.cursor()
    query = "UPDATE aluno SET nome=%s, telefone=%s, email=%s, usuario=%s, senha=%s WHERE idusuario=%s"
    cursor.execute(query,(user_id, nome, cnpj, email, endereco, telefone, cont_principal, site))
    conn.commit()
    cursor.close()
    conn.close()

def delete_user(user_id):
    conn = get_connection()
    cursor = conn.cursor()
    query = "DELETE FROM aluno WHERE idusuario = %s"
    cursor.execute(query,(user_id))
    conn.commit()
    cursor.close()
    conn.close()