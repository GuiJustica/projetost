# src/dao/emprestimo_dao.py
import sqlite3
from models.emprestimo import Emprestimo
from dao.database import criar_conexao
from config import DB_PATH
from datetime import datetime
from dao.usuario_dao import UsuarioDAO
from dao.livro_dao import LivroDAO
from typing import Optional

from logger_config import configurar_logger
logger = configurar_logger()
class EmprestimoDAO:

    def __init__(self):
        self.conn = criar_conexao()  # Conexão com o banco de dados
        self.livro_dao = LivroDAO(self.conn)
        self.usuario_dao = UsuarioDAO(self.conn)
        self._criar_tabela()

    def _criar_tabela(self):
        """ Cria a tabela de empréstimos, se não existir. """
        try:
            cursor = self.conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS emprestimos (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    livro_id INTEGER NOT NULL,
                    usuario_id INTEGER NOT NULL,
                    data_emprestimo TEXT NOT NULL,
                    FOREIGN KEY (livro_id) REFERENCES livros(id),
                    FOREIGN KEY (usuario_id) REFERENCES usuarios(id)
                )
            """)
            self.conn.commit()
        except sqlite3.Error as e:
            print(f"⚠️ Erro ao criar tabela de empréstimos: {e}")

    def criar(self, emprestimo: Emprestimo):
        """ Cria um novo empréstimo no banco de dados. """
        cursor = self.conn.cursor()
        cursor.execute("""
            INSERT INTO emprestimos (livro_id, usuario_id, data_emprestimo)
            VALUES (?, ?, ?)
        """, (
            emprestimo.livro.id,
            emprestimo.usuario.id,
            emprestimo.data_emprestimo.strftime("%Y-%m-%d %H:%M:%S")

        ))
        self.conn.commit()

    def listar(self):
        conn = self.conn
        cursor = conn.cursor()
        cursor.execute("""
            SELECT id, livro_id, usuario_id, data_emprestimo
            FROM emprestimos
        """)
        rows = cursor.fetchall()

        # Passando a conexão 'conn' para os DAOs de Usuario e Livro
        usuario_dao = UsuarioDAO(conn)  # Passando a conexão para o DAO de Usuario
        livro_dao = LivroDAO(conn)  # Passando a conexão para o DAO de Livro

        emprestimos = []
        for r in rows:
            id, livro_id, usuario_id, data_emp = r

            # Recuperar o objeto Livro e Usuario pelo ID
            livro = livro_dao.buscar_por_id(livro_id)
            usuario = usuario_dao.buscar_por_id(usuario_id)

            if livro and usuario:
                emprestimos.append(Emprestimo(
                    id=id,
                    usuario=usuario,
                    livro=livro,
                    data_emprestimo=datetime.fromisoformat(data_emp)

                ))

        return emprestimos

    def buscar_por_id(self, emprestimo_id: int) -> Optional[Emprestimo]:
        """Busca um empréstimo pelo ID."""
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT id, livro_id, usuario_id, data_emprestimo
            FROM emprestimos
            WHERE id = ?
        """, (emprestimo_id,))
        row = cursor.fetchone()

        if row:
            id, livro_id, usuario_id, data_emprestimo = row

            # Buscar o livro e o usuário pelos seus IDs
            livro = self.livro_dao.buscar_por_id(livro_id)
            usuario = self.usuario_dao.buscar_por_id(usuario_id)

            if livro and usuario:
                return Emprestimo(
                    id=id,
                    livro=livro,
                    usuario=usuario,
                    data_emprestimo=datetime.fromisoformat(data_emprestimo)
                )
            else:
                logger.warning(f"⚠️ Livro ou Usuário não encontrado para o Empréstimo ID {emprestimo_id}.")
                return None
        return None

    def remover_emprestimo(self, emprestimo_id: int) -> bool:
        """Remove um empréstimo do banco de dados com base no ID."""
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        # Remover o empréstimo do banco
        cursor.execute("DELETE FROM emprestimos WHERE id = ?", (emprestimo_id,))
        conn.commit()

        if cursor.rowcount > 0:  # Verifica se alguma linha foi deletada
            conn.close()
            logger.info(f"✅ Empréstimo ID {emprestimo_id} removido com sucesso.")
            return True
        else:
            conn.close()
            logger.warning(f"⚠️ Empréstimo ID {emprestimo_id} não encontrado.")
            return False
