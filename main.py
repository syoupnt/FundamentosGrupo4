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
