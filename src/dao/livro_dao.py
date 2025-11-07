from dao.database import Database

class LivroDAO:
    def __init__(self):
        self.db = Database()

    def criar(self, livro):
        conn = self.db.conectar()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO livros (titulo, autor, ano_publicacao)
            VALUES (?, ?, ?)
        """, (livro.titulo, livro.autor, livro.ano_publicacao))
        conn.commit()
        conn.close()

    def listar(self):
        conn = self.db.conectar()
        cursor = conn.cursor()
        cursor.execute("SELECT id, titulo, autor, ano_publicacao FROM livros")
        rows = cursor.fetchall()
        conn.close()
        return rows

    def atualizar(self, livro_id, novo_titulo, novo_autor, novo_ano):
        conn = self.db.conectar()
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE livros
            SET titulo = ?, autor = ?, ano_publicacao = ?
            WHERE id = ?
        """, (novo_titulo, novo_autor, novo_ano, livro_id))
        conn.commit()
        atualizado = cursor.rowcount > 0
        conn.close()
        return atualizado

    def remover(self, livro_id):
        conn = self.db.conectar()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM livros WHERE id = ?", (livro_id,))
        conn.commit()
        removido = cursor.rowcount > 0
        conn.close()
        return removido
