from models.livro import Livro
from validators.validador import Validador
from dao.livro_dao import LivroDAO
from exceptions.erros import BibliotecaError

class LivroService:
    def __init__(self):
        self.dao = LivroDAO()

    def criar_livro(self, titulo, autor, ano_publicacao):
        try:
            livros_existentes = self.dao.listar()
            Validador.validar_livro(titulo, autor, ano_publicacao, [
                Livro(r[1], r[2], r[3]) for r in livros_existentes
            ])

            livro = Livro(titulo, autor, ano_publicacao)
            self.dao.criar(livro)
            print(f"✅ Livro '{titulo}' cadastrado com sucesso!")

        except BibliotecaError as e:
            print(f"❌ Erro: {e}")

    def listar_livros(self):
        livros = self.dao.listar()
        if livros:
            print("\n📚 Livros cadastrados:")
            for _, titulo, autor, ano in livros:
                print(f"- {titulo} | {autor} | {ano}")
        else:
            print("⚠️ Nenhum livro cadastrado.")

    def atualizar_livro(self, livro_id, novo_titulo, novo_autor, novo_ano):
        if self.dao.atualizar(livro_id, novo_titulo, novo_autor, novo_ano):
            print(f"✏️ Livro {livro_id} atualizado com sucesso!")
        else:
            print("⚠️ Livro não encontrado.")

    def remover_livro(self, livro_id):
        if self.dao.remover(livro_id):
            print(f"🗑️ Livro {livro_id} removido com sucesso!")
        else:
            print("⚠️ Livro não encontrado.")

    def consultar_livros(self, filtro_por=None, valor=None, ordenar_por=None, ordem_crescente=True):
        livros = self.dao.listar()

        # 🔍 Filtros
        if filtro_por and valor:
            if filtro_por == "titulo":
                livros = [l for l in livros if valor.lower() in l[1].lower()]
            elif filtro_por == "autor":
                livros = [l for l in livros if valor.lower() in l[2].lower()]
            elif filtro_por == "ano":
                try:
                    valor = int(valor)
                    livros = [l for l in livros if l[3] == valor]
                except ValueError:
                    print("⚠️ Valor inválido para filtro de ano.")

        # ↕️ Ordenação
        if ordenar_por in ["titulo", "autor", "ano_publicacao"]:
            idx = {"titulo": 1, "autor": 2, "ano_publicacao": 3}[ordenar_por]
            livros.sort(key=lambda l: l[idx], reverse=not ordem_crescente)

        # 📋 Exibe
        if livros:
            print("\n📚 Resultados da consulta:")
            for _, titulo, autor, ano in livros:
                print(f"- {titulo} | {autor} | {ano}")
        else:
            print("❌ Nenhum livro encontrado com os critérios informados.")
