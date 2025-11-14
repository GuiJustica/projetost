from datetime import datetime, timedelta
from typing import Optional, List  # Importando o List
from src.models.emprestimo import Emprestimo
from src.services.usuario_service import UsuarioService
from src.services.livro_service import LivroService
from src.logger_config import configurar_logger
from src.dao.emprestimo_dao import EmprestimoDAO
from src.dao.database import criar_conexao
from src.dao.livro_dao import LivroDAO
from src.exceptions.erros import EntradaInvalidaError, LivroIndisponivelError


logger = configurar_logger()
logger.info("📖 Serviço de empréstimo inicializado.")
DB_PATH = "biblioteca.db"

class EmprestimoService:

    def __init__(self, usuario_service: Optional[UsuarioService] = None,
                 livro_service: Optional[LivroService] = None,
                 emprestimo_dao: Optional[EmprestimoDAO] = None) -> None:
        self.usuario_service = usuario_service or UsuarioService()
        self.livro_service = livro_service or LivroService()
        self.dao = emprestimo_dao or EmprestimoDAO()    # Inicializa o DAO de empréstimos

    def criar_emprestimo(self, usuario_id: int, livro_id: int) -> Optional[Emprestimo]:
        """ Cria um novo empréstimo para um usuário e livro especificados. """
        # Busca usuário e livro diretamente do banco
        usuario = next((u for u in self.usuario_service.listar_usuarios() if u.id == usuario_id), None)

        livro = self.livro_service.buscar_por_id(livro_id)

        if not usuario:
            logger.warning("⚠️ Usuário não encontrado.")
            raise EntradaInvalidaError("usuario", "Usuário não encontrado")
        if not livro:
            logger.warning("⚠️ Livro não encontrado.")
            raise EntradaInvalidaError("livro", "Livro não encontrado")

        # Verifica se o livro está disponível
        if not livro.disponivel:
            print(f"❌ O livro '{livro.titulo}' já está emprestado.")
            raise LivroIndisponivelError(livro.titulo)

        # Registra o empréstimo no banco
        data_emprestimo = datetime.now()
        emprestimo = Emprestimo(None, usuario, livro, data_emprestimo)
        self.dao.criar(emprestimo)

        # Marca o livro como não disponível
        self.livro_service.atualizar_livro(
            livro.id, livro.titulo, livro.autor, livro.ano_publicacao, disponivel=False
        )
        livro.disponivel = False

        logger.info(f"✅ Empréstimo registrado: {livro.titulo} → {usuario.nome}")
        return emprestimo

    def listar_emprestimos(self) -> List[Emprestimo]:
        """ Retorna uma lista de todos os empréstimos registrados no sistema. """
        emprestimos = self.dao.listar()  # Recupera todos os empréstimos do banco
        logger.info(f"📜 {len(emprestimos)} empréstimos listados.")
        return emprestimos

    def remover_emprestimo(self, emprestimo_id: int) -> None:
        """Remove um empréstimo usando o ID e atualiza o livro para disponível."""
        emprestimo = self.dao.buscar_por_id(emprestimo_id)  # Busca primeiro o empréstimo
        if not emprestimo:
            print(f"⚠️ Empréstimo ID {emprestimo_id} não encontrado.")
            return

        # Atualiza o livro como disponível no banco de dados
        livro = emprestimo.livro
        livro.disponivel = True  # Marca como disponível

        # Atualiza o livro no banco, pois a disponibilidade mudou
        self.livro_service.atualizar_livro(
            livro.id, livro.titulo, livro.autor, livro.ano_publicacao, livro.disponivel
        )

        # Agora remove o empréstimo
        if self.dao.remover_emprestimo(emprestimo_id):
            print(f"✅ Empréstimo ID {emprestimo_id} removido com sucesso!")
            logger.info(f"✅ Empréstimo ID {emprestimo_id} removido com sucesso.")
        else:
            print(f"⚠️ Erro ao remover o empréstimo ID {emprestimo_id}.")
            logger.warning(f"⚠️ Erro ao remover o empréstimo ID {emprestimo_id}.")

    def buscar_por_id(self, emprestimo_id: int) -> Optional[Emprestimo]:
            """
            Busca um empréstimo pelo ID.

            Args:
                emprestimo_id: ID do empréstimo a ser buscado.

            Returns:
                Um objeto Emprestimo ou None se não encontrado.
            """
            emprestimo = self.dao.buscar_por_id(emprestimo_id)
            if emprestimo:
                return emprestimo
            else:
                print(f"⚠️ Empréstimo com ID {emprestimo_id} não encontrado.")
                return None
