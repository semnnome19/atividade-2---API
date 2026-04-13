from datetime import datetime


class Reserva:
    def __init__(
        self,
        id: int,
        usuario_id: int,
        sala_id: int,
        data: str,
        hora_inicio: str,
        hora_fim: str,
        status: str = "active"
    ):
        self.id = id
        self.usuario_id = usuario_id
        self.sala_id = sala_id
        self.data = data
        self.hora_inicio = hora_inicio
        self.hora_fim = hora_fim
        self.status = status

    def cancelar(self):
        """Cancela a reserva alterando o status para 'cancelled'"""
        if self.status == "active":
            self.status = "cancelled"
            return True
        return False

    def finalizar(self, hora_atual: str):
        """
        Finaliza a reserva alterando o status para 'completed'
        hour_atual no formato HH:MM
        """
        if self.status == "active":
            # Verifica se a hora atual é >= hora_fim
            hora_atual_obj = datetime.strptime(hora_atual, "%H:%M")
            hora_fim_obj = datetime.strptime(self.hora_fim, "%H:%M")
            
            if hora_atual_obj >= hora_fim_obj:
                self.status = "completed"
                return True
            else:
                return False
        return False

    def duracao_em_horas(self) -> float:
        """Calcula a duração da reserva em horas"""
        hora_inicio_obj = datetime.strptime(self.hora_inicio, "%H:%M")
        hora_fim_obj = datetime.strptime(self.hora_fim, "%H:%M")
        
        diferenca = hora_fim_obj - hora_inicio_obj
        horas = diferenca.total_seconds() / 3600
        
        return horas

    def conflita_com(self, outra_reserva) -> bool:
        """
        Verifica se esta reserva conflita com outra
        Retorna True se houver conflito de horário e data
        """
        # Se não são no mesmo dia, não há conflito
        if self.data != outra_reserva.data:
            return False
        
        # Se não são no mesmo sala, não há conflito
        if self.sala_id != outra_reserva.sala_id:
            return False
        
        # Se uma das reservas não está ativa, não há conflito
        if self.status != "active" or outra_reserva.status != "active":
            return False
        
        # Converte horários para objetos datetime
        hora_inicio_self = datetime.strptime(self.hora_inicio, "%H:%M")
        hora_fim_self = datetime.strptime(self.hora_fim, "%H:%M")
        hora_inicio_outro = datetime.strptime(outra_reserva.hora_inicio, "%H:%M")
        hora_fim_outro = datetime.strptime(outra_reserva.hora_fim, "%H:%M")
        
        # Verifica se há sobreposição de horários
        # Conflita se: inicio_self < fim_outro AND fim_self > inicio_outro
        return hora_inicio_self < hora_fim_outro and hora_fim_self > hora_inicio_outro