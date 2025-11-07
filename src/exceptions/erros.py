class BibliotecaError(Exception):
    """Erro base do sistema de biblioteca."""
    def __init__(self, mensagem="Algo deu errado, tente novamente mais tarde."):
        super().__init__(mensagem)


class LivroIndisponivelError(BibliotecaError):
    def __init__(self, livro_titulo):
        super().__init__(f"O livro '{livro_titulo}' não está disponível para empréstimo.")


class UsuarioComPendenciaError(BibliotecaError):
    def __init__(self, usuario_nome):
        super().__init__(f"O usuário '{usuario_nome}' possui pendências e não pode realizar empréstimos.")


class EntradaInvalidaError(BibliotecaError):
    def __init__(self, campo, mensagem):
        super().__init__(f"Entrada inválida no campo '{campo}': {mensagem}")


class DadosInvalidosError(BibliotecaError):
    def __init__(self, mensagem):
        super().__init__(f"Dados inválidos: {mensagem}")


class LivroNaoEncontradoError(BibliotecaError):
    def __init__(self, livro_titulo):
        super().__init__(f"O livro '{livro_titulo}' não foi encontrado.")


class LivroDuplicadoError(BibliotecaError):
    def __init__(self, titulo,autor):
        super().__init__(f"O livro '{titulo}','{autor}' já está cadastrado.")
