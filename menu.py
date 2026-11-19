from almacenamiento import cargar_expedientes
from colores import BLUE, BRIGHT, CYAN, GREEN, RED, RESET, YELLOW
from expedientes import (
    actualizar_estado,
    buscar_expediente,
    generar_reporte,
    listar_expedientes,
    registrar_tramite,
)


def main():
    try:
        expedientes = cargar_expedientes()
    except RuntimeError as error:
        print(RED + str(error) + RESET)
        print(YELLOW + "Revise el archivo JSON antes de continuar." + RESET)
        return

    continuar = True

    while continuar:
        print()
        print(BRIGHT + CYAN + "====================================" + RESET)
        print(BRIGHT + CYAN + "   MESA DE PARTES DIGITAL - ONPE" + RESET)
        print(BRIGHT + CYAN + "====================================" + RESET)

        print(GREEN + "1. Registrar nuevo trámite" + RESET)
        print(BLUE + "2. Buscar expediente" + RESET)
        print(CYAN + "3. Listar expedientes" + RESET)
        print(YELLOW + "4. Actualizar estado del trámite" + RESET)
        print(GREEN + "5. Generar reporte diario" + RESET)
        print(RED + "6. Salir del sistema" + RESET)

        opcion = input(YELLOW + "\nSeleccione una opción: " + RESET).strip()

        match opcion:
            case "1":
                registrar_tramite(expedientes)

            case "2":
                buscar_expediente(expedientes)

            case "3":
                listar_expedientes(expedientes)

            case "4":
                actualizar_estado(expedientes)

            case "5":
                generar_reporte(expedientes)

            case "6":
                continuar = False
                print(GREEN + "Gracias por utilizar el sistema." + RESET)

            case _:
                print(RED + "Opción no válida. Seleccione del 1 al 6." + RESET)
