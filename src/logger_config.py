import os
import logging
from  src.config import carregar_config

def configurar_logger():
    config = carregar_config()
    log_file = config["logging"]["file"]
    log_dir = os.path.dirname(log_file)
    os.makedirs(log_dir, exist_ok=True)  # 🔹 Cria a pasta se não existir

    logger = logging.getLogger("biblioteca_logger")
    logger.setLevel(config["logging"]["level"])

    handler_console = logging.StreamHandler()
    handler_file = logging.FileHandler(log_file, encoding="utf-8")

    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    handler_console.setFormatter(formatter)
    handler_file.setFormatter(formatter)

    logger.addHandler(handler_console)
    logger.addHandler(handler_file)

    return logger
