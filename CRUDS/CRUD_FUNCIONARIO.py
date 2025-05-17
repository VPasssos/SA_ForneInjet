from tkinter import messagebox
from CONFIG import get_connection

def ADD_FUNCIONARIO(entries, tree_funcionarios):
    conn = get_connection()
    cursor = conn.cursor()
    query = """
    INSERT INTO Funcionario (nome, cargo, telefone, email, usuario, senha, permissao, situacao, data_admissao)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
    """
    valores = (
        entries["Nome"].get(),
        entries["Cargo"].get(),
        entries["Telefone"].get(),
        entries["E-mail"].get(),
        entries["Usuário"].get(),
        entries["Senha"].get(),
        entries["Permissão"].get(),
        entries["Situação"].get(),
        entries["Data Admissão"].get()
    )
    
    cursor.execute(query, valores)
    id_funcionario = cursor.lastrowid
    
    # Inserir endereço do funcionário
    query_end = """
    INSERT INTO EnderecoFornecedor (ID_Funcionario, rua, numero, bairro, cidade, estado, cep)
    VALUES (%s, %s, %s, %s, %s, %s, %s)
    """
    valores_end = (
        id_funcionario,
        entries["Rua"].get(),
        entries["Número"].get(),
        entries["Bairro"].get(),
        entries["Cidade"].get(),
        entries["Estado"].get(),
        entries["CEP"].get()
    )
    
    cursor.execute(query_end, valores_end)
    conn.commit()
    
    messagebox.showinfo("Sucesso", "Funcionário cadastrado com sucesso!")
    UPD_TABELA_FUNCIONARIO(tree_funcionarios)
    cursor.close()
    conn.close()

def DEL_FUNCIONARIO(funcionario_id, tree):
    id_func = funcionario_id.get()
    if not id_func:
        messagebox.showwarning("Aviso", "Selecione um funcionário para excluir!")
        return
        
    resposta = messagebox.askyesno("Confirmar", "Deseja realmente excluir este funcionário?")
    if resposta:
        conn = get_connection()
        cursor = conn.cursor()
        
        # Primeiro excluir o endereço
        cursor.execute("DELETE FROM EnderecoFuncionario WHERE ID_Funcionario = %s", (id_func,))
        # Depois excluir o funcionário
        cursor.execute("DELETE FROM Funcionario WHERE ID_Funcionario = %s", (id_func,))
        
        conn.commit()
        messagebox.showinfo("Sucesso", "Funcionário excluído com sucesso!")
        UPD_TABELA_FUNCIONARIO(tree)
        cursor.close()
        conn.close()

def UPD_FUNCIONARIO(entries, funcionario_id, tree):
    id_func = funcionario_id.get()
    if not id_func:
        messagebox.showwarning("Aviso", "Selecione um funcionário para atualizar!")
        return
        
    conn = get_connection()
    cursor = conn.cursor()
    
    # Atualizar funcionário
    query = """
    UPDATE Funcionario SET 
        nome = %s,
        cargo = %s,
        telefone = %s,
        email = %s,
        usuario = %s,
        senha = %s,
        permissao = %s,
        situacao = %s,
        data_admissao = %s
    WHERE ID_Funcionario = %s
    """
    valores = (
        entries["Nome"].get(),
        entries["Cargo"].get(),
        entries["Telefone"].get(),
        entries["E-mail"].get(),
        entries["Usuário"].get(),
        entries["Senha"].get(),
        entries["Permissão"].get(),
        entries["Situação"].get(),
        entries["Data Admissão"].get(),
        id_func
    )
    
    cursor.execute(query, valores)
    
    # Atualizar endereço do funcionário
    query_end = """
    UPDATE EnderecoFuncionario SET 
        rua = %s,
        numero = %s,
        bairro = %s,
        cidade = %s,
        estado = %s,
        cep = %s
    WHERE ID_Funcionario = %s
    """
    valores_end = (
        entries["Rua"].get(),
        entries["Número"].get(),
        entries["Bairro"].get(),
        entries["Cidade"].get(),
        entries["Estado"].get(),
        entries["CEP"].get(),
        id_func
    )
    
    cursor.execute(query_end, valores_end)
    conn.commit()
    
    messagebox.showinfo("Sucesso", "Funcionário atualizado com sucesso!")
    UPD_TABELA_FUNCIONARIO(tree)
    cursor.close()
    conn.close()

def UPD_TABELA_FUNCIONARIO(tree):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    
    # Limpar a treeview
    for item in tree.get_children():
        tree.delete(item)
    
    # Buscar funcionários com informações de endereço
    query = """
    SELECT f.*, 
           CONCAT(e.rua, ', ', e.numero, ', ', e.bairro, ', ', e.cidade, ', ', e.estado) as endereco
    FROM Funcionario f
    LEFT JOIN EnderecoFuncionario e ON f.ID_Funcionario = e.ID_Funcionario
    """
    cursor.execute(query)
    funcionarios = cursor.fetchall()
    
    # Preencher a treeview
    for func in funcionarios:
        tree.insert("", "end", values=(
            func["ID_Funcionario"],
            func["nome"],
            func["cargo"],
            func["telefone"],
            func["email"],
            func["usuario"],
            func["senha"],
            func["permissao"],
            func["situacao"],
            func["data_admissao"].strftime("%d/%m/%Y") if func["data_admissao"] else "",
            func["endereco"]
        ))
        
    cursor.close()
    conn.close()

def UPD_CAMPOS_FUNCIONARIO(entries, funcionario_id, id_func):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    
    # Buscar dados do funcionário
    query = """
    SELECT f.*, e.* 
    FROM Funcionario f
    LEFT JOIN EnderecoFuncionario e ON f.ID_Funcionario = e.ID_Funcionario
    WHERE f.ID_Funcionario = %s
    """
    cursor.execute(query, (id_func,))
    func = cursor.fetchone()
    
    if func:
        # Preencher os campos principais
        entries["Nome"].delete(0, "end")
        entries["Nome"].insert(0, func["nome"])
        
        entries["Cargo"].delete(0, "end")
        entries["Cargo"].insert(0, func["cargo"] if func["cargo"] else "")
        
        entries["Telefone"].delete(0, "end")
        entries["Telefone"].insert(0, func["telefone"] if func["telefone"] else "")
        
        entries["E-mail"].delete(0, "end")
        entries["E-mail"].insert(0, func["email"] if func["email"] else "")
        
        entries["Usuário"].delete(0, "end")
        entries["Usuário"].insert(0, func["usuario"])
        
        entries["Senha"].delete(0, "end")
        entries["Senha"].insert(0, func["senha"])
        
        entries["Permissão"].delete(0, "end")
        entries["Permissão"].set(func["permissao"])
        
        entries["Situação"].delete(0, "end")
        entries["Situação"].set(func["situacao"])
        
        entries["Data Admissão"].delete(0, "end")
        entries["Data Admissão"].insert(0, func["data_admissao"].strftime("%d/%m/%Y") if func["data_admissao"] else "")
        
        entries["Rua"].delete(0, "end")
        entries["Rua"].insert(0, func["rua"] if func["rua"] else "")
        
        entries["Número"].delete(0, "end")
        entries["Número"].insert(0, func["numero"] if func["numero"] else "")
        
        entries["Bairro"].delete(0, "end")
        entries["Bairro"].insert(0, func["bairro"] if func["bairro"] else "")
        
        entries["Cidade"].delete(0, "end")
        entries["Cidade"].insert(0, func["cidade"] if func["cidade"] else "")
        
        entries["Estado"].delete(0, "end")
        entries["Estado"].insert(0, func["estado"] if func["estado"] else "")
        
        entries["CEP"].delete(0, "end")
        entries["CEP"].insert(0, func["cep"] if func["cep"] else "")

        # Atualizar o ID do funcionário
        funcionario_id.delete(0, "end")
        funcionario_id.insert(0, str(func["ID_Funcionario"]))
        
    cursor.close()
    conn.close()

def UPD_DADOS_FUNCIONARIOS(id_funcionario):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    
   
    query = """
    SELECT 
        f.ID_Funcionario,
        f.nome,
        f.cargo,
        f.telefone,
        f.email,
        f.usuario,
        f.permissao,
        f.situacao,
        f.data_admissao,
        e.rua,
        e.numero,
        e.bairro,
        e.cidade,
        e.estado,
        e.cep
    FROM Funcionario f
    LEFT JOIN EnderecoFuncionario e ON f.ID_Funcionario = e.ID_Funcionario
    WHERE f.ID_Funcionario = %s
    """
    
    cursor.execute(query, (id_funcionario,))
    dados = cursor.fetchone() 
    
    cursor.close()
    conn.close()
        
    return dados if dados else {}  