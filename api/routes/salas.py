from fastapi import APIRouter, HTTPException
from schemas.sala import SalaCreate, SalaOut
from services.reserva_services import criar_sala, listar_salas

router = APIRouter(prefix="/salas", tags=["Salas"])


@router.post("", response_model=SalaOut)
def criar_sala_route(data: SalaCreate):
    """Cria uma nova sala com validação de capacidade"""
    sala, erro = criar_sala(nome=data.nome, capacidade=data.capacidade, bloco=data.bloco)
    
    if erro:
        raise HTTPException(status_code=400, detail=erro)
    
    return sala


@router.get("")
def listar_salas_route():
    """Lista todas as salas"""
    salas = listar_salas()
    return [
        {
            "id": s.id,
            "nome": s.nome,
            "capacidade": s.capacidade,
            "bloco": s.bloco
        }
        for s in salas
    ]