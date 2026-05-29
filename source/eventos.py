from abc import ABC, abstractmethod
from datetime import datetime


class EventoLog(ABC):
    def __init__(self, usuario: str, nivel: str = "INFO"):
        self.timestamp: str = datetime.now().isoformat()
        self.usuario: str = usuario
        self.nivel: str = nivel

    @abstractmethod
    def serializar(self) -> str:
        pass

    @abstractmethod
    def get_tipo(self) -> str:
        pass

    def __repr__(self):
        return f"[{self.nivel}] {self.get_tipo()} | usuario={self.usuario} | ts={self.timestamp}"


class EventoLogin(EventoLog):
    def __init__(self, usuario: str, ip_origen: str, exito: bool):
        super().__init__(usuario, nivel="INFO" if exito else "WARNING")
        self.ip_origen: str = ip_origen
        self.exito: bool = exito

    def serializar(self) -> str:
        return (
            f"TIPO={self.get_tipo()}|TS={self.timestamp}|USUARIO={self.usuario}"
            f"|IP={self.ip_origen}|EXITO={self.exito}|NIVEL={self.nivel}"
        )

    def get_tipo(self) -> str:
        return "LOGIN"