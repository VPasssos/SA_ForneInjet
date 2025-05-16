from tkinter import messagebox
from CONFIG import get_connection

def ADD_FUNCIONARIO(entries, tree_funcionarios):
    pass

def DEL_FUNCIONARIO(funcionario_id, tree):
    pass
def UPD_FUNCIONARIO(entries, funcionario_id, tree):
    pass

def UPD_TABELA_FUNCIONARIO(tree):
    pass

def UPD_CAMPOS_FUNCIONARIO(entries, funcionario_id, id_func):
    pass

def GET_CLIENTES():
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT ID_Cliente, nome FROM Cliente ORDER BY nome")
    clientes = cursor.fetchall()
    
    conn.close()
    return clientes