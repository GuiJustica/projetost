#src/repositories/base_repository.py


class BaseRepository:
    def __init__(self):
        self._itens = []
        self.proximo_id = 1

    def adicionar(self, item):
        if not hasattr(item, 'id') or item.id is None:
                    item.id = self.proximo_id
                    self.proximo_id += 1
        else:
            # atualiza o próximo id para não repetir
            if item.id >= self.proximo_id:
                self.proximo_id = item.id + 1

        self._itens.append(item)
        return item

    def listar(self):
        return self._itens

    def buscar_por_id(self, id):
        for item in self._itens:
            if item.id == id:
                return item
        return None

    def remover(self, id):
        self._itens = [item for item in self._itens if item.id != id]


    def atualizar(self, id_, novo_objeto):
        for i, item in enumerate(self._itens):
            if item.id == id_:
                self._itens[i] = novo_objeto
                return novo_objeto
        raise KeyError("Registro não encontrado.")
