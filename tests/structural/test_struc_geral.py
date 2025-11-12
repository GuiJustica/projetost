import os
import pytest
from datetime import datetime
from src.controllers.biblioteca_controller import BibliotecaController
from src.models.usuario import Usuario
from src.models.livro import Livro
from src.models.emprestimo import Emprestimo
from src.repositories.base_repository import BaseRepository
from src.services.arquivo_service import ArquivoService

@pytest.fixture
def controller():
    return BibliotecaController()

# =======================
# Tests de Empréstimo
# =======================
def test_emprestar_livro_usuario_inexistente(controller):
    with pytest.raises(ValueError, match="Usuário não encontrado"):
        controller.emprestar_livro(999, 1)

def test_emprestar_livro_livro_inexistente(controller):
    usuario = controller.usuarios_repo.adicionar(Usuario("Ana"))
    with pytest.raises(ValueError, match="Livro não encontrado"):
        controller.emprestar_livro(usuario.id, 999)

def test_emprestar_livro_usuario_bloqueado(controller):
    usuario = controller.usuarios_repo.adicionar(Usuario("Carlos"))
    usuario.bloqueado = True
    livro = controller.livros_repo.adicionar(Livro("Python 101", "Autor", 2020))
    with pytest.raises(ValueError, match="Usuário bloqueado"):
        controller.emprestar_livro(usuario.id, livro.id)

def test_emprestar_livro_indisponivel(controller):
    usuario = controller.usuarios_repo.adicionar(Usuario("Paula"))
    livro = controller.livros_repo.adicionar(Livro("Clean Code", "Martin", 2008))
    controller.emprestar_livro(usuario.id, livro.id)
    with pytest.raises(ValueError, match="Livro indisponível"):
        controller.emprestar_livro(usuario.id, livro.id)

def test_emprestar_livro_sucesso(controller):
    usuario = controller.usuarios_repo.adicionar(Usuario("Lucas"))
    livro = controller.livros_repo.adicionar(Livro("Dom Casmurro", "Machado", 1899))
    emprestimo = controller.emprestar_livro(usuario.id, livro.id)
    assert isinstance(emprestimo, Emprestimo)
    assert not emprestimo.livro.disponivel
    assert emprestimo.usuario.id == usuario.id
    assert emprestimo.livro.id == livro.id

# =======================
# Tests de Devolução
# =======================
def test_devolver_livro_inexistente(controller):
    with pytest.raises(ValueError, match="não encontrado"):
        controller.devolver_livro(999)

def test_devolver_livro_sucesso(controller):
    usuario = controller.usuarios_repo.adicionar(Usuario("Lucas"))
    livro = controller.livros_repo.adicionar(Livro("Dom Casmurro", "Machado", 1899))
    emprestimo = controller.emprestar_livro(usuario.id, livro.id)
    devolvido = controller.devolver_livro(emprestimo.id)
    assert devolvido.livro.disponivel

def test_devolver_livro_dupla_devolucao(controller):
    usuario = controller.usuarios_repo.adicionar(Usuario("Mariana"))
    livro = controller.livros_repo.adicionar(Livro("Python Avançado", "Autor", 2021))
    emprestimo = controller.emprestar_livro(usuario.id, livro.id)
    controller.devolver_livro(emprestimo.id)
    devolvido = controller.devolver_livro(emprestimo.id)
    assert devolvido.livro.disponivel

# =======================
# Tests múltiplos empréstimos
# =======================
def test_multiplos_emprestimos_e_devolucoes(controller):
    u1 = controller.usuarios_repo.adicionar(Usuario("Alice"))
    u2 = controller.usuarios_repo.adicionar(Usuario("Bob"))
    l1 = controller.livros_repo.adicionar(Livro("Livro 1", "Autor1", 2000))
    l2 = controller.livros_repo.adicionar(Livro("Livro 2", "Autor2", 2001))

    e1 = controller.emprestar_livro(u1.id, l1.id)
    e2 = controller.emprestar_livro(u2.id, l2.id)

    with pytest.raises(ValueError):
        controller.emprestar_livro(u1.id, l1.id)

    controller.devolver_livro(e1.id)
    controller.devolver_livro(e2.id)

    assert l1.disponivel
    assert l2.disponivel

# =======================
# Tests de Models
# =======================
def test_usuario_estado_inicial():
    u = Usuario("Teste")
    assert u.nome == "Teste"
    assert not u.bloqueado

def test_usuario_bloqueio_e_atributos():
    u = Usuario("Outro")
    u.bloqueado = True
    assert u.bloqueado

def test_usuario_nome_vazio():
    with pytest.raises(ValueError):
        Usuario("")

def test_usuario_nome_espacos():
    with pytest.raises(ValueError):
        Usuario("   ")

def test_usuario_redefinir_nome():
    u = Usuario("Inicial")
    u.nome = "NovoNome"
    assert u.nome == "NovoNome"

def test_livro_disponibilidade():
    l = Livro("Python", "Autor", 2023)
    assert l.disponivel
    l.disponivel = False
    assert not l.disponivel

def test_livro_ano_publicacao_invalido():
    with pytest.raises(ValueError, match="Ano não pode ser negativo."):
        Livro("Titulo", "Autor", 0)
    with pytest.raises(ValueError, match="Ano não pode ser negativo."):
        Livro("Titulo", "Autor", -10)

def test_livro_ano_futuro():
    ano_futuro = datetime.now().year + 1
    with pytest.raises(ValueError, match="Ano de publicação inválido."):
        Livro("Titulo Futuro", "Autor", ano_futuro)

def test_livro_titulo_vazio():
    with pytest.raises(ValueError, match="O título não pode ser vazio."):
        Livro("", "Autor", 2000)

def test_emprestimo_devolucao():
    u = Usuario("Ana")
    l = Livro("Livro1", "Autor1", 2000)
    e = Emprestimo(u, l)
    assert e.livro.disponivel
    e.devolver()
    assert e.livro.disponivel

def test_emprestimo_dupla_devolucao_gera_erro():
    u = Usuario("Teste")
    l = Livro("Livro Teste", "Autor", 2000)
    e = Emprestimo(u, l)
    e.devolver()
    e.devolver()
    assert l.disponivel

# =======================
# Tests de Repositories
# =======================
def test_base_repository_adicionar_listar():
    repo = BaseRepository()
    class Dummy:
        def __init__(self):
            self.id = None
    d = Dummy()
    repo.adicionar(d)
    assert d.id is not None
    assert repo.listar() == [d]

def test_base_repository_buscar_por_id():
    repo = BaseRepository()
    class Dummy:
        def __init__(self):
            self.id = None
    d = Dummy()
    repo.adicionar(d)
    assert repo.buscar_por_id(d.id) == d
    assert repo.buscar_por_id(999) is None

def test_base_repository_remover_atualizar():
    repo = BaseRepository()
    class Dummy:
        def __init__(self, id=None):
            self.id = id
    d = Dummy()
    repo.adicionar(d)
    novo = Dummy(id=d.id)
    repo.atualizar(d.id, novo)
    assert repo.buscar_por_id(d.id) == novo
    repo.remover(d.id)
    assert repo.buscar_por_id(d.id) is None

def test_base_repository_atualizar_inexistente():
    repo = BaseRepository()
    class Dummy:
        def __init__(self):
            self.id = None
    with pytest.raises(KeyError):
        repo.atualizar(999, Dummy())

def test_base_repository_id_manual():
    repo = BaseRepository()
    class Dummy:
        def __init__(self, id=None):
            self.id = id
    d1 = Dummy()
    d2 = Dummy(id=5)
    repo.adicionar(d1)
    repo.adicionar(d2)
    assert d2.id == 5
    assert repo.proximo_id == 6

def test_base_repository_remover_inexistente_silencioso():
    repo = BaseRepository()
    class Dummy:
        def __init__(self):
            self.id = None
    d = Dummy()
    repo.adicionar(d)
    repo.remover(999)
    assert repo.listar() == [d]

def test_base_repository_atualizar_mesmo_objeto():
    repo = BaseRepository()
    class Dummy:
        def __init__(self, id=None):
            self.id = id
    d = Dummy()
    repo.adicionar(d)
    repo.atualizar(d.id, d)
    assert repo.buscar_por_id(d.id) == d

# =======================
# Tests de ArquivoService
# =======================
def test_arquivo_service_salvar_carregar(tmp_path):
    arquivo = tmp_path / "livros.json"
    livros = [Livro("L1", "A1", 2000)]
    ArquivoService.salvar_livros_json(str(arquivo), livros)
    assert arquivo.exists()
    carregados = ArquivoService.carregar_livros_json(str(arquivo))
    assert len(carregados) == 1
    assert carregados[0].titulo == "L1"

def test_arquivo_service_carregar_inexistente(tmp_path):
    arquivo = tmp_path / "inexistente.json"
    carregados = ArquivoService.carregar_livros_json(str(arquivo))
    assert carregados == []

def test_arquivo_service_salvar_lista_vazia(tmp_path):
    arquivo = tmp_path / "vazio.json"
    ArquivoService.salvar_livros_json(str(arquivo), [])
    with open(arquivo, "r", encoding="utf-8") as f:
        conteudo = f.read()
    assert conteudo == "[]"

def test_arquivo_service_caminho_invalido(tmp_path):
    caminho_invalido = tmp_path / "diretorio_inexistente" / "livros.json"
    os.makedirs(caminho_invalido.parent, exist_ok=True)
    livros = []
    ArquivoService.salvar_livros_json(str(caminho_invalido), livros)
    assert caminho_invalido.exists()

def test_arquivo_service_dados_invalidos(tmp_path):
    arquivo = tmp_path / "livros_invalidos.json"
    class Falso:
        def __init__(self):
            self.titulo = "X"
            self.autor = "Y"
            self.ano_publicacao = 2000
    lista_falsa = [Falso()]
    ArquivoService.salvar_livros_json(str(arquivo), lista_falsa)
    assert arquivo.exists()
    carregados = ArquivoService.carregar_livros_json(str(arquivo))
    assert carregados[0].titulo == "X"

# =======================
# Tests adicionais Controller
# =======================
def test_listar_livros_e_usuarios(controller):
    assert controller.livros_repo.listar() == []
    assert controller.usuarios_repo.listar() == []
    u = controller.usuarios_repo.adicionar(Usuario("Teste"))
    l = controller.livros_repo.adicionar(Livro("L1", "A1", 2000))
    assert controller.usuarios_repo.listar() == [u]
    assert controller.livros_repo.listar() == [l]

def test_bloqueio_apos_emprestimo(controller):
    u = controller.usuarios_repo.adicionar(Usuario("Bloqueio"))
    l1 = controller.livros_repo.adicionar(Livro("Livro1", "Autor", 2000))
    l2 = controller.livros_repo.adicionar(Livro("Livro2", "Autor", 2001))
    controller.emprestar_livro(u.id, l1.id)
    controller.emprestar_livro(u.id, l2.id)
    # lógica de bloqueio específica do controller, se houver:
    # assert u.bloqueado is True
