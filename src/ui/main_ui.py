import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import tkinter as tk
from tkinter import messagebox
from services.livro_service import LivroService
from services.usuario_service import UsuarioService
class App:
    def __init__(self, root):
        self.root = root
        self.root.title("📚 Sistema de Biblioteca")
        self.root.geometry("500x400")

        self.livro_service = LivroService()
        self.usuario_service = UsuarioService()

        self.menu_principal()

    def limpar_tela(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def menu_principal(self):
        self.limpar_tela()
        tk.Label(self.root, text="Sistema de Biblioteca", font=("Arial", 16, "bold")).pack(pady=20)

        tk.Button(self.root, text="📖 Gerenciar Livros", width=25, command=self.menu_livros).pack(pady=10)
        tk.Button(self.root, text="👥 Gerenciar Usuários", width=25, command=self.menu_usuarios).pack(pady=10)
        tk.Button(self.root, text="❌ Sair", width=25, command=self.root.quit).pack(pady=20)

    # ------------------- LIVROS -------------------
    def menu_livros(self):
        self.limpar_tela()
        tk.Label(self.root, text="Gerenciar Livros", font=("Arial", 14, "bold")).pack(pady=10)

        tk.Label(self.root, text="Título:").pack()
        titulo_entry = tk.Entry(self.root, width=40)
        titulo_entry.pack()

        tk.Label(self.root, text="Autor:").pack()
        autor_entry = tk.Entry(self.root, width=40)
        autor_entry.pack()

        tk.Label(self.root, text="Ano de Publicação:").pack()
        ano_entry = tk.Entry(self.root, width=40)
        ano_entry.pack()

        def cadastrar_livro():
            try:
                titulo = titulo_entry.get()
                autor = autor_entry.get()
                ano = int(ano_entry.get())
                self.livro_service.criar_livro(titulo, autor, ano)
                messagebox.showinfo("Sucesso", f"Livro '{titulo}' cadastrado!")
            except Exception as e:
                messagebox.showerror("Erro", str(e))

        tk.Button(self.root, text="Cadastrar Livro", command=cadastrar_livro).pack(pady=5)
        tk.Button(self.root, text="Voltar", command=self.menu_principal).pack(pady=10)

    # ------------------- USUÁRIOS -------------------
    def menu_usuarios(self):
        self.limpar_tela()
        tk.Label(self.root, text="Gerenciar Usuários", font=("Arial", 14, "bold")).pack(pady=10)

        tk.Label(self.root, text="Nome:").pack()
        nome_entry = tk.Entry(self.root, width=40)
        nome_entry.pack()

        tk.Label(self.root, text="Multa:").pack()
        multa_entry = tk.Entry(self.root, width=40)
        multa_entry.pack()

        def cadastrar_usuario():
            try:
                nome = nome_entry.get()
                multa = float(multa_entry.get()) if multa_entry.get() else 0
                self.usuario_service.criar_usuario(nome, multa)
                messagebox.showinfo("Sucesso", f"Usuário '{nome}' cadastrado!")
            except Exception as e:
                messagebox.showerror("Erro", str(e))

        tk.Button(self.root, text="Cadastrar Usuário", command=cadastrar_usuario).pack(pady=5)
        tk.Button(self.root, text="Voltar", command=self.menu_principal).pack(pady=10)


if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
