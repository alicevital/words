from datetime import date
import unicodedata
import os
from venv import logger

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))

PALAVRAS = []
PALAVRAS_SET = set()

def normalizar(palavra: str) -> str:
    palavra = palavra.lower()

    return ''.join(
        c for c in unicodedata.normalize('NFD', palavra)
        if unicodedata.category(c) != 'Mn'
    )

def carregar_palavras():
    global PALAVRAS, PALAVRAS_SET

    caminho = os.getenv(
        "PALAVRAS_PATH",
        os.path.join(BASE_DIR, "data", "palavras.txt")
    )

    logger.info("Carregando palavras de caminho!{caminho}")

    if not os.path.exists(caminho):
        raise FileNotFoundError(f"Arquivo não foi encontrado! {caminho}")
    
    with open(caminho, encoding="utf-8") as f:
        palavras_raw = [linha.strip().lower() for linha in f if linha.strip()]

    palavras = []
    for p in palavras_raw:
        p_norm = normalizar(p)

        if len(p_norm) == 5 and p_norm.isalpha():
            palavras.append(p_norm)

    PALAVRAS = palavras
    PALAVRAS_SET = set(PALAVRAS)

    logger.info("Palavras carregadas")


def palavra_valida(palavra: str) -> bool:
    return palavra in PALAVRAS_SET


def palavra_do_dia() -> str:
    base = date(2022, 1, 1)
    hoje = date.today()
    index = (hoje - base).days
    return PALAVRAS[index % len(PALAVRAS)]