from fastapi import APIRouter, HTTPException
from schemas.usuario import UsuarioCreate, UsuarioOut
from services.reserva_services import criar_usuario, listar_usuarios

router = APIRouter(prefix="/usuarios", tags=["Usuários"])


@router.post("", response_model=UsuarioOut)
def criar_usuario_route(data: UsuarioCreate):
    """Cria um novo usuário com validação de email duplicado"""
    usuario, erro = criar_usuario(nome=data.nome, email=data.email)
    
    if erro:
        raise HTTPException(status_code=400, detail=erro)
    
    return usuario


@router.get("")
def listar_usuarios_route():
    """Lista todos os usuários"""
    usuarios = listar_usuarios()
    return [
        {
            "id": u.id,
            "nome": u.nome,
            "email": u.email
        }
        for u in usuarios
    ]