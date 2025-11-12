from src.controllers.biblioteca_controller import BibliotecaController

def test_fluxo_basico():
    controller = BibliotecaController()

    usuario = controller.cadastrar_usuario("Guilherme")
    livro = controller.cadastrar_livro("Clean Code", "Robert C. Martin")

    emprestimo = controller.emprestar_livro(usuario.id, livro.id)
    assert not livro.disponivel

    controller.devolver_livro(emprestimo.id)
    assert livro.disponivel
