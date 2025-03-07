from tkinter import * 
from tkinter import ttk

def Login_ADM():
    funcionarios = ttk.Button(text="Funcionario", width=15, command=funcionario)
    funcionarios.place(x=80, y=225)

    fornecedores = ttk.Button(text="Fornecedor", width=15, command=fornecedor)
    fornecedores.place(x=200, y=225)

    produtos = ttk.Button(text="Produto", width=15, command=produto)
    produtos.place(x=320, y=225)

def funcionario():
    print("oi")
def fornecedor():
    print("oi")
def produto():
    print("oi")