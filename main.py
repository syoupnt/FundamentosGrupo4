RED     = '\033[31m'
GREEN   = '\033[32m'
YELLOW  = '\033[33m'
BLUE    = '\033[34m'
CYAN    = '\033[36m'

BRIGHT    = '\033[1m'
DIM       = '\033[2m'
RESET_ALL = '\033[0m'

# Frank Anderssón
def es_solo_numeros(cadena_texto):
    longitud = len(cadena_texto)
    cont_numeros = 0

    for i in range(longitud):              # en Python los índices empiezan en 0
        caracter_actual = cadena_texto[i]
        if '0' <= caracter_actual <= '9':
            cont_numeros += 1

    return cont_numeros == longitud and longitud > 0

# Ricky Brandon
def tiene_un_arroba(correo):
    return correo.count('@') == 1

# Deyvis Angel
def tiene_un_punto_com(correo):
    len_correo = len(correo)
    sub = correo[len_correo-4:len_correo]

    if sub == '.com':
        val = True
    else:
        val = False

    return val

# Jhon Huaman
def generar_reporte(total_registros):
    print(DIM + '----------------------------------------' + RESET_ALL)
    print(BRIGHT + CYAN + '=== REPORTE DIARIO DE MESA DE PARTES ===' + RESET_ALL)
    print(BLUE + 'Total de expediente(s) ingresados hoy: ' + RESET_ALL, total_registros)
    print(GREEN + 'Cierre de jornada completado sin demoras operativas.' + RESET_ALL)
    print(DIM + '----------------------------------------' + RESET_ALL)

# Carlos De Zela
def registrar_tramite(contador):
    print(BRIGHT + CYAN + '--- REGISTRO DE TRÁMITE ---' + RESET_ALL)

    while True:
        dni = input(YELLOW + 'Ingrese DNI del ciudadano (8 dígitos): ' + RESET_ALL)
        if len(dni) == 8 and es_solo_numeros(dni):
            break
        print(RED + 'Error: Ingrese exactamente 8 números.' + RESET_ALL)

    nombre = input(YELLOW + 'Ingrese Nombres Completos: ' + RESET_ALL)

    while True:
        correo = input(YELLOW + 'Ingrese Correo Electrónico: ' + RESET_ALL)
        if tiene_un_arroba(correo) and tiene_un_punto_com(correo):
            break
        print(RED + 'Error: Tu correo no es válido.' + RESET_ALL)

    tipo_tramite = input(YELLOW + 'Ingrese Tipo de Trámite: ' + RESET_ALL)
    num_hojas = int(input(YELLOW + 'Ingrese Cantidad de Hojas: ' + RESET_ALL))

    expediente_generado = f'EXP-2026-00{contador}'
    print(DIM + '----------------------------------------' + RESET_ALL)
    print(BRIGHT + GREEN + '¡Trámite registrado con éxito!' + RESET_ALL)
    print(BLUE + 'Su número de expediente asignado es: ' + RESET_ALL, expediente_generado)
    print(GREEN + 'Comprobante digital (cargo) generado para el ciudadano.' + RESET_ALL)
    print(DIM + '----------------------------------------' + RESET_ALL)

    return contador + 1

def main():
    contador_correlativo = 1
    continuar = True

    while continuar:
        print()
        print(BRIGHT + CYAN + '=== SISTEMA MESA DE PARTES DIGITAL - ONPE ===' + RESET_ALL)
        print(GREEN + '1. Registrar nuevo trámite' + RESET_ALL)
        print(BLUE + '2. Generar reporte diario de cierre' + RESET_ALL)
        print(RED + '3. Salir' + RESET_ALL)

        opcion = int(input(YELLOW + 'Seleccione una opción: ' + RESET_ALL))

        match opcion:
            case 1:
                contador_correlativo = registrar_tramite(contador_correlativo)
            case 2:
                generar_reporte(contador_correlativo - 1)
            case 3:
                continuar = False
                print(BLUE + 'Saliendo del sistema...' + RESET_ALL)
            case _:
                print(RED + 'Opción no válida. Intente nuevamente.' + RESET_ALL)

main()
