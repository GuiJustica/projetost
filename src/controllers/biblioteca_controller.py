from src.models.livro import Livro
from src.models.usuario import Usuario
from src.models.emprestimo import Emprestimo
from src.repositories.livro_repository import LivroRepository
from src.repositories.autor_repository import AutorRepository
from src.repositories.usuario_repository import UsuarioRepository
from src.repositories.emprestimo_repository import EmprestimoRepository
from src.services.arquivo_service import ArquivoService
from datetime import datetime

class BibliotecaController:
    def __init__(self):
        self.livros_repo = LivroRepository()
        self.autor_repo = AutorRepository()
        self.usuarios_repo = UsuarioRepository()
        self.emprestimos_repo = EmprestimoRepository()
        self.arquivo_service = ArquivoService()

    def cadastrar_usuario(self, nome: str) -> Usuario:
        novo_id = self.usuarios_repo.proximo_id  # gera ID baseado no repositório
        usuario = Usuario(novo_id, nome)
        self.usuarios_repo.adicionar(usuario)
        return usuario

    def cadastrar_livro(self, titulo: str, autor: str, ano_publicacao: int = 2024) -> Livro:
        novo_id = self.livros_repo.proximo_id
        livro = Livro(novo_id, titulo, autor, ano_publicacao)
        self.livros_repo.adicionar(livro)
        return livro

    def emprestar_livro(self, usuario_id, livro_id):
        usuario = self.usuarios_repo.buscar_por_id(usuario_id)
        livro = self.livros_repo.buscar_por_id(livro_id)

        if not usuario:
            raise ValueError("Usuário não encontrado.")
        if not livro:
            raise ValueError("Livro não encontrado.")
        if not livro.disponivel:
            raise ValueError("Livro indisponível.")


        livro.disponivel = False
        emprestimo = self.emprestimos_repo.adicionar(Emprestimo(usuario, livro))
        return emprestimo

    def devolver_livro(self, emprestimo_id):
        emprestimo = self.emprestimos_repo.buscar_por_id(emprestimo_id)

        if not emprestimo:
            raise ValueError("Empréstimo não encontrado.")

        emprestimo.devolver()

        livro = self.livros_repo.buscar_por_id(emprestimo.livro.id)
        livro.disponivel = True
        self.livros_repo.atualizar(livro.id, livro)
        return emprestimo

    def listar_livros(self):
        return self.livros_repo.listar()

