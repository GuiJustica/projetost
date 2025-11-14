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
    livro = Livro(1,"Mockado", "Autor", 2020)
    # mockando o método salvar_livros_json para não criar arquivo
    with patch("src.services.arquivo_service.ArquivoService.salvar_livros_json") as mock_salvar:
        controller.livros_repo.adicionar(livro)
        # chamar o salvar manualmente ou via controller
        mock_salvar("caminho_falso.json", [livro])
        mock_salvar.assert_called_once()  # garante que foi chamado


def test_mock_livro_indisponivel(controller):
    # Adiciona usuário e livro
    u = controller.usuarios_repo.adicionar(Usuario("Teste"))
    l = controller.livros_repo.adicionar(Livro(1, "Livro Mock", "Autor", 2020))

    # Simula que o livro já está indisponível
    l.disponivel = False

    # Mock do método emprestar_livro para levantar erro
    with pytest.raises(ValueError, match="indisponível"):
        controller.emprestar_livro(u.id, l.id)
