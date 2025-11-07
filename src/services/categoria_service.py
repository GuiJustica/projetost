from models.categoria import Categoria

class CategoriaService:
    def __init__(self):
        self.categorias = []

    def criar_categoria(self, nome):
        novo_id = len(self.categorias) + 1
        categoria = Categoria(novo_id, nome)
        self.categorias.append(categoria)
        print(f"✅ Categoria '{nome}' cadastrada com sucesso!")

    def listar_categorias(self):
        if not self.categorias:
            print("Nenhuma categoria cadastrada.")
        else:
            for categoria in self.categorias:
                print(categoria)

    def atualizar_categoria(self, categoria_id, novo_nome):
        for categoria in self.categorias:
            if categoria.id == categoria_id:
                categoria.nome = novo_nome
                print(f"✏️ Categoria {categoria_id} atualizada com sucesso!")
                return
        print("⚠️ Categoria não encontrada.")

    def remover_categoria(self, categoria_id):
        for categoria in self.categorias:
            if categoria.id == categoria_id:
                self.categorias.remove(categoria)
                print(f"🗑️ Categoria {categoria_id} removida com sucesso!")
                return
        print("⚠️ Categoria não encontrada.")
