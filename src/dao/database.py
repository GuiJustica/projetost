import sqlite3
import os

class Database:
    def __init__(self, nome_arquivo="biblioteca.db"):
        self.nome_arquivo = nome_arquivo
        self._criar_tabelas()

    def conectar(self):
        return sqlite3.connect(self.nome_arquivo)

    def _criar_tabelas(self):
        if not os.path.exists(self.nome_arquivo):
            conn = self.conectar()
            cursor = conn.cursor()

            cursor.execute("""
                CREATE TABLE IF NOT EXISTS usuarios (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nome TEXT NOT NULL,
                    multa REAL DEFAULT 0
                )
            """)

            cursor.execute("""
                CREATE TABLE IF NOT EXISTS livros (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    titulo TEXT NOT NULL,
                    autor TEXT NOT NULL,
                    ano_publicacao INTEGER NOT NULL
                )
            """)

            conn.commit()
            conn.close()
