import argparse
import json

from auditor import AuditorLog
from eventos import (
    EventoLogin,
    EventoBorradoArchivo,
    EventoCambioPermiso,
    EventoAccesoFallido,
)


def crear_auditor_demo() -> AuditorLog:
    auditor = AuditorLog()

    eventos = [
        EventoLogin("alice", "192.168.1.10", True),
        EventoLogin("bob", "10.0.0.5", False),
        EventoBorradoArchivo("alice", "/var/log/auth.log", 2048),
        EventoCambioPermiso("root", "/etc/passwd", "644", "600"),
        EventoAccesoFallido("mallory", "/admin", 7),
    ]

    for evento in eventos:
        auditor.registrar(evento)

    return auditor


def ejecutar_demo() -> None:
    print("=" * 60)
    print("  DEMO: Registro de Auditoría Inmutable con Árbol de Merkle")
    print("=" * 60)

    print("\n--- 1. Registrando eventos ---\n")
    auditor = crear_auditor_demo()

    print("\n--- 2. Estado del árbol ---")
    auditor.mostrar_arbol()

    print("--- 3. Verificación de integridad (sin tampering) ---")
    auditor.verificar()

    print("\n--- 4. Pruebas Merkle individuales ---")
    for i in range(len(auditor.arbol.eventos)):
        auditor.verificar_evento(i)

    print("\n--- 5. Simulación de tampering ---")
    auditor.simular_tampering(2, "hacker")

    print("\n--- 6. Verificación tras tampering ---")
    auditor.verificar()

    print("\n--- 7. Exportar informe JSON ---")
    informe = auditor.exportar_informe()

    with open("informe_auditoria.json", "w", encoding="utf-8") as archivo:
        archivo.write(informe)

    datos = json.loads(informe)

    print("Informe guardado en: informe_auditoria.json")
    print(f"Total eventos   : {datos['total_eventos']}")
    print(f"Hash raíz       : {datos['hash_raiz'][:28]}...")
    print(f"Integridad OK   : {datos['integridad_ok']}")

    print("\n[DEMO COMPLETADA]")


def registrar_evento_manual(auditor: AuditorLog) -> None:
    print("\nTipos de evento disponibles:")
    print("1. Login")
    print("2. Borrado de archivo")
    print("3. Cambio de permiso")
    print("4. Acceso fallido")

    opcion = input("Selecciona una opción: ").strip()

    if opcion == "1":
        usuario = input("Usuario: ").strip()
        ip = input("IP de origen: ").strip()
        exito_txt = input("¿Login exitoso? (s/n): ").strip().lower()
        exito = exito_txt == "s"

        evento = EventoLogin(usuario, ip, exito)

    elif opcion == "2":
        usuario = input("Usuario: ").strip()
        ruta = input("Ruta del archivo: ").strip()
        tamanyo = int(input("Tamaño en bytes: ").strip())

        evento = EventoBorradoArchivo(usuario, ruta, tamanyo)

    elif opcion == "3":
        usuario = input("Usuario: ").strip()
        recurso = input("Recurso: ").strip()
        permiso_anterior = input("Permiso anterior: ").strip()
        permiso_nuevo = input("Permiso nuevo: ").strip()

        evento = EventoCambioPermiso(usuario, recurso, permiso_anterior, permiso_nuevo)

    elif opcion == "4":
        usuario = input("Usuario: ").strip()
        recurso = input("Recurso: ").strip()
        intentos = int(input("Número de intentos: ").strip())

        evento = EventoAccesoFallido(usuario, recurso, intentos)

    else:
        print("[ERROR] Opción no válida.")
        return

    auditor.registrar(evento)


def exportar_informe(auditor: AuditorLog) -> None:
    informe = auditor.exportar_informe()

    with open("informe_auditoria.json", "w", encoding="utf-8") as archivo:
        archivo.write(informe)

    print("[OK] Informe exportado como informe_auditoria.json")


def ejecutar_menu() -> None:
    auditor = AuditorLog()

    while True:
        print("\n" + "=" * 50)
        print(" Registro de Auditoría Inmutable")
        print("=" * 50)
        print("1. Registrar evento")
        print("2. Mostrar árbol")
        print("3. Verificar integridad")
        print("4. Verificar evento por índice")
        print("5. Simular tampering")
        print("6. Exportar informe JSON")
        print("7. Cargar eventos de demo")
        print("0. Salir")

        opcion = input("Selecciona una opción: ").strip()

        if opcion == "1":
            registrar_evento_manual(auditor)

        elif opcion == "2":
            auditor.mostrar_arbol()

        elif opcion == "3":
            auditor.verificar()

        elif opcion == "4":
            try:
                indice = int(input("Índice del evento: ").strip())
                auditor.verificar_evento(indice)
            except ValueError:
                print("[ERROR] El índice debe ser un número entero.")

        elif opcion == "5":
            try:
                indice = int(input("Índice del evento a modificar: ").strip())
                nuevo_usuario = input("Nuevo usuario: ").strip()
                auditor.simular_tampering(indice, nuevo_usuario)
            except ValueError:
                print("[ERROR] El índice debe ser un número entero.")

        elif opcion == "6":
            exportar_informe(auditor)

        elif opcion == "7":
            auditor = crear_auditor_demo()
            print("[OK] Eventos de demo cargados.")

        elif opcion == "0":
            print("Saliendo del sistema.")
            break

        else:
            print("[ERROR] Opción no válida.")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Registro de auditoría inmutable basado en Árboles de Merkle"
    )

    parser.add_argument(
        "--demo",
        action="store_true",
        help="Ejecuta una demostración automática del sistema",
    )

    args = parser.parse_args()

    if args.demo:
        ejecutar_demo()
    else:
        ejecutar_menu()


if __name__ == "__main__":
    main()