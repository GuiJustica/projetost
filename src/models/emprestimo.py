from datetime import datetime, timedelta

class Emprestimo:
    def __init__(self, id, usuario, livro, ativo=True):
        self.id = id
        self.usuario = usuario
        self.livro = livro
        self.ativo = ativo
        self.data_emprestimo = datetime.now()
        self.data_devolucao = None
        self.prazo = self.data_emprestimo + timedelta(days=7)  # 7 dias

    def __repr__(self):
        status = "Ativo" if self.ativo else "Devolvido"
        return f"<Empréstimo {self.id} - {self.usuario.nome}, '{self.livro.titulo}', Status: {status}>"
