#src/validators/validador.py

from datetime import datetime
from exceptions.erros import (
    BibliotecaError,
    LivroDuplicadoError,
    EntradaInvalidaError,
    LivroIndisponivelError,
    UsuarioComPendenciaError
)


class Validador:
    @staticmethod
    def validar_usuario(nome, usuarios_existentes=None):
        nome = str(nome).strip() if nome is not None else ""

        if not nome:
            raise EntradaInvalidaError("nome", "O nome do usuário é obrigatório.")

        if usuarios_existentes:
            for usuario in usuarios_existentes:
                if usuario.nome.lower() == nome.lower():
                    raise EntradaInvalidaError("nome", f"O usuário '{nome}' já está cadastrado.")

    @staticmethod
    def validar_livro(titulo, autor, ano_publicacao, livros_existentes):
        titulo = str(titulo).strip() if titulo is not None else ""
        autor = str(autor).strip() if autor is not None else ""

        # Validação do título e autor
        if not titulo or not titulo.strip():
            raise EntradaInvalidaError("titulo", "Título não pode estar vazio ou em branco.")
        if len(titulo) < 3:
            raise EntradaInvalidaError("titulo", "Entrada inválida no campo 'titulo': deve ter ao menos 3 caracteres")
        if len(autor) < 3:
            raise EntradaInvalidaError("autor", "Entrada inválida no campo 'autor': deve ter ao menos 3 caracteres")

        ano_atual = datetime.now().year
        if int(ano_publicacao) > ano_atual:
            raise EntradaInvalidaError("ano_publicacao", "Entrada inválida no campo 'ano': não pode ser no futuro")

        # Verificação de livro duplicado
        for livro in livros_existentes:
            if livro.titulo.lower() == titulo.lower() and livro.autor.lower() == autor.lower():
                raise LivroDuplicadoError(titulo, autor)
    @staticmethod
    def validar_emprestimo(livro, usuario):
        if not livro:
            raise ValueError("Livro inválido.")
        if not usuario:
            raise ValueError("Usuário inválido.")
        if not livro.disponivel:
            raise LivroIndisponivelError(livro.titulo)


