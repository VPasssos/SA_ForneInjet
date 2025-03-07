# IMPORTAR AS BIBLIOTECAS
from tkinter import * # Importa todos os módulos do tkinter
from tkinter import messagebox # Importa o modulo de caixas de mensagem do tkinter
from tkinter import ttk # Importa o modulo de widgets tematicos o tkinter


# CRIAR A JANELA
jan = Tk() # Criar uma instância da janela principal
jan.title("VP Sytens - Painel de Acesso") # Define o título da janela
jan.geometry("600x300") # Define o tamanho da janela
jan.configure(background="white") # Configura a cor de fundo da janela
jan.resizable(width=False,height=False) # Impede que a janela seja redimensionada

def produtos():
    def voltar():
        Voltar.place(x=50000)
        RegisterButton.place(x=220, y=225)
    RegisterButton.place(x=50000)
    Voltar = ttk.Button(text="VOLTAR", width=15,command=voltar)
    Voltar.place(x=220, y=225)

RegisterButton = ttk.Button(text="Produtos", width=15,command=produtos)
RegisterButton.place(x=220, y=225)

jan.mainloop()