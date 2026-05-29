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


class EventoBorradoArchivo(EventoLog):
    def __init__(self, usuario: str, ruta_archivo: str, tamanyo_bytes: int):
        super().__init__(usuario, nivel="WARNING")
        self.ruta_archivo: str = ruta_archivo
        self.tamanyo_bytes: int = tamanyo_bytes

    def serializar(self) -> str:
        return (
            f"TIPO={self.get_tipo()}|TS={self.timestamp}|USUARIO={self.usuario}"
            f"|RUTA={self.ruta_archivo}|BYTES={self.tamanyo_bytes}|NIVEL={self.nivel}"
        )

    def get_tipo(self) -> str:
        return "BORRADO_ARCHIVO"


class EventoCambioPermiso(EventoLog):
    def __init__(self, usuario: str, recurso: str, permiso_anterior: str, permiso_nuevo: str):
        super().__init__(usuario, nivel="WARNING")
        self.recurso: str = recurso
        self.permiso_anterior: str = permiso_anterior
        self.permiso_nuevo: str = permiso_nuevo

    def serializar(self) -> str:
        return (
            f"TIPO={self.get_tipo()}|TS={self.timestamp}|USUARIO={self.usuario}"
            f"|RECURSO={self.recurso}|PERM_ANT={self.permiso_anterior}"
            f"|PERM_NOU={self.permiso_nuevo}|NIVEL={self.nivel}"
        )

    def get_tipo(self) -> str:
        return "CAMBIO_PERMISO"


class EventoAccesoFallido(EventoLog):
    def __init__(self, usuario: str, recurso: str, intentos: int):
        super().__init__(usuario, nivel="ERROR" if intentos >= 5 else "WARNING")
        self.recurso: str = recurso
        self.intentos: int = intentos

    def serializar(self) -> str:
        return (
            f"TIPO={self.get_tipo()}|TS={self.timestamp}|USUARIO={self.usuario}"
            f"|RECURSO={self.recurso}|INTENTOS={self.intentos}|NIVEL={self.nivel}"
        )

    def get_tipo(self) -> str:
        return "ACCESO_FALLIDO"