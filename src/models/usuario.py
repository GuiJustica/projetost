#src/models/usuario.py
class Usuario:
    def __init__(self, nome: str, id: int = None):
        if not nome or not nome.strip():
            raise ValueError("O nome do usuário é obrigatório e não pode ser vazio.")
        self.id = id
        self.nome = nome.strip()

