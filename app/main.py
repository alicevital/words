import uuid
from app.schemas.daily_schema import DailyResponse
from app.schemas.guess_schema import GuessRequest, GuessResponse
from fastapi import FastAPI, Request, Response, HTTPException
from app.game.words import carregar_palavras, normalizar, palavra_do_dia, palavra_valida
from app.game.logic import avaliar_tentativa
import os
import hashlib
from datetime import date
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

tentativas_por_usuario = {}
MAX_TENTATIVAS = 5
SECRET = os.getenv("HASH_SECRET", "dev_secret")


def gerar_session_id():
    return str(uuid.uuid4())


def gerar_hash(palavra: str) -> str:
    hoje = date.today().isoformat()
    combinado = f"{palavra}:{hoje}:{SECRET}"
    return hashlib.sha256(combinado.encode()).hexdigest()


@app.on_event("startup")
def startup():
    carregar_palavras()


@app.get("/daily")
def daily() -> DailyResponse:
    palavra = palavra_do_dia()
    return {
        "date": date.today().isoformat(),
        "tamanho": len(palavra),
        "hash": gerar_hash(palavra)
    }


@app.post("/guess")
def guess(req: GuessRequest, request: Request, response: Response) -> GuessResponse:
    palavra = normalizar(req.palavra)
    resposta = palavra_do_dia()

    session_id = request.cookies.get("session_id")

    if not session_id:
        session_id = gerar_session_id()
        response.set_cookie(key="session_id", value=session_id)

    if session_id not in tentativas_por_usuario:
        tentativas_por_usuario[session_id] = []

    tentativas = tentativas_por_usuario[session_id]

    if len(tentativas) >= MAX_TENTATIVAS:
        raise HTTPException(status_code=403, detail="limite de tentativas atingido!")

    if not palavra_valida(palavra):
        raise HTTPException(status_code=400, detail="palavra inválida")

    if len(palavra) != 5:
        raise HTTPException(status_code=400, detail="tamanho de palavra inválido")

    resultado = avaliar_tentativa(palavra, resposta)

    tentativas.append(palavra)

    venceu = all(r == "correct" for r in resultado)

    return {
        "resultado": resultado,
        "tentativas_restantes": MAX_TENTATIVAS - len(tentativas),
        "venceu": venceu
    }