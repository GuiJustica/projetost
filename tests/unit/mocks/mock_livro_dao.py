#tests/unit/mocks/mock_livro_dao.py

class MockLivroRepository:
    def __init__(self):
        self.livros = []

    def adicionar(self, livro):
        self.livros.append(livro)

    def listar(self):
        return self.livros

    def buscar_por_titulo(self, titulo):
        for livro in self.livros:
            if livro.titulo == titulo:
                return livro
        return None
