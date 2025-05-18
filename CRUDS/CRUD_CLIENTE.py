from tkinter import messagebox
from CONFIG import get_connection

def ADD_CLIENTE(entries, tree_clientes):
    conn = get_connection()
    cursor = conn.cursor()
    
    query = """
    INSERT INTO Cliente (nome, CNPJ, telefone, email, cadastrado_por)
    VALUES (%s, %s, %s, %s, %s)
    """
    valores = (
        entries["Nome"].get(),
        entries["CNPJ"].get(),
        entries["Telefone"].get(),
        entries["E-mail"].get(),
        int(entries["Cadastrado Por"].get())
    )
    
    cursor.execute(query, valores)
    id_cliente = cursor.lastrowid
    
    # Inserir endereço
    query_end = """
    INSERT INTO EnderecoCliente (ID_Cliente, rua, numero, bairro, cidade, estado, cep)
    VALUES (%s, %s, %s, %s, %s, %s, %s)
    """
    valores_end = (
        id_cliente,
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
    UPD_TABELA_CLIENTE(tree_clientes)
    cursor.close()
    conn.close()


def DEL_CLIENTE(cliente_id, tree):
    id_cli = cliente_id.get()
    if not id_cli:
        messagebox.showwarning("Aviso", "Selecione um cliente para excluir!")
        return
    
    resposta = messagebox.askyesno("Confirmar", "Deseja realmente excluir este cliente?")
    if resposta:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("DELETE FROM EnderecoCliente WHERE ID_Cliente = %s", (id_cli,))
        cursor.execute("DELETE FROM Cliente WHERE ID_Cliente = %s", (id_cli,))

        conn.commit()
        messagebox.showinfo("Sucesso", "Cliente excluído com sucesso!")
        UPD_TABELA_CLIENTE(tree)
        cursor.close()
        conn.close()


def UPD_CLIENTE(entries, cliente_id, tree):
    id_cli = cliente_id.get()
    if not id_cli:
        messagebox.showwarning("Aviso", "Selecione um cliente para atualizar!")
        return
    
    conn = get_connection()
    cursor = conn.cursor()

    query = """
    UPDATE Cliente SET 
        nome = %s,
        CNPJ = %s,
        telefone = %s,
        email = %s,
        cadastrado_por = %s
    WHERE ID_Cliente = %s
    """
    valores = (
        entries["Nome"].get(),
        entries["CNPJ"].get(),
        entries["Telefone"].get(),
        entries["E-mail"].get(),
        int(entries["Cadastrado Por"].get()),
        id_cli
    )
    
    cursor.execute(query, valores)

    query_end = """
    UPDATE EnderecoCliente SET
        rua = %s,
        numero = %s,
        bairro = %s,
        cidade = %s,
        estado = %s,
        cep = %s
    WHERE ID_Cliente = %s
    """
    valores_end = (
        entries["Rua"].get(),
        entries["Número"].get(),
        entries["Bairro"].get(),
        entries["Cidade"].get(),
        entries["Estado"].get(),
        entries["CEP"].get(),
        id_cli
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

    for item in tree.get_children():
        tree.delete(item)
    
    query = """
    SELECT c.*, CONCAT(e.rua, ', ', e.numero, ', ', e.bairro, ', ', e.cidade, ', ', e.estado) AS endereco
    FROM Cliente c
    LEFT JOIN EnderecoCliente e ON c.ID_Cliente = e.ID_Cliente
    """
    cursor.execute(query)
    clientes = cursor.fetchall()

    for cli in clientes:
        tree.insert("", "end", values=(
            cli["ID_Cliente"],
            cli["nome"],
            cli["CNPJ"],
            cli["telefone"],
            cli["email"],
            cli["cadastrado_por"],
            cli["endereco"]
        ))
    
    cursor.close()
    conn.close()


def UPD_CAMPOS_CLIENTE(entries, cliente_id, id_cli):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    query = """
    SELECT c.*, e.*
    FROM Cliente c
    LEFT JOIN EnderecoCliente e ON c.ID_Cliente = e.ID_Cliente
    WHERE c.ID_Cliente = %s
    """
    cursor.execute(query, (id_cli,))
    cli = cursor.fetchone()

    if cli:
        entries["Nome"].delete(0, "end")
        entries["Nome"].insert(0, cli["nome"])

        entries["CNPJ"].delete(0, "end")
        entries["CNPJ"].insert(0, cli["CNPJ"])

        entries["Telefone"].delete(0, "end")
        entries["Telefone"].insert(0, cli["telefone"] or "")

        entries["E-mail"].delete(0, "end")
        entries["E-mail"].insert(0, cli["email"] or "")

        entries["Cadastrado Por"].delete(0, "end")
        entries["Cadastrado Por"].insert(0, str(cli["cadastrado_por"]))

        entries["Rua"].delete(0, "end")
        entries["Rua"].insert(0, cli["rua"] or "")

        entries["Número"].delete(0, "end")
        entries["Número"].insert(0, cli["numero"] or "")

        entries["Bairro"].delete(0, "end")
        entries["Bairro"].insert(0, cli["bairro"] or "")

        entries["Cidade"].delete(0, "end")
        entries["Cidade"].insert(0, cli["cidade"] or "")

        entries["Estado"].delete(0, "end")
        entries["Estado"].insert(0, cli["estado"] or "")

        entries["CEP"].delete(0, "end")
        entries["CEP"].insert(0, cli["cep"] or "")

        cliente_id.delete(0, "end")
        cliente_id.insert(0, str(cli["ID_Cliente"]))

    cursor.close()
    conn.close()


def UPD_DADOS_CLIENTE(id_cliente):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    query = """
    SELECT 
        c.ID_Cliente,
        c.nome,
        c.CNPJ,
        c.telefone,
        c.email,
        c.cadastrado_por,
        e.rua,
        e.numero,
        e.bairro,
        e.cidade,
        e.estado,
        e.cep
    FROM Cliente c
    LEFT JOIN EnderecoCliente e ON c.ID_Cliente = e.ID_Cliente
    WHERE c.ID_Cliente = %s
    """
    cursor.execute(query, (id_cliente,))
    dados = cursor.fetchone()

    cursor.close()
    conn.close()
    return dados if dados else {}

def GET_CLIENTES():
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT ID_Cliente, nome FROM cliente ORDER BY nome")
    clientes = cursor.fetchall()
    
    conn.close()
    return clientes