import hashlib
from typing import Optional, List

from eventos import EventoLog


def sha256(data: str) -> str:
    return hashlib.sha256(data.encode("utf-8")).hexdigest()


class NodoMerkle:
    def __init__(
        self,
        izquierdo: Optional["NodoMerkle"] = None,
        derecho: Optional["NodoMerkle"] = None,
        evento: Optional[EventoLog] = None,
    ):
        self.izquierdo: Optional["NodoMerkle"] = izquierdo
        self.derecho: Optional["NodoMerkle"] = derecho
        self.evento: Optional[EventoLog] = evento
        self.hash: str = self.calcular_hash()

    def es_hoja(self) -> bool:
        return self.izquierdo is None and self.derecho is None

    def calcular_hash(self) -> str:
        if self.es_hoja():
            datos = self.evento.serializar() if self.evento else ""
            return sha256(datos)

        hash_izq = self.izquierdo.hash if self.izquierdo else ""
        hash_der = self.derecho.hash if self.derecho else ""

        return sha256(hash_izq + hash_der)

    def __repr__(self):
        if self.es_hoja():
            tipo = self.evento.get_tipo() if self.evento else "VACIO"
            return f"NodoHoja(hash={self.hash[:8]}..., evento={tipo})"

        return f"NodoInterno(hash={self.hash[:8]}...)"


class ArbolMerkle:
    def __init__(self):
        self.raiz: Optional[NodoMerkle] = None
        self.eventos: List[EventoLog] = []

    def insertar_evento(self, evento: EventoLog) -> None:
        self.eventos.append(evento)
        self.construir_arbol()

    def construir_arbol(self) -> None:
        if not self.eventos:
            self.raiz = None
            return

        hojas = [NodoMerkle(evento=e) for e in self.eventos]
        self.raiz = self._construir_recursivo(hojas)

    def _construir_recursivo(self, nodos: List[NodoMerkle]) -> NodoMerkle:
        if len(nodos) == 1:
            return nodos[0]

        if len(nodos) % 2 != 0:
            nodos.append(nodos[-1])

        nivel_superior = []

        for i in range(0, len(nodos), 2):
            padre = NodoMerkle(
                izquierdo=nodos[i],
                derecho=nodos[i + 1],
            )
            nivel_superior.append(padre)

        return self._construir_recursivo(nivel_superior)

    def get_raiz_hash(self) -> Optional[str]:
        return self.raiz.hash if self.raiz else None

    def recalcular_raiz_hash(self) -> Optional[str]:
        if not self.eventos:
            return None

        hojas = [NodoMerkle(evento=e) for e in self.eventos]
        raiz_recalculada = self._construir_recursivo(hojas)

        return raiz_recalculada.hash

    def verificar_integridad(self) -> bool:
        if not self.eventos:
            return True

        return self.recalcular_raiz_hash() == self.get_raiz_hash()

    def obtener_prueba(self, indice_evento: int) -> List[dict]:
        if indice_evento < 0 or indice_evento >= len(self.eventos):
            raise IndexError(f"Índice {indice_evento} fuera de rango.")

        hojas = [NodoMerkle(evento=e) for e in self.eventos]
        prueba = []

        self._recopilar_prueba(hojas, indice_evento, prueba)

        return prueba

    def _recopilar_prueba(
        self,
        nodos: List[NodoMerkle],
        indice: int,
        prueba: List[dict],
    ) -> None:
        if len(nodos) == 1:
            return

        if len(nodos) % 2 != 0:
            nodos.append(nodos[-1])

        if indice % 2 == 0:
            prueba.append(
                {
                    "hash": nodos[indice + 1].hash,
                    "posicion": "derecha",
                }
            )
        else:
            prueba.append(
                {
                    "hash": nodos[indice - 1].hash,
                    "posicion": "izquierda",
                }
            )

        nivel_superior = []

        for i in range(0, len(nodos), 2):
            padre = NodoMerkle(
                izquierdo=nodos[i],
                derecho=nodos[i + 1],
            )
            nivel_superior.append(padre)

        indice_padre = indice // 2
        self._recopilar_prueba(nivel_superior, indice_padre, prueba)