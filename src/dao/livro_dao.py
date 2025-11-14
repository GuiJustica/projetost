
#src/dao/livro_dao.py
from src.dao.database import criar_conexao
from src.models.livro import Livro

import sqlite3
from src.config import DB_PATH


class LivroDAO:
    def __init__(self,conn: sqlite3.Connection):
        self.conn = criar_conexao()  # Usando a função criar_conexao
        self._criar_tabela()


    def _criar_tabela(self):
        cursor = self.conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS livros (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                titulo TEXT NOT NULL,
                autor TEXT NOT NULL,
                ano_publicacao INTEGER NOT NULL,
                disponivel BOOLEAN DEFAULT 1
            )
        """)
        self.conn.commit()



    def criar(self, livro):
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO livros (titulo, autor, ano_publicacao, disponivel)
            VALUES (?, ?, ?, ?)
        """, (livro.titulo, livro.autor, livro.ano_publicacao, int(livro.disponivel)))
        conn.commit()
        conn.close()

    def listar(self):
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT id, titulo, autor, ano_publicacao, disponivel FROM livros")
        rows = cursor.fetchall()
        conn.close()
        return rows

    def atualizar(self, livro_id, novo_titulo, novo_autor, novo_ano, disponivel: bool) -> bool:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE livros
            SET titulo = ?, autor = ?, ano_publicacao = ?, disponivel = ?
            WHERE id = ?
        """, (novo_titulo, novo_autor, novo_ano, int(disponivel), livro_id))  # Convertendo bool para int
        conn.commit()
        atualizado = cursor.rowcount > 0
        conn.close()
        return atualizado

    def remover(self, livro_id):
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM livros WHERE id = ?", (livro_id,))
        conn.commit()
        removido = cursor.rowcount > 0
        conn.close()
        return removido

    def atualizar_disponibilidade(self, livro_id, disponivel):
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE livros SET disponivel = ? WHERE id = ?
        """, (int(disponivel), livro_id))
        conn.commit()
        conn.close()

    def buscar_por_id(self, livro_id: int) -> Livro | None:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT id, titulo, autor, ano_publicacao, disponivel FROM livros WHERE id = ?", (livro_id,))
        row = cursor.fetchone()
        conn.close()

        if row:
            id, titulo, autor, ano, disponivel = row
            livro = Livro(id=id, titulo=titulo, autor=autor, ano_publicacao=ano, disponivel=bool(disponivel))
            return livro
        return None
