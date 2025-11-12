# src/models/emprestimo.py
from datetime import datetime, timedelta
from models.usuario import Usuario
from models.livro import Livro

class Emprestimo:
    """
    Representa o empréstimo de um livro para um usuário.
    """

    def __init__(self, id: int, usuario: Usuario, livro: Livro,
                 data_emprestimo: datetime = None):
        self.id = id
        self.usuario = usuario
        self.livro = livro
        self.data_emprestimo = data_emprestimo or datetime.now()


    def __repr__(self):
        status = "Devolvido" if self.devolvido else "Em andamento"
        return (f"<Empréstimo {self.id}: Usuário={self.usuario.nome}, "
                f"Livro={self.livro.titulo}, Status={status}>")
