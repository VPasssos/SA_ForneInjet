from tkinter import messagebox
from CONFIG import get_connection

def ADD_CLIENTE(entries, tree_cliente, funcionario_id):
    """
    Cadastra um novo cliente no sistema com validações e tratamento de dados.
    
    Args:
        entries (dict): Dicionário com os campos do formulário
        tree_cliente (ttk.Treeview): Componente de tabela para exibição
        funcionario_id (int): ID do funcionário responsável pelo cadastro
    """
    conn = None
    cursor = None
    try:
        # Estabelece conexão com o banco de dados
        conn = get_connection()
        cursor = conn.cursor()
        
        # Validação de campos obrigatórios
        required_fields = ["Nome", "CNPJ"]
        for field in required_fields:
            if not entries[field].get().strip():
                messagebox.showerror("Erro", f"O campo {field} é obrigatório!")
                return
        
        # Query SQL para inserir novo cliente
        query = """
        INSERT INTO Cliente (nome, CNPJ, telefone, email, cadastrado_por)
        VALUES (%s, %s, %s, %s, %s)
        """
        # Valores obtidos dos campos do formulário
        valores = (
            entries["Nome"].get(),
            entries["CNPJ"].get(),
            entries["Telefone"].get(),
            entries["E-mail"].get(),
            funcionario_id  # Registra quem cadastrou
        )
        
        # Executa a inserção e obtém o ID gerado
        cursor.execute(query, valores)
        id_cliente = cursor.lastrowid
        
        # Verifica se há dados de endereço para inserir (pelo menos um campo preenchido)
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
        
        # Confirma as alterações no banco
        conn.commit()
        messagebox.showinfo("Sucesso", "Cliente cadastrado com sucesso!")
        
        # Atualiza a interface
        UPD_TABELA_CLIENTE(tree_cliente)
        LIMPAR_CAMPOS(entries)
        
    except Exception as e:
        # Em caso de erro, reverte as alterações
        if conn:
            conn.rollback()
        messagebox.showerror("Erro", f"Falha ao cadastrar cliente: {str(e)}")
    finally:
        # Fecha as conexões com o banco
        if cursor:
            cursor.close()
        if conn:
            conn.close()

def DEL_CLIENTE(cliente_id, tree):
    """
    Remove um cliente do sistema após validações de integridade.
    
    Args:
        cliente_id (StringVar/IntVar): ID do cliente a ser removido
        tree (ttk.Treeview): Componente de tabela para atualização
    """
    id_cli = cliente_id.get()
    if not id_cli:
        messagebox.showwarning("Aviso", "Selecione um cliente para excluir!")
        return
        
    # Confirmação de exclusão com o usuário    
    resposta = messagebox.askyesno("Confirmar", 
        "Deseja realmente excluir este cliente? Esta ação também excluirá todos os dados associados (endereço, vendas, etc.)")
    if not resposta:
        return
    
    conn = None
    cursor = None
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        # Verifica se existem vendas associadas ao cliente
        cursor.execute("SELECT COUNT(*) FROM Venda WHERE ID_Cliente = %s", (id_cli,))
        if cursor.fetchone()[0] > 0:
            messagebox.showerror("Erro", "Este cliente possui vendas associadas e não pode ser excluído!")
            return
        
        # Exclusão em transação (primeiro endereço, depois cliente)
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
    """
    Atualiza os dados de um cliente existente no sistema.
    
    Args:
        entries (dict): Campos do formulário com os novos valores
        cliente_id (StringVar/IntVar): ID do cliente sendo editado
        tree (ttk.Treeview): Tabela para atualização visual
        funcionario_id (int): ID do funcionário realizando a atualização
    """
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
        
        # Query de atualização dos dados principais
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
        
        # Verifica se o cliente já possui endereço cadastrado
        cursor.execute("SELECT COUNT(*) FROM EnderecoCliente WHERE ID_Cliente = %s", (id_cli,))
        endereco_existe = cursor.fetchone()[0] > 0
        
        # Prepara os dados do endereço
        endereco_data = (
            entries["Rua"].get(),
            entries["Número"].get(),
            entries["Bairro"].get(),
            entries["Cidade"].get(),
            entries["Estado"].get(),
            entries["CEP"].get(),
            id_cli
        )
        
        # Decide entre UPDATE ou INSERT do endereço
        if endereco_existe:
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
    """
    Atualiza a tabela de exibição com todos os clientes cadastrados.
    
    Args:
        tree (ttk.Treeview): Componente de tabela a ser atualizado
    """
    conn = None
    cursor = None
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        
        # Limpa todos os itens atuais da tabela
        tree.delete(*tree.get_children())
        
        # Query que combina dados do cliente com endereço (LEFT JOIN)
        query = """
        SELECT c.*, 
               CONCAT(e.rua, ', ', e.numero, ', ', e.bairro, ', ', e.cidade, ', ', e.estado) as endereco
        FROM Cliente c
        LEFT JOIN EnderecoCliente e ON c.ID_Cliente = e.ID_Cliente
        ORDER BY c.nome
        """
        cursor.execute(query)
        
        # Insere cada cliente na tabela de exibição
        for cli in cursor.fetchall():
            tree.insert("", "end", values=(
                cli["ID_Cliente"],
                cli["nome"],
                cli["CNPJ"],
                cli["telefone"] or "",  # Trata valores nulos
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
    """
    Preenche os campos do formulário com os dados de um cliente selecionado.
    
    Args:
        entries (dict): Campos do formulário a serem preenchidos
        cliente_id (StringVar/IntVar): Variável para armazenar o ID
        id_cli (int): ID do cliente a ser carregado
    """
    conn = None
    cursor = None
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        
        # Busca os dados do cliente e endereço (se existir)
        query = """
        SELECT c.*, e.* 
        FROM Cliente c
        LEFT JOIN EnderecoCliente e ON c.ID_Cliente = e.ID_Cliente
        WHERE c.ID_Cliente = %s
        """
        cursor.execute(query, (id_cli,))
        cli = cursor.fetchone()
        
        if cli:
            # Mapeamento de campos para preenchimento automático
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
            
            # Atualiza o campo de ID do cliente
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
    """
    Obtém lista simplificada de clientes para uso em comboboxes ou seleções.
    
    Returns:
        list: Tuplas com (ID_Cliente, nome) ordenadas por nome
    """
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
    """
    Limpa todos os campos de entrada do formulário.
    
    Args:
        entries (dict): Dicionário com referências aos campos de entrada
    """
    for entry in entries.values():
        entry.delete(0, "end")