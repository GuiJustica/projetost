import pytest
from unittest.mock import MagicMock
from src.controllers.biblioteca_controller import BibliotecaController

@pytest.fixture
def biblioteca_vazia() -> BibliotecaController:
    repo_livros = MagicMock()
    repo_usuarios = MagicMock()
    repo_emprestimos = MagicMock()
    return BibliotecaController(repo_livros, repo_usuarios, repo_emprestimos)
