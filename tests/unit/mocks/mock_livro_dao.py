from src.models.livro import Livro

class MockLivroDAO:
    def __init__(self):
        self.livros = []
        self.next_id = 1

    def criar(self, livro: Livro):
        livro.id = self.next_id
        self.next_id += 1
        self.livros.append(livro)
        return livro  # Retornando o objeto Livro

    def listar(self):
        return self.livros  # Já são objetos Livro

    def buscar_por_id(self, livro_id: int):
        for livro in self.livros:
            if livro.id == livro_id:
                return livro
        return None

    def atualizar(self, livro_id: int, novo_titulo, novo_autor, novo_ano, disponivel=True):
        for i, l in enumerate(self.livros):
            if l.id == livro_id:
                self.livros[i].titulo = novo_titulo
                self.livros[i].autor = novo_autor
                self.livros[i].ano_publicacao = novo_ano
                self.livros[i].disponivel = disponivel
                return True
        return False

    def remover(self, livro_id: int):
        for i, l in enumerate(self.livros):
            if l.id == livro_id:
                self.livros.pop(i)
                return True
        return False
