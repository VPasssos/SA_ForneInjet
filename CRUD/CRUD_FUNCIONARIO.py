import hashlib
from datetime import datetime
from Config import get_connection
import tkinter.messagebox as messagebox
import re

def criar_funcionario(nome, cargo, telefone, email, usuario, senha, 
                     permissao="usuario", situacao="ativo", data_admissao=None, 
                     rua=None, numero=None, bairro=None, cidade=None, estado=None, cep=None):
    """Cadastra um novo funcionário no sistema com endereço"""
    conn = None
    cursor = None
    try:
        # Validações básicas
        if not all([nome, cargo, telefone, usuario, senha]):
            raise ValueError("Preencha todos os campos obrigatórios!")
        
        if email and not validar_email(email):
            raise ValueError("E-mail inválido!")
        
        # Converter data se for string
        if data_admissao and isinstance(data_admissao, str):
            try:
                data_admissao = datetime.strptime(data_admissao, '%d/%m/%Y').date()
            except ValueError:
                raise ValueError("Formato de data inválido! Use DD/MM/AAAA")
        
        # Hash da senha
        senha_hash = hashlib.sha256(senha.encode()).hexdigest()
        
        conn = get_connection()
        if not conn:
            raise Exception("Não foi possível conectar ao banco de dados")
        
        cursor = conn.cursor()
        
        # Iniciar transação
        conn.start_transaction()
        
        # Inserir funcionário
        query_func = """
        INSERT INTO Funcionario 
            (nome, cargo, telefone, email, usuario, senha, permissao, situacao, data_admissao) 
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        cursor.execute(query_func, (nome, cargo, telefone, email, usuario, senha_hash, 
                                  permissao, situacao, data_admissao))
        
        # Obter ID do novo funcionário
        id_funcionario = cursor.lastrowid
        
        # Inserir endereço se fornecido
        if any([rua, numero, bairro, cidade, estado, cep]):
            query_end = """
            INSERT INTO EnderecoFuncionario 
                (ID_Funcionario, rua, numero, bairro, cidade, estado, cep) 
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            """
            cursor.execute(query_end, (id_funcionario, rua, numero, bairro, cidade, estado, cep))
        
        # Confirmar transação
        conn.commit()
        
        return id_funcionario
        
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

def listar_funcionarios():
    """Retorna todos os funcionários com seus endereços"""
    conn = None
    cursor = None
    try:
        conn = get_connection()
        if not conn:
            raise Exception("Não foi possível conectar ao banco de dados")
        
        cursor = conn.cursor(dictionary=True)
        
        query = """
        SELECT 
            f.ID_Funcionario, f.nome, f.cargo, f.telefone, f.email, 
            f.usuario, f.permissao, f.situacao, f.data_admissao,
            e.rua, e.numero, e.bairro, e.cidade, e.estado, e.cep,
            e.ID_EnderecoFunc
        FROM Funcionario f
        LEFT JOIN EnderecoFuncionario e ON f.ID_Funcionario = e.ID_Funcionario
        ORDER BY f.nome
        """
        cursor.execute(query)
        return cursor.fetchall()
        
    except Exception as e:
        messagebox.showerror("Erro", f"Falha ao listar funcionários: {str(e)}")
        return []
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

def atualizar_funcionario(id_funcionario, dados_func, dados_endereco=None):
    """Atualiza os dados de um funcionário e seu endereço"""
    conn = None
    cursor = None
    try:
        conn = get_connection()
        if not conn:
            raise Exception("Não foi possível conectar ao banco de dados")
        
        cursor = conn.cursor()
        
        # Iniciar transação
        conn.start_transaction()
        
        # Atualizar dados do funcionário
        if dados_func:
            campos = []
            valores = []
            
            if 'nome' in dados_func:
                campos.append("nome = %s")
                valores.append(dados_func['nome'])
            if 'cargo' in dados_func:
                campos.append("cargo = %s")
                valores.append(dados_func['cargo'])
            if 'telefone' in dados_func:
                campos.append("telefone = %s")
                valores.append(dados_func['telefone'])
            if 'email' in dados_func:
                if dados_func['email'] and not validar_email(dados_func['email']):
                    raise ValueError("E-mail inválido!")
                campos.append("email = %s")
                valores.append(dados_func['email'])
            if 'usuario' in dados_func:
                campos.append("usuario = %s")
                valores.append(dados_func['usuario'])
            if 'senha' in dados_func and dados_func['senha']:
                senha_hash = hashlib.sha256(dados_func['senha'].encode()).hexdigest()
                campos.append("senha = %s")
                valores.append(senha_hash)
            if 'permissao' in dados_func:
                campos.append("permissao = %s")
                valores.append(dados_func['permissao'])
            if 'situacao' in dados_func:
                campos.append("situacao = %s")
                valores.append(dados_func['situacao'])
            if 'data_admissao' in dados_func:
                if dados_func['data_admissao'] and isinstance(dados_func['data_admissao'], str):
                    try:
                        data = datetime.strptime(dados_func['data_admissao'], '%d/%m/%Y').date()
                        campos.append("data_admissao = %s")
                        valores.append(data)
                    except ValueError:
                        raise ValueError("Formato de data inválido! Use DD/MM/AAAA")
            
            if campos:
                query = f"UPDATE Funcionario SET {', '.join(campos)} WHERE ID_Funcionario = %s"
                valores.append(id_funcionario)
                cursor.execute(query, valores)
        
        # Atualizar endereço
        if dados_endereco:
            # Verificar se já existe endereço
            cursor.execute("SELECT ID_EnderecoFunc FROM EnderecoFuncionario WHERE ID_Funcionario = %s", 
                          (id_funcionario,))
            existe_endereco = cursor.fetchone()
            
            if existe_endereco:
                # Atualizar endereço existente
                query = """
                UPDATE EnderecoFuncionario 
                SET rua = %s, numero = %s, bairro = %s, cidade = %s, estado = %s, cep = %s
                WHERE ID_Funcionario = %s
                """
                cursor.execute(query, (
                    dados_endereco.get('rua'),
                    dados_endereco.get('numero'),
                    dados_endereco.get('bairro'),
                    dados_endereco.get('cidade'),
                    dados_endereco.get('estado'),
                    dados_endereco.get('cep'),
                    id_funcionario
                ))
            else:
                # Inserir novo endereço
                query = """
                INSERT INTO EnderecoFuncionario 
                    (ID_Funcionario, rua, numero, bairro, cidade, estado, cep) 
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                """
                cursor.execute(query, (
                    id_funcionario,
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

def deletar_funcionario(id_funcionario):
    """Remove um funcionário do sistema"""
    conn = None
    cursor = None
    try:
        conn = get_connection()
        if not conn:
            raise Exception("Não foi possível conectar ao banco de dados")
        
        cursor = conn.cursor()
        
        # Iniciar transação
        conn.start_transaction()
        
        # Primeiro deleta o endereço
        cursor.execute("DELETE FROM EnderecoFuncionario WHERE ID_Funcionario = %s", (id_funcionario,))
        
        # Depois deleta o funcionário
        cursor.execute("DELETE FROM Funcionario WHERE ID_Funcionario = %s", (id_funcionario,))
        
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

def buscar_funcionario_por_id(id_funcionario):
    """Retorna um funcionário específico com seu endereço"""
    conn = None
    cursor = None
    try:
        conn = get_connection()
        if not conn:
            raise Exception("Não foi possível conectar ao banco de dados")
        
        cursor = conn.cursor(dictionary=True)
        
        query = """
        SELECT 
            f.ID_Funcionario, f.nome, f.cargo, f.telefone, f.email, 
            f.usuario, f.permissao, f.situacao, f.data_admissao,
            e.rua, e.numero, e.bairro, e.cidade, e.estado, e.cep,
            e.ID_EnderecoFunc
        FROM Funcionario f
        LEFT JOIN EnderecoFuncionario e ON f.ID_Funcionario = e.ID_Funcionario
        WHERE f.ID_Funcionario = %s
        """
        cursor.execute(query, (id_funcionario,))
        return cursor.fetchone()
        
    except Exception as e:
        messagebox.showerror("Erro", f"Falha ao buscar funcionário: {str(e)}")
        return None
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

def validar_email(email):
    """Valida o formato de um e-mail"""
    if not email:
        return True
    regex = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return re.match(regex, email) is not None

# Funções para integração com a interface gráfica
def carregar_funcionarios_na_tabela(tabela):
    """Carrega todos os funcionários em uma tabela tkinter"""
    for row in tabela.get_children():
        tabela.delete(row)
    
    funcionarios = listar_funcionarios()
    for func in funcionarios:
        # Formatar data
        data_adm = func['data_admissao'].strftime('%d/%m/%Y') if func['data_admissao'] else ""
        
        # Formatar endereço
        endereco = ""
        if func['rua']:
            endereco = f"{func['rua']}, {func['numero']}" 
            if func['bairro']:
                endereco += f" - {func['bairro']}"
            if func['cidade']:
                endereco += f", {func['cidade']}/{func['estado']}"
        
        tabela.insert("", "end", values=(
            func['ID_Funcionario'],
            func['nome'],
            func['cargo'],
            func['telefone'],
            func['email'] or "",
            func['usuario'],
            func['permissao'],
            func['situacao'],
            data_adm,
            endereco
        ))

def salvar_funcionario_gui(entries, endereco_entries, id_entry=None, tabela=None):
    """Salva/atualiza um funcionário a partir dos dados da interface"""
    # Dados básicos
    dados = {
        'nome': entries['Nome'].get(),
        'cargo': entries['Cargo'].get(),
        'telefone': entries['Telefone'].get(),
        'email': entries['E-mail'].get(),
        'usuario': entries['Usuário'].get(),
        'senha': entries['Senha'].get(),
        'permissao': entries['Permissão'].get(),
        'situacao': entries['Situação'].get(),
        'data_admissao': entries['Data Admissão'].get() or None
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
    campos_obrigatorios = ['nome', 'cargo', 'telefone', 'usuario']
    for campo in campos_obrigatorios:
        if not dados[campo]:
            messagebox.showerror("Erro", f"O campo {campo.capitalize()} é obrigatório!")
            return False
    
    if id_entry and id_entry.get():  # Atualização
        id_func = int(id_entry.get())
        sucesso = atualizar_funcionario(id_func, dados, endereco)
        if sucesso:
            messagebox.showinfo("Sucesso", "Funcionário atualizado com sucesso!")
            if tabela:
                carregar_funcionarios_na_tabela(tabela)
            return True
    else:  # Cadastro novo
        id_func = criar_funcionario(**dados, **endereco)
        if id_func:
            messagebox.showinfo("Sucesso", "Funcionário cadastrado com sucesso!")
            if tabela:
                carregar_funcionarios_na_tabela(tabela)
            return True
    
    return False

def preencher_campos_funcionario(entries, endereco_entries, id_entry, id_funcionario):
    """Preenche os campos da interface com os dados de um funcionário"""
    func = buscar_funcionario_por_id(id_funcionario)
    if not func:
        messagebox.showerror("Erro", "Funcionário não encontrado!")
        return
    
    # Preencher campos básicos
    id_entry.delete(0, 'end')
    id_entry.insert(0, str(func['ID_Funcionario']))
    
    entries['Nome'].delete(0, 'end')
    entries['Nome'].insert(0, func['nome'])
    
    entries['Cargo'].delete(0, 'end')
    entries['Cargo'].insert(0, func['cargo'])
    
    entries['Telefone'].delete(0, 'end')
    entries['Telefone'].insert(0, func['telefone'])
    
    entries['E-mail'].delete(0, 'end')
    entries['E-mail'].insert(0, func['email'] or "")
    
    entries['Usuário'].delete(0, 'end')
    entries['Usuário'].insert(0, func['usuario'])
    
    entries['Senha'].delete(0, 'end')
    entries['Senha'].insert(0, "")  # Senha não é exibida
    
    if 'Permissão' in entries:
        entries['Permissão'].set(func['permissao'])
    if 'Situação' in entries:
        entries['Situação'].set(func['situacao'])
    
    entries['Data Admissão'].delete(0, 'end')
    entries['Data Admissão'].insert(0, func['data_admissao'].strftime('%d/%m/%Y') 
                                   if func['data_admissao'] else "")
    
    # Endereço
    if func['rua']:
        endereco_entries['Rua'].delete(0, 'end')
        endereco_entries['Rua'].insert(0, func['rua'])
        
        endereco_entries['Número'].delete(0, 'end')
        endereco_entries['Número'].insert(0, func['numero'])
        
        endereco_entries['Bairro'].delete(0, 'end')
        endereco_entries['Bairro'].insert(0, func['bairro'])
        
        endereco_entries['Cidade'].delete(0, 'end')
        endereco_entries['Cidade'].insert(0, func['cidade'])
        
        endereco_entries['Estado'].delete(0, 'end')
        endereco_entries['Estado'].insert(0, func['estado'])
        
        endereco_entries['CEP'].delete(0, 'end')
        endereco_entries['CEP'].insert(0, func['cep'])
    else:
        for entry in endereco_entries.values():
            entry.delete(0, 'end')

def limpar_campos_funcionario(entries, endereco_entries, id_entry):
    """Limpa todos os campos do formulário"""
    id_entry.delete(0, 'end')
    for entry in entries.values():
        if isinstance(entry, ttk.Entry):
            entry.delete(0, 'end')
        elif isinstance(entry, ttk.Combobox):
            entry.set('')
    
    for entry in endereco_entries.values():
        entry.delete(0, 'end')

def excluir_funcionario_gui(id_entry, tabela):
    """Exclui um funcionário após confirmação"""
    if not id_entry.get():
        messagebox.showwarning("Aviso", "Selecione um funcionário para excluir")
        return
    
    if messagebox.askyesno("Confirmar", "Tem certeza que deseja excluir este funcionário?"):
        if deletar_funcionario(int(id_entry.get())):
            messagebox.showinfo("Sucesso", "Funcionário excluído com sucesso!")
            carregar_funcionarios_na_tabela(tabela)
        else:
            messagebox.showerror("Erro", "Falha ao excluir funcionário")

import mysql.connector

class Database:
    def __init__(self):
        self.conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="ForneInjet"  # Corrigido para o nome novo do banco
        )
        self.cursor = self.conn.cursor()  # Cria um cursor para executar comandos SQL
        
        # Corrigido para a nova tabela Funcionario conforme sua estrutura
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS Funcionario (
                ID_Funcionario INT PRIMARY KEY AUTO_INCREMENT,
                nome VARCHAR(100) NOT NULL,
                cargo VARCHAR(50),
                telefone VARCHAR(20),
                email VARCHAR(100) UNIQUE,
                usuario VARCHAR(50) UNIQUE NOT NULL,
                senha VARCHAR(255) NOT NULL,
                permissao VARCHAR(20),
                situacao VARCHAR(20),
                data_admissao DATE
            );
        ''')
        self.conn.commit()  # Confirma criação da tabela
        print("Conectado ao banco de dados")

    def close_connection(self):
        self.conn.close()  # Fecha a conexão com o banco de dados
