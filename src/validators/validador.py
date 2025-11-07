from datetime import datetime
from exceptions.erros import LivroDuplicadoError, EntradaInvalidaError


class Validador:
    @staticmethod
    def validar_usuario(nome, multa=0):
        """Valida os dados de um usuário antes do cadastro."""
        if not nome or len(nome.strip()) == 0:
            raise EntradaInvalidaError("nome", "não pode ser vazio")

        if multa < 0:
            raise EntradaInvalidaError("multa", "não pode ser negativa")

    @staticmethod
    def validar_livro(titulo, autor, ano_publicacao, livros_existentes):
        """Valida os dados de um livro antes do cadastro."""
        # 🔹 Título e autor obrigatórios e com tamanho mínimo
        if not titulo or len(titulo.strip()) < 3:
            raise EntradaInvalidaError("titulo", "deve ter ao menos 3 caracteres")

        if not autor or len(autor.strip()) < 3:
            raise EntradaInvalidaError("autor", "deve ter ao menos 3 caracteres")

        # 🔹 Ano futuro
        ano_atual = datetime.now().year
        if ano_publicacao > ano_atual:
            raise EntradaInvalidaError("ano_publicacao", "não pode ser no futuro")

        # 🔹 Livro duplicado (mesmo título e autor)
        for livro in livros_existentes:
            if livro.titulo.lower() == titulo.lower() and livro.autor.lower() == autor.lower():
                raise LivroDuplicadoError(titulo, autor)
