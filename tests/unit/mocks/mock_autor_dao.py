#tests/unit/mocks/mock_autor_dao.py


from src.models.autor import Autor

class MockAutorDAO:
    def __init__(self):
        self.autores = []
        self._next_id = 1

    def criar(self, autor: Autor):
        if autor.id is None:
            autor.id = self._next_id
            self._next_id += 1
        self.autores.append(autor)
        return autor

    def listar(self):
        return self.autor  # retorna objetos Usuario

    def buscar_por_id(self, autor_id):
        for autor in self.autor:
            if autor.id == autor_id:
                return autor
        return None

    def atualizar(self, autor_id, novo_descricao):
        autor = self.buscar_por_id(autor_id)
        if autor:
            autor.descricao = novo_descricao
            return True
        return False

    def remover(self, autor_id):
        autor = self.buscar_por_id(autor_id)
        if autor:
            self.autores.remove(autor)
            return True
        return False
