# tests/type_specific/test_oo.py
import pytest
from abc import ABC, abstractmethod
from src.models.livro import Livro
from src.models.usuario import Usuario
from src.models.emprestimo import Emprestimo

# 1️⃣ Teste de Encapsulamento e Devolução
def test_emprestimo_encapsulamento():
    u = Usuario("Encap")
    l = Livro(1,"Livro Enc", "Autor", 2000)
    e = Emprestimo(u, l)

    # verificar atributos do objeto
    assert e.usuario.nome == "Encap"
    assert e.livro.titulo == "Livro Enc"

    # devolver altera estado interno do livro
    e.devolver()
    assert l.disponivel is True

# 2️⃣ Teste de Herança e Polimorfismo
def test_heranca_polimorfismo():
    class Pessoa:
        def falar(self):
            return "..."

    class UsuarioEspecial(Usuario, Pessoa):
        def falar(self):
            return f"Sou {self.nome}"

    u = UsuarioEspecial("Polimorfo")
    assert isinstance(u, Usuario)
    assert isinstance(u, Pessoa)
    assert u.falar() == "Sou Polimorfo"

# 3️⃣ Teste de Métodos Abstratos
def test_metodo_abstrato():
    class Base(ABC):
        @abstractmethod
        def fazer_algo(self):
            pass

    class Concreto(Base):
        def fazer_algo(self):
            return 42

    obj = Concreto()
    assert obj.fazer_algo() == 42
