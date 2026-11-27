import json
import os

from colores import RED, RESET


ARCHIVO_JSON = "expedientes.json"


def cargar_expedientes():
    """
    Lee los expedientes guardados.
    Si el archivo no existe, comienza con una lista vacía.
    Convierte los registros JSON con campos a la estructura de listas.
    """
    if not os.path.exists(ARCHIVO_JSON):
        return []

    try:
        with open(ARCHIVO_JSON, 'r', encoding='utf-8') as archivo:
            datos = json.load(archivo)

        if not isinstance(datos, list):
            raise ValueError("El contenido JSON debe ser una lista.")

        if all(isinstance(registro, dict) for registro in datos):
            expedientes = []
            for registro in datos:
                observacion = registro.get("observacion", "") or ""
                notificaciones = [
                    [aviso.get("fecha_hora", ""), aviso.get("mensaje", "")]
                    for aviso in registro.get("notificaciones", [])
                ]
                expedientes.append([
                    registro.get("dni", ""),
                    registro.get("nombre", ""),
                    registro.get("telefono", ""),
                    registro.get("tipo_tramite", ""),
                    registro.get("expediente", ""),
                    registro.get("fecha_hora", ""),
                    registro.get(
                        "estado",
                        "Observado" if observacion else "Recibido"
                    ),
                    registro.get("area_responsable", ""),
                    notificaciones,
                    registro.get("fecha_observacion", ""),
                    registro.get("correo", ""),
                    observacion,
                    observacion,
                ])
            return expedientes

        if all(isinstance(registro, list) and len(registro) >= 7 for registro in datos):
            return datos

        raise ValueError("Hay registros con una estructura incorrecta.")

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
