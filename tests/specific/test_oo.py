# tests/type_specific/test_oo.py
import pytest
from src.models.livro import Livro
from src.models.usuario import Usuario
from src.models.emprestimo import Emprestimo

def test_emprestimo_devolucao_encapsulamento():
    u = Usuario("Encap")
    l = Livro("Livro Enc", "Autor", 2000)
    e = Emprestimo(u, l)

    # verificar atributos privados / encapsulamento
    assert e.usuario.nome == "Encap"
    assert e.livro.titulo == "Livro Enc"

    # devolver altera estado interno do livro
    e.devolver()
    assert l.disponivel is True

def test_heranca_polimorfismo():
    # Dummy exemplo de polimorfismo
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

def test_metodos_abstratos():
    # exemplo simples usando ABC se tivesse método abstrato
    from abc import ABC, abstractmethod

    class Base(ABC):
        @abstractmethod
        def fazer_algo(self):
            pass

    class Concreto(Base):
        def fazer_algo(self):
            return 42

    obj = Concreto()
    assert obj.fazer_algo() == 42
