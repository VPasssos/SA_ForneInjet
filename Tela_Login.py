# IMPORTAR AS BIBLIOTECAS
import tkinter as tk
from tkinter import * # Importa todos os módulos do tkinter
from tkinter import messagebox # Importa o modulo de caixas de mensagem do tkinter
from tkinter import ttk # Importa o modulo de widgets tematicos o tkinter
from CRUD_Funcionarios import Database # Importa a classe Database do modulo DataBase
from Tela_ADM import TelaAbas

class tela_Login:
    def __init__(self,root):
        self.root = root
        self.root.title("SA ForneInjet - Painel de Acesso")
        self.root.geometry("600x300")
        self.root.configure(background="white")
        self.root.attributes("-alpha", 0.9)  # Define a transparência da janela (0.0 a 1.0)
        self.create_widgets()
    def create_widgets(self):
        # IMAGEM
        self.logo = PhotoImage(file="icons/LogoVinicius.png")  # Carrega a imagem da logo

        # FRAMES
        self.LeftFrame = Frame(self.root, width=200, height=300, bg="white", relief="raise")  # Cria um frame à esquerda com fundo branco
        self.LeftFrame.pack(side=LEFT)  # Posiciona o frame à esquerda

        self.RightFrame = Frame(self.root, width=395, height=300, bg="white", relief="raise")  # Cria um frame à direita com fundo branco
        self.RightFrame.pack(side=RIGHT)  # Posiciona o frame à direita

        # LOGO
        self.LogoLabel = Label(self.LeftFrame,image=self.logo, bg="white")  # Cria uma label que carrega a logo
        self.LogoLabel.place(x=50, y=100)  # Posiciona o label no frame esquerdo

        # ADICIONAR CAMPOS DE USUARIO E SENHA
        self.UsuarioLabel = Label(self.RightFrame, text="Usuario:", font=("Century Gothic", 20), bg="white", fg="black")  # Cria um label para o usuario
        self.UsuarioLabel.place(x=5, y=100)  # Posiciona o label no frame direito

        self.UsuarioEntry = ttk.Entry(self.RightFrame,width=30)  # Cria um campo de entrada para o usuario
        self.UsuarioEntry.place(x=120, y=115)  # Posiciona o campo de entrada

        self.SenhaLabel = Label(self.RightFrame,text="Senha:", font=("Century Gothic", 20), bg="white", fg="black")  # Cria um label para a senha
        self.SenhaLabel.place(x=5, y=150)  # Posiciona o label no frame direito

        self.SenhaEntry = ttk.Entry(self.RightFrame, width=30, show="*")  # Cria um campo de entrada para a senha
        self.SenhaEntry.place(x=120, y=165)  # Posiciona o campo de entrada

        # CRIANDO BOTOES
        self.LoginButton = ttk.Button(self.RightFrame,text="LOGIN", width=15, command=self.Login) # Cria um botao de login
        self.LoginButton.place(x=80, y=225) # Posiciona o botao de login
    
    # FUNCAO DE LOGIN
    
    def Login(self):
        usuario = self.UsuarioEntry.get() # Obtem o valor do campo de entrada 'UsuarioEntry'
        senha = self.SenhaEntry.get() # Obtem o valor do campo de entrada 'SenhaEntry'

        # Conectar ao banco de dados
        db = Database() # Cria uma instancia da classe Database
        db.cursor.execute("""
        SELECT * FROM funcionario
        WHERE usuario = %s AND senha = %s""",(usuario, senha)) # execulta a consulta SQL para verificar o usuario e a senha
        VerifyLogin = db.cursor.fetchone() # Obtem o resultado da consulta

        # Verificar se o usuario foi encontrado
        if VerifyLogin:
            is_admin = VerifyLogin[7]  # Supondo que o índice 3 seja a coluna 'is_admin' na sua tabela
            
            if is_admin != "1":  # Se o usuário for administrador
                messagebox.showinfo(title="INFO LOGIN", message="Acesso Confirmado. Bem-vindo, Administrador!")
                self.UsuarioLabel.place(x=5000)  
                self.UsuarioEntry.place(x=5000)  
                self.SenhaLabel.place(x=5000) 
                self.SenhaEntry.place(x=5000) 
                self.LogoLabel.place(x=5000)
                self.LoginButton.place(x=5000)
                # Chama a função para tela de administrador
                self.root.withdraw()  # Oculta a tela de login
                self.show_main_screen()  # Chama a função para mostrar as abas

            else:
                messagebox.showinfo(title="INFO LOGIN", message="Acesso Confirmado. Bem-vindo, Usuário!")
                # Chama a tela de usuário comum, se necessário
            # REMOVENDO WIDGETS DE LOGIN

            
            
        else:
            messagebox.showinfo(title="INFO LOGIN", message="Acesso Negado. Verifique se está cadastrado no Sistema!") # Exibe mensagem de erro


    def show_main_screen(self):
        main_window = tk.Toplevel()  # Cria uma nova janela
        main_window.geometry("600x400")  # Define o tamanho da nova janela
        app = TelaAbas(main_window)  # Cria a instância da tela com as abas
        main_window.mainloop()
