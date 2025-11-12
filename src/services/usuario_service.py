from __future__ import annotations
from typing import Optional, List
from models.usuario import Usuario
from dao.usuario_dao import UsuarioDAO
from validators.validador import Validador
from exceptions.erros import BibliotecaError
from logger_config import configurar_logger
from dao.database import criar_conexao



logger = configurar_logger()
logger.info("👤 Serviço de usuários inicializado.")


class UsuarioService:
    """Serviço responsável pelas operações de CRUD e controle de usuários."""

    def __init__(self, dao: Optional[UsuarioDAO] = None) -> None:
        """
        Inicializa o serviço de usuários.

        Args:
            dao: Objeto DAO responsável pela persistência (padrão: UsuarioDAO real).
        """
        conn = criar_conexao()
        self.dao: UsuarioDAO = dao or UsuarioDAO(conn)

    def criar_usuario(self, nome: str) -> None:
        """
        Cadastra um novo usuário após validação.

        Args:
            nome: Nome do usuário.
         """
        try:
            usuarios_existentes = self.dao.listar()
            Validador.validar_usuario(nome,  [
                Usuario(r[1], r[0]) for r in usuarios_existentes
            ])

            novo_id = len(usuarios_existentes) + 1
            usuario = Usuario(nome, novo_id)
            self.dao.criar(usuario)

            logger.info(f"✅ Usuário '{nome}' cadastrado com sucesso.")
            print(f"✅ Usuário '{nome}' cadastrado com sucesso!")

        except BibliotecaError as e:
            logger.error(f"Erro ao criar usuário: {e}")
            print(f"❌ Erro: {e}")

    def listar_usuarios(self) -> List[Usuario]:
        """
        Retorna a lista de todos os usuários cadastrados.

        Returns:
            Uma lista de objetos Usuario.
        """
        return [Usuario(r[1], r[0]) for r in self.dao.listar()]

    def atualizar_usuario(self, usuario_id: int, novo_nome: str) -> None:
        """
        Atualiza os dados de um usuário existente.

        Args:
            usuario_id: ID do usuário.
            novo_nome: Novo nome.
        """
        if self.dao.atualizar(usuario_id, novo_nome):
            logger.info(f"✏️ Usuário {usuario_id} atualizado com sucesso.")
            print(f"✏️ Usuário {usuario_id} atualizado com sucesso!")
        else:
            logger.warning(f"Tentativa de atualizar usuário inexistente: ID {usuario_id}")
            print("⚠️ Usuário não encontrado.")

    def remover_usuario(self, usuario_id: int) -> None:
        """
        Remove um usuário do sistema.

        Args:
            usuario_id: ID do usuário a ser removido.
        """
        if self.dao.remover(usuario_id):
            logger.info(f"🗑️ Usuário {usuario_id} removido com sucesso.")
            print(f"🗑️ Usuário {usuario_id} removido com sucesso!")
        else:
            logger.warning(f"Tentativa de remover usuário inexistente: ID {usuario_id}")
            print("⚠️ Usuário não encontrado.")
