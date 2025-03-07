# IMPORTAR AS BIBLIOTECAS
from tkinter import * # Importa todos os módulos do tkinter
from tkinter import messagebox # Importa o modulo de caixas de mensagem do tkinter
from tkinter import ttk # Importa o modulo de widgets tematicos o tkinter
from CRUD_Funcionarios import Database # Importa a classe Database do modulo DataBase
from Tela_ADM import Login_ADM

# CRIAR A JANELA
jan = Tk()  # Criar uma instância da janela principal
jan.title("VP Sytens - Painel de Acesso")  # Define o título da janela
jan.geometry("600x300")  # Define o tamanho da janela
jan.configure(background="white")  # Configura a cor de fundo da janela como branco
jan.resizable(width=False, height=False)  # Impede que a janela seja redimensionada

# TELA TRANSPARENTE
jan.attributes("-alpha", 0.9)  # Define a transparência da janela (0.0 a 1.0)

# IMAGEM
logo = PhotoImage(file="icons/LogoVinicius.png")  # Carrega a imagem da logo

# FRAMES
LeftFrame = Frame(jan, width=200, height=300, bg="white", relief="raise")  # Cria um frame à esquerda com fundo branco
LeftFrame.pack(side=LEFT)  # Posiciona o frame à esquerda

RightFrame = Frame(jan, width=395, height=300, bg="white", relief="raise")  # Cria um frame à direita com fundo branco
RightFrame.pack(side=RIGHT)  # Posiciona o frame à direita

# LOGO
LogoLabel = Label(LeftFrame, image=logo, bg="white")  # Cria uma label que carrega a logo
LogoLabel.place(x=50, y=100)  # Posiciona o label no frame esquerdo

# ADICIONAR CAMPOS DE USUARIO E SENHA
UsuarioLabel = Label(RightFrame, text="Usuario:", font=("Century Gothic", 20), bg="white", fg="black")  # Cria um label para o usuario
UsuarioLabel.place(x=5, y=100)  # Posiciona o label no frame direito

UsuarioEntry = ttk.Entry(RightFrame, width=30)  # Cria um campo de entrada para o usuario
UsuarioEntry.place(x=120, y=115)  # Posiciona o campo de entrada

SenhaLabel = Label(RightFrame, text="Senha:", font=("Century Gothic", 20), bg="white", fg="black")  # Cria um label para a senha
SenhaLabel.place(x=5, y=150)  # Posiciona o label no frame direito

SenhaEntry = ttk.Entry(RightFrame, width=30, show="*")  # Cria um campo de entrada para a senha
SenhaEntry.place(x=120, y=165)  # Posiciona o campo de entrada

# FUNCAO DE LOGIN
def Login():
    usuario = UsuarioEntry.get() # Obtem o valor do campo de entrada 'UsuarioEntry'
    senha = SenhaEntry.get() # Obtem o valor do campo de entrada 'SenhaEntry'

    # Conectar ao banco de dados
    db = Database() # Cria uma instancia da classe Database
    db.cursor.execute("""
    SELECT * FROM funcionario
    WHERE usuario = %s AND senha = %s""",(usuario, senha)) # execulta a consulta SQL para verificar o usuario e a senha
    VerifyLogin = db.cursor.fetchone() # Obtem o resultado da consulta

    # Verificar se o usuario foi encontrado
    if VerifyLogin:
        messagebox.showinfo(title="INFO LOGIN", message="Acesso Confirmado. Bem Vindo!") # Exibe mensagem de sucesso
        # REMOVENDO WIDGETS DE LOGIN
        UsuarioLabel.place(x=5000)  
        UsuarioEntry.place(x=5000)  
        SenhaLabel.place(x=5000) 
        SenhaEntry.place(x=5000) 
        LogoLabel.place(x=5000)
        LoginButton.place(x=5000)
        Login_ADM()
        
    else:
        messagebox.showinfo(title="INFO LOGIN", message="Acesso Negado. Verifique se está cadastrado no Sistema!") # Exibe mensagem de erro

# CRIANDO BOTOES
LoginButton = ttk.Button(RightFrame, text="LOGIN", width=15, command=Login) # Cria um botao de login
LoginButton.place(x=80, y=225) # Posiciona o botao de login

jan.mainloop()

