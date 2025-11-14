import pytest
from src.controllers.biblioteca_controller import BibliotecaController
from src.models.usuario import Usuario
from src.models.livro import Livro
from src.models.autor import Autor
from src.services.arquivo_service import ArquivoService


@pytest.fixture
def controller():
    return BibliotecaController()


# 1️⃣ Fluxo completo: Autor → Livro → Empréstimo → Devolução
def test_fluxo_completo_integrado(controller):
    autor = controller.autor_repo.adicionar(Autor("George Orwell", "Escritor britânico"))
    livro = controller.livros_repo.adicionar(Livro(1, "1984", autor.nome, 1949))
    usuario = controller.usuarios_repo.adicionar(Usuario("Marcos"))

    emprestimo = controller.emprestar_livro(usuario.id, livro.id)

    assert not livro.disponivel
    assert emprestimo.livro.titulo == "1984"
    assert emprestimo.usuario.nome == "Marcos"

    controller.devolver_livro(emprestimo.id)
    assert livro.disponivel


# 2️⃣ Tentar empréstimo de livro indisponível
def test_livro_indisponivel_integrado(controller):
    u1 = controller.usuarios_repo.adicionar(Usuario("Ana"))
    u2 = controller.usuarios_repo.adicionar(Usuario("Paulo"))
    autor = controller.autor_repo.adicionar(Autor("Orwell", "Autor inglês"))
    livro = controller.livros_repo.adicionar(Livro(1, "A Revolução dos Bichos", autor.nome, 1945))

    controller.emprestar_livro(u1.id, livro.id)

    with pytest.raises(ValueError, match="indisponível"):
        controller.emprestar_livro(u2.id, livro.id)


# 3️⃣ Usuário bloqueado não pode emprestar
def test_usuario_bloqueado_integrado(controller):
    usuario = controller.usuarios_repo.adicionar(Usuario("Danilo"))
    usuario.bloqueado = True

    autor = controller.autor_repo.adicionar(Autor("Cervantes", "Espanhol"))
    livro = controller.livros_repo.adicionar(Livro(1, "Dom Quixote", autor.nome, 1605))

    with pytest.raises(ValueError, match="bloqueado"):
        controller.emprestar_livro(usuario.id, livro.id)


# 4️⃣ Atualização e recuperação de dados entre módulos
def test_atualizar_e_buscar_usuario_integrado(controller):
    usuario = controller.usuarios_repo.adicionar(Usuario("Beatriz"))
    novo_usuario = Usuario("Beatriz Oliveira", id=usuario.id)

    controller.usuarios_repo.atualizar(usuario.id, novo_usuario)
    recuperado = controller.usuarios_repo.buscar_por_id(usuario.id)

    assert recuperado.nome == "Beatriz Oliveira"


# 5️⃣ Múltiplos empréstimos integrados
def test_multiplos_emprestimos_integrado(controller):
    autor = controller.autor_repo.adicionar(Autor("Martin Fowler", "Arquiteto de software"))
    l1 = controller.livros_repo.adicionar(Livro(1, "Refactoring", autor.nome, 1999))
    l2 = controller.livros_repo.adicionar(Livro(2, "Patterns", autor.nome, 2004))

    u1 = controller.usuarios_repo.adicionar(Usuario("Lucas"))
    u2 = controller.usuarios_repo.adicionar(Usuario("Clara"))

    e1 = controller.emprestar_livro(u1.id, l1.id)
    e2 = controller.emprestar_livro(u2.id, l2.id)

    assert not l1.disponivel
    assert not l2.disponivel
    assert e1.usuario.nome == "Lucas"
    assert e2.usuario.nome == "Clara"


# 6️⃣ Tentativa de devolver empréstimo inexistente
def test_devolver_emprestimo_inexistente(controller):
    with pytest.raises(ValueError, match="não encontrado"):
        controller.devolver_livro(9999)


# 7️⃣ Remover livro e recriar com mesmo título
def test_remover_e_recriar_livro_integrado(controller):
    autor = controller.autor_repo.adicionar(Autor("Tolkien", "Autor de fantasia"))

    livro = controller.livros_repo.adicionar(Livro(1, "O Hobbit", autor.nome, 1937))
    controller.livros_repo.remover(livro.id)

    assert controller.livros_repo.buscar_por_id(livro.id) is None

    novo = controller.livros_repo.adicionar(Livro(2, "O Hobbit", autor.nome, 1937))
    assert novo.id != livro.id


# 8️⃣ Validação integrada (dados inválidos)
def test_validacao_integrada(controller):
    with pytest.raises(ValueError):
        controller.livros_repo.adicionar(Livro(1, "", "Autor", 2000))

    with pytest.raises(ValueError):
        controller.usuarios_repo.adicionar(Usuario(""))


# 9️⃣ Rollback após exceção no fluxo
def test_integracao_rollback(controller):
    usuario = controller.usuarios_repo.adicionar(Usuario("Lia"))
    autor = controller.autor_repo.adicionar(Autor("Dan Brown", "Autor"))
    livro = controller.livros_repo.adicionar(Livro(1, "Inferno", autor.nome, 2013))

    controller.emprestar_livro(usuario.id, livro.id)

    with pytest.raises(ValueError):
        controller.emprestar_livro(usuario.id, livro.id)

    assert not livro.disponivel  # estado permanece consistente


# 🔟 Integração com ArquivoService (persistência JSON)
def test_persistencia_completa_integrada(tmp_path):
    caminho = tmp_path / "acervo.json"

    livros = [
        Livro(1, "Clean Code", "Robert C. Martin", 2008),
        Livro(2, "Refactoring", "Martin Fowler", 1999),
    ]

    ArquivoService.salvar_livros_json(str(caminho), livros)
    carregados = ArquivoService.carregar_livros_json(str(caminho))

    assert len(carregados) == 2
    assert carregados[0].titulo == "Clean Code"
    assert carregados[1].autor == "Martin Fowler"
