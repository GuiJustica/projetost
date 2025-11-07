from tests.fixtures.mock_usuario_dao import MockUsuarioDAO
from src.models.usuario import Usuario

def test_criar_usuario_mock():
    mock_dao = MockUsuarioDAO()

    usuario = Usuario("Guilherme", 0)
    mock_dao.criar(usuario)

    usuarios = mock_dao.listar()

    assert len(usuarios) == 1
    assert usuarios[0].nome == "Guilherme"
