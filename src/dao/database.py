import sqlite3
import os
import logging
from config import DB_PATH  # Supondo que DB_PATH seja um caminho absoluto do banco de dados

def criar_conexao():
    """Cria a conexão com o banco de dados"""
    caminho_db = os.path.join(os.path.dirname(__file__), DB_PATH)  # Usa o DB_PATH para definir o caminho do banco
    logging.debug(f"[DEBUG] Usando banco de dados em: {caminho_db}")
    conn = sqlite3.connect(caminho_db, check_same_thread=False)
    return conn
