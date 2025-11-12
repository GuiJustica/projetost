# src/dao/mock_usuario_dao.py


class MockUsuarioDAO:
    """Simula o comportamento do UsuarioDAO, sem usar banco real."""
    def __init__(self):
        self.usuarios = []
        self.next_id = 1

    def criar(self, usuario):
        usuario.id = self.next_id
        self.next_id += 1
        self.usuarios.append(usuario)

    def listar(self):
        return [(u.id, u.nome) for u in self.usuarios]

    def atualizar(self, usuario_id, novo_nome):
        for u in self.usuarios:
            if u.id == usuario_id:
                u.nome = novo_nome
                return True
        return False

    def remover(self, usuario_id):
        for u in self.usuarios:
            if u.id == usuario_id:
                self.usuarios.remove(u)
                return True
        return False
