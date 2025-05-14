from tkinter import messagebox
from CONFIG import get_connection

def ADD_FORNECEDOR(entries, tree_fornecedor):
    conn = get_connection()
    cursor = conn.cursor()
    
    # Inserir novo fornecedor
    query = """
    INSERT INTO Fornecedor (NM_Fornecedor, CNPJ, telefone, email, website, cadastrado_por)
    VALUES (%s, %s, %s, %s, %s, %s)
    """
    valores = (
        entries["Nome"].get(),
        entries["CNPJ"].get(),
        entries["Telefone"].get(),
        entries["E-mail"].get(),
        entries["Website"].get()
    )
    
    cursor.execute(query, valores)
    id_fornecedor = cursor.lastrowid
    
    # Inserir endereço do fornecedor
    query_end = """
    INSERT INTO EnderecoFornecedor (ID_Fornecedor, rua, numero, bairro, cidade, estado, cep)
    VALUES (%s, %s, %s, %s, %s, %s, %s)
    """
    valores_end = (
        id_fornecedor,
        entries["Rua"].get(),
        entries["Número"].get(),
        entries["Bairro"].get(),
        entries["Cidade"].get(),
        entries["Estado"].get(),
        entries["CEP"].get()
    )
    
    cursor.execute(query_end, valores_end)
    conn.commit()
    
    messagebox.showinfo("Sucesso", "Fornecedor cadastrado com sucesso!")
    UPD_TABELA_FORNECEDOR(tree_fornecedor)
    cursor.close()
    conn.close()

def DEL_FORNECEDOR(fornecedor_id, tree):
    id_for = fornecedor_id.get()
    if not id_for:
        messagebox.showwarning("Aviso", "Selecione um fornecedor para excluir!")
        return
        
    resposta = messagebox.askyesno("Confirmar", "Deseja realmente excluir este fornecedor?")
    if resposta:
        conn = get_connection()
        cursor = conn.cursor()
        
        # Primeiro excluir o endereço
        cursor.execute("DELETE FROM EnderecoFornecedor WHERE ID_Fornecedor = %s", (id_for,))
        # Depois excluir o fornecedor
        cursor.execute("DELETE FROM Fornecedor WHERE ID_Fornecedor = %s", (id_for,))
        
        conn.commit()
        messagebox.showinfo("Sucesso", "Fornecedor excluído com sucesso!")
        UPD_TABELA_FORNECEDOR(tree)
        cursor.close()
        conn.close()

def UPD_FORNECEDOR(entries, fornecedor_id, tree, funcionario_id):
    id_for = fornecedor_id.get()
    if not id_for:
        messagebox.showwarning("Aviso", "Selecione um fornecedor para atualizar!")
        return
        
    conn = get_connection()
    cursor = conn.cursor()
    
    # Atualizar fornecedor
    query = """
    UPDATE Fornecedor SET 
        NM_Fornecedor = %s,
        CNPJ = %s,
        telefone = %s,
        email = %s,
        website = %s,
        cadastrado_por = %s
    WHERE ID_Fornecedor = %s
    """
    valores = (
        entries["Nome"].get(),
        entries["CNPJ"].get(),
        entries["Telefone"].get(),
        entries["E-mail"].get(),
        entries["Website"].get(),
        funcionario_id,
        id_for
    )
    
    cursor.execute(query, valores)
    
    # Atualizar endereço do fornecedor
    query_end = """
    UPDATE EnderecoFornecedor SET 
        rua = %s,
        numero = %s,
        bairro = %s,
        cidade = %s,
        estado = %s,
        cep = %s
    WHERE ID_Fornecedor = %s
    """
    valores_end = (
        entries["Rua"].get(),
        entries["Número"].get(),
        entries["Bairro"].get(),
        entries["Cidade"].get(),
        entries["Estado"].get(),
        entries["CEP"].get(),
        id_for
    )
    
    cursor.execute(query_end, valores_end)
    conn.commit()
    
    messagebox.showinfo("Sucesso", "Fornecedor atualizado com sucesso!")
    UPD_TABELA_FORNECEDOR(tree)
    cursor.close()
    conn.close()

def UPD_TABELA_FORNECEDOR(tree):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    
    # Limpar a treeview
    for item in tree.get_children():
        tree.delete(item)
    
    # Buscar fornecedores com informações de endereço
    query = """
    SELECT f.*, 
           CONCAT(e.rua, ', ', e.numero, ', ', e.bairro, ', ', e.cidade, ', ', e.estado) as endereco
    FROM Fornecedor f
    LEFT JOIN EnderecoFornecedor e ON f.ID_Fornecedor = e.ID_Fornecedor
    """
    cursor.execute(query)
    fornecedores = cursor.fetchall()
    
    # Preencher a treeview
    for forn in fornecedores:
        tree.insert("", "end", values=(
            forn["ID_Fornecedor"],
            forn["NM_Fornecedor"],
            forn["CNPJ"],
            forn["telefone"],
            forn["email"],
            forn["endereco"]
        ))
        
    cursor.close()
    conn.close()

def UPD_CAMPOS_FORNECEDOR(entries, fornecedor_id, id_for):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    
    # Buscar dados do fornecedor
    query = """
    SELECT f.*, e.* 
    FROM Fornecedor f
    LEFT JOIN EnderecoFornecedor e ON f.ID_Fornecedor = e.ID_Fornecedor
    WHERE f.ID_Fornecedor = %s
    """
    cursor.execute(query, (id_for,))
    forn = cursor.fetchone()
    
    if forn:
        # Preencher os campos
        entries["Nome"].delete(0, "end")
        entries["Nome"].insert(0, forn["NM_Fornecedor"])
        
        entries["CNPJ"].delete(0, "end")
        entries["CNPJ"].insert(0, forn["CNPJ"])
        
        entries["Telefone"].delete(0, "end")
        entries["Telefone"].insert(0, forn["telefone"] if forn["telefone"] else "")
        
        entries["E-mail"].delete(0, "end")
        entries["E-mail"].insert(0, forn["email"] if forn["email"] else "")
        
        entries["Website"].delete(0, "end")
        entries["Website"].insert(0, forn["website"] if forn["website"] else "")
        
        entries["Rua"].delete(0, "end")
        entries["Rua"].insert(0, forn["rua"] if forn["rua"] else "")
        
        entries["Número"].delete(0, "end")
        entries["Número"].insert(0, forn["numero"] if forn["numero"] else "")
        
        entries["Bairro"].delete(0, "end")
        entries["Bairro"].insert(0, forn["bairro"] if forn["bairro"] else "")
        
        entries["Cidade"].delete(0, "end")
        entries["Cidade"].insert(0, forn["cidade"] if forn["cidade"] else "")
        
        entries["Estado"].delete(0, "end")
        entries["Estado"].insert(0, forn["estado"] if forn["estado"] else "")
        
        entries["CEP"].delete(0, "end")
        entries["CEP"].insert(0, forn["cep"] if forn["cep"] else "")
        
        # Atualizar o ID do fornecedor
        fornecedor_id.delete(0, "end")
        fornecedor_id.insert(0, str(forn["ID_Fornecedor"]))
        
    cursor.close()
    conn.close()