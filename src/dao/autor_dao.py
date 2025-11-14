
from src.dao.database import criar_conexao
from src.models.autor import Autor
import sqlite3
from src.config import DB_PATH


class AutorDAO:
    def __init__(self, conn: sqlite3.Connection):
        self.conn = criar_conexao()  # Usando a função criar_conexao
        self._criar_tabela()

    def _criar_tabela(self):
        """Cria a tabela de usuários caso ela não exista."""
        cursor = self.conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS autores (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                descricao TEXT NOT NULL
            )
        """)
        self.conn.commit()

    def criar(self, autor):
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO autores (nome, descricao)
            VALUES (?,?)
        """, (autor.nome,autor.descricao))
        conn.commit()
        conn.close()

    def listar(self):
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT id, nome ,descricao FROM autores")
        rows = cursor.fetchall()
        conn.close()
        return rows

    def atualizar(self, autor_id, descricao):
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("UPDATE autores SET descricao = ? WHERE id = ?", (descricao, autor_id))
        conn.commit()
        atualizado = cursor.rowcount > 0
        conn.close()
        return atualizado

    def remover(self, autor_id):
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM autores WHERE id = ?", (autor_id,))
        conn.commit()
        removido = cursor.rowcount > 0
        conn.close()
        return removido

    def buscar_por_id(self, autor_id: int) -> Autor | None:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT id, nome FROM autores WHERE id = ?", (autor_id,))
        row = cursor.fetchone()
        conn.close()
        if row:
            return Autor(id=row[0], nome=row[1])
        return None

