import tkinter as tk
from TELAS.TELA_LOGIN import TelaLogin  # Importando a classe de tela de login

if __name__ == "__main__":
    root = tk.Tk()  # Janela principal
    login_screen = TelaLogin(root)  # Exibe a tela de login
    root.mainloop()  # Inicia o loop da interface gráfica
    