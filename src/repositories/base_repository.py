class BaseRepository:
    def __init__(self):
        self._dados = {}
        self._contador = 1

    def criar(self, objeto):
        objeto.id = self._contador
        self._dados[self._contador] = objeto
        self._contador += 1
        return objeto

    def listar(self):
        return list(self._dados.values())

    def buscar_por_id(self, id_):
        return self._dados.get(id_)

    def atualizar(self, id_, novo_objeto):
        if id_ not in self._dados:
            raise KeyError("Registro não encontrado.")
        self._dados[id_] = novo_objeto
        return novo_objeto

    def deletar(self, id_):
        if id_ in self._dados:
            del self._dados[id_]
        else:
            raise KeyError("Registro não encontrado.")
