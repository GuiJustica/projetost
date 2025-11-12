#src/models/livro.py

from typing import Any
from datetime import datetime

class Livro:
    """
    Representa um livro no sistema da biblioteca.
    """

    def __init__(self, id: int, titulo: str, autor: str, ano_publicacao: int, disponivel: bool = True):

        """
        Inicializa um objeto Livro.

        Args:
            id (int): Identificador único do livro.
            titulo (str): Título do livro.
            autor (str): Autor do livro.
            ano_publicacao (int): Ano de publicação.
            disponivel (bool): Define se o livro está disponível.
            **kwargs (Any): Ignora parâmetros extras vindos de arquivos.
        """

        if not titulo or not titulo.strip():
            raise ValueError("O título não pode ser vazio.")
        if ano_publicacao > datetime.now().year:
            raise ValueError("Ano de publicação inválido.")
        if ano_publicacao <= 0:
            raise ValueError("Ano não pode ser negativo.")

        self.id = id
        self.titulo = titulo
        self.autor = autor
        self.ano_publicacao = ano_publicacao
        self.disponivel = disponivel

    def __repr__(self):
        return f"<Livro {self.id}: {self.titulo} - {self.autor} ({self.ano_publicacao})>"
