import pytest
from src.controllers.biblioteca_controller import BibliotecaController
from src.models.usuario import Usuario
from src.models.livro import Livro
from src.models.emprestimo import Emprestimo


@pytest.fixture
def controller():
    return BibliotecaController()


# 1️⃣ Fluxo completo de empréstimo e devolução
def test_fluxo_completo_integrado(controller):
    usuario = Usuario("João")
    livro = Livro("Dom Casmurro", "Machado de Assis", 1899)
    controller.usuarios_repo.adicionar(usuario)
    controller.livros_repo.adicionar(livro)

    emprestimo = controller.emprestar_livro(usuario.id, livro.id)
    assert emprestimo.livro.disponivel is False

    controller.devolver_livro(emprestimo.id)
    assert livro.disponivel is True


# 2️⃣ Usuário bloqueado tentando pegar livro
def test_emprestimo_usuario_bloqueado_integrado(controller):
    usuario = Usuario("Maria")
    usuario.bloquear()
    livro = Livro("O Hobbit", "Tolkien", 1937)
    controller.usuarios_repo.adicionar(usuario)
    controller.livros_repo.adicionar(livro)

    with pytest.raises(ValueError, match="Usuário bloqueado"):
        controller.emprestar_livro(usuario.id, livro.id)


# 3️⃣ Livro indisponível em novo empréstimo
def test_emprestimo_livro_indisponivel_integrado(controller):
    usuario1 = Usuario("Ana")
    usuario2 = Usuario("Carlos")
    livro = Livro("1984", "George Orwell", 1949)

    controller.usuarios_repo.adicionar(usuario1)
    controller.usuarios_repo.adicionar(usuario2)
    controller.livros_repo.adicionar(livro)

    controller.emprestar_livro(usuario1.id, livro.id)

    with pytest.raises(ValueError, match="Livro indisponível"):
        controller.emprestar_livro(usuario2.id, livro.id)


# 4️⃣ Integração com serviço de arquivo (salvar/carregar)
def test_salvar_e_carregar_integrado(controller, tmp_path):
    arquivo = tmp_path / "livros.json"
    livros = [Livro("A Revolução dos Bichos", "George Orwell", 1945)]
    controller.arquivo_service.salvar_livros_json(str(arquivo),livros)
    carregados = controller.arquivo_service.carregar_livros_json(arquivo)

    assert len(carregados) == 1
    assert carregados[0].titulo == "A Revolução dos Bichos"


# 5️⃣ Atualização de dados entre repositórios
def test_atualizar_usuario_integrado(controller):
    usuario = controller.usuarios_repo.adicionar(Usuario("Lucas"))
    usuario.nome = "Lucas Silva"
    usuario_atualizado = Usuario(nome="Lucas Silva", id=usuario.id)
    controller.usuarios_repo.atualizar(usuario.id, usuario_atualizado)
    assert controller.usuarios_repo.buscar_por_id(usuario.id).nome == "Lucas Silva"


# 6️⃣ Remoção e re-adição de item
def test_remover_e_recriar_livro_integrado(controller):
    livro = controller.livros_repo.adicionar(Livro("O Pequeno Príncipe", "Saint-Exupéry", 1943))
    controller.livros_repo.remover(livro.id)
    assert controller.livros_repo.buscar_por_id(livro.id) is None

    novo = controller.livros_repo.adicionar(Livro("O Pequeno Príncipe", "Saint-Exupéry", 1943))
    assert novo.id != livro.id


# 7️⃣ Empréstimos múltiplos e independentes
def test_multiplos_emprestimos_integrado(controller):
    u1 = controller.usuarios_repo.adicionar(Usuario("João"))
    u2 = controller.usuarios_repo.adicionar(Usuario("Pedro"))
    l1 = controller.livros_repo.adicionar(Livro("Livro A", "Autor A", 2000))
    l2 = controller.livros_repo.adicionar(Livro("Livro B", "Autor B", 2001))

    e1 = controller.emprestar_livro(u1.id, l1.id)
    e2 = controller.emprestar_livro(u2.id, l2.id)

    assert not l1.disponivel
    assert not l2.disponivel
    assert e1.usuario.nome == "João"
    assert e2.usuario.nome == "Pedro"


# 8️⃣ Tentativa de devolver empréstimo inexistente
def test_devolver_inexistente_integrado(controller):
    with pytest.raises(ValueError, match="não encontrado"):
        controller.devolver_livro(999)


# 9️⃣ Teste de persistência simulada em repositórios
def test_persistencia_simulada_integrado(controller):
    usuario = controller.usuarios_repo.adicionar(Usuario("Bruno"))
    livro = controller.livros_repo.adicionar(Livro("Clean Code", "Robert Martin", 2008))

    # Primeiro empréstimo
    emprestimo = controller.emprestar_livro(usuario.id, livro.id)
    assert emprestimo in controller.emprestimos_repo.listar()

    # Devolver o livro para que ele fique disponível
    controller.devolver_livro(emprestimo.id)
    assert livro.disponivel  # agora o livro está disponível novamente

    # Segundo empréstimo (após devolver)
    emprestimo2 = controller.emprestar_livro(usuario.id, livro.id)
    assert emprestimo2 in controller.emprestimos_repo.listar()
    assert not livro.disponivel


# 🔟 Integração com exceções esperadas e rollback lógico
def test_integracao_excecao_e_recuperacao(controller):
    usuario = controller.usuarios_repo.adicionar(Usuario("Lia"))
    livro = controller.livros_repo.adicionar(Livro("O Código Da Vinci", "Dan Brown", 2003))

    controller.emprestar_livro(usuario.id, livro.id)
    assert not livro.disponivel

    with pytest.raises(ValueError):
        controller.emprestar_livro(usuario.id, livro.id)

    # O estado do livro não deve ser alterado por causa da exceção
    assert not livro.disponivel
