from src.models.livro import Livro

class MockLivroDAO:
    def __init__(self):
        self.livros = []

    def criar(self, livro: Livro):
        self.livros.append(livro)

    def listar(self):
        return self.livros
