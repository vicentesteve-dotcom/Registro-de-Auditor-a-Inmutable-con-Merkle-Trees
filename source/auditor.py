from typing import Optional

from merkle import ArbolMerkle
from eventos import EventoLog


class AuditorLog:
    def __init__(self):
        self.arbol: ArbolMerkle = ArbolMerkle()
        self.hash_conocido: Optional[str] = None

    def registrar(self, evento: EventoLog) -> None:
        self.arbol.insertar_evento(evento)
        self.hash_conocido = self.arbol.get_raiz_hash()

    def sellar(self) -> Optional[str]:
        self.hash_conocido = self.arbol.get_raiz_hash()
        return self.hash_conocido