from datetime import date
from models.livro import Livro
from models.usuario import Usuario
from models.emprestimo import Emprestimo
from exceptions.erros import (
    LivroIndisponivelError,
    UsuarioComMultaError,
    LimiteEmprestimosError,
    RegistroNaoEncontradoError
)


class BibliotecaController:
    def __init__(self, repo_livros, repo_usuarios, repo_emprestimos):
        self.repo_livros = repo_livros
        self.repo_usuarios = repo_usuarios
        self.repo_emprestimos = repo_emprestimos

    # ============================================================
    # CRUD LIVROS
    # ============================================================
    def criar_livro(self, titulo, autor, ano_publicacao):
        livro = Livro(None, titulo, autor, ano_publicacao)
        return self.repo_livros.criar(livro)

    def listar_livros(self):
        return self.repo_livros.listar()

    def atualizar_livro(self, id_livro, **novos_dados):
        livro = self.repo_livros.buscar_por_id(id_livro)
        if not livro:
            raise RegistroNaoEncontradoError("Livro não encontrado.")

        for campo, valor in novos_dados.items():
            setattr(livro, campo, valor)
        return self.repo_livros.atualizar(id_livro, livro)

    def deletar_livro(self, id_livro):
        self.repo_livros.deletar(id_livro)

    # ============================================================
    # CRUD USUÁRIOS
    # ============================================================
    def criar_usuario(self, nome, email):
        usuario = Usuario(None, nome, email)
        return self.repo_usuarios.criar(usuario)

    def listar_usuarios(self):
        return self.repo_usuarios.listar()

    def atualizar_usuario(self, id_usuario, **novos_dados):
        usuario = self.repo_usuarios.buscar_por_id(id_usuario)
        if not usuario:
            raise RegistroNaoEncontradoError("Usuário não encontrado.")

        for campo, valor in novos_dados.items():
            setattr(usuario, campo, valor)
        return self.repo_usuarios.atualizar(id_usuario, usuario)

    def deletar_usuario(self, id_usuario):
        self.repo_usuarios.deletar(id_usuario)

    # ============================================================
    # CRUD EMPRÉSTIMOS
    # ============================================================
    def criar_emprestimo(self, id_usuario, id_livro):
        usuario = self.repo_usuarios.buscar_por_id(id_usuario)
        livro = self.repo_livros.buscar_por_id(id_livro)

        if not usuario or not livro:
            raise RegistroNaoEncontradoError("Usuário ou livro não encontrado.")

        # ===== Validações das regras de negócio =====
        if not livro.disponivel:
            raise LivroIndisponivelError("Este livro não está disponível.")
        if len(usuario.livros_emprestados) >= 3:
            raise LimiteEmprestimosError("Usuário atingiu o limite de empréstimos.")
        if usuario.multa_total > 0:
            raise UsuarioComMultaError("Usuário possui multa pendente.")

        # Cria o empréstimo
        emprestimo = Emprestimo(None, id_usuario, id_livro)
        self.repo_emprestimos.criar(emprestimo)

        # Atualiza status
        livro.disponivel = False
        usuario.livros_emprestados.append(id_livro)

        self.repo_livros.atualizar(id_livro, livro)
        self.repo_usuarios.atualizar(id_usuario, usuario)

        return emprestimo

    def finalizar_emprestimo(self, id_emprestimo):
        emprestimo = self.repo_emprestimos.buscar_por_id(id_emprestimo)
        if not emprestimo:
            raise RegistroNaoEncontradoError("Empréstimo não encontrado.")

        usuario = self.repo_usuarios.buscar_por_id(emprestimo.id_usuario)
        livro = self.repo_livros.buscar_por_id(emprestimo.id_livro)

        # Calcula multa se houver atraso
        dias_atraso = (date.today() - emprestimo.data_emprestimo).days - 7
        if dias_atraso > 0:
            multa = dias_atraso * 2.0
            usuario.multa_total += multa

        # Atualiza status
        emprestimo.status = "Finalizado"
        emprestimo.data_devolucao = date.today()
        livro.disponivel = True

        # Remove o livro da lista do usuário
        if livro.id in usuario.livros_emprestados:
            usuario.livros_emprestados.remove(livro.id)

        # Atualiza repositórios
        self.repo_livros.atualizar(livro.id, livro)
        self.repo_usuarios.atualizar(usuario.id, usuario)
        self.repo_emprestimos.atualizar(emprestimo.id, emprestimo)

        return emprestimo

    def listar_emprestimos(self):
        return self.repo_emprestimos.listar()

    # ============================================================
    # CONSULTAS E FILTROS
    # ============================================================
    def buscar_livros(self, titulo=None, autor=None, disponivel=None):
        livros = self.repo_livros.listar()
        resultados = livros

        if titulo:
            resultados = [l for l in resultados if titulo.lower() in l.titulo.lower()]
        if autor:
            resultados = [l for l in resultados if autor.lower() in l.autor.lower()]
        if disponivel is not None:
            resultados = [l for l in resultados if l.disponivel == disponivel]

        return resultados

    def listar_emprestimos_por_usuario(self, id_usuario, status=None):
        emprestimos = self.repo_emprestimos.listar()
        filtrados = [e for e in emprestimos if e.id_usuario == id_usuario]

        if status:
            filtrados = [e for e in filtrados if e.status.lower() == status.lower()]

        return filtrados
