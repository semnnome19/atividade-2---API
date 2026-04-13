from fastapi import APIRouter, HTTPException
from schemas.reserva import ReservaCreate, ReservaOut
from services.reserva_services import (
    criar_reserva,
    listar_reservas,
    listar_reservas_usuario,
    buscar_reserva,
    cancelar_reserva,
    finalizar_reserva,
    mudar_status
)

router = APIRouter(prefix="/reservas", tags=["Reservas"])


@router.post("", response_model=ReservaOut)
def criar_reserva_route(data: ReservaCreate):
    """Cria uma nova reserva com múltiplas validações"""
    reserva, erro = criar_reserva(
        usuario_id=data.usuario_id,
        sala_id=data.sala_id,
        data=data.data,
        hora_inicio=data.hora_inicio,
        hora_fim=data.hora_fim
    )
    
    if erro:
        raise HTTPException(status_code=400, detail=erro)
    
    return reserva


@router.get("")
def listar_reservas_route():
    """Lista todas as reservas"""
    reservas = listar_reservas()
    return [
        {
            "id": r.id,
            "usuario_id": r.usuario_id,
            "sala_id": r.sala_id,
            "data": r.data,
            "hora_inicio": r.hora_inicio,
            "hora_fim": r.hora_fim,
            "status": r.status,
            "duracao_horas": r.duracao_em_horas()
        }
        for r in reservas
    ]


@router.get("/usuario/{usuario_id}")
def listar_reservas_usuario_route(usuario_id: int):
    """Lista todas as reservas de um usuário específico"""
    reservas = listar_reservas_usuario(usuario_id)
    return [
        {
            "id": r.id,
            "usuario_id": r.usuario_id,
            "sala_id": r.sala_id,
            "data": r.data,
            "hora_inicio": r.hora_inicio,
            "hora_fim": r.hora_fim,
            "status": r.status,
            "duracao_horas": r.duracao_em_horas()
        }
        for r in reservas
    ]


@router.get("/{reserva_id}")
def buscar_reserva_route(reserva_id: int):
    """Busca uma reserva pelo ID"""
    reserva = buscar_reserva(reserva_id)
    
    if reserva is None:
        raise HTTPException(status_code=404, detail="Reserva não encontrada")
    
    return {
        "id": reserva.id,
        "usuario_id": reserva.usuario_id,
        "sala_id": reserva.sala_id,
        "data": reserva.data,
        "hora_inicio": reserva.hora_inicio,
        "hora_fim": reserva.hora_fim,
        "status": reserva.status,
        "duracao_horas": reserva.duracao_em_horas()
    }


@router.put("/{reserva_id}/cancelar")
def cancelar_reserva_route(reserva_id: int):
    """Cancela uma reserva ativa"""
    resultado = cancelar_reserva(reserva_id)
    
    if not resultado:
        raise HTTPException(
            status_code=400,
            detail="Não foi possível cancelar a reserva (não encontrada ou já cancelada)"
        )
    
    reserva = buscar_reserva(reserva_id)
    return {
        "mensagem": "Reserva cancelada com sucesso",
        "reserva": {
            "id": reserva.id,
            "usuario_id": reserva.usuario_id,
            "sala_id": reserva.sala_id,
            "data": reserva.data,
            "hora_inicio": reserva.hora_inicio,
            "hora_fim": reserva.hora_fim,
            "status": reserva.status
        }
    }


@router.put("/{reserva_id}/finalizar")
def finalizar_reserva_route(reserva_id: int, hora_atual: str):
    """Finaliza uma reserva ativa (hora_atual no formato HH:MM)"""
    resultado = finalizar_reserva(reserva_id, hora_atual)
    
    if not resultado:
        raise HTTPException(
            status_code=400,
            detail="Não foi possível finalizar a reserva (não encontrada, já finalizada ou horário inválido)"
        )
    
    reserva = buscar_reserva(reserva_id)
    return {
        "mensagem": "Reserva finalizada com sucesso",
        "reserva": {
            "id": reserva.id,
            "usuario_id": reserva.usuario_id,
            "sala_id": reserva.sala_id,
            "data": reserva.data,
            "hora_inicio": reserva.hora_inicio,
            "hora_fim": reserva.hora_fim,
            "status": reserva.status,
            "duracao_horas": reserva.duracao_em_horas()
        }
    }


@router.put("/{reserva_id}/status")
def mudar_status_route(reserva_id: int, novo_status: str):
    """
    Muda o status de uma reserva
    Status válidos: 'active', 'cancelled', 'completed'
    """
    sucesso, erro = mudar_status(reserva_id, novo_status)
    
    if erro:
        status_code = 404 if "Reserva não encontrada" in erro else 400
        raise HTTPException(status_code=status_code, detail=erro)
    
    reserva = buscar_reserva(reserva_id)
    return {
        "mensagem": f"Status alterado para '{novo_status}' com sucesso",
        "reserva": {
            "id": reserva.id,
            "usuario_id": reserva.usuario_id,
            "sala_id": reserva.sala_id,
            "data": reserva.data,
            "hora_inicio": reserva.hora_inicio,
            "hora_fim": reserva.hora_fim,
            "status": reserva.status,
            "duracao_horas": reserva.duracao_em_horas()
        }
    }