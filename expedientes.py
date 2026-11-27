def actualizar_estado(expedientes):
    pass

def buscar_expediente(expedientes):
    pass

def consultar_notificaciones(expedientes):
    pass

def derivar_expediente(expedientes):
    pass

def generar_reporte(expedientes):
    pass

def listar_expedientes(expedientes):
    pass

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




