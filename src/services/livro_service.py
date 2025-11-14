from __future__ import annotations
from typing import Optional, List
from models.livro import Livro
from dao.livro_dao import LivroDAO
from validators.validador import Validador
from exceptions.erros import BibliotecaError,LivroDuplicadoError
from logger_config import configurar_logger
from dao.database import criar_conexao





logger = configurar_logger()
logger.info("📘 Serviço de livros inicializado.")




class LivroService:
    """Serviço responsável pelas operações de CRUD e consulta de livros."""

    def __init__(self, dao: Optional[LivroDAO] = None) -> None:
        """
        Inicializa o serviço de livros.

        Args:
            dao: Objeto DAO responsável pela persistência (padrão: LivroDAO real).
        """
        # Passando a conexão para o LivroDAO
        conn = criar_conexao()  # Obtém a conexão do banco de dados
        self.dao: LivroDAO = dao or LivroDAO(conn)  # Passando a conexão para o LivroDAO

    def criar_livro(self, titulo: str, autor: str, ano_publicacao: int) -> None:

        """
        Cria e cadastra um novo livro após validação.

        Args:
            titulo: Título do livro.
            autor: Nome do autor.
            ano_publicacao: Ano de publicação do livro.
        """

        try:
            # Garante que campos de texto são strings seguras
            titulo = str(titulo).strip()
            autor = str(autor).strip()

            # Valida o livro (ano_publicacao pode permanecer int)
            livros_existentes = self.dao.listar()
            for l in livros_existentes:
                if l[1].strip().lower() == titulo.lower() and l[2].strip().lower() == autor.lower():
                    raise LivroDuplicadoError(f"O livro '{titulo}' de {autor} já está cadastrado.")

            Validador.validar_livro(
                titulo, autor, ano_publicacao,
                [Livro(r[0], r[1], r[2], int(r[3])) for r in livros_existentes]
            )

            novo_id = len(livros_existentes) + 1
            livro = Livro(novo_id, titulo, autor, ano_publicacao)
            self.dao.criar(livro)

            logger.info(f"✅ Livro '{titulo}' cadastrado com sucesso.")
            print(f"✅ Livro '{titulo}' cadastrado com sucesso!")
            return livro

        except BibliotecaError as e:
            logger.error(f"Erro ao criar livro: {e}")
            print(f"❌ Erro: {e}")

    def listar_livros(self) -> List[Livro]:
        """
        Retorna a lista de todos os livros cadastrados.

        Returns:
            Uma lista de objetos Livro.
        """
        livros = self.dao.listar()
        return [Livro(r[0], r[1], r[2], r[3]) for r in livros]

    def atualizar_livro(self, livro_id: int, novo_titulo: str,
                        novo_autor: str, novo_ano: int, disponivel: bool = True) -> None:
        """
        Atualiza os dados de um livro existente.

        Args:
            livro_id: ID do livro a ser atualizado.
            novo_titulo: Novo título.
            novo_autor: Novo autor.
            novo_ano: Novo ano de publicação.
            disponivel: Novo status de disponibilidade do livro.
        """
        if self.dao.atualizar(livro_id, novo_titulo, novo_autor, novo_ano,disponivel):
            logger.info(f"✏️ Livro {livro_id} atualizado com sucesso.")
            print(f"✏️ Livro {livro_id} atualizado com sucesso!")
        else:
            logger.warning(f"Tentativa de atualizar livro inexistente: ID {livro_id}")
            print("⚠️ Livro não encontrado.")

    def remover_livro(self, livro_id: int) -> None:
        """
        Remove um livro do sistema.

        Args:
            livro_id: ID do livro a ser removido.
        """
        if self.dao.remover(livro_id):
            logger.info(f"🗑️ Livro {livro_id} removido com sucesso.")
            print(f"🗑️ Livro {livro_id} removido com sucesso!")
        else:
            logger.warning(f"Tentativa de remover livro inexistente: ID {livro_id}")
            print("⚠️ Livro não encontrado.")

    def consultar_livros(
        self,
        filtro_por: Optional[str] = None,
        valor: Optional[str] = None,
        ordenar_por: Optional[str] = None,
        ordem_crescente: bool = True
    ) -> None:
        """
        Consulta livros com base em filtros e ordenação.

        Args:
            filtro_por: Campo de filtro ("titulo", "autor" ou "ano").
            valor: Valor a ser buscado.
            ordenar_por: Campo para ordenação.
            ordem_crescente: Define a direção da ordenação (padrão: True).
        """
        livros = self.listar_livros()  # Agora trabalha com objetos Livro

        # 🔍 Aplicar filtro
        if filtro_por and valor:
            if filtro_por == "titulo":
                livros = [l for l in livros if valor.lower() in l.titulo.lower()]
            elif filtro_por == "autor":
                livros = [l for l in livros if valor.lower() in l.autor.lower()]
            elif filtro_por == "ano":
                try:
                    valor_int = int(valor)
                    livros = [l for l in livros if l.ano_publicacao == valor_int]
                except ValueError:
                    logger.warning("Valor inválido para filtro de ano.")
                    print("⚠️ Valor inválido para filtro de ano.")

        # ↕️ Ordenar resultados
        if ordenar_por in ["titulo", "autor", "ano_publicacao"]:
            if ordenar_por == "titulo":
                livros.sort(key=lambda l: l.titulo, reverse=not ordem_crescente)
            elif ordenar_por == "autor":
                livros.sort(key=lambda l: l.autor, reverse=not ordem_crescente)
            elif ordenar_por == "ano_publicacao":
                livros.sort(key=lambda l: l.ano_publicacao, reverse=not ordem_crescente)

        # 📋 Exibir resultados
        if livros:
            print("\n📚 Resultados da consulta:")
            for livro in livros:
                print(f"- {livro.titulo} | {livro.autor} | {livro.ano_publicacao}")
        else:
            logger.info("Nenhum livro encontrado na consulta.")
            print("❌ Nenhum livro encontrado com os critérios informados.")


    def buscar_por_id(self, livro_id: int) -> Livro | None:
        return self.dao.buscar_por_id(livro_id)
