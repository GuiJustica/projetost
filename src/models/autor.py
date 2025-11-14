#src/models/autor.py
class Autor:
    def __init__(self, nome: str, descricao: str, id: int = None):
        if not nome or not nome.strip():
            raise ValueError("O nome do autor é obrigatório e não pode ser vazio.")
        if not descricao or not descricao.strip():
            raise ValueError("A descrição do autor é obrigatória e não pode ser vazia.")

        self.id = id
        self.nome = nome.strip()
        self.descricao = descricao.strip()

