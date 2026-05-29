import json
from datetime import datetime
from typing import Optional

from merkle import ArbolMerkle, sha256
from eventos import EventoLog


class AuditorLog:
    def __init__(self):
        self.arbol: ArbolMerkle = ArbolMerkle()
        self.hash_conocido: Optional[str] = None

    def registrar(self, evento: EventoLog) -> None:
        self.arbol.insertar_evento(evento)
        self.hash_conocido = self.arbol.get_raiz_hash()

        print(f"  [+] Evento registrado: {evento}")
        print(f"      Hash raíz actual : {self.hash_conocido[:16]}...")

    def sellar(self) -> Optional[str]:
        self.hash_conocido = self.arbol.get_raiz_hash()

        if self.hash_conocido is None:
            print("\n[SELLADO] No hay eventos para sellar.")
            return None

        print(f"\n[SELLADO] Hash raíz guardado: {self.hash_conocido}")
        return self.hash_conocido

    def verificar(self) -> bool:
        if self.hash_conocido is None:
            print("[VERIFICACIÓN] No hay hash de referencia sellado.")
            return False

        hash_actual = self.arbol.recalcular_raiz_hash()

        if hash_actual == self.hash_conocido:
            print(f"[VERIFICACIÓN] ✓ Integridad confirmada. Hash: {hash_actual[:16]}...")
            return True

        print("[VERIFICACIÓN] ✗ ¡ALERTA! Hash no coincide.")
        print(f"  Esperado : {self.hash_conocido[:16]}...")
        print(f"  Actual   : {hash_actual[:16]}...")

        return False

    def verificar_evento(self, indice: int) -> bool:
        try:
            prueba = self.arbol.obtener_prueba(indice)
            evento = self.arbol.eventos[indice]
            hash_actual = sha256(evento.serializar())

            for paso in prueba:
                if paso["posicion"] == "derecha":
                    hash_actual = sha256(hash_actual + paso["hash"])
                else:
                    hash_actual = sha256(paso["hash"] + hash_actual)

            valido = hash_actual == self.hash_conocido
            estado = "✓ VÁLIDO" if valido else "✗ INVÁLIDO"

            print(f"[PRUEBA MERKLE] Evento {indice} ({evento.get_tipo()}): {estado}")

            return valido

        except IndexError as error:
            print(f"[ERROR] {error}")
            return False

    def exportar_informe(self) -> str:
        hash_recalculado = self.arbol.recalcular_raiz_hash()

        informe = {
            "fecha_informe": datetime.now().isoformat(),
            "total_eventos": len(self.arbol.eventos),
            "hash_raiz": hash_recalculado,
            "hash_sellado": self.hash_conocido,
            "integridad_ok": hash_recalculado == self.hash_conocido,
            "eventos": [
                {
                    "indice": i,
                    "tipo": evento.get_tipo(),
                    "usuario": evento.usuario,
                    "timestamp": evento.timestamp,
                    "nivel": evento.nivel,
                    "serializado": evento.serializar(),
                }
                for i, evento in enumerate(self.arbol.eventos)
            ],
        }

        return json.dumps(informe, indent=2, ensure_ascii=False)

    def mostrar_arbol(self) -> None:
        print("\n=== Estado del Árbol de Merkle ===")
        print(f"Total eventos : {len(self.arbol.eventos)}")
        print(f"Hash raíz     : {self.arbol.get_raiz_hash()}")
        print("Eventos (hojas):")

        for i, evento in enumerate(self.arbol.eventos):
            hash_evento = sha256(evento.serializar())
            print(
                f"  [{i}] {evento.get_tipo():20s} | "
                f"hash={hash_evento[:12]}... | "
                f"usuario={evento.usuario}"
            )

        print("==================================\n")

    def simular_tampering(self, indice: int, nuevo_usuario: str) -> None:
        if 0 <= indice < len(self.arbol.eventos):
            evento = self.arbol.eventos[indice]

            print(
                f"\n[TAMPERING] Modificando evento {indice}: "
                f"usuario '{evento.usuario}' → '{nuevo_usuario}'"
            )

            evento.usuario = nuevo_usuario
        else:
            print(f"[ERROR] Índice {indice} fuera de rango.")