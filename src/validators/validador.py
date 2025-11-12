#src/validators/validador.py

from datetime import datetime
from exceptions.erros import BibliotecaError,LivroDuplicadoError, EntradaInvalidaError


class Validador:
    @staticmethod
    def validar_usuario(nome, usuarios_existentes=None):
        if not nome:
            raise BibliotecaError("O nome do usuário é obrigatório.")

        if usuarios_existentes:
            for usuario in usuarios_existentes:
                if usuario.nome.lower() == nome.lower():
                    raise BibliotecaError(f"O usuário '{nome}' já está cadastrado.")

    @staticmethod
    def validar_livro(titulo, autor, ano_publicacao, livros_existentes):
        titulo = str(titulo).strip() if titulo is not None else ""
        autor = str(autor).strip() if autor is not None else ""
        """Valida os dados de um livro antes do cadastro."""
        # 🔹 Título e autor obrigatórios e com tamanho mínimo
        if len(titulo) < 3:
            raise EntradaInvalidaError("titulo", "deve ter ao menos 3 caracteres")
        if len(autor) < 3:
            raise EntradaInvalidaError("autor", "deve ter ao menos 3 caracteres")

        ano_atual = datetime.now().year
        if int(ano_publicacao) > ano_atual:
            raise EntradaInvalidaError("ano_publicacao", "não pode ser no futuro")

        for livro in livros_existentes:
            if livro.titulo.lower() == titulo.lower() and livro.autor.lower() == autor.lower():
                raise LivroDuplicadoError(titulo, autor)
    @staticmethod
    def validar_emprestimo(livro, usuario):
        if not livro:
            raise BibliotecaError("Livro inexistente.")
        if not usuario:
            raise BibliotecaError("Usuário inexistente.")
        if not livro.disponivel:
            raise BibliotecaError("Livro já emprestado.")
        if usuario.bloqueado:
            raise BibliotecaError("Usuário bloqueado.")

