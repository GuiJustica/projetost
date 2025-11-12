import pytest
from src.controllers.biblioteca_controller import BibliotecaController
from src.models.usuario import Usuario
from src.models.livro import Livro

@pytest.fixture
def controller():
    return BibliotecaController()

# 1️⃣ Empréstimo de livro disponível
def test_emprestar_livro_disponivel(controller):
    usuario = controller.usuarios_repo.adicionar(Usuario("Alice"))
    livro = controller.livros_repo.adicionar(Livro("1984", "George Orwell", 1949))
    emprestimo = controller.emprestar_livro(usuario.id, livro.id)
    assert emprestimo.livro.disponivel is False
    assert emprestimo.usuario.id == usuario.id

# 2️⃣ Tentativa de empréstimo de livro indisponível
def test_emprestar_livro_indisponivel(controller):
    usuario1 = controller.usuarios_repo.adicionar(Usuario("Bob"))
    usuario2 = controller.usuarios_repo.adicionar(Usuario("Carol"))
    livro = controller.livros_repo.adicionar(Livro("O Pequeno Príncipe", "Saint-Exupéry", 1943))

    controller.emprestar_livro(usuario1.id, livro.id)
    with pytest.raises(ValueError, match="indisponível"):
        controller.emprestar_livro(usuario2.id, livro.id)

# 3️⃣ Usuário bloqueado tenta pegar livro
def test_usuario_bloqueado(controller):
    usuario = controller.usuarios_repo.adicionar(Usuario("Danilo"))
    usuario.bloqueado = True
    livro = controller.livros_repo.adicionar(Livro("Dom Quixote", "Cervantes", 1605))

    with pytest.raises(ValueError, match="bloqueado"):
        controller.emprestar_livro(usuario.id, livro.id)

# 4️⃣ Devolução de livro
def test_devolver_livro(controller):
    usuario = controller.usuarios_repo.adicionar(Usuario("Eva"))
    livro = controller.livros_repo.adicionar(Livro("O Hobbit", "Tolkien", 1937))
    emprestimo = controller.emprestar_livro(usuario.id, livro.id)

    controller.devolver_livro(emprestimo.id)
    assert livro.disponivel is True

# 5️⃣ Tentativa de devolver empréstimo inexistente
def test_devolver_inexistente(controller):
    with pytest.raises(ValueError, match="não encontrado"):
        controller.devolver_livro(999)

# 6️⃣ Múltiplos empréstimos e devoluções
def test_multiplos_emprestimos_devolucoes(controller):
    usuario = controller.usuarios_repo.adicionar(Usuario("Fábio"))
    livro1 = controller.livros_repo.adicionar(Livro("A Revolução dos Bichos", "Orwell", 1945))
    livro2 = controller.livros_repo.adicionar(Livro("Capitães da Areia", "Jorge Amado", 1937))

    e1 = controller.emprestar_livro(usuario.id, livro1.id)
    e2 = controller.emprestar_livro(usuario.id, livro2.id)
    controller.devolver_livro(e1.id)

    assert livro1.disponivel is True
    assert livro2.disponivel is False

# 7️⃣ Listar livros disponíveis
def test_listar_livros_disponiveis(controller):
    livro1 = controller.livros_repo.adicionar(Livro("Livro A", "Autor A", 2000))
    livro2 = controller.livros_repo.adicionar(Livro("Livro B", "Autor B", 2001))

    usuario = controller.usuarios_repo.adicionar(Usuario("Gabriel"))
    controller.emprestar_livro(usuario.id, livro1.id)

    disponiveis = [l for l in controller.livros_repo.listar() if l.disponivel]
    assert livro2 in disponiveis
    assert livro1 not in disponiveis

# 8️⃣ Persistência simulada (salvar e carregar)
def test_persistencia_simulada(controller, tmp_path):
    arquivo = tmp_path / "livros.json"
    livros = [Livro("Clean Code", "Robert Martin", 2008)]
    controller.livros_repo._itens = livros.copy()  # simula livros no repositório

    from src.services.arquivo_service import ArquivoService
    ArquivoService.salvar_livros_json(str(arquivo), livros)
    carregados = ArquivoService.carregar_livros_json(str(arquivo))

    assert len(carregados) == 1
    assert carregados[0].titulo == "Clean Code"
