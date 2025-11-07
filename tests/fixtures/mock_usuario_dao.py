from src.models.usuario import Usuario

class MockUsuarioDAO:
    def __init__(self):
        # Simula um "banco" em memória
        self.usuarios = []

    def criar(self, usuario: Usuario):
        self.usuarios.append(usuario)

    def listar(self):
        return self.usuarios
