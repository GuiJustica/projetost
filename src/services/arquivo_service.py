import os
import json
from src.models.livro import Livro
from src.models.usuario import Usuario
class ArquivoService:
    @staticmethod
    def salvar_livros_json(caminho: str, livros: list):
        try:
            with open(caminho, "w", encoding="utf-8") as arquivo:
                json.dump([livro.__dict__ for livro in livros], arquivo, ensure_ascii=False, indent=4)
        except Exception as e:
            print(f"Erro ao salvar livros: {e}")
            raise

    @staticmethod
    def carregar_livros_json(caminho: str):
        if not os.path.exists(caminho):
            return []
        try:
            with open(caminho, "r", encoding="utf-8") as arquivo:
                dados = json.load(arquivo)
                livros = []
                for d in dados:
                    livros.append(
                        Livro(
                            id=d.get("id"),
                            titulo=d.get("titulo"),
                            autor=d.get("autor"),
                            ano_publicacao=d.get("ano_publicacao", 0)

                        )
                    )
                return livros
        except Exception as e:
            print(f"Erro ao carregar livros: {e}")
            return []
    @staticmethod
    def salvar_usuarios_json(caminho: str, usuarios: list):
        with open(caminho, "w", encoding="utf-8") as arquivo:
            json.dump([u.__dict__ for u in usuarios], arquivo, ensure_ascii=False, indent=4)

    @staticmethod
    def carregar_usuarios_json(caminho: str):
        if not os.path.exists(caminho):
            return []
        with open(caminho, "r", encoding="utf-8") as arquivo:
            dados = json.load(arquivo)
            return [Usuario(d.get("nome")) for d in dados]
