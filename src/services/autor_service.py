from models.autor import Autor

class AutorService:
    def __init__(self):
        self.autores = []

    def criar_autor(self, nome):
        novo_id = len(self.autores) + 1
        autor = Autor(novo_id, nome)
        self.autores.append(autor)
        print(f"✅ Autor '{nome}' cadastrado com sucesso!")

    def listar_autores(self):
        if not self.autores:
            print("Nenhum autor cadastrado.")
        else:
            for autor in self.autores:
                print(autor)

    def atualizar_autor(self, autor_id, novo_nome):
        for autor in self.autores:
            if autor.id == autor_id:
                autor.nome = novo_nome
                print(f"✏️ Autor {autor_id} atualizado com sucesso!")
                return
        print("⚠️ Autor não encontrado.")

    def remover_autor(self, autor_id):
        for autor in self.autores:
            if autor.id == autor_id:
                self.autores.remove(autor)
                print(f"🗑️ Autor {autor_id} removido com sucesso!")
                return
        print("⚠️ Autor não encontrado.")
