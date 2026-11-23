import re

# es solo numeros
def es_solo_numeros(cadena_texto):
    """Comprueba que una cadena contenga únicamente números."""
    return (
        len(cadena_texto) > 0
        and all('0' <= caracter <= '9' for caracter in cadena_texto)
    )


def validar_dni(dni):
    """El DNI debe contener exactamente 8 dígitos."""

    return len(dni) == 8 and es_solo_numeros(dni)


def tiene_un_arroba(correo):
    """Comprueba que exista exactamente un símbolo @."""
    return correo.count('@') == 1


def validar_correo(correo):
    """
    Comprueba que el correo tenga usuario, dominio
    y una extensión válida, por ejemplo .com o .gob.pe.
    """
    correo = correo.strip()

    if not tiene_un_arroba(correo):
        return 

    if ' ' in correo or '..' in correo:
        return False

    usuario, dominio = correo.split('@')

    # Validar el usuario y el dominio
    if not usuario or usuario.startswith('.') or usuario.endswith('.'):
        return False

    partes_dominio = dominio.split('.')

    if len(partes_dominio) < 2:
        return False

    if any(not parte for parte in partes_dominio):
        return False

    patron_dominio = r'^[A-Za-z0-9](?:[A-Za-z0-9-]*[A-Za-z0-9])?$'

    for parte in partes_dominio:
        if not re.fullmatch(patron_dominio, parte):
            return False

    extension = partes_dominio[-1]

    return len(extension) >= 2 and extension.isalpha()


def validar_telefono(telefono): 
    """Valida un número de celular de 9 dígitos."""
    return len(telefono) == 9 and es_solo_numeros(telefono)


def validar_nombre(nombre):
    """Comprueba que el nombre no esté vacío ni tenga números."""
    return (
        len(nombre.strip()) >= 3
        and not any(caracter.isdigit() for caracter in nombre)
    )
False