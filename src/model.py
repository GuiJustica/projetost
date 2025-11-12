class Livro:
    """Representa um livro no sistema de biblioteca."""

    def __init__(self, id: int, titulo: str, autor: str, disponivel: bool = True):
        self.id = id
        self.titulo = titulo
        self.autor = autor
        self.disponivel = disponivel

    def __repr__(self) -> str:
        status = "Disponível" if self.disponivel else "Emprestado"
        return f"<Livro {self.id}: {self.titulo} ({status})>"


class Usuario:
    """Representa um usuário cadastrado no sistema."""

    def __init__(self, id: int, nome: str,ativo: bool = True):
        self.id = id
        self.nome = nome
        self.ativo = ativo

    def __repr__(self) -> str:
        status = "Ativo" if self.ativo else "Inativo"
        return f"<Usuário {self.id}: {self.nome}>"
