from abc import ABC, abstractmethod

class BaseDAO(ABC):
    """Interface base para os DAOs, garantindo consistência entre implementações."""

    @abstractmethod
    def criar(self, obj):
        pass

    @abstractmethod
    def listar(self):
        pass

    @abstractmethod
    def atualizar(self, obj):
        pass

    @abstractmethod
    def remover(self, obj_id):
        pass
