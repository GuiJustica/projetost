# tests/unit/mocks/mock_emprestimo_dao.py
from src.models.emprestimo import Emprestimo

class MockEmprestimoDAO:
    def __init__(self):
        self.emprestimos = []
        self.next_id = 1

    def criar(self, emprestimo: Emprestimo):
        emprestimo.id = self.next_id
        self.next_id += 1
        self.emprestimos.append(emprestimo)
        return emprestimo

    def listar(self):
        return self.emprestimos
