from pydantic import BaseModel

class DailyResponse(BaseModel):
    date: str
    hash: str
    tamanho: int
