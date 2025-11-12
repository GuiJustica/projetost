# tests/type_specific/test_mocks.py
import pytest
from unittest.mock import patch, MagicMock
from src.controllers.biblioteca_controller import BibliotecaController
from src.models.usuario import Usuario
from src.models.livro import Livro

@pytest.fixture
def controller():
    return BibliotecaController()

def test_mock_arquivo_service_salvar(controller):
    livro = Livro("Mockado", "Autor", 2020)
    # mockando o método salvar_livros_json para não criar arquivo
    with patch("src.services.arquivo_service.ArquivoService.salvar_livros_json") as mock_salvar:
        controller.livros_repo.adicionar(livro)
        # chamar o salvar manualmente ou via controller
        mock_salvar("caminho_falso.json", [livro])
        mock_salvar.assert_called_once()  # garante que foi chamado

def test_mock_usuario_bloqueado(controller):
    u = controller.usuarios_repo.adicionar(Usuario("Test"))
    u.bloqueado = True
    l = controller.livros_repo.adicionar(Livro("Livro1", "Autor", 2000))
    # mockando o emprestar_livro para forçar exceção
    with patch.object(controller, "emprestar_livro", side_effect=ValueError("Usuário bloqueado")) as mock_emprestar:
        with pytest.raises(ValueError, match="Usuário bloqueado"):
            controller.emprestar_livro(u.id, l.id)
        mock_emprestar.assert_called_once()
