def TieneUnPuntoCom(correo):
    len_correo = len(correo)
    sub = correo[len_correo-4:len_correo]

    if sub == '.com':
        val = True
    else:
        val = False

    return val
def tiene_un_arroba(correo):
    return correo.count('@') == 1
def generar_reporte(total_registros):
    print('----------------------------------------')
    print('=== REPORTE DIARIO DE MESA DE PARTES ===')
    print('Total de expediente(s) ingresados hoy: ', total_registros)
    print('Cierre de jornada completado sin demoras operativas.')
    print('----------------------------------------')
#Es solo numeros//
def es_solo_numeros(cadena_texto):
    longitud = len(cadena_texto)
    cont_numeros = 0

    for i in range(longitud):              # en Python los índices empiezan en 0
        caracter_actual = cadena_texto[i]
        if '0' <= caracter_actual <= '9':
            cont_numeros += 1

    return cont_numeros == longitud and longitud > 0

print(es_solo_numeros("12345678"))  # True
print(es_solo_numeros("1234a678"))  # False
print(es_solo_numeros(""))          # False (por la condición len > 0)
