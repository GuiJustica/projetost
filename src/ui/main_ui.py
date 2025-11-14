# src/ui/main_ui.py

import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import customtkinter as ctk
from tkinter import messagebox
from datetime import datetime
import logging
from services.livro_service import LivroService
from services.usuario_service import UsuarioService
from services.emprestimo_service import EmprestimoService
from services.autor_service import AutorService

from dao.database import criar_conexao
from dao.livro_dao import LivroDAO


def safe_strip(value):
    """Garante retorno de string sem erro em .strip()."""
    if value is None:
        return ""
    try:
        return str(value).strip()
    except Exception:
        return ""


class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

        conn = criar_conexao()
        livro_dao = LivroDAO(conn)
        livro_service = LivroService(livro_dao)
        self.title("📚 Sistema de Biblioteca")
        self.geometry("900x600")
        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("pink.json")
        self.autor_service = AutorService()
        self.livro_service = LivroService()
        self.usuario_service = UsuarioService()
        self.emprestimo_service = EmprestimoService(
            usuario_service=self.usuario_service,
            livro_service=self.livro_service
        )

        # ---------------- Layout base ----------------
        self.columnconfigure(1, weight=1)  # direita expande
        self.rowconfigure(0, weight=1)

        # Painel lateral fixo (menu)
        self.sidebar = ctk.CTkFrame(self, width=240, corner_radius=0)
        self.sidebar.grid(row=0, column=0, sticky="nswe")
        self.sidebar.grid_propagate(False)

        ctk.CTkLabel(
            self.sidebar,
            text="📚 Biblioteca",
            font=ctk.CTkFont(size=20, weight="bold")
        ).pack(pady=(30, 20))

        self.btn_home = ctk.CTkButton(
            self.sidebar, text="🏠 Início", width=140, command=self.mostrar_home
        )
        self.btn_home.pack(pady=5)

        self.btn_cad_livros = ctk.CTkButton(
            self.sidebar, text="📖 Livros", width=140, command=self.mostrar_menu_livros
        )
        self.btn_cad_livros.pack(pady=5)


        self.btn_cad_usuarios = ctk.CTkButton(
            self.sidebar, text="👥 Usuários", width=140, command=self.mostrar_menu_usuarios
        )
        self.btn_cad_usuarios.pack(pady=5)

        self.btn_cad_emprestimos = ctk.CTkButton(
            self.sidebar, text="📘 Empréstimos", width=140, command=self.mostrar_menu_emprestimos
        )
        self.btn_cad_emprestimos.pack(pady=5)
        self.btn_cad_autores = ctk.CTkButton(
        self.sidebar, text="✍️ Autores", width=140, command=self.mostrar_menu_autores)
        self.btn_cad_autores.pack(pady=5)


        ctk.CTkButton(
            self.sidebar,
            text="❌ Sair",
            fg_color="#d9534f",
            hover_color="#c9302c",
            width=160,
            command=self.destroy,
        ).pack(side="bottom", pady=20)

        # Frame dinâmico à direita
        self.main_frame = ctk.CTkFrame(self)
        self.main_frame.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)

        self.mostrar_home()



    # ---------------- telas ----------------
    def limpar_main(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()

    def mostrar_home(self):
        self.limpar_main()
        ctk.CTkLabel(
            self.main_frame,
            text="Bem-vindo ao Sistema de Biblioteca!",
            font=ctk.CTkFont(size=22, weight="bold")
        ).pack(pady=40)
        ctk.CTkLabel(
            self.main_frame,
            text="Use o menu à esquerda para gerenciar livros e usuários.",
            font=ctk.CTkFont(size=16)
        ).pack(pady=10)

    # ---------------- LIVROS ----------------
    def mostrar_menu_livros(self):
        self.limpar_main()
        ctk.CTkLabel(
            self.main_frame,
            text="📖 Gerenciar Livros",
            font=ctk.CTkFont(size=20, weight="bold"),
        ).pack(pady=20)

        # Entradas para novo livro
        titulo_entry = self._entrada_com_label("Título:", self.main_frame)
        autor_entry = self._entrada_com_label("Autor:", self.main_frame)
        ano_entry = self._entrada_com_label("Ano de Publicação:", self.main_frame)

        lista_frame = ctk.CTkFrame(self.main_frame,fg_color="white")
        lista_frame.pack(fill="both", expand=True, pady=(10, 0))

        def atualizar_lista_livros():
            for widget in lista_frame.winfo_children():
                widget.destroy()

            livros = self.livro_service.listar_livros()
            self.livro_vars_check = {}
            for l in livros:
                var = ctk.BooleanVar()
                cb = ctk.CTkCheckBox(lista_frame, text=f"[{l.id}] {l.titulo} — {l.autor}", variable=var)
                cb.pack(anchor="w", padx=5, pady=2)
                self.livro_vars_check[l.id] = (var, l)

        atualizar_lista_livros()

        # Botões para gerenciar livros
        def cadastrar_livro():
            try:
                titulo = safe_strip(titulo_entry.get())
                autor = safe_strip(autor_entry.get())
                ano_txt = safe_strip(ano_entry.get())

                if not titulo or not autor or not ano_txt:
                    raise ValueError("Preencha todos os campos.")

                try:
                    ano = int(ano_txt)
                except ValueError:
                    raise ValueError("Ano deve ser número inteiro.")

                ano_atual = datetime.now().year
                if ano <= 0 or ano > ano_atual:
                    raise ValueError(f"Ano inválido (1 - {ano_atual}).")

                self.livro_service.criar_livro(titulo, autor, ano)
                messagebox.showinfo("Sucesso", f"Livro '{titulo}' cadastrado!")
                titulo_entry.delete(0, "end")
                autor_entry.delete(0, "end")
                ano_entry.delete(0, "end")
                atualizar_lista_livros()
            except Exception as e:
                messagebox.showerror("Erro", str(e))
        def remover_livros_selecionados():
            removidos = 0
            for l_id, (var, livro) in self.livro_vars_check.items():
                if var.get():
                    self.livro_service.remover_livro(livro.id)  # <-- passar id
                    removidos += 1
            if removidos:
                messagebox.showinfo("Sucesso", f"{removidos} livro(s) removido(s)!")
            else:
                messagebox.showwarning("Aviso", "Nenhum livro selecionado.")
            atualizar_lista_livros()

        def atualizar_livro_selecionado():
            for l_id, (var, livro) in self.livro_vars_check.items():
                if var.get():
                    from tkinter.simpledialog import askstring, askinteger
                    novo_titulo = askstring("Atualizar Livro", "Título:", initialvalue=livro.titulo)
                    novo_autor = askstring("Atualizar Livro", "Autor:", initialvalue=livro.autor)
                    novo_ano = askinteger("Atualizar Livro", "Ano:", initialvalue=livro.ano_publicacao)
                    if novo_titulo and novo_autor and novo_ano:
                        self.livro_service.atualizar_livro(livro.id, novo_titulo, novo_autor, novo_ano)  # <-- passar os valores
                        messagebox.showinfo("Sucesso", f"Livro [{livro.id}] atualizado!")
            atualizar_lista_livros()

        ctk.CTkButton(self.main_frame, text="Cadastrar Livro", command=cadastrar_livro).pack(pady=5)
        ctk.CTkButton(self.main_frame, text="Remover Livros Selecionados", command=remover_livros_selecionados).pack(pady=5)
        ctk.CTkButton(self.main_frame, text="Atualizar Livro Selecionado", command=atualizar_livro_selecionado).pack(pady=5)

    # ---------------- USUÁRIOS ----------------

    def mostrar_menu_usuarios(self):
        self.limpar_main()
        ctk.CTkLabel(
            self.main_frame,
            text="👥 Gerenciar Usuários",
            font=ctk.CTkFont(size=20, weight="bold"),
        ).pack(pady=20)

        nome_entry = self._entrada_com_label("Nome:", self.main_frame)

        lista_frame = ctk.CTkFrame(self.main_frame,fg_color="white")
        lista_frame.pack(fill="both", expand=True, pady=(10, 0))

        def atualizar_lista_usuarios():
            for widget in lista_frame.winfo_children():
                widget.destroy()

            usuarios = self.usuario_service.listar_usuarios()
            self.usuario_vars_check = {}
            for u in usuarios:
                var = ctk.BooleanVar()
                cb = ctk.CTkCheckBox(lista_frame, text=f"[{u.id}] {u.nome}", variable=var)
                cb.pack(anchor="w", padx=5, pady=2)
                self.usuario_vars_check[u.id] = (var, u)

        atualizar_lista_usuarios()

        # Botões
        def cadastrar_usuario():
            nome = safe_strip(nome_entry.get())
            if not nome:
                messagebox.showerror("Erro", "Preencha o nome do usuário.")
                return
            self.usuario_service.criar_usuario(nome)
            messagebox.showinfo("Sucesso", f"Usuário '{nome}' cadastrado!")
            nome_entry.delete(0, "end")
            atualizar_lista_usuarios()

        def remover_usuarios_selecionados():
            removidos = 0
            for u_id, (var, usuario) in self.usuario_vars_check.items():
                if var.get():
                    self.usuario_service.remover_usuario(usuario.id)
                    removidos += 1
            if removidos:
                messagebox.showinfo("Sucesso", f"{removidos} usuário(s) removido(s)!")
            else:
                messagebox.showwarning("Aviso", "Nenhum usuário selecionado.")
            atualizar_lista_usuarios()

        def atualizar_usuario_selecionado():
            for u_id, (var, usuario) in self.usuario_vars_check.items():
                if var.get():
                    from tkinter.simpledialog import askstring
                    novo_nome = askstring("Atualizar Usuário", "Nome:", initialvalue=usuario.nome)
                    if novo_nome:
                        # Chama com ID e novo nome
                        self.usuario_service.atualizar_usuario(usuario.id, novo_nome)
                        messagebox.showinfo("Sucesso", f"Usuário [{usuario.id}] atualizado!")
            atualizar_lista_usuarios()

        ctk.CTkButton(self.main_frame, text="Cadastrar Usuário", command=cadastrar_usuario).pack(pady=5)
        ctk.CTkButton(self.main_frame, text="Remover Usuários Selecionados", command=remover_usuarios_selecionados).pack(pady=5)
        ctk.CTkButton(self.main_frame, text="Atualizar Usuário Selecionado", command=atualizar_usuario_selecionado).pack(pady=5)

        # ---------------- Empréstimo ----------------
    def mostrar_menu_emprestimos(self):
        self.limpar_main()

        # Título
        ctk.CTkLabel(
            self.main_frame,
            text="📘 Gerenciar Empréstimos",
            font=ctk.CTkFont(size=20, weight="bold"),
        ).pack(pady=20)

        # Inicializa conjuntos de selecionados
        self.usuarios_selecionados = set()
        self.livros_selecionados = set()

        # Frames laterais
        selecao_frame = ctk.CTkFrame(self.main_frame)
        selecao_frame.pack(fill="both", expand=True, padx=10, pady=10)
        selecao_frame.columnconfigure(0, weight=1)
        selecao_frame.columnconfigure(1, weight=1)

        # --------- Usuários ---------
        usuarios_frame = ctk.CTkFrame(selecao_frame)
        usuarios_frame.grid(row=0, column=0, sticky="nsew", padx=(0, 5))
        ctk.CTkLabel(
            usuarios_frame,
            text="👥 Usuários",
            font=ctk.CTkFont(size=16, weight="bold")
        ).pack(pady=10)
        self.lista_usuarios_box = usuarios_frame

        # --------- Livros ---------
        livros_frame = ctk.CTkFrame(selecao_frame)
        livros_frame.grid(row=0, column=1, sticky="nsew", padx=(5, 0))
        ctk.CTkLabel(
            livros_frame,
            text="📚 Livros Disponíveis",
            font=ctk.CTkFont(size=16, weight="bold")
        ).pack(pady=10)
        self.lista_livros_box = livros_frame

        # --------- Empréstimos Ativos ---------
        ativos_frame = ctk.CTkFrame(self.main_frame)
        ativos_frame.pack(fill="both", expand=True, padx=10, pady=10)
        ctk.CTkLabel(
            ativos_frame,
            text="📌 Empréstimos Ativos",
            font=ctk.CTkFont(size=16, weight="bold")
        ).pack(pady=5)
        self.lista_emprestimos_box = ctk.CTkFrame(ativos_frame)
        self.lista_emprestimos_box.pack(fill="both", expand=True, padx=8, pady=8)

        # ---------------- Função de atualização ----------------
        def atualizar_listas_emprestimo():
            # Limpa frames
            for widget in self.lista_usuarios_box.winfo_children()[1:]:
                widget.destroy()
            for widget in self.lista_livros_box.winfo_children()[1:]:
                widget.destroy()
            for widget in self.lista_emprestimos_box.winfo_children():
                widget.destroy()

            try:
                usuarios = self.usuario_service.listar_usuarios()
                livros = [l for l in self.livro_service.listar_livros() if l.disponivel]
                emprestimos = self.emprestimo_service.listar_emprestimos()
            except Exception:
                usuarios, livros, emprestimos = [], [], []

            # Usuários
            self.usuario_vars = {}
            for u in usuarios:
                var = ctk.BooleanVar()
                from functools import partial
                cb = ctk.CTkCheckBox(
                    self.lista_usuarios_box,
                    text=f"[{u.id}] {u.nome}",
                    variable=var,
                    command=partial(self._selecionar_usuario_unico, u.id)
                )
                cb.pack(anchor="w", padx=5, pady=2)
                self.usuario_vars[u.id] = var

            # Livros
            self.livro_vars = {}
            for l in livros:
                var = ctk.BooleanVar()
                cb = ctk.CTkCheckBox(
                    self.lista_livros_box,
                    text=f"[{l.id}] {l.titulo} — {l.autor}",
                    variable=var,
                    command=partial(self._selecionar_livro_unico, l.id)
                )
                cb.pack(anchor="w", padx=5, pady=2)
                self.livro_vars[l.id] = var

            # Empréstimos ativos com checkboxes
            self.emprestimo_vars = {}
            for e in emprestimos:
                var = ctk.BooleanVar()
                usuario_nome = getattr(e.usuario, "nome", str(e.usuario))
                livro_titulo = getattr(e.livro, "titulo", str(e.livro))
                cb = ctk.CTkCheckBox(
                    self.lista_emprestimos_box,
                    text=f"[{e.id}] Usuário: {usuario_nome} — Livro: {livro_titulo}",
                    variable=var
                )
                cb.pack(anchor="w", padx=5, pady=2)
                self.emprestimo_vars[e.id] = (var, e)

        # ---------- Botões ----------
        btn_frame = ctk.CTkFrame(self.main_frame)
        btn_frame.pack(pady=10)

        # Registrar empréstimo
        def registrar_emprestimo():
            if not self.usuarios_selecionados or not self.livros_selecionados:
                messagebox.showwarning("Atenção", "Selecione ao menos um usuário e um livro.")
                return

            sucesso = 0
            for uid in self.usuarios_selecionados:
                for lid in self.livros_selecionados:
                    try:
                        emprestimo = self.emprestimo_service.criar_emprestimo(uid, lid)
                        if emprestimo:
                            sucesso += 1
                    except Exception:
                        continue

            if sucesso > 0:
                messagebox.showinfo("Sucesso", f"{sucesso} empréstimo(s) registrado(s) com sucesso!")
            else:
                messagebox.showwarning("Aviso", "Não foi possível registrar os empréstimos.")

            self.usuarios_selecionados.clear()
            self.livros_selecionados.clear()
            atualizar_listas_emprestimo()

        # Devolver empréstimos selecionados
        def remover_emprestimos_selecionados():
            devolvidos = 0
            for e_id, (var, emprestimo) in self.emprestimo_vars.items():
                if var.get():
                    self.emprestimo_service.remover_emprestimo(emprestimo.id)
                    devolvidos += 1

            if devolvidos > 0:
                messagebox.showinfo("Sucesso", f"{devolvidos} empréstimo(s) devolvido(s) com sucesso!")
            else:
                messagebox.showwarning("Aviso", "Nenhum empréstimo selecionado para devolução.")

            atualizar_listas_emprestimo()

        ctk.CTkButton(btn_frame, text="Registrar Empréstimo", width=200, command=registrar_emprestimo).pack(pady=5)
        ctk.CTkButton(btn_frame, text="Devolver Empréstimos Selecionados", width=250, command=remover_emprestimos_selecionados).pack(pady=5)

        # Inicializa listas
        atualizar_listas_emprestimo()



    # ---------------- MÉTODOS AUXILIARES ----------------
    def _selecionar_usuario_unico(self, usuario_id):
        if not hasattr(self, "usuarios_selecionados"):
            self.usuarios_selecionados = set()
        if usuario_id in self.usuarios_selecionados:
            self.usuarios_selecionados.remove(usuario_id)
        else:
            self.usuarios_selecionados.add(usuario_id)
        print("Usuários selecionados:", self.usuarios_selecionados)

    def _selecionar_livro_unico(self, livro_id):
        if not hasattr(self, "livros_selecionados"):
            self.livros_selecionados = set()
        if livro_id in self.livros_selecionados:
            self.livros_selecionados.remove(livro_id)
        else:
            self.livros_selecionados.add(livro_id)
        print("Livros selecionados:", self.livros_selecionados)


    # ---------------- ATUALIZAR LISTA DE EMPRÉSTIMOS ----------------
    def atualizar_listas_emprestimo(self):
        """Atualiza checkboxes de usuários, livros disponíveis e lista de empréstimos ativos."""
        try:
            usuarios = self.usuario_service.listar_usuarios()
            livros = [l for l in self.livro_service.listar_livros() if not getattr(l, "emprestado", False)]
            emprestimos = self.emprestimo_service.listar_emprestimos()
        except Exception:
            usuarios, livros, emprestimos = [], [], []

        # Usuários
        for widget in self.lista_usuarios_box.winfo_children():
            widget.destroy()
        self.usuario_vars = {}
        for u in usuarios:
            var = ctk.BooleanVar()
            from functools import partial
            cb = ctk.CTkCheckBox(
                self.lista_usuarios_box,
                text=f"[{u.id}] {u.nome}",
                variable=var,
                command=partial(self._selecionar_usuario_unico, u.id)
            )
            cb.pack(anchor="w")
            self.usuario_vars[u.id] = var

        # Livros
        for widget in self.lista_livros_box.winfo_children():
            widget.destroy()
        self.livro_vars = {}
        for l in livros:
            var = ctk.BooleanVar()
            cb = ctk.CTkCheckBox(self.lista_livros_box, text=f"[{l.id}] {l.titulo} — {l.autor}", variable=var)
            cb.pack(anchor="w")
            self.livro_vars[l.id] = var

        # Empréstimos ativos
        # Emprestimos ativos
        self.lista_emprestimos_box.configure(state="normal")
        self.lista_emprestimos_box.delete("0.0", "end")
        if not emprestimos:
            self.lista_emprestimos_box.insert("0.0", "Nenhum empréstimo ativo.\n")
        else:
            for e in emprestimos:
                # Pega o nome do usuário e o título do livro
                usuario_nome = getattr(e.usuario, "nome", str(e.usuario))
                livro_titulo = getattr(e.livro, "titulo", str(e.livro))
                self.lista_emprestimos_box.insert(
                    "end", f"[{getattr(e,'id','')}] Usuário: {usuario_nome} — Livro: {livro_titulo}\n"
                )
        self.lista_emprestimos_box.configure(state="disabled")



    # ---------------- Autores ----------------
    def mostrar_menu_autores(self):
            self.limpar_main()
            ctk.CTkLabel(
                self.main_frame,
                text="✍️ Gerenciar Autores",
                font=ctk.CTkFont(size=20, weight="bold"),
            ).pack(pady=20)

            nome_entry = self._entrada_com_label("Nome:", self.main_frame)
            descricao_entry = self._entrada_com_label("Descrição:", self.main_frame)

            lista_frame = ctk.CTkFrame(self.main_frame, fg_color="white")
            lista_frame.pack(fill="both", expand=True, pady=(10, 0))

            def atualizar_lista_autores():
                for widget in lista_frame.winfo_children():
                    widget.destroy()

                autores = self.autor_service.listar_autor()
                self.autor_vars_check = {}
                for a in autores:
                    var = ctk.BooleanVar()
                    cb = ctk.CTkCheckBox(lista_frame, text=f"[{a.id}] {a.nome} — {a.descricao}", variable=var)
                    cb.pack(anchor="w", padx=5, pady=2)
                    self.autor_vars_check[a.id] = (var, a)

            atualizar_lista_autores()

            # -------- Botões de ação --------
            def cadastrar_autor():
                nome = safe_strip(nome_entry.get())
                descricao = safe_strip(descricao_entry.get())

                if not nome or not descricao:
                    messagebox.showerror("Erro", "Preencha todos os campos.")
                    return

                try:
                    self.autor_service.criar_autor(nome, descricao)
                    messagebox.showinfo("Sucesso", f"Autor '{nome}' cadastrado!")
                    nome_entry.delete(0, "end")
                    descricao_entry.delete(0, "end")
                    atualizar_lista_autores()
                except Exception as e:
                    messagebox.showerror("Erro", str(e))

            def remover_autores_selecionados():
                removidos = 0
                for a_id, (var, autor) in self.autor_vars_check.items():
                    if var.get():
                        self.autor_service.remover_autor(autor.id)
                        removidos += 1
                if removidos:
                    messagebox.showinfo("Sucesso", f"{removidos} autor(es) removido(s)!")
                else:
                    messagebox.showwarning("Aviso", "Nenhum autor selecionado.")
                atualizar_lista_autores()

            def atualizar_autor_selecionado():
                for a_id, (var, autor) in self.autor_vars_check.items():
                    if var.get():
                        from tkinter.simpledialog import askstring
                        nova_descricao = askstring("Atualizar Autor", "Descrição:", initialvalue=autor.descricao)
                        if nova_descricao:
                            self.autor_service.atualizar_autor(autor.id, nova_descricao)
                            messagebox.showinfo("Sucesso", f"Autor [{autor.id}] atualizado!")
                atualizar_lista_autores()

            # -------- Botões de interface --------
            ctk.CTkButton(self.main_frame, text="Cadastrar Autor", command=cadastrar_autor).pack(pady=5)
            ctk.CTkButton(self.main_frame, text="Remover Autores Selecionados", command=remover_autores_selecionados).pack(pady=5)
            ctk.CTkButton(self.main_frame, text="Atualizar Autor Selecionado", command=atualizar_autor_selecionado).pack(pady=5)




    # ---------------- COMPONENTE AUXILIAR ----------------
    def _entrada_com_label(self, texto, parent):
        frame = ctk.CTkFrame(parent)
        frame.pack(anchor="w", pady=4)
        ctk.CTkLabel(frame, text=texto).pack(anchor="w")
        entry = ctk.CTkEntry(frame, width=300)
        entry.pack(anchor="w", pady=3)
        return entry


if __name__ == "__main__":
    app = App()
    app.mainloop()
