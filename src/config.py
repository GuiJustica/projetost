import yaml
import os

def carregar_config():
    caminho = os.path.join(os.path.dirname(__file__), "../config.yaml")
    with open(caminho, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)

config = carregar_config()

# Caminho do diretório raiz do projeto
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

# Caminho absoluto e fixo do banco (sempre fora de src)
DB_PATH = os.path.join(BASE_DIR, "biblioteca.db")

print(f"[DEBUG] Usando banco de dados em: {DB_PATH}")
