def TieneUnPuntoCom(correo):
    len_correo = len(correo)
    sub = correo[len_correo-4:len_correo]

    if sub == '.com':
        val = True
    else:
        val = False

    return val