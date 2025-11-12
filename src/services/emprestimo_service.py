from datetime import datetime, timedelta
from typing import Optional, List  # Importando o List
from models.emprestimo import Emprestimo
from services.usuario_service import UsuarioService
from services.livro_service import LivroService
from logger_config import configurar_logger
from dao.emprestimo_dao import EmprestimoDAO
from dao.database import criar_conexao


logger = configurar_logger()
logger.info("📖 Serviço de empréstimo inicializado.")
DB_PATH = "biblioteca.db"

class EmprestimoService:

    def __init__(self, usuario_service: Optional[UsuarioService] = None,
                 livro_service: Optional[LivroService] = None) -> None:
        self.usuario_service = usuario_service or UsuarioService()
        self.livro_service = livro_service or LivroService()
        self.dao = EmprestimoDAO()  # Inicializa o DAO de empréstimos

    def criar_emprestimo(self, usuario_id: int, livro_id: int) -> Optional[Emprestimo]:
        """ Cria um novo empréstimo para um usuário e livro especificados. """
        # Busca usuário e livro diretamente
        usuario = next((u for u in self.usuario_service.listar_usuarios() if u.id == usuario_id), None)
        livro = next((l for l in self.livro_service.listar_livros() if l.id == livro_id), None)

        if not usuario:
            logger.warning("⚠️ Usuário não encontrado.")
            return None
        if not livro:
            logger.warning("⚠️ Livro não encontrado.")
            return None

        # Verifica se o livro está disponível
        if not livro.disponivel:
            print(f"❌ O livro '{livro.titulo}' já está emprestado.")
            return None

        # Registra o empréstimo no banco
        data_emprestimo = datetime.now()


        emprestimo = Emprestimo(None, usuario, livro, data_emprestimo)
        self.dao.criar(emprestimo)  # Cria o empréstimo no banco

        # Marca o livro como não disponível
        livro.disponivel = False

        # Retorna o objeto do empréstimo
        logger.info(f"✅ Empréstimo registrado: {livro.titulo} → {usuario.nome}")
        return emprestimo

    def listar_emprestimos(self) -> List[Emprestimo]:
        """ Retorna uma lista de todos os empréstimos registrados no sistema. """
        emprestimos = self.dao.listar()  # Recupera todos os empréstimos do banco
        logger.info(f"📜 {len(emprestimos)} empréstimos listados.")
        return emprestimos

    def remover_emprestimo(self, emprestimo_id: int) -> None:
        """Remove um empréstimo usando o ID."""
        if self.dao.remover_emprestimo(emprestimo_id):
            print(f"✅ Empréstimo ID {emprestimo_id} removido com sucesso!")
        else:
            print(f"⚠️ Empréstimo ID {emprestimo_id} não encontrado.")

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
