import pytest
from unittest.mock import MagicMock
from src.models.livro import Livro
from src.models.usuario import Usuario
from src.models.autor import Autor
from src.models.emprestimo import Emprestimo
from src.services.autor_service import AutorService
from src.services.livro_service import LivroService
from src.services.usuario_service import UsuarioService
from src.services.emprestimo_service import EmprestimoService
from src.controllers.biblioteca_controller import BibliotecaController
from src.repositories.autor_repository import AutorRepository
from src.exceptions.erros import EntradaInvalidaError, LivroDuplicadoError, LivroIndisponivelError

# ======================================================
# 🔧 FIXTURES GERAIS
# ======================================================

@pytest.fixture
def autor_repository():
    autores = []

    mock_repo = MagicMock()

    def criar_autor(autor):
        autores.append(autor)
        return autor

    def listar_autores():
        return [(a.id, a.nome, a.descricao) for a in autores]

    def buscar_por_id(autor_id):
        for a in autores:
            if a.id == autor_id:
                return a
        return None

    def atualizar_autor(autor_id, descricao):
        for a in autores:
            if a.id == autor_id:
                a.descricao = descricao
                return True
        return False

    def remover_autor(autor_id):
        for a in autores:
            if a.id == autor_id:
                autores.remove(a)
                return True
        return False

    mock_repo.criar.side_effect = criar_autor
    mock_repo.listar.side_effect = listar_autores
    mock_repo.buscar_por_id.side_effect = buscar_por_id
    mock_repo.atualizar.side_effect = atualizar_autor
    mock_repo.remover.side_effect = remover_autor
    return mock_repo

@pytest.fixture
def usuario_repository():
    usuarios = []

    mock_repo = MagicMock()

    def criar_usuario(usuario):
        usuarios.append((usuario.id, usuario.nome))
        return usuario

    def listar_usuarios():
        return usuarios

    def buscar_por_id(usuario_id):
        for u in usuarios:
            if u[0] == usuario_id:
                return Usuario(u[1], u[0])
        return None

    mock_repo.criar.side_effect = criar_usuario
    mock_repo.listar.side_effect = listar_usuarios
    mock_repo.buscar_por_id.side_effect = buscar_por_id
    return mock_repo

@pytest.fixture
def livro_repository():
    livros = []

    mock_repo = MagicMock()

    def criar_livro(livro):
        livros.append((livro.id, livro.titulo, livro.autor, livro.ano_publicacao))
        return livro

    def listar_livros():
        return livros

    def buscar_por_id(livro_id):
        for l in livros:
            if l[0] == livro_id:
                return Livro(l[1], l[2], l[3], l[0])
        return None

    mock_repo.criar.side_effect = criar_livro
    mock_repo.listar.side_effect = listar_livros
    mock_repo.buscar_por_id.side_effect = buscar_por_id
    return mock_repo


@pytest.fixture
def emprestimo_repository():
    emprestimos = []

    mock_repo = MagicMock()

    def criar_emprestimo(emprestimo):
        emprestimo.id = len(emprestimos)+1
        emprestimos.append(emprestimo)
        return emprestimo

    def listar_emprestimos():
        return emprestimos

    def buscar_por_id(emprestimo_id):
        for e in emprestimos:
            if e.id == emprestimo_id:
                return e
        return None

    def remover_emprestimo(emprestimo_id):
        for e in emprestimos:
            if e.id == emprestimo_id:
                emprestimos.remove(e)
                return True
        return False

    mock_repo.criar.side_effect = criar_emprestimo
    mock_repo.listar.side_effect = listar_emprestimos
    mock_repo.buscar_por_id.side_effect = buscar_por_id
    mock_repo.remover_emprestimo.side_effect = remover_emprestimo
    return mock_repo


@pytest.fixture
def usuario_service(usuario_repository):
    return UsuarioService(usuario_repository)


@pytest.fixture
def livro_service(livro_repository):
    return LivroService(livro_repository)


@pytest.fixture
def emprestimo_service(emprestimo_repository, livro_service, usuario_service):
    return EmprestimoService(
        usuario_service=usuario_service,
        livro_service=livro_service,
        emprestimo_dao=emprestimo_repository
    )


@pytest.fixture
def controller(emprestimo_service, livro_service, usuario_service):
    return BibliotecaController(emprestimo_service, livro_service, usuario_service)

@pytest.fixture
def autor_service(autor_repository):
    return AutorService(autor_repository)



def test_criar_autor_modelo_valido():
    autor = Autor("Machado de Assis", "Autor de Dom Casmurro", id=1)
    assert autor.nome == "Machado de Assis"
    assert autor.descricao == "Autor de Dom Casmurro"
    assert isinstance(repr(autor), str)

@pytest.mark.parametrize("nome,descricao", [
    ("", "Descrição válida"),
    ("   ", "Descrição válida"),
    ("Autor válido", ""),
    ("Autor válido", "   "),
])
def test_campos_invalidos_levantam_erro_modelo(nome, descricao):
    with pytest.raises(ValueError):
        Autor(nome, descricao)

# ======================================================
# 🧠 TESTES DE SERVICE (CRUD)
# ======================================================

def test_criar_autor_valido(autor_service):
    autor = autor_service.criar_autor("George Orwell", "Autor de 1984")
    assert autor.nome == "George Orwell"
    assert autor.descricao == "Autor de 1984"

def test_criar_autor_invalido(autor_service):
    autor = autor_service.criar_autor("", "Sem nome")
    assert autor is None

def test_listar_autores(autor_service):
    autor_service.criar_autor("Orwell", "Inglês")
    autor_service.criar_autor("Machado", "Brasileiro")
    autores = autor_service.dao.listar()
    assert len(autores) == 2
    assert any(r[1] == "Orwell" for r in autores)

def test_atualizar_autor(autor_service):
    autor = autor_service.criar_autor("Tolkien", "Fantasia")
    autor_service.atualizar_autor(autor.id, "Autor de O Senhor dos Anéis")
    autores = autor_service.listar_autor()
    assert autores[0].descricao == "Autor de O Senhor dos Anéis"

def test_remover_autor(autor_service):
    autor = autor_service.criar_autor("J.K. Rowling", "Harry Potter")
    autores_antes = len(autor_service.listar_autor())
    autor_service.remover_autor(autor.id)
    autores_depois = len(autor_service.listar_autor())
    assert autores_depois == autores_antes - 1

def test_remover_autor_inexistente(autor_service):
    resultado = autor_service.remover_autor(999)
    assert resultado is None or resultado is False

# ======================================================
# 🧩 TESTE DE INTEGRAÇÃO ENTRE SERVICE + MOCK
# ======================================================

def test_fluxo_completo_autor(autor_service):
    # Criação
    autor = autor_service.criar_autor("Isaac Asimov", "Autor de Eu, Robô")
    assert autor is not None

    autores = autor_service.listar_autor()
    assert len(autores) == 1

    # Atualização
    autor_service.atualizar_autor(autor.id, "Pai da ficção científica")
    autores = autor_service.listar_autor()
    assert autores[0].descricao == "Pai da ficção científica"

    # Remoção
    autor_service.remover_autor(autor.id)
    assert len(autor_service.listar_autor()) == 0




# ======================================================
# 👤 TESTES DE USUÁRIO
# ======================================================

def test_criar_usuario_valido(usuario_service):
    usuario = usuario_service.criar_usuario("Guilherme")
    assert usuario.nome == "Guilherme"

def test_usuario_sem_nome(usuario_service):
    usuario = usuario_service.criar_usuario("")
    assert usuario is None

def test_usuario_nome_apenas_espacos(usuario_service):
    usuario = usuario_service.criar_usuario("   ")
    assert usuario is None


# ======================================================
# 📚 TESTES DE LIVRO
# ======================================================

def test_criar_livro(livro_service):
    livro = livro_service.criar_livro("1984", "George Orwell", 1949)
    assert livro.titulo == "1984"
    assert livro.autor == "George Orwell"
    assert livro.ano_publicacao == 1949

def test_repr_livro(livro_service):
    livro = livro_service.criar_livro("1984", "George Orwell", 1949)
    assert "1984" in repr(livro)

def test_livro_ano_futuro(livro_service):
    livro = livro_service.criar_livro("Futuro", "Autor", 3000)
    assert livro is None

def test_livro_titulo_curto(livro_service):
    livro = livro_service.criar_livro("1", "Geo", 1949)
    assert livro is None

def test_livro_duplicado(livro_service):
    livro_service.criar_livro("1984", "George Orwell", 1949)

    with pytest.raises(LivroDuplicadoError):
        livro_service.criar_livro("1984", "George Orwell", 1949)


# ======================================================
# 📦 TESTES DE EMPRÉSTIMO
# ======================================================

def test_criar_emprestimo(emprestimo_service, usuario_service, livro_service):
    usuario = usuario_service.criar_usuario("Guilherme")
    livro = livro_service.criar_livro("1984", "George Orwell", 1949)
    emprestimo = emprestimo_service.criar_emprestimo(usuario.id, livro.id)

    assert emprestimo is not None
    assert emprestimo.usuario.nome == "Guilherme"
    assert emprestimo.livro.titulo == "1984"
    assert livro.disponivel is False

def test_devolver_livro(emprestimo_service, livro_service, usuario_service):
    usuario = usuario_service.criar_usuario("Guilherme")
    livro = livro_service.criar_livro("1984", "George Orwell", 1949)
    emprestimo = emprestimo_service.criar_emprestimo(usuario.id, livro.id)

    assert emprestimo is not None

    emprestimo_service.remover_emprestimo(emprestimo.id)
    assert livro.disponivel is True

def test_emprestimo_livro_indisponivel(emprestimo_service, usuario_service, livro_service):
    usuario = usuario_service.criar_usuario("Paulo")
    livro = livro_service.criar_livro("Livro Raro", "Autor X", 1999)
    livro.disponivel = False

    emprestimo = emprestimo_service.criar_emprestimo(usuario.id, livro.id)
    assert emprestimo is None

def test_emprestimo_usuario_invalido(emprestimo_service, livro_service):
    livro = livro_service.criar_livro("1984", "George Orwell", 1949)
    emprestimo = emprestimo_service.criar_emprestimo(999, livro.id)
    assert emprestimo is None

def test_emprestimo_livro_invalido(emprestimo_service, usuario_service):
    usuario = usuario_service.criar_usuario("Maria")
    emprestimo = emprestimo_service.criar_emprestimo(usuario.id, 999)
    assert emprestimo is None


# ======================================================
# 🧪 TESTES EXTREMOS
# ======================================================

@pytest.mark.parametrize("titulo", ["", " "*50, "A"*1000])
def test_titulos_extremos(livro_service, titulo):
    if not titulo.strip():
        with pytest.raises(EntradaInvalidaError) as exc_info:
            livro_service.criar_livro(titulo, "Autor", 2020)
        assert exc_info.value.campo == "titulo"
        assert "Entrada inválida no campo 'titulo'" in str(exc_info.value)
    else:
        livro = livro_service.criar_livro(titulo, "Autor", 2020)
        assert livro.titulo == titulo


def test_repr_modelos(usuario_service, livro_service):
    usuario = usuario_service.criar_usuario("Guilherme")
    livro = livro_service.criar_livro("1984", "George Orwell", 1949)
    assert isinstance(repr(usuario), str)
    assert isinstance(repr(livro), str)


# ======================================================
# 📈 TESTES DE INTEGRAÇÃO
# ======================================================

def test_criar_usuario_e_livro(usuario_service, livro_service):
    usuario = usuario_service.criar_usuario("Guilherme")
    livro = livro_service.criar_livro("1984", "George Orwell", 1949)
    assert usuario.nome == "Guilherme"
    assert livro.titulo == "1984"

def test_emprestimo_usuario_e_livro(emprestimo_service, usuario_service, livro_service):
    usuario = usuario_service.criar_usuario("Guilherme")
    livro = livro_service.criar_livro("1984", "George Orwell", 1949)

    emprestimo = emprestimo_service.criar_emprestimo(usuario.id, livro.id)
    assert emprestimo is not None
    assert emprestimo.usuario.nome == "Guilherme"
    assert emprestimo.livro.titulo == "1984"
    assert livro.disponivel is False

def test_devolucao_livro_integracao(emprestimo_service, livro_service, usuario_service):
    usuario = usuario_service.criar_usuario("Guilherme")
    livro = livro_service.criar_livro("1984", "George Orwell", 1949)

    emprestimo = emprestimo_service.criar_emprestimo(usuario.id, livro.id)
    assert emprestimo is not None

    emprestimo_service.remover_emprestimo(emprestimo.id)
    assert livro.disponivel is True
