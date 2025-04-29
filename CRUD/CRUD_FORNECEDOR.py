from Config import get_connection
import tkinter.messagebox as messagebox
import re

def criar_fornecedor(nome, cnpj, telefone=None, email=None, website=None, cadastrado_por=None,
                    rua=None, numero=None, bairro=None, cidade=None, estado=None, cep=None):
    """Cadastra um novo fornecedor no sistema com endereço"""
    conn = None
    cursor = None
    try:
        # Validações básicas
        if not all([nome, cnpj]):
            raise ValueError("Nome e CNPJ são obrigatórios!")
        
        if not validar_cnpj(cnpj):
            raise ValueError("CNPJ inválido!")
        
        if email and not validar_email(email):
            raise ValueError("E-mail inválido!")
        
        conn = get_connection()
        if not conn:
            raise Exception("Não foi possível conectar ao banco de dados")
        
        cursor = conn.cursor()
        
        # Iniciar transação
        conn.start_transaction()
        
        # Inserir fornecedor
        query_forn = """
        INSERT INTO Fornecedor 
            (NM_Fornecedor, CNPJ, telefone, email, website, cadastrado_por) 
        VALUES (%s, %s, %s, %s, %s, %s)
        """
        cursor.execute(query_forn, (nome, cnpj, telefone, email, website, cadastrado_por))
        
        # Obter ID do novo fornecedor
        id_fornecedor = cursor.lastrowid
        
        # Inserir endereço se fornecido
        if any([rua, numero, bairro, cidade, estado, cep]):
            query_end = """
            INSERT INTO EnderecoFornecedor 
                (ID_Fornecedor, rua, numero, bairro, cidade, estado, cep) 
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            """
            cursor.execute(query_end, (id_fornecedor, rua, numero, bairro, cidade, estado, cep))
        
        # Confirmar transação
        conn.commit()
        
        return id_fornecedor
        
    except Exception as e:
        if conn:
            conn.rollback()
        messagebox.showerror("Erro", f"Falha ao cadastrar: {str(e)}")
        return None
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

def listar_fornecedores():
    """Retorna todos os fornecedores com seus endereços"""
    conn = None
    cursor = None
    try:
        conn = get_connection()
        if not conn:
            raise Exception("Não foi possível conectar ao banco de dados")
        
        cursor = conn.cursor(dictionary=True)
        
        query = """
        SELECT 
            f.ID_Fornecedor, f.NM_Fornecedor, f.CNPJ, f.telefone, f.email, f.website,
            e.rua, e.numero, e.bairro, e.cidade, e.estado, e.cep,
            e.ID_EnderecoForn
        FROM Fornecedor f
        LEFT JOIN EnderecoFornecedor e ON f.ID_Fornecedor = e.ID_Fornecedor
        ORDER BY f.NM_Fornecedor
        """
        cursor.execute(query)
        return cursor.fetchall()
        
    except Exception as e:
        messagebox.showerror("Erro", f"Falha ao listar fornecedores: {str(e)}")
        return []
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

def atualizar_fornecedor(id_fornecedor, dados_forn, dados_endereco=None):
    """Atualiza os dados de um fornecedor e seu endereço"""
    conn = None
    cursor = None
    try:
        conn = get_connection()
        if not conn:
            raise Exception("Não foi possível conectar ao banco de dados")
        
        cursor = conn.cursor()
        
        # Iniciar transação
        conn.start_transaction()
        
        # Atualizar dados do fornecedor
        if dados_forn:
            campos = []
            valores = []
            
            if 'NM_Fornecedor' in dados_forn:
                campos.append("NM_Fornecedor = %s")
                valores.append(dados_forn['NM_Fornecedor'])
            if 'CNPJ' in dados_forn:
                if not validar_cnpj(dados_forn['CNPJ']):
                    raise ValueError("CNPJ inválido!")
                campos.append("CNPJ = %s")
                valores.append(dados_forn['CNPJ'])
            if 'telefone' in dados_forn:
                campos.append("telefone = %s")
                valores.append(dados_forn['telefone'])
            if 'email' in dados_forn:
                if dados_forn['email'] and not validar_email(dados_forn['email']):
                    raise ValueError("E-mail inválido!")
                campos.append("email = %s")
                valores.append(dados_forn['email'])
            if 'website' in dados_forn:
                campos.append("website = %s")
                valores.append(dados_forn['website'])
            
            if campos:
                query = f"UPDATE Fornecedor SET {', '.join(campos)} WHERE ID_Fornecedor = %s"
                valores.append(id_fornecedor)
                cursor.execute(query, valores)
        
        # Atualizar endereço
        if dados_endereco:
            # Verificar se já existe endereço
            cursor.execute("SELECT ID_EnderecoForn FROM EnderecoFornecedor WHERE ID_Fornecedor = %s", 
                          (id_fornecedor,))
            existe_endereco = cursor.fetchone()
            
            if existe_endereco:
                # Atualizar endereço existente
                query = """
                UPDATE EnderecoFornecedor 
                SET rua = %s, numero = %s, bairro = %s, cidade = %s, estado = %s, cep = %s
                WHERE ID_Fornecedor = %s
                """
                cursor.execute(query, (
                    dados_endereco.get('rua'),
                    dados_endereco.get('numero'),
                    dados_endereco.get('bairro'),
                    dados_endereco.get('cidade'),
                    dados_endereco.get('estado'),
                    dados_endereco.get('cep'),
                    id_fornecedor
                ))
            else:
                # Inserir novo endereço
                query = """
                INSERT INTO EnderecoFornecedor 
                    (ID_Fornecedor, rua, numero, bairro, cidade, estado, cep) 
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                """
                cursor.execute(query, (
                    id_fornecedor,
                    dados_endereco.get('rua'),
                    dados_endereco.get('numero'),
                    dados_endereco.get('bairro'),
                    dados_endereco.get('cidade'),
                    dados_endereco.get('estado'),
                    dados_endereco.get('cep')
                ))
        
        # Confirmar transação
        conn.commit()
        return True
        
    except Exception as e:
        if conn:
            conn.rollback()
        messagebox.showerror("Erro", f"Falha ao atualizar: {str(e)}")
        return False
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

def deletar_fornecedor(id_fornecedor):
    """Remove um fornecedor do sistema"""
    conn = None
    cursor = None
    try:
        conn = get_connection()
        if not conn:
            raise Exception("Não foi possível conectar ao banco de dados")
        
        cursor = conn.cursor()
        
        # Iniciar transação
        conn.start_transaction()
        
        # Primeiro verificar se há injetoras associadas
        cursor.execute("SELECT COUNT(*) FROM Injetora WHERE ID_Fornecedor = %s", (id_fornecedor,))
        if cursor.fetchone()[0] > 0:
            raise Exception("Não é possível excluir fornecedor com injetoras cadastradas!")
        
        # Depois deleta o endereço
        cursor.execute("DELETE FROM EnderecoFornecedor WHERE ID_Fornecedor = %s", (id_fornecedor,))
        
        # Finalmente deleta o fornecedor
        cursor.execute("DELETE FROM Fornecedor WHERE ID_Fornecedor = %s", (id_fornecedor,))
        
        # Confirmar transação
        conn.commit()
        return True
        
    except Exception as e:
        if conn:
            conn.rollback()
        messagebox.showerror("Erro", f"Falha ao excluir: {str(e)}")
        return False
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

def buscar_fornecedor_por_id(id_fornecedor):
    """Retorna um fornecedor específico com seu endereço"""
    conn = None
    cursor = None
    try:
        conn = get_connection()
        if not conn:
            raise Exception("Não foi possível conectar ao banco de dados")
        
        cursor = conn.cursor(dictionary=True)
        
        query = """
        SELECT 
            f.ID_Fornecedor, f.NM_Fornecedor, f.CNPJ, f.telefone, f.email, f.website,
            e.rua, e.numero, e.bairro, e.cidade, e.estado, e.cep,
            e.ID_EnderecoForn
        FROM Fornecedor f
        LEFT JOIN EnderecoFornecedor e ON f.ID_Fornecedor = e.ID_Fornecedor
        WHERE f.ID_Fornecedor = %s
        """
        cursor.execute(query, (id_fornecedor,))
        return cursor.fetchone()
        
    except Exception as e:
        messagebox.showerror("Erro", f"Falha ao buscar fornecedor: {str(e)}")
        return None
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

def validar_cnpj(cnpj):
    """Valida o formato de um CNPJ (formato básico)"""
    if not cnpj:
        return False
    # Remove caracteres não numéricos
    cnpj = ''.join(filter(str.isdigit, cnpj))
    return len(cnpj) == 14

def validar_email(email):
    """Valida o formato de um e-mail"""
    if not email:
        return True
    regex = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return re.match(regex, email) is not None

# Funções para integração com a interface gráfica
def carregar_fornecedores_na_tabela(tabela):
    """Carrega todos os fornecedores em uma tabela tkinter"""
    for row in tabela.get_children():
        tabela.delete(row)
    
    fornecedores = listar_fornecedores()
    for forn in fornecedores:
        # Formatar endereço
        endereco = ""
        if forn['rua']:
            endereco = f"{forn['rua']}, {forn['numero']}" 
            if forn['bairro']:
                endereco += f" - {forn['bairro']}"
            if forn['cidade']:
                endereco += f", {forn['cidade']}/{forn['estado']}"
        
        tabela.insert("", "end", values=(
            forn['ID_Fornecedor'],
            forn['NM_Fornecedor'],
            forn['CNPJ'],
            forn['telefone'] or "",
            forn['email'] or "",
            forn['website'] or "",
            endereco
        ))

def salvar_fornecedor_gui(entries, endereco_entries, id_entry=None, tabela=None, funcionario_logado_id=None):
    """Salva/atualiza um fornecedor a partir dos dados da interface"""
    # Dados básicos
    dados = {
        'NM_Fornecedor': entries['Nome'].get(),
        'CNPJ': entries['CNPJ'].get(),
        'telefone': entries['Telefone'].get(),
        'email': entries['E-mail'].get(),
        'website': entries['Website'].get(),
    }
    
    # Dados de endereço
    endereco = {
        'rua': endereco_entries['Rua'].get(),
        'numero': endereco_entries['Número'].get(),
        'bairro': endereco_entries['Bairro'].get(),
        'cidade': endereco_entries['Cidade'].get(),
        'estado': endereco_entries['Estado'].get(),
        'cep': endereco_entries['CEP'].get()
    }
    
    # Validação obrigatória
    campos_obrigatorios = ['NM_Fornecedor', 'CNPJ']
    for campo in campos_obrigatorios:
        if not dados[campo]:
            messagebox.showerror("Erro", f"O campo {campo.replace('_', ' ')} é obrigatório!")
            return False
    
    if id_entry and id_entry.get():  # Atualização
        id_forn = int(id_entry.get())
        sucesso = atualizar_fornecedor(id_forn, dados, endereco)
        if sucesso:
            messagebox.showinfo("Sucesso", "Fornecedor atualizado com sucesso!")
            if tabela:
                carregar_fornecedores_na_tabela(tabela)
            return True
    else:  # Cadastro novo
        id_forn = criar_fornecedor(**dados, **endereco, cadastrado_por=funcionario_logado_id)
        if id_forn:
            messagebox.showinfo("Sucesso", "Fornecedor cadastrado com sucesso!")
            if tabela:
                carregar_fornecedores_na_tabela(tabela)
            return True
    
    return False

def preencher_campos_fornecedor(entries, endereco_entries, id_entry, id_fornecedor):
    """Preenche os campos da interface com os dados de um fornecedor"""
    forn = buscar_fornecedor_por_id(id_fornecedor)
    if not forn:
        messagebox.showerror("Erro", "Fornecedor não encontrado!")
        return
    
    # Dados básicos
    id_entry.delete(0, 'end')
    id_entry.insert(0, str(forn['ID_Fornecedor']))
    
    entries['Nome'].delete(0, 'end')
    entries['Nome'].insert(0, forn['NM_Fornecedor'])
    
    entries['CNPJ'].delete(0, 'end')
    entries['CNPJ'].insert(0, forn['CNPJ'])
    
    entries['Telefone'].delete(0, 'end')
    entries['Telefone'].insert(0, forn['telefone'] or "")
    
    entries['E-mail'].delete(0, 'end')
    entries['E-mail'].insert(0, forn['email'] or "")
    
    entries['Website'].delete(0, 'end')
    entries['Website'].insert(0, forn['website'] or "")
    
    # Endereço
    if 'Rua' in entries:
        entries['Rua'].delete(0, 'end')
        entries['Rua'].insert(0, forn.get('rua', ''))
        
        endereco_entries['Número'].delete(0, 'end')
        endereco_entries['Número'].insert(0, forn['numero'])
        
        endereco_entries['Bairro'].delete(0, 'end')
        endereco_entries['Bairro'].insert(0, forn['bairro'])
        
        endereco_entries['Cidade'].delete(0, 'end')
        endereco_entries['Cidade'].insert(0, forn['cidade'])
        
        endereco_entries['Estado'].delete(0, 'end')
        endereco_entries['Estado'].insert(0, forn['estado'])
        
        endereco_entries['CEP'].delete(0, 'end')
        endereco_entries['CEP'].insert(0, forn['cep'])
    else:
        for entry in endereco_entries.values():
            entry.delete(0, 'end')

def limpar_campos_fornecedor(entries, endereco_entries, id_entry):
    """Limpa todos os campos do formulário"""
    id_entry.delete(0, 'end')
    for entry in entries.values():
        if isinstance(entry, ttk.Entry):
            entry.delete(0, 'end')
    
    for entry in endereco_entries.values():
        entry.delete(0, 'end')

def excluir_fornecedor_gui(id_entry, tabela):
    """Exclui um fornecedor após confirmação"""
    if not id_entry.get():
        messagebox.showwarning("Aviso", "Selecione um fornecedor para excluir")
        return
    
    if messagebox.askyesno("Confirmar", "Tem certeza que deseja excluir este fornecedor?"):
        if deletar_fornecedor(int(id_entry.get())):
            messagebox.showinfo("Sucesso", "Fornecedor excluído com sucesso!")
            carregar_fornecedores_na_tabela(tabela)
        else:
            messagebox.showerror("Erro", "Falha ao excluir fornecedor")