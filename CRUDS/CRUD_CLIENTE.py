from tkinter import messagebox
from CONFIG import get_connection

def ADD_CLIENTE(entries,tree_Cliente):
    conn = get_connection()
    cursor = conn.cursor()
    
    # Inserir Cliente
    query = """
    INSERT INTO cliente (nome, cnpj, telefone, email, Cadastrado_por)
    VALUES (%s, %s, %s, %s, %s)
    """
    valores = (
        entries["Nome"].get(),
        entries["cnpj"].get(),
        entries["Telefone"].get(),
        entries["E-mail"].get(),
        entries["Cadastrado por"].get()
    )
    
    cursor.execute(query, valores)
    ID_cliente = cursor.lastrowid

    # Inserir endereço do Cliente
    query_end = """
    INSERT INTO EnderecoCliente (ID_cliente, rua, numero, bairro, cidade, estado, cep)
    VALUES (%s, %s, %s, %s, %s, %s, %s)
    """
    valores_end = (
        ID_cliente,
        entries["Rua"].get(),
        entries["Número"].get(),
        entries["Bairro"].get(),
        entries["Cidade"].get(),
        entries["Estado"].get(),
        entries["CEP"].get()
    )
    
    cursor.execute(query_end, valores_end)
    conn.commit()
    
    messagebox.showinfo("Sucesso", "Cliente cadastrado com sucesso!")
    UPD_TABELA_CLIENTE(tree_Cliente)
    cursor.close()
    conn.close()

def DEL_CLIENTE(ID_cliente, tree):
    ID_clie = ID_cliente.get()
    if not ID_clie:
        messagebox.showwarning("Aviso", "Selecione um Cliente para excluir!")
        return
        
    resposta = messagebox.askyesno("Confirmar", "Deseja realmente excluir este Cliente?")
    if resposta:
        conn = get_connection()
        cursor = conn.cursor()
        
        cursor.execute("DELETE FROM EnderecoCliente WHERE ID_cliente = %s", (ID_clie,))
        cursor.execute("DELETE FROM Cliente WHERE ID_cliente = %s", (ID_clie,))
        
        conn.commit()
        messagebox.showinfo("Sucesso", "Cliente excluído com sucesso!")
        UPD_TABELA_CLIENTE(tree)
        cursor.close()
        conn.close()

def UPD_CLIENTE(entries, ID_cliente, tree):
    ID_clie = ID_cliente.get()
    if not ID_clie:
        messagebox.showwarning("Aviso", "Selecione um Cliente para atualizar!")
        return

    conn = get_connection()
    cursor = conn.cursor()
    
    # Atualizar Cliente
    query = """
    UPDATE cliente SET 
        nome = %s,
        cnpj = %s,
        telefone = %s,
        email = %s,
        Cadastrado_por = %s
    WHERE ID_cliente = %s
    """
    valores = (
        entries["Nome"].get(),
        entries["cnpj"].get(),
        entries["Telefone"].get(),
        entries["E-mail"].get(),
        entries["Cadastrado por"].get(),
        ID_clie
    )
    cursor.execute(query, valores)

    # Atualizar endereço
    query_end = """
    UPDATE EnderecoCliente SET 
        rua = %s,
        numero = %s,
        bairro = %s,
        cidade = %s,
        estado = %s,
        cep = %s
    WHERE ID_cliente = %s
    """
    valores_end = (
        entries["Rua"].get(),
        entries["Número"].get(),
        entries["Bairro"].get(),
        entries["Cidade"].get(),
        entries["Estado"].get(),
        entries["CEP"].get(),
        ID_clie
    )
    
    cursor.execute(query_end, valores_end)
    conn.commit()
    
    messagebox.showinfo("Sucesso", "Cliente atualizado com sucesso!")
    UPD_TABELA_CLIENTE(tree)
    cursor.close()
    conn.close()

def UPD_TABELA_CLIENTE(tree):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    
    # Limpar a treeview
    for item in tree.get_children():
        tree.delete(item)
    
    # Buscar clientes e endereço
    query = """
    SELECT c.*, 
           CONCAT(e.rua, ', ', e.numero, ', ', e.bairro, ', ', e.cidade, ', ', e.estado) as endereco
    FROM Cliente c
    LEFT JOIN EnderecoCliente e ON c.ID_cliente = e.ID_cliente
    """
    cursor.execute(query)
    clientes = cursor.fetchall()
    
    for clie in clientes:
        tree.insert("", "end", values=(
            clie["ID_cliente"],
            clie["nome"],
            clie["cnpj"],
            clie["telefone"],
            clie["email"],
            clie["Cadastrado_por"],
            clie["endereco"]
        ))
        
    cursor.close()
    conn.close()

def UPD_CAMPOS_CLIENTE(entries, ID_cliente, ID_clie, Cliente):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    
    query = """
    SELECT f.*, e.* 
    FROM Cliente f
    LEFT JOIN EnderecoCliente e ON f.ID_cliente = e.ID_cliente
    WHERE f.ID_cliente = %s
    """
    cursor.execute(query, (ID_clie,))
    clie = cursor.fetchone()
    
    if clie:
        entries["Nome"].delete(0, "end")
        entries["Nome"].insert(0, clie["nome"])

        entries["cnpj"].delete(0, "end")
        entries["cnpj"].insert(0, clie["cnpj"] or "")

        entries["Telefone"].delete(0, "end")
        entries["Telefone"].insert(0, clie["telefone"] or "")

        entries["E-mail"].delete(0, "end")
        entries["E-mail"].insert(0, clie["email"] or "")

        entries["Cadastrado por"].delete(0, "end")
        entries["Cadastrado por"].insert(0, clie["Cadastrado_por"])

        entries["Rua"].delete(0, "end")
        entries["Rua"].insert(0, clie["rua"] or "")

        entries["Número"].delete(0, "end")
        entries["Número"].insert(0, clie["numero"] or "")

        entries["Bairro"].delete(0, "end")
        entries["Bairro"].insert(0, clie["bairro"] or "")

        entries["Cidade"].delete(0, "end")
        entries["Cidade"].insert(0, clie["cidade"] or "")

        entries["Estado"].delete(0, "end")
        entries["Estado"].insert(0, clie["estado"] or "")

        entries["CEP"].delete(0, "end")
        entries["CEP"].insert(0, clie["cep"] or "")

        ID_cliente.delete(0, "end")
        ID_cliente.insert(0, str(clie["ID_cliente"]))
        
    cursor.close()
    conn.close()
