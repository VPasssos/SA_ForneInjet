from tkinter import messagebox
from CONFIG import get_connection

def ADD_CLIENTE(entries, tree_cliente, funcionario_id):
    conn = None
    cursor = None
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        # Validação de campos obrigatórios
        required_fields = ["Nome", "CNPJ"]
        for field in required_fields:
            if not entries[field].get().strip():
                messagebox.showerror("Erro", f"O campo {field} é obrigatório!")
                return
        
        # Inserir novo cliente
        query = """
        INSERT INTO Cliente (nome, CNPJ, telefone, email, cadastrado_por)
        VALUES (%s, %s, %s, %s, %s)
        """
        valores = (
            entries["Nome"].get(),
            entries["CNPJ"].get(),
            entries["Telefone"].get(),
            entries["E-mail"].get(),
            funcionario_id
        )
        
        cursor.execute(query, valores)
        id_cliente = cursor.lastrowid
        
        # Inserir endereço do cliente (se pelo menos um campo de endereço foi preenchido)
        if any(entries[field].get().strip() for field in ["Rua", "Número", "Bairro", "Cidade", "Estado", "CEP"]):
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
        UPD_TABELA_CLIENTE(tree_cliente)
        LIMPAR_CAMPOS(entries)
        
    except Exception as e:
        if conn:
            conn.rollback()
        messagebox.showerror("Erro", f"Falha ao cadastrar cliente: {str(e)}")
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

def DEL_CLIENTE(cliente_id, tree):
    id_cli = cliente_id.get()
    if not id_cli:
        messagebox.showwarning("Aviso", "Selecione um cliente para excluir!")
        return
        
    resposta = messagebox.askyesno("Confirmar", "Deseja realmente excluir este cliente? Esta ação também excluirá todos os dados associados (endereço, vendas, etc.)")
    if not resposta:
        return
    
    conn = None
    cursor = None
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        # Verificar se existem vendas associadas
        cursor.execute("SELECT COUNT(*) FROM Venda WHERE ID_Cliente = %s", (id_cli,))
        if cursor.fetchone()[0] > 0:
            messagebox.showerror("Erro", "Este cliente possui vendas associadas e não pode ser excluído!")
            return
        
        # Excluir em transação segura
        cursor.execute("DELETE FROM EnderecoCliente WHERE ID_Cliente = %s", (id_cli,))
        cursor.execute("DELETE FROM Cliente WHERE ID_Cliente = %s", (id_cli,))
        
        conn.commit()
        messagebox.showinfo("Sucesso", "Cliente excluído com sucesso!")
        UPD_TABELA_CLIENTE(tree)

    except Exception as e:
        if conn:
            conn.rollback()
        messagebox.showerror("Erro", f"Falha ao excluir cliente: {str(e)}")
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

def UPD_CLIENTE(entries, cliente_id, tree, funcionario_id):
    id_cli = cliente_id.get()
    if not id_cli:
        messagebox.showwarning("Aviso", "Selecione um cliente para atualizar!")
        return
        
    conn = None
    cursor = None
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        # Validação de campos obrigatórios
        required_fields = ["Nome", "CNPJ"]
        for field in required_fields:
            if not entries[field].get().strip():
                messagebox.showerror("Erro", f"O campo {field} é obrigatório!")
                return
        
        # Atualizar cliente
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
            funcionario_id,
            id_cli
        )
        cursor.execute(query, valores)
        
        # Verificar se endereço existe
        cursor.execute("SELECT COUNT(*) FROM EnderecoCliente WHERE ID_Cliente = %s", (id_cli,))
        endereco_existe = cursor.fetchone()[0] > 0
        
        # Dados do endereço
        endereco_data = (
            entries["Rua"].get(),
            entries["Número"].get(),
            entries["Bairro"].get(),
            entries["Cidade"].get(),
            entries["Estado"].get(),
            entries["CEP"].get(),
            id_cli
        )
        
        if endereco_existe:
            # Atualizar endereço existente
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
        else:
            # Inserir novo endereço
            query_end = """
            INSERT INTO EnderecoCliente 
                (rua, numero, bairro, cidade, estado, cep, ID_Cliente)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            """
        
        cursor.execute(query_end, endereco_data)
        conn.commit()
        
        messagebox.showinfo("Sucesso", "Cliente atualizado com sucesso!")
        UPD_TABELA_CLIENTE(tree)
        LIMPAR_CAMPOS(entries)
        
    except Exception as e:
        if conn:
            conn.rollback()
        messagebox.showerror("Erro", f"Falha ao atualizar cliente: {str(e)}")
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

def UPD_TABELA_CLIENTE(tree):
    conn = None
    cursor = None
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        
        # Limpar a treeview
        tree.delete(*tree.get_children())
        
        # Buscar clientes com informações de endereço
        query = """
        SELECT c.*, 
               CONCAT(e.rua, ', ', e.numero, ', ', e.bairro, ', ', e.cidade, ', ', e.estado) as endereco
        FROM Cliente c
        LEFT JOIN EnderecoCliente e ON c.ID_Cliente = e.ID_Cliente
        ORDER BY c.nome
        """
        cursor.execute(query)
        
        # Preencher a treeview
        for cli in cursor.fetchall():
            tree.insert("", "end", values=(
                cli["ID_Cliente"],
                cli["nome"],
                cli["CNPJ"],
                cli["telefone"] or "",
                cli["email"] or "",
                cli["endereco"] or "Endereço não cadastrado"
            ))
            
    except Exception as e:
        messagebox.showerror("Erro", f"Falha ao carregar clientes: {str(e)}")
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

def UPD_CAMPOS_CLIENTE(entries, cliente_id, id_cli):
    conn = None
    cursor = None
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        
        # Buscar dados do cliente
        query = """
        SELECT c.*, e.* 
        FROM Cliente c
        LEFT JOIN EnderecoCliente e ON c.ID_Cliente = e.ID_Cliente
        WHERE c.ID_Cliente = %s
        """
        cursor.execute(query, (id_cli,))
        cli = cursor.fetchone()
        
        if cli:
            # Limpar e preencher campos
            for field, db_field in [
                ("Nome", "nome"),
                ("CNPJ", "CNPJ"),
                ("Telefone", "telefone"),
                ("E-mail", "email"),
                ("Rua", "rua"),
                ("Número", "numero"),
                ("Bairro", "bairro"),
                ("Cidade", "cidade"),
                ("Estado", "estado"),
                ("CEP", "cep")
            ]:
                entries[field].delete(0, "end")
                entries[field].insert(0, cli.get(db_field, ""))
            
            # Atualizar o ID do cliente
            cliente_id.delete(0, "end")
            cliente_id.insert(0, str(cli["ID_Cliente"]))
            
    except Exception as e:
        messagebox.showerror("Erro", f"Falha ao carregar dados do cliente: {str(e)}")
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

def GET_CLIENTES():
    conn = None
    cursor = None
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT ID_Cliente, nome FROM Cliente ORDER BY nome")
        return cursor.fetchall()
    except Exception as e:
        messagebox.showerror("Erro", f"Falha ao obter lista de clientes: {str(e)}")
        return []
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

def LIMPAR_CAMPOS(entries):
    for entry in entries.values():
        entry.delete(0, "end")
