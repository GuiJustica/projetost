from src.dao.mock_livro_dao import MockLivroDAO
from src.dao.mock_usuario_dao import MockUsuarioDAO
from src.models.livro import Livro
from src.models.usuario import Usuario

# Teste rápido para MockLivroDAO
livro_dao = MockLivroDAO()
livro_dao.criar(Livro(None, "1984", "George Orwell", 1949))
print("📚 Livros:", livro_dao.listar())

# Teste rápido para MockUsuarioDAO
usuario_dao = MockUsuarioDAO()
usuario_dao.criar(Usuario("Ana"))
print("👤 Usuários:", usuario_dao.listar())
