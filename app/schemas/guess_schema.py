from pydantic import BaseModel

class GuessRequest(BaseModel):
    palavra: str

class GuessResponse(BaseModel):
    resultado: list[str]
    tentativas_restantes: int
    venceu: bool