from models.emprestimo import Emprestimo
from datetime import datetime
from exceptions.erros import LivroIndisponivelError, UsuarioComPendenciaError

class EmprestimoService:
    def __init__(self, usuario_service, livro_service):
        self.emprestimos = []
        self.usuario_service = usuario_service
        self.livro_service = livro_service

    def criar_emprestimo(self, usuario_id, livro_id):
        usuario = next((u for u in self.usuario_service.usuarios if u.id == usuario_id), None)
        livro = next((l for l in self.livro_service.livros if l.id == livro_id), None)

        # Validações de existência
        if not usuario:
            print("⚠️ Usuário não encontrado.")
            return
        if not livro:
            print("⚠️ Livro não encontrado.")
            return

        # ✅ Regra 1: Limite de empréstimos e multa pendente
        emprestimos_ativos = [e for e in self.emprestimos if e.usuario.id == usuario.id and e.ativo]
        if len(emprestimos_ativos) >= 3:
            print("❌ Usuário já possui 3 empréstimos ativos.")
            return
        if usuario.multa > 0:
            print(f"❌ Usuário possui multa pendente de R${usuario.multa:.2f}.")
            return
        if usuario.bloqueado:
            print("🚫 Usuário bloqueado! Pague as multas para liberar novos empréstimos.")
            return

        # Livro disponível?
        if livro.emprestado:
            print("❌ Este livro já está emprestado.")
            return

        # Registrar empréstimo
        livro.emprestado = True
        novo_id = len(self.emprestimos) + 1
        emprestimo = Emprestimo(novo_id, usuario, livro)
        self.emprestimos.append(emprestimo)
        print(f"✅ Empréstimo registrado com sucesso! ({livro.titulo} → {usuario.nome})")

    def listar_emprestimos(self):
        if not self.emprestimos:
            print("Nenhum empréstimo registrado.")
        else:
            for emp in self.emprestimos:
                print(emp)

    def devolver_livro(self, emprestimo_id):
        emprestimo = next((e for e in self.emprestimos if e.id == emprestimo_id and e.ativo), None)
        if not emprestimo:
            print("⚠️ Empréstimo não encontrado ou já devolvido.")
            return

        emprestimo.ativo = False
        emprestimo.livro.emprestado = False
        emprestimo.data_devolucao = datetime.now()

        # ✅ Regra 2: Cálculo de multa por atraso
        dias_atraso = (emprestimo.data_devolucao - emprestimo.prazo).days
        if dias_atraso > 0:
            multa = dias_atraso * 2.0
            emprestimo.usuario.aplicar_multa(multa)
            print(f"⚠️ Livro devolvido com {dias_atraso} dias de atraso. Multa: R${multa:.2f}")
        else:
            print("✅ Livro devolvido no prazo.")

        # ✅ Regra 3: Bloqueio automático se multa > 20
        if emprestimo.usuario.bloqueado:
            print("🚫 Usuário bloqueado por excesso de multas (acima de R$20,00).")

    def pagar_multa(self, usuario_id, valor):
        usuario = next((u for u in self.usuario_service.usuarios if u.id == usuario_id), None)
        if not usuario:
            print("⚠️ Usuário não encontrado.")
            return

        usuario.pagar_multa(valor)
        print(f"💰 Multa paga! Novo saldo: R${usuario.multa:.2f}")



    def realizar_emprestimo(usuario, livro, emprestimos):
        if not livro.disponivel:
            raise LivroIndisponivelError(livro.titulo)
        if usuario.multa > 0:
            raise UsuarioComPendenciaError(usuario.nome)

        novo = Emprestimo(len(emprestimos)+1, usuario, livro)
        emprestimos.append(novo)
        livro.disponivel = False
        return novo

