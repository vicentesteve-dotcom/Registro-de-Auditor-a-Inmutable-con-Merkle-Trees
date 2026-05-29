# Registro de Auditoría Inmutable con Árbol de Merkle

## Descripción

Este proyecto implementa un sistema de auditoría de logs basado en árboles de Merkle. Su objetivo es registrar eventos de seguridad y detectar si alguno de ellos ha sido modificado después de ser guardado.

El sistema utiliza hashes SHA-256 para generar una raíz de Merkle que representa el estado completo del registro. Si un evento cambia, el hash raíz recalculado deja de coincidir con el hash original.

## Contexto del problema

En ciberseguridad, los logs son esenciales para investigar accesos, cambios de permisos, borrados de archivos o intentos fallidos. El problema es que un atacante que comprometa un sistema podría intentar borrar o modificar esos registros para ocultar sus acciones.

Este proyecto propone una solución sencilla: cada evento se transforma en un hash y todos los hashes se organizan en un árbol de Merkle. De esta forma, cualquier modificación en un evento altera la raíz del árbol y puede detectarse comparando el hash actual con el hash sellado.

## Funcionalidades principales

* Registro de diferentes eventos de seguridad.
* Construcción de un árbol de Merkle a partir de los eventos.
* Cálculo del hash raíz del registro.
* Verificación de integridad del log.
* Generación de pruebas Merkle para eventos individuales.
* Simulación de manipulación de un evento.
* Exportación de un informe en formato JSON.
* Menú interactivo y demo automática.

## Estructura del proyecto

```text
/
├── README.md
├── docs/
│   ├── uml.png
│   ├── flux_registrar_evento.png
│   ├── flux_verificar_integridad.png
│   ├── flux_obtener_prueba.png
│   ├── estudi_complexitat.pdf
│   └── conclusions_i_propostes_futur.pdf
└── source/
    ├── main.py
    ├── eventos.py
    ├── merkle.py
    └── auditor.py
```

## Diseño del sistema

El proyecto está dividido en tres módulos principales:

* `eventos.py`: define la jerarquía de eventos del log.
* `merkle.py`: implementa los nodos y el árbol de Merkle.
* `auditor.py`: gestiona el registro, la verificación y la generación de informes.
* `main.py`: contiene el menú principal y la demo del sistema.

## Programación orientada a objetos y polimorfismo

El sistema utiliza programación orientada a objetos para separar responsabilidades.

La clase abstracta `EventoLog` define la estructura común de todos los eventos. A partir de ella heredan clases concretas como `EventoLogin`, `EventoBorradoArchivo`, `EventoCambioPermiso` y `EventoAccesoFallido`.

El polimorfismo aparece en los métodos `serializar()` y `get_tipo()`. Cada tipo de evento implementa estos métodos de forma distinta, pero el árbol de Merkle puede tratarlos todos como objetos de tipo `EventoLog`.

## Estructuras de datos

La estructura principal es un árbol binario de Merkle. Cada hoja representa un evento de seguridad y cada nodo interno contiene el hash de sus hijos.

También se utiliza una lista para almacenar los eventos registrados y facilitar la reconstrucción del árbol cuando se añade un nuevo evento.

## Complejidad

| Operación                     | Complejidad |
| ----------------------------- | ----------: |
| Obtener hash raíz             |        O(1) |
| Construir el árbol            |        O(n) |
| Insertar un evento            |        O(n) |
| Verificar integridad completa |        O(n) |
| Obtener prueba Merkle         |    O(log n) |
| Verificar evento individual   |    O(log n) |

## Ejecución

Desde la raíz del proyecto:

```bash
python source/main.py
```

Para ejecutar la demo automática:

```bash
python source/main.py --demo
```

En Windows también puede ejecutarse con:

```bash
py source/main.py
py source/main.py --demo
```

## Dependencias

El proyecto utiliza únicamente librerías estándar de Python:

* `hashlib`
* `json`
* `datetime`
* `argparse`
* `typing`
* `abc`

No es necesario instalar dependencias externas.

## Vídeo demostrativo

El vídeo demostrativo del proyecto está disponible en el siguiente enlace:

https://youtu.be/sUJhKSgC5ec

## Uso de herramientas externas o IA

Durante el desarrollo se han utilizado herramientas de apoyo para revisar errores, mejorar la estructura del código y redactar documentación. La lógica principal del sistema se basa en los conceptos trabajados en la asignatura: árboles, hashes, recursividad, programación orientada a objetos y análisis de complejidad.

## Conclusiones y trabajo futuro

El sistema permite detectar modificaciones en un registro de auditoría mediante la comparación del hash raíz original con el hash recalculado. Esto demuestra cómo los árboles de Merkle pueden aplicarse a la integridad de logs en ciberseguridad.

Como mejoras futuras, se podría guardar el hash raíz en un servidor externo, añadir una base de datos, implementar firma digital de informes o crear una interfaz gráfica para facilitar el uso del sistema.
