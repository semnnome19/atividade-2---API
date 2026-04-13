from domain.usuario import Usuario
from domain.sala import Sala
from domain.reserva import Reserva
from repositories.memory import db
from datetime import datetime

# Constantes de validação
MAX_DURACAO_HORAS = 4.0
MAX_RESERVAS_POR_DIA = 3


def criar_usuario(nome: str, email: str):
    """
    Cria um novo usuário com validação de email duplicado
    Retorna: (usuario, error_message) ou (None, error_message) se houver erro
    """
    # Validação de email duplicado
    for usuario in db.usuarios.values():
        if usuario.email.lower() == email.lower():
            return None, "Email já cadastrado"
    
    usuario = Usuario(id=db.next_usuario_id, nome=nome, email=email)
    db.usuarios[db.next_usuario_id] = usuario
    db.next_usuario_id += 1
    return usuario, None


def listar_usuarios():
    return list(db.usuarios.values())


def criar_sala(nome: str, capacidade: int, bloco: str):
    """
    Cria uma nova sala com validação de capacidade
    Retorna: (sala, error_message) ou (None, error_message) se houver erro
    """
    # Validação de capacidade mínima
    if capacidade < 1:
        return None, "Capacidade da sala deve ser no mínimo 1"
    
    sala = Sala(id=db.next_sala_id, nome=nome, capacidade=capacidade, bloco=bloco)
    db.salas[db.next_sala_id] = sala
    db.next_sala_id += 1
    return sala, None


def listar_salas():
    return list(db.salas.values())


def criar_reserva(usuario_id: int, sala_id: int, data: str, hora_inicio: str, hora_fim: str):
    """
    Cria uma nova reserva com múltiplas validações
    Retorna: (reserva, error_message) ou (None, error_message) se houver erro
    """
    # Verifica se usuário existe
    if usuario_id not in db.usuarios:
        return None, "Usuário não encontrado"
    
    # Verifica se sala existe
    if sala_id not in db.salas:
        return None, "Sala não encontrada"
    
    # Cria a nova reserva
    nova_reserva = Reserva(
        id=db.next_reserva_id,
        usuario_id=usuario_id,
        sala_id=sala_id,
        data=data,
        hora_inicio=hora_inicio,
        hora_fim=hora_fim,
        status="active"
    )
    
    # Validação de duração máxima da reserva
    duracao = nova_reserva.duracao_em_horas()
    if duracao > MAX_DURACAO_HORAS:
        return None, f"Duração máxima permitida é {MAX_DURACAO_HORAS} horas"
    
    if duracao <= 0:
        return None, "Hora de fim deve ser posterior à hora de início"
    
    # Validação de limite de reservas por dia
    reservas_dia = [
        r for r in db.reservas.values()
        if r.usuario_id == usuario_id and r.data == data and r.status == "active"
    ]
    if len(reservas_dia) >= MAX_RESERVAS_POR_DIA:
        return None, f"Limite de {MAX_RESERVAS_POR_DIA} reservas por dia atingido"
    
    # Verifica conflitos com outras reservas ativas
    for reserva in db.reservas.values():
        if nova_reserva.conflita_com(reserva):
            return None, "Conflito: Horário indisponível para esta sala"  # Conflito encontrado
    
    # Adiciona à base de dados
    db.reservas[db.next_reserva_id] = nova_reserva
    db.next_reserva_id += 1
    return nova_reserva, None


def listar_reservas():
    return list(db.reservas.values())


def listar_reservas_usuario(usuario_id: int):
    """Lista todas as reservas de um usuário"""
    return [r for r in db.reservas.values() if r.usuario_id == usuario_id]


def buscar_reserva(reserva_id: int):
    """Busca uma reserva pelo ID"""
    return db.reservas.get(reserva_id)


def cancelar_reserva(reserva_id: int):
    """Cancela uma reserva ativa"""
    reserva = db.reservas.get(reserva_id)
    if reserva:
        return reserva.cancelar()
    return False


def finalizar_reserva(reserva_id: int, hora_atual: str):
    """Finaliza uma reserva ativa"""
    reserva = db.reservas.get(reserva_id)
    if reserva:
        return reserva.finalizar(hora_atual)
    return False


def mudar_status(reserva_id: int, novo_status: str):
    """
    Muda o status de uma reserva
    Status válidos: 'active', 'cancelled', 'completed'
    Retorna: (True, None) ou (False, error_message) se houver erro
    """
    status_validos = ['active', 'cancelled', 'completed']
    
    if novo_status not in status_validos:
        return False, f"Status inválido. Valores permitidos: {', '.join(status_validos)}"
    
    reserva = db.reservas.get(reserva_id)
    if not reserva:
        return False, "Reserva não encontrada"
    
    reserva.status = novo_status
    return True, None