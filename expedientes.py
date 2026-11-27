#################################
#         Carlos Matías         #
#################################

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

def preparar_expediente(registro):
    if len(registro) == 7:
        observacion = registro[6] or ""
        registro[6] = "Observado" if observacion else "Recibido"
        registro.extend(["", [], "", "", observacion, observacion])

    if registro[11] != registro[12]:
        registro[11] = registro[12]
        if registro[12]:
            registro[6] = "Observado"
            registro[10] = datetime.datetime.now().astimezone().isoformat(
                timespec="seconds"
            )
        else:
            registro[6] = "Recibido"
            registro[9] = ""

def crear_notificacion(registro, estado_anterior, motivo):
    estado_actual = registro[6]
    codigo = registro[4]
    if estado_anterior == estado_actual:
        mensaje = f"Su expediente {codigo} mantiene el estado {estado_actual}."
    else:
        mensaje = (
            f"Su expediente {codigo} cambió de estado: "
            f"{estado_anterior} -> {estado_actual}."
        )
    if motivo:
        mensaje += f" {motivo}"

    notificacion = [
        datetime.datetime.now().astimezone().isoformat(timespec="seconds"),
        mensaje,
    ]
    registro[8].append(notificacion)
    return notificacion

def mostrar_notificacion(registro, notificacion):
    print("\n=== NOTIFICACIÓN AL CIUDADANO ===")
    print("Para:", registro[1], "| DNI:", registro[0])
    print("Correo:", registro[10])
    print("Celular:", registro[2])
    print("Asunto: Estado de su expediente", registro[4])
    print("Mensaje:", notificacion[1])

def pedir_expediente(expedientes, mensaje):
    codigo = entradas.pedir_texto(mensaje)
    encontrados = buscar_registros(expedientes, codigo)
    if not encontrados:
        print("Expediente no encontrado.")
        return None
    registro = encontrados[0]
    preparar_expediente(registro)
    return registro

def pedir_expedientes(expedientes):
    criterio = entradas.pedir_texto(
        "Ingrese el código del expediente o el DNI: "
    )
    encontrados = buscar_registros(expedientes, criterio)
    if not encontrados:
        print("No se encontraron expedientes.")
        return []
    for registro in encontrados:
        preparar_expediente(registro)
    return encontrados

def seleccionar_opcion(opciones, mensaje):
    for indice, opcion in enumerate(opciones, start=1):
        print(f"{indice}. {opcion}")
    numero = entradas.pedir_entero_positivo(mensaje)
    if numero > len(opciones):
        print("Opción no válida.")
        return None
    return opciones[numero - 1]

def actualizar_estado(expedientes):
    print("\n=== ACTUALIZAR ESTADO ===")
    registro = pedir_expediente(
        expedientes,
        "Ingrese código de expediente: "
    )
    if registro is None:
        return

    print("Estados disponibles:")
    nuevo_estado = seleccionar_opcion(
        ESTADOS,
        "Seleccione el nuevo estado: "
    )
    if nuevo_estado is None:
        return

    estado_anterior = registro[6]
    if nuevo_estado == estado_anterior:
        print("El expediente ya se encuentra en ese estado.")
        return

    registro[6] = nuevo_estado
    notificacion = crear_notificacion(registro, estado_anterior, "")
    if almacenamiento.guardar_expedientes(expedientes):
        mostrar_notificacion(registro, notificacion)
        print("Estado actualizado correctamente.")
        return

    registro[6] = estado_anterior
    registro[8].pop()
    print("No se pudo guardar el cambio.")

def buscar_expediente(expedientes):
    print("\n=== CONSULTA DE EXPEDIENTES ===")
    encontrados = pedir_expedientes(expedientes)
    for registro in encontrados:
        print("\n---------- EXPEDIENTE ----------")
        print("Código:", registro[4])
        print("DNI:", registro[0])
        print("Ciudadano:", registro[1])
        print("Celular:", registro[2])
        print("Trámite:", registro[3])
        print("Fecha:", registro[5])
        print("Estado:", registro[6])
        print("Área responsable:", registro[7])
        print("Observación:", registro[12])
        print("Notificaciones:", len(registro[8]))
        print("-------------------------------")

def consultar_notificaciones(expedientes):
    print("\n=== NOTIFICACIONES AL CIUDADANO ===")
    encontrados = pedir_expedientes(expedientes)
    for registro in encontrados:
        print("\n---------- NOTIFICACIONES ----------")
        print("Expediente:", registro[4])
        print("Ciudadano:", registro[1])
        print("Correo:", registro[10])
        notificaciones = registro[8]
        if not notificaciones:
            print("Todavía no hay notificaciones.")
        for notificacion in notificaciones:
            print("-", notificacion[0], "|", notificacion[1])
        print("-------------------------------------")

def derivar_expediente(expedientes):
    print("\n=== DERIVAR DOCUMENTOS A UN ÁREA ===")
    registro = pedir_expediente(
        expedientes,
        "Ingrese código de expediente: "
    )
    if registro is None:
        return

    print("Áreas disponibles:")
    area = seleccionar_opcion(
        AREAS_RESPONSABLES,
        "Seleccione el área responsable: "
    )
    if area is None:
        return

    estado_anterior = registro[6]
    area_anterior = registro[7]
    registro[6] = "Derivado"
    registro[7] = area
    notificacion = crear_notificacion(
        registro,
        estado_anterior,
        f"Área responsable: {area}."
    )
    if almacenamiento.guardar_expedientes(expedientes):
        mostrar_notificacion(registro, notificacion)
        print("Expediente derivado correctamente.")
        return

    registro[6] = estado_anterior
    registro[7] = area_anterior
    registro[8].pop()
    print("No se pudo guardar la derivación.")

def generar_reporte(expedientes):
    print("=== REPORTE DIARIO DE MESA DE PARTES ===")
    hoy = datetime.datetime.now().astimezone().date().isoformat()
    registros_hoy = []
    for registro in expedientes:
        preparar_expediente(registro)
        if str(registro[5]).startswith(hoy):
            registros_hoy.append(registro)
    print("Fecha del reporte:", hoy)
    print("Total de expedientes ingresados hoy:", len(registros_hoy))
    if not registros_hoy:
        print("No existen trámites registrados hoy.")
        return

    for titulo, indice in (
        ("Cantidad por tipo de trámite:", 3),
        ("Cantidad por estado:", 6)
    ):
        print("\n" + titulo)
        conteo = []
        for registro in registros_hoy:
            valor = registro[indice] or "Sin especificar"
            for grupo in conteo:
                if grupo[0] == valor:
                    grupo[1] += 1
                    break
            else:
                conteo.append([valor, 1])
        for valor, cantidad in conteo:
            print(f"- {valor}: {cantidad}")
    print("\nReporte generado correctamente.")

def listar_expedientes(expedientes):
    print("\n=== LISTA DE EXPEDIENTES ===")
    if not expedientes:
        print("Todavía no existen registros.")
        return

    for registro in expedientes:
        preparar_expediente(registro)
        print(registro[4], "|", registro[1], "|", registro[3], "|", registro[6])

#################################
#         Deyvis Marcos         #
#################################

import validaciones
import entradas
import datetime
import almacenamiento

def registrar_tramite(expedientes):
    DNI = pedir_datos(validaciones.validar_dni, "DNI (8 dígitos)")

    Nombre = pedir_datos(validaciones.validar_nombre, "Nombre")

    telefono = pedir_datos(validaciones.validar_telefono, "telefono (9 digitos)")

    tipo_tramite = entradas.pedir_texto("Tipo de trámite: ")

    codigo = generar_codigo_expediente(expedientes)

    fecha_hora = datetime.datetime.now().astimezone().isoformat(timespec="seconds")

    nuevo_expediente = [DNI, Nombre, telefono, tipo_tramite, codigo, fecha_hora, None]

    expedientes.append(nuevo_expediente)

    almacenamiento.guardar_expedientes(expedientes)
    
    print("ya se guardo el expediente")

def registrar_observacion(expedientes):
    codigo = entradas.pedir_texto("ingerse el codigo del expediente: ")
    registros = buscar_registros(expedientes, codigo)
    registro = registros [0]
    observacion = entradas.pedir_texto("ingrese la observacion: ")
    registro[-1] = observacion 
    almacenamiento.guardar_expedientes(expedientes)
        
    print("se registro la observavion correctamente")

# FUNCIONES DE AYUDA

def pedir_datos(funcion_validacion, mensaje):
    while True:
        datos = input(f'Ingrese su {mensaje}: ')
        validacion = funcion_validacion(datos)

        if validacion:
            break
        else:
            print(f"{mensaje} inválido. Por favor, ingrese un {mensaje} válido.")
    
    return datos

def generar_codigo_expediente(expedientes):
    """
    Genera códigos correlativos según el año actual.
    Ejemplo: EXP-2026-001.
    """
    anio = datetime.datetime.now().year
    prefijo = f"EXP-{anio}-"

    numeros_existentes = []

    for registro in expedientes:
        
        codigo = registro[4]

        if codigo.startswith(prefijo):
            try:
                numero = int(codigo.split("-")[-1])
                numeros_existentes.append(numero)
            except ValueError:
                continue

    siguiente = max(numeros_existentes, default=0) + 1

    return f"{prefijo}{siguiente:03d}"

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

    codigo = registro[4].lower()
    dni = registro[0]

    if criterio == codigo or criterio == dni:
        encontrados.insert(0, registro)

    return encontrados




