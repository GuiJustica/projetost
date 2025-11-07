class Categoria:
    def __init__(self, id, nome):
        self.id = id
        self.nome = nome

    def __repr__(self):
        return f"<Categoria {self.id}: {self.nome}>"
