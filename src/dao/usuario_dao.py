
from dao.database import criar_conexao
from models.usuario import Usuario
import sqlite3
from config import DB_PATH


class UsuarioDAO:
    def __init__(self, conn: sqlite3.Connection):
        self.conn = criar_conexao()  # Usando a função criar_conexao
        self._criar_tabela()

    def _criar_tabela(self):
        """Cria a tabela de usuários caso ela não exista."""
        cursor = self.conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS usuarios (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL
            )
        """)
        self.conn.commit()

    def criar(self, usuario):
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO usuarios (nome)
            VALUES (?)
        """, (usuario.nome,))
        conn.commit()
        conn.close()

    def listar(self):
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT id, nome FROM usuarios")
        rows = cursor.fetchall()
        conn.close()
        return rows

    def atualizar(self, usuario_id, novo_nome):
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("UPDATE usuarios SET nome = ? WHERE id = ?", (novo_nome, usuario_id))
        conn.commit()
        atualizado = cursor.rowcount > 0
        conn.close()
        return atualizado

    def remover(self, usuario_id):
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM usuarios WHERE id = ?", (usuario_id,))
        conn.commit()
        removido = cursor.rowcount > 0
        conn.close()
        return removido

    def buscar_por_id(self, usuario_id: int) -> Usuario | None:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT id, nome FROM usuarios WHERE id = ?", (usuario_id,))
        row = cursor.fetchone()
        conn.close()
        if row:
            return Usuario(id=row[0], nome=row[1])
        return None

