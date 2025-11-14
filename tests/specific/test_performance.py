# tests/specific/test_performance.py
import pytest
from src.controllers.biblioteca_controller import BibliotecaController
from src.models.usuario import Usuario
from src.models.livro import Livro

@pytest.fixture
def controller():
    return BibliotecaController()

@pytest.mark.benchmark(group="emprestimos")
def test_emprestimos_em_massa(benchmark, controller):
    # Criar 100 usuários e 100 livros
    usuarios = [controller.usuarios_repo.adicionar(Usuario(f"U{i}")) for i in range(100)]
    livros = [controller.livros_repo.adicionar(Livro(i + 1, f"L{i}", "Autor", 2000)) for i in range(100)]

    def emprestar_tudo():
        for u, l in zip(usuarios, livros):
            try:
                # PASSAR OBJETOS DIRETAMENTE
                controller.emprestar_livro(u, l)
            except ValueError:
                pass

    benchmark(emprestar_tudo)
@pytest.mark.benchmark(group="criacao_massa")
def test_criacao_usuarios_livros_em_massa(benchmark):
    def criar_usuarios_livros():
        usuarios = [Usuario(f"User{i}") for i in range(1000)]
        livros = [Livro(i + 1, f"Livro{i}", "Autor", 2000) for i in range(1000)]
        return usuarios, livros

    usuarios, livros = benchmark(criar_usuarios_livros)

    # validação simples
    assert len(usuarios) == 1000
    assert len(livros) == 1000
