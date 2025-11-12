# tests/type_specific/test_performance.py
import pytest
from src.controllers.biblioteca_controller import BibliotecaController
from src.models.usuario import Usuario
from src.models.livro import Livro


@pytest.fixture
def controller():
    return BibliotecaController()

@pytest.mark.benchmark(group="emprestimos")
def test_emprestimos_em_massa(benchmark, controller):
    # criar 1000 usuários e 1000 livros
    usuarios = [controller.usuarios_repo.adicionar(Usuario(f"U{i}")) for i in range(100)]
    livros = [controller.livros_repo.adicionar(Livro(f"L{i}", "Autor", 2000)) for i in range(100)]

    def emprestar_tudo():
        for u, l in zip(usuarios, livros):
            try:
                controller.emprestar_livro(u.id, l.id)
            except ValueError:
                pass

    benchmark(emprestar_tudo)
