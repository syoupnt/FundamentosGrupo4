from datetime import datetime

from almacenamiento import guardar_expedientes
from colores import BLUE, BRIGHT, CYAN, GREEN, RED, RESET, YELLOW
from entradas import pedir_entero_positivo, pedir_texto
from validaciones import (
    validar_correo,
    validar_dni,
    validar_nombre,
    validar_telefono,
)


ESTADOS = [
    "Recibido",
    "En revisión",
    "Derivado",
    "Atendido",
    "Observado"
]


def generar_codigo_expediente(expedientes):
    """
    Genera códigos correlativos según el año actual.
    Ejemplo: EXP-2026-001.
    """
    anio = datetime.now().year
    prefijo = f"EXP-{anio}-"

    numeros_existentes = []

    for registro in expedientes:
        codigo = registro.get("expediente", "")

        if codigo.startswith(prefijo):
            try:
                numero = int(codigo.split("-")[-1])
                numeros_existentes.append(numero)
            except ValueError:
                continue

    siguiente = max(numeros_existentes, default=0) + 1

    return f"{prefijo}{siguiente:03d}"


def registrar_tramite(expedientes):
    print(BRIGHT + CYAN + "\n=== REGISTRO DE NUEVO TRÁMITE ===" + RESET)

    while True:
        dni = input(YELLOW + "Ingrese DNI (8 dígitos): " + RESET).strip()

        if validar_dni(dni):
            break

        print(RED + "Error: El DNI debe tener exactamente 8 números." + RESET)

    while True:
        nombre = input(YELLOW + "Nombres completos: " + RESET).strip()

        if validar_nombre(nombre):
            break

        print(RED + "Error: Ingrese un nombre válido." + RESET)

    while True:
        telefono = input(YELLOW + "Celular (9 dígitos): " + RESET).strip()

        if validar_telefono(telefono):
            break

        print(RED + "Error: El celular debe tener 9 números." + RESET)

    while True:
        correo = input(YELLOW + "Correo electrónico: " + RESET).strip()

        if validar_correo(correo):
            break

        print(RED + "Error: Ingrese un correo electrónico válido." + RESET)

    tipo_tramite = pedir_texto("Tipo de trámite: ")
    codigo = generar_codigo_expediente(expedientes)
    fecha_hora = datetime.now().astimezone().isoformat(timespec="seconds")

    nuevo_expediente = {
        "expediente": codigo,
        "dni": dni,
        "nombre": nombre,
        "telefono": telefono,
        "correo": correo,
        "tipo_tramite": tipo_tramite,
        "fecha_hora": fecha_hora,
        "estado": "Recibido"
    }

    expedientes.append(nuevo_expediente)

    if not guardar_expedientes(expedientes):
        expedientes.pop()
        print(RED + "No se pudo completar el registro." + RESET)
        return

    print(GREEN + "\n¡TRÁMITE REGISTRADO CORRECTAMENTE!" + RESET)
    print(CYAN + "========== CARGO DIGITAL ==========" + RESET)
    print("Expediente:", codigo)
    print("Ciudadano:", nombre)
    print("DNI:", dni)
    print("Tipo de trámite:", tipo_tramite)
    print("Fecha y hora:", fecha_hora)
    print("Estado:", "Recibido")
    print(CYAN + "===================================" + RESET)


def mostrar_detalle(registro):
    print(BLUE + "\n---------- EXPEDIENTE ----------" + RESET)
    print("Código:", registro.get("expediente", ""))
    print("DNI:", registro.get("dni", ""))
    print("Ciudadano:", registro.get("nombre", ""))
    print("Celular:", registro.get("telefono", ""))
    print("Correo:", registro.get("correo", ""))
    print("Trámite:", registro.get("tipo_tramite", ""))
    print("Fecha:", registro.get("fecha_hora", ""))
    print("Estado:", registro.get("estado", ""))
    print(BLUE + "-------------------------------" + RESET)


def buscar_expediente(expedientes):
    print(BRIGHT + CYAN + "\n=== CONSULTA DE EXPEDIENTES ===" + RESET)

    criterio = pedir_texto(
        "Ingrese el código del expediente o el DNI: "
    ).lower()

    encontrados = []

    for registro in expedientes:
        codigo = registro.get("expediente", "").lower()
        dni = registro.get("dni", "")

        if criterio == codigo or criterio == dni:
            encontrados.append(registro)

    if not encontrados:
        print(RED + "No se encontraron expedientes." + RESET)
        return

    for registro in encontrados:
        mostrar_detalle(registro)


def listar_expedientes(expedientes):
    print(BRIGHT + CYAN + "\n=== LISTA DE EXPEDIENTES ===" + RESET)

    if not expedientes:
        print(YELLOW + "Todavía no existen registros." + RESET)
        return

    for registro in expedientes:
        print(
            registro.get("expediente", ""),
            "|",
            registro.get("nombre", ""),
            "|",
            registro.get("tipo_tramite", ""),
            "|",
            registro.get("estado", "")
        )


def actualizar_estado(expedientes):
    print(BRIGHT + CYAN + "\n=== ACTUALIZAR ESTADO ===" + RESET)

    codigo = pedir_texto("Ingrese código de expediente: ").upper()

    registro_encontrado = None

    for registro in expedientes:
        if registro.get("expediente", "").upper() == codigo:
            registro_encontrado = registro
            break

    if registro_encontrado is None:
        print(RED + "Expediente no encontrado." + RESET)
        return

    print("Estados disponibles:")

    for indice, estado in enumerate(ESTADOS, start=1):
        print(f"{indice}. {estado}")

    opcion = pedir_entero_positivo("Seleccione el nuevo estado: ")

    if opcion < 1 or opcion > len(ESTADOS):
        print(RED + "Opción de estado no válida." + RESET)
        return

    estado_anterior = registro_encontrado["estado"]
    registro_encontrado["estado"] = ESTADOS[opcion - 1]

    if guardar_expedientes(expedientes):
        print(GREEN + "Estado actualizado correctamente." + RESET)
    else:
        registro_encontrado["estado"] = estado_anterior
        print(RED + "No se pudo guardar el cambio." + RESET)


def generar_reporte(expedientes):
    print(BRIGHT + CYAN + "\n=== REPORTE DIARIO DE MESA DE PARTES ===" + RESET)

    hoy = datetime.now().astimezone().date().isoformat()

    registros_hoy = [
        registro
        for registro in expedientes
        if registro.get("fecha_hora", "").startswith(hoy)
    ]

    print("Fecha del reporte:", hoy)
    print("Total de expedientes ingresados hoy:", len(registros_hoy))

    if not registros_hoy:
        print(YELLOW + "No existen trámites registrados hoy." + RESET)
        return

    print("\nCantidad por tipo de trámite:")

    conteo = {}

    for registro in registros_hoy:
        tipo = registro.get("tipo_tramite", "Sin especificar")
        conteo[tipo] = conteo.get(tipo, 0) + 1

    for tipo, cantidad in conteo.items():
        print(f"- {tipo}: {cantidad}")

    print("\nCantidad por estado:")

    conteo_estados = {}

    for registro in registros_hoy:
        estado = registro.get("estado", "Sin estado")
        conteo_estados[estado] = conteo_estados.get(estado, 0) + 1

    for estado, cantidad in conteo_estados.items():
        print(f"- {estado}: {cantidad}")

    print(GREEN + "\nReporte generado correctamente." + RESET)
