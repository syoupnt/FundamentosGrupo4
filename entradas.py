from colores import RED, RESET, YELLOW


def pedir_texto(mensaje):
    """Solicita un texto obligatorio."""
    while True:
        dato = input(YELLOW + mensaje + RESET).strip()

        if dato:
            return dato

        print(RED + "Error: Este campo no puede estar vacío." + RESET)


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
