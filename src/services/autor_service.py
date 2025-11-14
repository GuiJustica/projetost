from __future__ import annotations
from typing import Optional, List
from models.autor import Autor
from dao.autor_dao import AutorDAO
from validators.validador import Validador
from exceptions.erros import BibliotecaError
from logger_config import configurar_logger
from dao.database import criar_conexao
from validators.validador import Validador
from exceptions.erros import EntradaInvalidaError


logger = configurar_logger()
logger.info("👤 Serviço de autor inicializado.")


class AutorService:
    """Serviço responsável pelas operações de CRUD e controle de autor."""

    def __init__(self, dao: Optional[AutorDAO] = None) -> None:
        """
        Inicializa o serviço de autor.

        Args:
            dao: Objeto DAO responsável pela persistência (padrão: AutorDAO real).
        """
        conn = criar_conexao()

        self.dao: AutorDAO = dao or AutorDAO(conn)

    def criar_autor(self, nome: str, descricao:str) -> None:
        """
        Cadastra um novo autor após validação.

        Args:
            nome: Nome do autor.
         """
        try:

            autors_existentes = self.dao.listar()
            Validador.validar_usuario(nome,  [
                Autor(r[1], r[2]) for r in autors_existentes
            ])

            novo_id = len(autors_existentes) + 1
            autor = Autor(nome,descricao, novo_id)
            self.dao.criar(autor)

            logger.info(f"✅ Autor '{nome}' cadastrado com sucesso.")
            print(f"✅ Autor '{nome}' cadastrado com sucesso!")
            return autor

        except BibliotecaError as e:
            logger.error(f"Erro ao criar Autor: {e}")
            print(f"❌ Erro: {e}")
            return None




    def listar_autor(self) -> List[Autor]:
        """
        Retorna a lista de todos os autor cadastrados.

        Returns:
            Uma lista de objetos autor.
        """
        return [Autor(r[1], r[2], r[0]) for r in self.dao.listar()]

    def atualizar_autor(self, autor_id: int, descricao: str) -> None:
        """
        Atualiza os dados de um autor existente.

        Args:
            autor_id: ID do autor.
            descricao: Novo descricao.
        """
        if self.dao.atualizar(autor_id, descricao):
            logger.info(f"✏️ Usuário {autor_id} atualizado com sucesso.")
            print(f"✏️ Usuário {autor_id} atualizado com sucesso!")
        else:
            logger.warning(f"Tentativa de atualizar usuário inexistente: ID {autor_id}")
            print("⚠️ Usuário não encontrado.")

    def remover_autor(self, autor_id: int) -> None:
        """
        Remove um autor do sistema.

        Args:
            autor_id: ID do autor a ser removido.
        """
        if self.dao.remover(autor_id):
            logger.info(f"🗑️ Usuário {autor_id} removido com sucesso.")
            print(f"🗑️ Autor {autor_id} removido com sucesso!")
        else:
            logger.warning(f"Tentativa de remover usuário inexistente: ID {autor_id}")
            print("⚠️ Autor não encontrado.")
