#src/dao/mock_livro_dao.py

class MockLivroDAO:
    """Simula o comportamento do LivroDAO, sem usar banco real."""
    def __init__(self):
        # Armazena os livros em memória
        self.livros = []
        self.next_id = 1

    def criar(self, livro):
        livro.id = self.next_id
        self.next_id += 1
        self.livros.append(livro)

    def listar(self):
        # Retorna uma lista no mesmo formato da query real
        return [(l.id, l.titulo, l.autor, l.ano_publicacao) for l in self.livros]

    def atualizar(self, livro_id, novo_titulo, novo_autor, novo_ano):
        for l in self.livros:
            if l.id == livro_id:
                l.titulo = novo_titulo
                l.autor = novo_autor
                l.ano_publicacao = novo_ano
                return True
        return False

    def remover(self, livro_id):
        for l in self.livros:
            if l.id == livro_id:
                self.livros.remove(l)
                return True
        return False
