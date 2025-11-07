from models.usuario import Usuario
from validators.validador import Validador
from dao.usuario_dao import UsuarioDAO

class UsuarioService:
    def __init__(self):
        self.dao = UsuarioDAO()

    def criar_usuario(self, nome, multa=0):
        # Lista todos os usuários já cadastrados
        usuarios_existentes = self.dao.listar()
        Validador.validar_usuario(nome, multa)

        # Cria o novo usuário e salva no banco
        usuario = Usuario(nome, multa)
        self.dao.criar(usuario)
        print(f"✅ Usuário '{nome}' cadastrado com sucesso!")

    def listar_usuarios(self):
        usuarios = self.dao.listar()
        if usuarios:
            print("\n👥 Usuários cadastrados:")
            for nome, multa in usuarios:
                print(f"- {nome} | Multa: R${multa:.2f}")
        else:
            print("⚠️ Nenhum usuário cadastrado.")

    def atualizar_usuario(self, usuario_id, novo_nome):
        if self.dao.atualizar(usuario_id, novo_nome):
            print(f"✏️ Usuário {usuario_id} atualizado com sucesso!")
        else:
            print("⚠️ Usuário não encontrado.")

    def remover_usuario(self, usuario_id):
        if self.dao.remover(usuario_id):
            print(f"🗑️ Usuário {usuario_id} removido com sucesso!")
        else:
            print("⚠️ Usuário não encontrado.")

    def consultar_usuarios(self, filtro_por=None, valor=None, ordenar_por=None, ordem_crescente=True):
        usuarios = self.dao.listar()

        # 🔍 Filtro
        if filtro_por and valor:
            if filtro_por == "nome":
                usuarios = [u for u in usuarios if valor.lower() in u[0].lower()]
            elif filtro_por == "multa":
                try:
                    valor = float(valor)
                    usuarios = [u for u in usuarios if float(u[1]) == valor]
                except ValueError:
                    print("⚠️ Valor inválido para filtro de multa.")

        # ↕️ Ordenação
        if ordenar_por == "nome":
            usuarios.sort(key=lambda u: u[0], reverse=not ordem_crescente)
        elif ordenar_por == "multa":
            usuarios.sort(key=lambda u: u[1], reverse=not ordem_crescente)

        # 🧾 Resultado
        if usuarios:
            print("\n👥 Resultados da consulta:")
            for nome, multa in usuarios:
                print(f"- {nome} | Multa: R${multa:.2f}")
        else:
            print("❌ Nenhum usuário encontrado com os critérios informados.")
