import tkinter as tk
from tkinter import ttk

# Dados iniciais (lista de dicionários)
dados = [
    {"id": 1, "nome": "João", "idade": 25},
    {"id": 2, "nome": "Maria", "idade": 30},
    {"id": 3, "nome": "Pedro", "idade": 22},
    {"id": 4, "nome": "Ana", "idade": 28},
]

# Função para criar a tabela na interface gráfica
def create_table():
    # Limpa a tabela antes de adicionar novos dados
    for row in tree.get_children():
        tree.delete(row)

    # Adiciona os dados na tabela
    for item in dados:
        tree.insert('', 'end', values=(item["id"], item["nome"], item["idade"]))

# Função para adicionar um novo registro
def add_record():
    # Adiciona um novo registro à lista de dados
    novo_id = len(dados) + 1
    novo_nome = entry_nome.get()
    nova_idade = int(entry_idade.get())
    dados.append({"id": novo_id, "nome": novo_nome, "idade": nova_idade})

    # Limpa os campos de entrada
    entry_nome.delete(0, tk.END)
    entry_idade.delete(0, tk.END)

    # Atualiza a tabela
    create_table()

# Função para editar um registro
def edit_record(event):
    # Obtém o item selecionado na tabela
    selected_item = tree.selection()[0]
    item_values = tree.item(selected_item, 'values')

    # Cria uma janela de edição
    edit_window = tk.Toplevel(root)
    edit_window.title("Editar Registro")

    # Campos de edição
    tk.Label(edit_window, text="Nome:").grid(row=0, column=0, padx=5, pady=5)
    edit_nome = tk.Entry(edit_window)
    edit_nome.grid(row=0, column=1, padx=5, pady=5)
    edit_nome.insert(0, item_values[1])

    tk.Label(edit_window, text="Idade:").grid(row=1, column=0, padx=5, pady=5)
    edit_idade = tk.Entry(edit_window)
    edit_idade.grid(row=1, column=1, padx=5, pady=5)
    edit_idade.insert(0, item_values[2])

    # Função para salvar as alterações
    def save_changes():
        # Atualiza os dados na lista
        for item in dados:
            if item["id"] == int(item_values[0]):
                item["nome"] = edit_nome.get()
                item["idade"] = int(edit_idade.get())
                break

        # Atualiza a tabela
        create_table()

        # Fecha a janela de edição
        edit_window.destroy()

    # Botão para salvar as alterações
    btn_save = tk.Button(edit_window, text="Salvar", command=save_changes)
    btn_save.grid(row=2, column=0, columnspan=2, pady=10)

# Cria a janela principal
root = tk.Tk()
root.title('Tabela com Edição')

# Cria a tabela (Treeview)
columns = ('id', 'nome', 'idade')
tree = ttk.Treeview(root, columns=columns, show='headings')

# Define os cabeçalhos das colunas
tree.heading('id', text='ID')
tree.heading('nome', text='Nome')
tree.heading('idade', text='Idade')

# Ajusta a largura das colunas
tree.column('id', width=50)
tree.column('nome', width=150)
tree.column('idade', width=100)

# Posiciona a tabela na janela
tree.pack(padx=10, pady=10)

# Adiciona um evento de duplo clique para editar um registro
tree.bind("<Double-1>", edit_record)

# Campos de entrada para adicionar novos registros
frame_input = tk.Frame(root)
frame_input.pack(pady=10)

tk.Label(frame_input, text='Nome:').grid(row=0, column=0, padx=5)
entry_nome = tk.Entry(frame_input)
entry_nome.grid(row=0, column=1, padx=5)

tk.Label(frame_input, text='Idade:').grid(row=0, column=2, padx=5)
entry_idade = tk.Entry(frame_input)
entry_idade.grid(row=0, column=3, padx=5)

btn_add = tk.Button(frame_input, text='Adicionar', command=add_record)
btn_add.grid(row=0, column=4, padx=5)

# Carrega os dados inicialmente
create_table()

# Inicia o loop da interface gráfica
root.mainloop()