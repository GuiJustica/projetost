#tests/unit/mocks/mock_usuario_dao.py


from src.models.usuario import Usuario

class MockUsuarioDAO:
    def __init__(self):
        self.usuarios = []
        self._next_id = 1

    def criar(self, usuario: Usuario):
        if usuario.id is None:
            usuario.id = self._next_id
            self._next_id += 1
        self.usuarios.append(usuario)
        return usuario

    def listar(self):
        return self.usuarios  # retorna objetos Usuario

    def buscar_por_id(self, usuario_id):
        for usuario in self.usuarios:
            if usuario.id == usuario_id:
                return usuario
        return None

    def atualizar(self, usuario_id, novo_nome):
        usuario = self.buscar_por_id(usuario_id)
        if usuario:
            usuario.nome = novo_nome
            return True
        return False

    def remover(self, usuario_id):
        usuario = self.buscar_por_id(usuario_id)
        if usuario:
            self.usuarios.remove(usuario)
            return True
        return False
