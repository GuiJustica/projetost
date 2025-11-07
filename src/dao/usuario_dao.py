from dao.database import Database

class UsuarioDAO:
    def __init__(self):
        self.db = Database()

    def criar(self, usuario):
        conn = self.db.conectar()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO usuarios (nome, multa)
            VALUES (?, ?)
        """, (usuario.nome, usuario.multa))
        conn.commit()
        conn.close()

    def listar(self):
        conn = self.db.conectar()
        cursor = conn.cursor()
        cursor.execute("SELECT id, nome, multa FROM usuarios")
        rows = cursor.fetchall()
        conn.close()
        return [(r[1], r[2]) for r in rows]

    def atualizar(self, usuario_id, novo_nome):
        conn = self.db.conectar()
        cursor = conn.cursor()
        cursor.execute("UPDATE usuarios SET nome = ? WHERE id = ?", (novo_nome, usuario_id))
        conn.commit()
        atualizado = cursor.rowcount > 0
        conn.close()
        return atualizado

    def remover(self, usuario_id):
        conn = self.db.conectar()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM usuarios WHERE id = ?", (usuario_id,))
        conn.commit()
        removido = cursor.rowcount > 0
        conn.close()
        return removido
