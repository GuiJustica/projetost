import pytest
import os
import json
from src.models.livro import Livro
from src.models.usuario import Usuario
from src.models.emprestimo import Emprestimo
from src.repositories.base_repository import BaseRepository
from src.services.arquivo_service import ArquivoService
from src.controllers.biblioteca_controller import BibliotecaController

# ======================================================
# 🔧 FIXTURES GERAIS
# ======================================================

@pytest.fixture
def usuario_exemplo():
    return Usuario(id=1, nome="Guilherme")

@pytest.fixture
def livro_exemplo():
    return Livro(id=1, titulo="1984", autor="George Orwell", ano_publicacao=1949)

@pytest.fixture
def caminho_tmp(tmp_path):
    return tmp_path / "dados_teste.json"

@pytest.fixture
def controller():
    return BibliotecaController()

# ======================================================
# 👤 TESTES DE USUÁRIO
# ======================================================

def test_criar_usuario_valido(usuario_exemplo):
    assert usuario_exemplo.nome == "Guilherme"

def test_usuario_sem_nome():
    with pytest.raises(ValueError):
        Usuario(id=2, nome="")


# 🆕 Novo teste: usuário com nome só de espaços
def test_usuario_nome_apenas_espacos():
    with pytest.raises(ValueError):
        Usuario(id=10, nome="   ")

# ======================================================
# 📚 TESTES DE LIVRO
# ======================================================

def test_criacao_livro(livro_exemplo):
    assert livro_exemplo.titulo == "1984"
    assert livro_exemplo.autor == "George Orwell"

def test_repr_livro(livro_exemplo):
    assert "1984" in repr(livro_exemplo)

@pytest.mark.parametrize("ano", [0, 1999, 2024])
def test_livro_com_anos_validos(ano):
    livro = Livro(id=5, titulo="Genérico", autor="Alguém", ano_publicacao=ano)
    assert isinstance(livro.ano_publicacao, int)

# 🆕 Novo teste: livro com ano futuro
def test_livro_ano_futuro():
    with pytest.raises(ValueError):
        Livro(id=6, titulo="Futuro", autor="Autor", ano_publicacao=3000)

# ======================================================
# 💾 TESTES DE ARQUIVOSERVICE
# ======================================================

def test_salvar_e_carregar_livros_json(caminho_tmp, controller, livro_exemplo):
    controller.cadastrar_livro(livro_exemplo.titulo, livro_exemplo.autor)
    livros = controller.listar_livros()
    ArquivoService.salvar_livros_json(str(caminho_tmp), livros)
    assert os.path.exists(caminho_tmp)
    carregados = ArquivoService.carregar_livros_json(str(caminho_tmp))
    assert len(carregados) == len(livros)

def test_carregar_json_inexistente(caminho_tmp):
    livros = ArquivoService.carregar_livros_json(str(caminho_tmp))
    assert livros == []

def test_carregar_json_corrompido(tmp_path):
    caminho = tmp_path / "arquivo_ruim.json"
    with open(caminho, "w") as f:
        f.write("{invalido_json}")
    livros = ArquivoService.carregar_livros_json(str(caminho))
    assert livros == []

# ======================================================
# 🔁 TESTES DE REPOSITÓRIO
# ======================================================

def test_remover_item():
    repo = BaseRepository()
    u = Usuario(id=1, nome="Teste")
    repo.adicionar(u)
    repo.remover(1)
    assert repo.buscar_por_id(1) is None

def test_atualizar_item():
    repo = BaseRepository()
    u = Usuario(id=1, nome="Carlos")
    repo.adicionar(u)
    u.nome = "Carlos Silva"
    repo.atualizar(1, u)
    assert repo.buscar_por_id(1).nome == "Carlos Silva"

# ======================================================
# 📦 TESTES DE EMPRÉSTIMO
# ======================================================

def test_criar_emprestimo(usuario_exemplo, livro_exemplo):
    emp = Emprestimo(usuario=usuario_exemplo, livro=livro_exemplo)
    assert emp.usuario.nome == "Guilherme"
    assert emp.livro.titulo == "1984"

def test_devolver_livro(livro_exemplo, usuario_exemplo):
    emp = Emprestimo(usuario=usuario_exemplo, livro=livro_exemplo)
    emp.devolver()
    assert emp.data_devolucao is not None



# ======================================================
# 🏛️ TESTES DO CONTROLLER
# ======================================================

def test_fluxo_completo(controller):
    u = controller.cadastrar_usuario("João")
    l = controller.cadastrar_livro("Clean Code", "Robert C. Martin")
    e = controller.emprestar_livro(u.id, l.id)
    controller.devolver_livro(e.id)
    assert l.disponivel is True

def test_emprestimo_usuario_invalido(controller):
    with pytest.raises(ValueError):
        controller.emprestar_livro(999, 1)

def test_emprestimo_livro_invalido(controller):
    u = controller.cadastrar_usuario("Maria")
    with pytest.raises(ValueError):
        controller.emprestar_livro(u.id, 999)

def test_emprestimo_livro_indisponivel(controller):
    u = controller.cadastrar_usuario("Paulo")
    l = controller.cadastrar_livro("Livro Raro", "Autor X")
    controller.emprestar_livro(u.id, l.id)
    with pytest.raises(ValueError):
        controller.emprestar_livro(u.id, l.id)

def test_devolver_emprestimo_inexistente(controller):
    with pytest.raises(ValueError):
        controller.devolver_livro(999)

# ======================================================
# 🧪 TESTES EXTREMOS
# ======================================================

@pytest.mark.parametrize("titulo", ["", " "*50, "A"*1000])
def test_titulos_extremos(controller, titulo):
    if not titulo.strip():  # caso vazio ou só espaços
        with pytest.raises(ValueError):
            Livro(id=10, titulo=titulo, autor="Autor", ano_publicacao=2020)
    else:
        livro = Livro(id=10, titulo=titulo, autor="Autor", ano_publicacao=2020)
        assert livro.titulo == titulo

def test_repr_modelos(usuario_exemplo, livro_exemplo):
    assert isinstance(repr(usuario_exemplo), str)
    assert isinstance(repr(livro_exemplo), str)
