import tkinter as tk
from login_screen import LoginScreen  # Importando a classe de tela de login

if __name__ == "__main__":
    root = tk.Tk()  # Janela principal
    login_screen = LoginScreen(root)  # Exibe a tela de login
    root.mainloop()  # Inicia o loop da interface gráfica
