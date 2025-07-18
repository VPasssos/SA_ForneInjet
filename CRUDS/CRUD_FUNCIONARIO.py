from tkinter import messagebox
from datetime import datetime
from CONFIG import get_connection
import hashlib

def converter_data(data_str):
    """
    Converte uma string de data no formato dd/mm/aaaa para um objeto date.
    
    Args:
        data_str (str): Data no formato de string 'dd/mm/aaaa'
        
    Returns:
        date: Objeto date correspondente ou None se inválido
    """
    if not data_str.strip():
        return None
    try:
        return datetime.strptime(data_str, "%d/%m/%Y").date()
    except ValueError:
        messagebox.showerror("Erro", "Formato de data inválido! Use dd/mm/aaaa")
        return None

def ADD_FUNCIONARIO(entries, tree_funcionarios, funcionario_logado_id):
    """
    Adiciona um novo funcionário ao sistema com validações e tratamento de dados.
    
    Args:
        entries (dict): Dicionário com os campos do formulário
        tree_funcionarios (ttk.Treeview): Componente de tabela para exibição
        funcionario_logado_id (int): ID do funcionário logado (para auditoria)
    """
    conn = None
    cursor = None
    try:
        # Validação de campos obrigatórios
        required_fields = ["Nome", "Cargo", "Usuário", "Senha", "Permissão"]
        for field in required_fields:
            if not entries[field].get().strip():
                messagebox.showerror("Erro", f"O campo {field} é obrigatório!")
                return
        
        # Verificar unicidade do nome de usuário
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM Funcionario WHERE usuario = %s", 
                      (entries["Usuário"].get(),))
        if cursor.fetchone()[0] > 0:
            messagebox.showerror("Erro", "Nome de usuário já existe!")
            return

        # Conversão de data com tratamento de erro
        data_admissao = converter_data(entries["Data Admissão"].get())
        if data_admissao is None and entries["Data Admissão"].get().strip():
            return

        # Criptografia da senha usando SHA-256
        senha_hash = hashlib.sha256(entries["Senha"].get().encode()).hexdigest()

        # Query para inserir dados básicos do funcionário
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
            senha_hash,
            entries["Permissão"].get(),
            entries["Situação"].get() or 'ativo',  # Default para 'ativo' se vazio
            data_admissao
        )
        cursor.execute(query, valores)
        id_funcionario = cursor.lastrowid  # Obtém o ID do novo registro

        # Inserção de endereço (opcional)
        if any(entries[field].get().strip() for field in ["Rua", "Número", "Bairro", "Cidade", "Estado", "CEP"]):
            query_end = """
            INSERT INTO EnderecoFuncionario (ID_Funcionario, rua, numero, bairro, cidade, estado, cep)
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
        LIMPAR_CAMPOS(entries)
    except Exception as e:
        if conn:
            conn.rollback()  # Reverte em caso de erro
        messagebox.showerror("Erro", f"Falha ao cadastrar: {str(e)}")
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

def DEL_FUNCIONARIO(funcionario_id, tree, funcionario_logado_id):
    """
    Remove um funcionário do sistema com verificações de segurança.
    
    Args:
        funcionario_id (IntVar/StringVar): ID do funcionário a ser removido
        tree (ttk.Treeview): Componente de tabela para atualização
        funcionario_logado_id (int): ID do funcionário logado (para evitar autoexclusão)
    """
    id_func = funcionario_id.get()
    if not id_func:
        messagebox.showwarning("Aviso", "Selecione um funcionário para excluir!")
        return
        
    # Impede que um funcionário exclua a si mesmo
    if int(id_func) == int(funcionario_logado_id):
        messagebox.showerror("Erro", "Você não pode excluir a si mesmo!")
        return
        
    # Confirmação de exclusão
    resposta = messagebox.askyesno("Confirmar", "Deseja realmente excluir este funcionário?")
    if not resposta:
        return
    
    conn = None
    cursor = None
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        # Verificação de último administrador
        cursor.execute("SELECT COUNT(*) FROM Funcionario WHERE permissao = 'admin'")
        if cursor.fetchone()[0] <= 1:
            cursor.execute("SELECT permissao FROM Funcionario WHERE ID_Funcionario = %s", (id_func,))
            if cursor.fetchone()[0] == 'admin':
                messagebox.showerror("Erro", "Não é possível excluir o último administrador!")
                return
        
        # Exclusão em transação (primeiro endereço, depois funcionário)
        cursor.execute("DELETE FROM EnderecoFuncionario WHERE ID_Funcionario = %s", (id_func,))
        cursor.execute("DELETE FROM Funcionario WHERE ID_Funcionario = %s", (id_func,))
        
        conn.commit()
        messagebox.showinfo("Sucesso", "Funcionário excluído com sucesso!")
        UPD_TABELA_FUNCIONARIO(tree)
        
    except Exception as e:
        if conn:
            conn.rollback()
        messagebox.showerror("Erro", f"Falha ao excluir: {str(e)}")
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

def UPD_FUNCIONARIO(entries, funcionario_id, tree, funcionario_logado_id):
    """
    Atualiza os dados de um funcionário existente com validações.
    
    Args:
        entries (dict): Campos do formulário com novos valores
        funcionario_id (IntVar/StringVar): ID do funcionário sendo editado
        tree (ttk.Treeview): Tabela para atualização visual
        funcionario_logado_id (int): ID do funcionário logado (para validações)
    """
    id_func = funcionario_id.get()
    if not id_func:
        messagebox.showwarning("Aviso", "Selecione um funcionário para atualizar!")
        return
        
    conn = None
    cursor = None
    try:
        # Validação de campos obrigatórios
        required_fields = ["Nome", "Cargo", "Usuário", "Permissão"]
        for field in required_fields:
            if not entries[field].get().strip():
                messagebox.showerror("Erro", f"O campo {field} é obrigatório!")
                return
        
        # Validação de auto-alteração de permissões
        if int(id_func) == int(funcionario_logado_id) and entries["Permissão"].get() != 'admin':
            messagebox.showerror("Erro", "Você não pode remover seus próprios privilégios de admin!")
            return
        
        # Conversão de data de admissão
        data_admissao = converter_data(entries["Data Admissão"].get())
        if data_admissao is None and entries["Data Admissão"].get().strip():
            return

        conn = get_connection()
        cursor = conn.cursor()
        
        # Atualização dos dados básicos
        query = """
        UPDATE Funcionario SET 
            nome = %s,
            cargo = %s,
            telefone = %s,
            email = %s,
            usuario = %s,
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
            entries["Permissão"].get(),
            entries["Situação"].get(),
            data_admissao,
            id_func
        )
        cursor.execute(query, valores)
        
        # Atualização de senha (se foi alterada)
        if entries["Senha"].get():
            senha_hash = hashlib.sha256(entries["Senha"].get().encode()).hexdigest()
            cursor.execute("UPDATE Funcionario SET senha = %s WHERE ID_Funcionario = %s", 
                         (senha_hash, id_func))
        
        # Verificação e atualização de endereço (UPDATE ou INSERT)
        cursor.execute("SELECT COUNT(*) FROM EnderecoFuncionario WHERE ID_Funcionario = %s", (id_func,))
        endereco_existe = cursor.fetchone()[0] > 0
        
        endereco_data = (
            entries["Rua"].get(),
            entries["Número"].get(),
            entries["Bairro"].get(),
            entries["Cidade"].get(),
            entries["Estado"].get(),
            entries["CEP"].get(),
            id_func
        )
        
        if endereco_existe:
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
        else:
            query_end = """
            INSERT INTO EnderecoFuncionario 
                (rua, numero, bairro, cidade, estado, cep, ID_Funcionario)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            """
        
        cursor.execute(query_end, endereco_data)
        conn.commit()
        
        messagebox.showinfo("Sucesso", "Funcionário atualizado com sucesso!")
        UPD_TABELA_FUNCIONARIO(tree)
        LIMPAR_CAMPOS(entries)
        
    except Exception as e:
        if conn:
            conn.rollback()
        messagebox.showerror("Erro", f"Falha ao atualizar: {str(e)}")
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

def UPD_TABELA_FUNCIONARIO(tree):
    """
    Atualiza a tabela de exibição com todos os funcionários cadastrados.
    
    Args:
        tree (ttk.Treeview): Componente de tabela a ser atualizado
    """
    conn = None
    cursor = None
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        
        # Limpeza da tabela atual
        for item in tree.get_children():
            tree.delete(item)
        
        # Consulta com JOIN para obter dados completos
        query = """
        SELECT f.*, 
               CONCAT(e.rua, ', ', e.numero, ', ', e.bairro, ', ', e.cidade, ', ', e.estado) as endereco
        FROM Funcionario f
        LEFT JOIN EnderecoFuncionario e ON f.ID_Funcionario = e.ID_Funcionario
        ORDER BY f.nome
        """
        cursor.execute(query)
        
        # Preenchimento da tabela com formatação
        for func in cursor.fetchall():
            tree.insert("", "end", values=(
                func["ID_Funcionario"],
                func["nome"],
                func["cargo"],
                func["telefone"] or "",  # Tratamento para valores nulos
                func["email"] or "",
                func["usuario"],
                "********",  # Proteção da senha
                func["permissao"],
                func["situacao"],
                func["data_admissao"].strftime("%d/%m/%Y") if func["data_admissao"] else "",
                func["endereco"] or "Endereço não cadastrado"
            ))
            
    except Exception as e:
        messagebox.showerror("Erro", f"Falha ao carregar funcionários: {str(e)}")
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

def UPD_CAMPOS_FUNCIONARIO(entries, funcionario_id, id_func):
    """
    Preenche os campos do formulário com os dados de um funcionário selecionado.
    
    Args:
        entries (dict): Campos do formulário a serem preenchidos
        funcionario_id (IntVar/StringVar): Variável para armazenar o ID
        id_func (int): ID do funcionário a ser carregado
    """
    conn = None
    cursor = None
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        
        # Consulta com LEFT JOIN para obter dados mesmo sem endereço
        query = """
        SELECT f.*, e.* 
        FROM Funcionario f
        LEFT JOIN EnderecoFuncionario e ON f.ID_Funcionario = e.ID_Funcionario
        WHERE f.ID_Funcionario = %s
        """
        cursor.execute(query, (id_func,))
        func = cursor.fetchone()
        
        if func:
            # Mapeamento de campos do formulário para colunas do banco
            fields_map = {
                "Nome": "nome",
                "Cargo": "cargo",
                "Telefone": "telefone",
                "E-mail": "email",
                "Usuário": "usuario",
                "Rua": "rua",
                "Número": "numero",
                "Bairro": "bairro",
                "Cidade": "cidade",
                "Estado": "estado",
                "CEP": "cep"
            }
            
            # Preenchimento automático dos campos
            for field, db_field in fields_map.items():
                entries[field].delete(0, "end")
                entries[field].insert(0, func.get(db_field, ""))
            
            # Preenchimento de comboboxes
            if 'Permissão' in entries:
                entries['Permissão'].set(func.get('permissao', ''))
            if 'Situação' in entries:
                entries['Situação'].set(func.get('situacao', 'ativo'))
            
            # Formatação da data de admissão
            entries["Data Admissão"].delete(0, "end")
            if func.get("data_admissao"):
                entries["Data Admissão"].insert(0, func["data_admissao"].strftime("%d/%m/%Y"))
            
            # Limpeza do campo de senha por segurança
            if "Senha" in entries:
                entries["Senha"].delete(0, "end")
            
            # Atualização do ID no formulário
            if funcionario_id:
                funcionario_id.delete(0, "end")
                funcionario_id.insert(0, str(func["ID_Funcionario"]))
            
    except Exception as e:
        messagebox.showerror("Erro", f"Falha ao carregar dados: {str(e)}")
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

def GET_FUNCIONARIO():
    """
    Obtém lista simplificada de funcionários para comboboxes ou seleções.
    
    Returns:
        list: Tuplas com (ID_Funcionario, nome) ordenados por nome
    """
    conn = None
    cursor = None
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT ID_Funcionario, nome FROM Funcionario ORDER BY nome")
        return cursor.fetchall()
    except Exception as e:
        messagebox.showerror("Erro", f"Falha ao obter lista: {str(e)}")
        return []
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

def UPD_DADOS_FUNCIONARIOS(id_funcionario):
    """
    Obtém dados completos de um funcionário específico.
    
    Args:
        id_funcionario (int): ID do funcionário desejado
        
    Returns:
        dict: Dados do funcionário ou dicionário vazio se erro
    """
    conn = None
    cursor = None
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        
        query = """
        SELECT f.*, e.* 
        FROM Funcionario f
        LEFT JOIN EnderecoFuncionario e ON f.ID_Funcionario = e.ID_Funcionario
        WHERE f.ID_Funcionario = %s
        """
        cursor.execute(query, (id_funcionario,))
        return cursor.fetchone() or {}
    except Exception as e:
        messagebox.showerror("Erro", f"Falha ao obter dados: {str(e)}")
        return {}
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

def LIMPAR_CAMPOS(entries):
    """
    Limpa todos os campos de entrada do formulário.
    
    Args:
        entries (dict): Dicionário com referências aos campos
    """
    for entry in entries.values():
        entry.delete(0, "end")