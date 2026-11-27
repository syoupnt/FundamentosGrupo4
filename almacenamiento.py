import json
import os

from colores import RED, RESET


ARCHIVO_JSON = "expedientes.json"


def cargar_expedientes():
    """
    Lee los expedientes guardados.
    Si el archivo no existe, comienza con una lista vacía.
    """
    if not os.path.exists(ARCHIVO_JSON):
        return []

    try:
        with open(ARCHIVO_JSON, 'r', encoding='utf-8') as archivo:
            datos = json.load(archivo)

        if not isinstance(datos, list):
            raise ValueError("El contenido JSON debe ser una lista.")

        if not all(isinstance(registro, list) for registro in datos):
            raise ValueError("Hay registros con una estructura incorrecta.")

        return datos

    except (json.JSONDecodeError, OSError, ValueError) as error:
        raise RuntimeError(
            f"No se pudieron cargar los expedientes: {error}"
        )


def guardar_expedientes(expedientes):
    """
    Guarda los datos en JSON.
    Utiliza un archivo temporal para evitar dejar
    el archivo principal incompleto si ocurre un error.
    """
    archivo_temporal = ARCHIVO_JSON + ".tmp"

    try:
        with open(archivo_temporal, 'w', encoding='utf-8') as archivo:
            json.dump(
                expedientes,
                archivo,
                ensure_ascii=False,
                indent=4
            )

        os.replace(archivo_temporal, ARCHIVO_JSON)
        return True

    except OSError as error:
        print(RED + f"Error al guardar los datos: {error}" + RESET)

        if os.path.exists(archivo_temporal):
            os.remove(archivo_temporal)

        return False
