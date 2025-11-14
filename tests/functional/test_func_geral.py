import pytest
from src.controllers.biblioteca_controller import BibliotecaController
from src.models.usuario import Usuario
from src.models.livro import Livro
from src.models.autor import Autor
from src.services.arquivo_service import ArquivoService


@pytest.fixture
def controller():
    return BibliotecaController()


# 1️⃣ Fluxo completo com autor, livro e usuário
def test_fluxo_completo_funcional(controller):
    autor = controller.autores_repo.adicionar(Autor("George Orwell", "Escritor britânico"))
    livro = controller.livros_repo.adicionar(Livro(1, "1984", autor.nome, 1949))
    usuario = controller.usuarios_repo.adicionar(Usuario("Alice"))

    # Empréstimo
    emprestimo = controller.emprestar_livro(usuario.id, livro.id)
    assert not livro.disponivel
    assert emprestimo.usuario.nome == "Alice"
    assert emprestimo.livro.titulo == "1984"

    # Devolução
    controller.devolver_livro(emprestimo.id)
    assert livro.disponivel


# 2️⃣ Empréstimo de livro indisponível
def test_emprestar_livro_indisponivel_funcional(controller):
    autor = controller.autores_repo.adicionar(Autor("J.R.R. Tolkien", "Autor britânico"))
    livro = controller.livros_repo.adicionar(Livro(1, "O Hobbit", autor.nome, 1937))
    usuario1 = controller.usuarios_repo.adicionar(Usuario("Bruno"))
    usuario2 = controller.usuarios_repo.adicionar(Usuario("Clara"))

    controller.emprestar_livro(usuario1.id, livro.id)
    assert not livro.disponivel

    with pytest.raises(ValueError, match="indisponível"):
        controller.emprestar_livro(usuario2.id, livro.id)


# 3️⃣ Cadastro e atualização de autor
def test_cadastro_e_atualizacao_autor(controller):
    autor = controller.autores_repo.adicionar(Autor("Machado de Assis", "Romancista brasileiro"))
    autor.descricao = "Romancista e contista brasileiro"
    controller.autores_repo.atualizar(autor.id, autor)

    recuperado = controller.autores_repo.buscar_por_id(autor.id)
    assert recuperado.descricao == "Romancista e contista brasileiro"


# 4️⃣ Teste funcional de validação de dados
def test_validacao_funcional(controller):
    with pytest.raises(ValueError):
        controller.livros_repo.adicionar(Livro(1, "", "Autor", 2000))  # título vazio

    with pytest.raises(ValueError):
        controller.usuarios_repo.adicionar(Usuario(""))  # nome vazio


# 5️⃣ Fluxo com múltiplos autores e livros
def test_multiplos_autores_e_livros(controller):
    a1 = controller.autores_repo.adicionar(Autor("Robert C. Martin", "Engenheiro de software"))
    a2 = controller.autores_repo.adicionar(Autor("Martin Fowler", "Arquiteto de software"))

    l1 = controller.livros_repo.adicionar(Livro(1, "Clean Code", a1.nome, 2008))
    l2 = controller.livros_repo.adicionar(Livro(2, "Refactoring", a2.nome, 1999))

    u1 = controller.usuarios_repo.adicionar(Usuario("Lucas"))
    u2 = controller.usuarios_repo.adicionar(Usuario("Clara"))

    e1 = controller.emprestar_livro(u1.id, l1.id)
    e2 = controller.emprestar_livro(u2.id, l2.id)

    assert not l1.disponivel and not l2.disponivel
    assert e1.livro.titulo == "Clean Code"
    assert e2.usuario.nome == "Clara"


# 6️⃣ Tentativa de devolver empréstimo inexistente
def test_devolver_inexistente_funcional(controller):
    with pytest.raises(ValueError, match="não encontrado"):
        controller.devolver_livro(999)


# 7️⃣ Listagem e filtro de livros disponíveis
def test_listar_livros_disponiveis_funcional(controller):
    autor = controller.autores_repo.adicionar(Autor("Saint-Exupéry", "Escritor francês"))
    l1 = controller.livros_repo.adicionar(Livro(1, "O Pequeno Príncipe", autor.nome, 1943))
    l2 = controller.livros_repo.adicionar(Livro(2, "Voo Noturno", autor.nome, 1931))
    u = controller.usuarios_repo.adicionar(Usuario("Gabriel"))

    controller.emprestar_livro(u.id, l1.id)

    disponiveis = [livro for livro in controller.livros_repo.listar() if livro.disponivel]
    assert l2 in disponiveis
    assert l1 not in disponiveis


# 8️⃣ Persistência de autores e livros (funcional)
def test_persistencia_funcional(tmp_path):
    arquivo_autores = tmp_path / "autores.json"
    arquivo_livros = tmp_path / "livros.json"

    autores = [Autor("Orwell", "Autor britânico"), Autor("Tolkien", "Autor de fantasia")]
    livros = [Livro(1, "1984", "Orwell", 1949), Livro(2, "O Hobbit", "Tolkien", 1937)]

    # Simula salvamento
    ArquivoService.salvar_livros_json(str(arquivo_livros), livros)

    # Valida carregamento
    carregados = ArquivoService.carregar_livros_json(str(arquivo_livros))
    assert len(carregados) == 2
    assert carregados[0].titulo == "1984"
    assert carregados[1].autor == "Tolkien"
