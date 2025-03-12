import tkinter as tk

# Cria a janela principal
root = tk.Tk()

# Obtém as dimensões da tela
largura_tela = root.winfo_screenwidth()
altura_tela = root.winfo_screenheight()

# Define o tamanho da janela para ocupar toda a tela
root.geometry(f"{largura_tela}x{altura_tela}+0+0")

# Opcional: Remover a maximização da janela (se necessário)
root.resizable(False, False)  # Impede que o usuário redimensione a janela

# Inicia o loop principal da interface gráfica
root.mainloop()