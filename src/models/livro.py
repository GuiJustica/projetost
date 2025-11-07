class Livro:
    def __init__(self, id, titulo, autor, ano_publicacao, disponivel=True):
        if not titulo or not autor:
            raise ValueError("Título e autor são obrigatórios.")
        if ano_publicacao <= 0:
            raise ValueError("Ano de publicação inválido.")

        self.id = id
        self.titulo = titulo
        self.autor = autor
        self.ano_publicacao = ano_publicacao
        self.disponivel = disponivel

    def __repr__(self):
        status = "Disponível" if self.disponivel else "Emprestado"
        return f"<Livro {self.id}: {self.titulo} ({status})>"
