from pydantic import BaseModel

class SalaCreate(BaseModel):
    nome: str
    capacidade: int
    bloco: str

class SalaOut(BaseModel):
    id: int
    nome: str
    capacidade: int
    bloco: str