from colores import RED, RESET, YELLOW


def pedir_texto(mensaje):
    """Solicita un texto obligatorio."""
    while True:
        dato = input(YELLOW + mensaje + RESET).strip()

        if dato:
            return dato

        print(RED + "Error: Este campo no puede estar vacío." + RESET)


def pedir_solo_numeros(mensaje, longitud=None):
    """
    Solicita un dato que solo puede contener números.
    Si se indica `longitud`, el valor debe tener exactamente esa cantidad de dígitos.
    """
    while True:
        dato = input(YELLOW + mensaje + RESET).strip()

        if not dato:
            print(RED + "Error: Este campo no puede estar vacío." + RESET)
            continue

        if not all('0' <= caracter <= '9' for caracter in dato):
            print(RED + "Error: Ingrese solo números." + RESET)
            continue

        if longitud is not None and len(dato) != longitud:
            print(
                RED
                + f"Error: Debe ingresar exactamente {longitud} números."
                + RESET
            )
            continue

        return dato


def pedir_entero_positivo(mensaje):
    """Evita errores cuando se ingresan letras en un número."""
    while True:
        dato = input(YELLOW + mensaje + RESET).strip()

        try:
            numero = int(dato)

            if numero > 0:
                return numero

            print(RED + "Ingrese un número mayor que cero." + RESET)

        except ValueError:
            print(RED + "Error: Debe ingresar un número entero." + RESET)
