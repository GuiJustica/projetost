class Usuario:
    def __init__(self, id, nome,multa=0):
        if not nome:
            raise ValueError("O nome do usuário é obrigatório.")
        if multa < 0:
            raise ValueError("A multa não pode ser negativa.")
        self.id = id
        self.nome = nome
        self.multa = 0.0
        self.bloqueado = False

    def __repr__(self):
        status = "Bloqueado" if self.bloqueado else "Ativo"
        return f"<Usuário {self.id}: {self.nome}, Multa: R${self.multa:.2f}, Status: {status}>"

    def aplicar_multa(self, valor):
        self.multa += valor
        if self.multa > 20:
            self.bloqueado = True

    def pagar_multa(self, valor):
        self.multa = max(0, self.multa - valor)
        if self.multa == 0:
            self.bloqueado = False
