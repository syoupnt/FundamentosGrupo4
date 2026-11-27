
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


AREAS_RESPONSABLES = [
    "Área de Administración",
    "Área de Atención al Ciudadano",
    "Área de Identificación Civil",
    "Área Jurídica",
    "Área de Recursos Humanos",
    "Área de Tecnologías de la Información"
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

    if registro.get("area_responsable"):
        print("Área responsable:", registro.get("area_responsable"))

    if registro.get("observacion"):
        print("Observación:", registro.get("observacion"))

    print("Notificaciones:", len(registro.get("notificaciones", [])))
    print(BLUE + "-------------------------------" + RESET)


def buscar_registros(expedientes, criterio, indice=0):
    """
    Devuelve los expedientes que coinciden
    con el código o con el DNI ingresado.

    Recorre la lista de forma recursiva: procesa
    el registro en `indice` y llama a sí misma
    con el siguiente, hasta llegar al final.
    """
    if indice >= len(expedientes):
        return []

    registro = expedientes[indice]
    criterio = criterio.strip().lower()
    encontrados = buscar_registros(expedientes, criterio, indice + 1)

    codigo = registro.get("expediente", "").lower()
    dni = registro.get("dni", "")

    if criterio == codigo or criterio == dni:
        encontrados.insert(0, registro)

    return encontrados


def buscar_expediente(expedientes):
    print(BRIGHT + CYAN + "\n=== CONSULTA DE EXPEDIENTES ===" + RESET)

    criterio = pedir_texto(
        "Ingrese el código del expediente o el DNI: "
    )

    encontrados = buscar_registros(expedientes, criterio)

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

    encontrados = buscar_registros(expedientes, codigo)

    if not encontrados:
        print(RED + "Expediente no encontrado." + RESET)
        return

    registro_encontrado = encontrados[0]

    print("Estados disponibles:")

    for indice, estado in enumerate(ESTADOS, start=1):
        print(f"{indice}. {estado}")

    opcion = pedir_entero_positivo("Seleccione el nuevo estado: ")

    if opcion < 1 or opcion > len(ESTADOS):
        print(RED + "Opción de estado no válida." + RESET)
        return

    nuevo_estado = ESTADOS[opcion - 1]
    estado_anterior = registro_encontrado["estado"]

    if nuevo_estado == estado_anterior:
        print(YELLOW + "El expediente ya se encuentra en ese estado." + RESET)
        return

    registro_encontrado["estado"] = nuevo_estado
    notificacion = crear_notificacion(registro_encontrado, estado_anterior, "")

    if guardar_expedientes(expedientes):
        mostrar_notificacion(registro_encontrado, notificacion)
        print(GREEN + "Estado actualizado correctamente." + RESET)
        return

    registro_encontrado["estado"] = estado_anterior
    descartar_notificacion(registro_encontrado, notificacion)
    print(RED + "No se pudo guardar el cambio." + RESET)


def crear_notificacion(registro, estado_anterior, motivo):
    """
    Agrega al expediente el mensaje que se mostrará
    al ciudadano cuando cambie el estado de su trámite.
    """
    codigo = registro.get("expediente", "")
    estado_actual = registro.get("estado", "")
    fecha_hora = datetime.now().astimezone().isoformat(timespec="seconds")

    if estado_anterior == estado_actual:
        mensaje = f"Su expediente {codigo} mantiene el estado {estado_actual}."
    else:
        mensaje = (
            f"Su expediente {codigo} cambió de estado: "
            f"{estado_anterior} -> {estado_actual}."
        )

    if motivo:
        mensaje += f" {motivo}"

    notificacion = {
        "fecha_hora": fecha_hora,
        "mensaje": mensaje
    }

    registro.setdefault("notificaciones", []).append(notificacion)

    return notificacion


def mostrar_notificacion(registro, notificacion):
    """Muestra el aviso que recibiría el ciudadano."""
    print(BRIGHT + GREEN + "\n=== NOTIFICACIÓN AL CIUDADANO ===" + RESET)
    print("Para:", registro.get("nombre", ""), "| DNI:", registro.get("dni", ""))
    print("Correo:", registro.get("correo", ""))
    print("Celular:", registro.get("telefono", ""))
    print("Asunto: Estado de su expediente", registro.get("expediente", ""))
    print("Mensaje:", notificacion.get("mensaje", ""))
    print(GREEN + "===================================" + RESET)


def descartar_notificacion(registro, notificacion):
    """Elimina la notificación cuando no se pudo guardar el cambio."""
    notificaciones = registro.get("notificaciones", [])

    if notificacion in notificaciones:
        notificaciones.remove(notificacion)


def derivar_expediente(expedientes):
    print(BRIGHT + CYAN + "\n=== DERIVAR DOCUMENTOS A UN ÁREA ===" + RESET)

    codigo = pedir_texto("Ingrese código de expediente: ").upper()

    encontrados = buscar_registros(expedientes, codigo)

    if not encontrados:
        print(RED + "Expediente no encontrado." + RESET)
        return

    registro = encontrados[0]

    print("Áreas disponibles:")

    for indice, area in enumerate(AREAS_RESPONSABLES, start=1):
        print(f"{indice}. {area}")

    opcion = pedir_entero_positivo("Seleccione el área responsable: ")

    if opcion < 1 or opcion > len(AREAS_RESPONSABLES):
        print(RED + "Opción de área no válida." + RESET)
        return

    area = AREAS_RESPONSABLES[opcion - 1]
    estado_anterior = registro["estado"]
    registro["estado"] = "Derivado"
    registro["area_responsable"] = area
    notificacion = crear_notificacion(
        registro,
        estado_anterior,
        f"Área responsable: {area}."
    )

    if guardar_expedientes(expedientes):
        mostrar_notificacion(registro, notificacion)
        print(GREEN + "Expediente derivado correctamente." + RESET)
        return

    registro["estado"] = estado_anterior
    registro.pop("area_responsable", None)
    descartar_notificacion(registro, notificacion)
    print(RED + "No se pudo guardar la derivación." + RESET)


def registrar_observacion(expedientes):
    print(BRIGHT + CYAN + "\n=== REGISTRAR OBSERVACIÓN ===" + RESET)

    codigo = pedir_texto("Ingrese código de expediente: ").upper()

    encontrados = buscar_registros(expedientes, codigo)

    if not encontrados:
        print(RED + "Expediente no encontrado." + RESET)
        return

    registro = encontrados[0]

    detalle = pedir_texto("Documento o requisito faltante: ")

    estado_anterior = registro["estado"]
    registro["estado"] = "Observado"
    registro["observacion"] = detalle
    registro["fecha_observacion"] = (
        datetime.now().astimezone().isoformat(timespec="seconds")
    )
    notificacion = crear_notificacion(
        registro,
        estado_anterior,
        f"Falta el siguiente requisito: {detalle}."
    )

    if guardar_expedientes(expedientes):
        mostrar_notificacion(registro, notificacion)
        print(GREEN + "Observación registrada correctamente." + RESET)
        return

    registro["estado"] = estado_anterior
    registro.pop("observacion", None)
    registro.pop("fecha_observacion", None)
    descartar_notificacion(registro, notificacion)
    print(RED + "No se pudo guardar la observación." + RESET)


def consultar_notificaciones(expedientes):
    print(BRIGHT + CYAN + "\n=== NOTIFICACIONES AL CIUDADANO ===" + RESET)

    criterio = pedir_texto(
        "Ingrese el código del expediente o el DNI: "
    )

    encontrados = buscar_registros(expedientes, criterio)

    if not encontrados:
        print(RED + "No se encontraron expedientes." + RESET)
        return

    for registro in encontrados:
        notificaciones = registro.get("notificaciones", [])

        print(BLUE + "\n---------- NOTIFICACIONES ----------" + RESET)
        print("Expediente:", registro.get("expediente", ""))
        print("Ciudadano:", registro.get("nombre", ""))
        print("Correo:", registro.get("correo", ""))

        if not notificaciones:
            print(YELLOW + "Todavía no hay notificaciones." + RESET)

        for notificacion in notificaciones:
            print(
                "-",
                notificacion.get("fecha_hora", ""),
                "|",
                notificacion.get("mensaje", "")
            )

        print(BLUE + "-------------------------------------" + RESET)


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
