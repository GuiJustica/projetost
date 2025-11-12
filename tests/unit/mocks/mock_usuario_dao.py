#tests/unit/mocks/mock_usuario_dao.py


from src.models.usuario import Usuario

class MockUsuarioRepository:
    def __init__(self):
        self.usuarios = []
        self.next_id = 1

    def criar(self, usuario):
        usuario.id = self.next_id
        self.next_id += 1
        self.usuarios.append((usuario.id, usuario.nome))

    def listar(self):
        return self.usuarios

    def atualizar(self, usuario_id, novo_nome):
        for i, (uid, nome) in enumerate(self.usuarios):
            if uid == usuario_id:
                self.usuarios[i] = (uid, novo_nome)
                return True
        return False

    def remover(self, usuario_id):
        for i, (uid, _, _) in enumerate(self.usuarios):
            if uid == usuario_id:
                del self.usuarios[i]
                return True
        return False
