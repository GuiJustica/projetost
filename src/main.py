#src/main.py

from services.livro_service import LivroService
from services.usuario_service import UsuarioService
from services.emprestimo_service import EmprestimoService
from services.autor_service import AutorService
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
    9. Registrar Empréstimo
    10. Listar Empréstimos
    11. Devolver Livro
    12. Cadastrar Autor
    13. Listar Autor
    14. Atualizar Autor
    15. Remover Autor
    0. Sair
    """)

def main():
    livro_service = LivroService()
    autor_service  = AutorService()
    usuario_service = UsuarioService()
    emprestimo_service = EmprestimoService(usuario_service, livro_service)

    while True:
        menu()
        opcao = input("Escolha uma opção: ")

        match opcao:
            # LIVRO
            case "1":
                livro_service.criar_livro(input("Título: "), input("Autor: "), int(input("Ano: ")))
            case "2":
                livros = livro_service.listar_livros()
                if livros:
                    for l in livros:
                        print(f"[{l.id}] {l.titulo} — {l.autor} ({l.ano_publicacao})")
                else:
                    print("📚 Nenhum livro cadastrado.")
            case "3":
                livro_service.atualizar_livro(int(input("ID: ")), input("Novo título: "), input("Novo autor: "),int(input("Novo ano: ")))
            case "4":
                livro_service.remover_livro(int(input("ID: ")))

            # USUÁRIO
            case "5":
                usuario_service.criar_usuario(input("Nome: "))
            case "6":
                usuario = usuario_service.listar_usuarios()

                if usuario:
                    for u in usuario:
                        print(f"[{u.id}] {u.nome}")
                else:
                    print("📚 Nenhum usuário cadastrado.")
            case "7":
                usuario_service.atualizar_usuario(int(input("ID: ")), input("Novo nome: "))
            case "8":
                usuario_service.remover_usuario(int(input("ID: ")))


            # EMPRÉSTIMO
            case "9":
                emprestimo_service.criar_emprestimo(int(input("ID do Usuário: ")), int(input("ID do Livro: ")))
            case "10":
                emprestimo = emprestimo_service.listar_emprestimos()
                if emprestimo:
                    for e in emprestimo:
                        print(f"[{e.id}] Usuário: {e.usuario.nome} — Livro: {e.livro.titulo} — Data: {e.data_emprestimo}")
                else:
                    print("📖 Nenhum empréstimo registrado.")
            case "11":
                emprestimo_id = int(input("ID do Empréstimo: ")) # busca o objeto pelo ID
                if emprestimo_id:
                    emprestimo_service.remover_emprestimo(emprestimo_id)
                else:
                    print("⚠️ Empréstimo não encontrado.")


            # Autor
            case "12":
                autor_service.criar_autor(input("Nome: "), input("Descrição: "))
            case "13":
                autor = autor_service.listar_autor()

                if autor:
                    for u in autor:
                        print(f"[{u.id}] {u.nome} {u.descricao}")
                else:
                    print("📚 Nenhum autor cadastrado.")
            case "14":
                autor_service.atualizar_autor(int(input("ID: ")), input("Nova descricao: "))
            case "15":
                autor_service.remover_autor(int(input("ID: ")))


            # SAIR
            case "0":
                print("👋 Encerrando o sistema...")
                break

            case _:
                print("⚠️ Opção inválida.")





if __name__ == "__main__":
    main()
