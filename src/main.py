from services.livro_service import LivroService
from services.usuario_service import UsuarioService
from services.autor_service import AutorService
from services.categoria_service import CategoriaService
from services.emprestimo_service import EmprestimoService

def menu():
    print("""
    === 📚 Sistema de Biblioteca ===
    1. Cadastrar Livro
    2. Listar Livros
    3. Atualizar Livro
    4. Remover Livro
    5. Cadastrar Usuário
    6. Listar Usuários
    7. Atualizar Usuário
    8. Remover Usuário
    9. Cadastrar Autor
    10. Listar Autores
    11. Atualizar Autor
    12. Remover Autor
    13. Cadastrar Categoria
    14. Listar Categorias
    15. Atualizar Categoria
    16. Remover Categoria
    17. Registrar Empréstimo
    18. Listar Empréstimos
    19. Devolver Livro
    0. Sair
    """)

def main():
    livro_service = LivroService()
    usuario_service = UsuarioService()
    autor_service = AutorService()
    categoria_service = CategoriaService()
    emprestimo_service = EmprestimoService(usuario_service, livro_service)

    while True:
        menu()
        opcao = input("Escolha uma opção: ")

        match opcao:
            # LIVRO
            case "1":
                livro_service.criar_livro(input("Título: "), input("Autor: "))
            case "2":
                livro_service.listar_livros()
            case "3":
                livro_service.atualizar_livro(int(input("ID: ")), input("Novo título: "), input("Novo autor: "))
            case "4":
                livro_service.remover_livro(int(input("ID: ")))

            # USUÁRIO
            case "5":
                usuario_service.criar_usuario(input("Nome: "))
            case "6":
                usuario_service.listar_usuarios()
            case "7":
                usuario_service.atualizar_usuario(int(input("ID: ")), input("Novo nome: "))
            case "8":
                usuario_service.remover_usuario(int(input("ID: ")))

            # AUTOR
            case "9":
                autor_service.criar_autor(input("Nome: "))
            case "10":
                autor_service.listar_autores()
            case "11":
                autor_service.atualizar_autor(int(input("ID: ")), input("Novo nome: "))
            case "12":
                autor_service.remover_autor(int(input("ID: ")))

            # CATEGORIA
            case "13":
                categoria_service.criar_categoria(input("Nome: "))
            case "14":
                categoria_service.listar_categorias()
            case "15":
                categoria_service.atualizar_categoria(int(input("ID: ")), input("Novo nome: "))
            case "16":
                categoria_service.remover_categoria(int(input("ID: ")))

            # EMPRÉSTIMO
            case "17":
                emprestimo_service.criar_emprestimo(int(input("ID do Usuário: ")), int(input("ID do Livro: ")))
            case "18":
                emprestimo_service.listar_emprestimos()
            case "19":
                emprestimo_service.devolver_livro(int(input("ID do Empréstimo: ")))
            case "20":
                emprestimo_service.pagar_multa(int(input("ID do Usuário: ")), float(input("Valor a pagar: ")))

            # SAIR
            case "0":
                print("👋 Encerrando o sistema...")
                break

            case _:
                print("⚠️ Opção inválida.")



from services.livro_service import LivroService
from services.usuario_service import UsuarioService
from exceptions.erros import BibliotecaError

if __name__ == "__main__":
    livros = LivroService()
    usuarios = UsuarioService()

    livros.criar_livro("Clean Code", "Robert C. Martin", 2008)
    livros.criar_livro("Python Essencial", "Mark Lutz", 2013)

    usuarios.criar_usuario("Guilherme Justiça")
    usuarios.criar_usuario("Ana Souza")

    print("\n📚 Livros no banco de dados:")
    livros.listar_livros()

    print("\n👥 Usuários no banco de dados:")
    usuarios.listar_usuarios()
