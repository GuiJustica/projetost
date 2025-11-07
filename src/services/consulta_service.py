from models.livro import Livro
from models.usuario import Usuario

class ConsultaService:
    @staticmethod
    def buscar_livros(livros, titulo=None, autor=None, disponivel=None):
        resultados = livros

        if titulo:
            resultados = [l for l in resultados if titulo.lower() in l.titulo.lower()]
        if autor:
            resultados = [l for l in resultados if autor.lower() in l.autor.lower()]
        if disponivel is not None:
            resultados = [l for l in resultados if l.disponivel == disponivel]

        return resultados

    @staticmethod
    def ordenar_usuarios(usuarios, criterio="nome", reverso=False):
        if criterio == "nome":
            return sorted(usuarios, key=lambda u: u.nome, reverse=reverso)
        elif criterio == "multa":
            return sorted(usuarios, key=lambda u: u.multa, reverse=reverso)
        else:
            raise ValueError("Critério de ordenação inválido. Use 'nome' ou 'multa'.")
