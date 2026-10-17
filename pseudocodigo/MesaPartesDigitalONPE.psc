Función esNumero <- EsSoloNumeros(cadenaTexto) 
	Definir esNumero Como Lógico 
	Definir i, contNumeros, len Como Entero 
	Definir caracterActual Como Cadena 

	len <- Longitud(cadenaTexto) 

	contNumeros <- 0 

	Para i<-1 Hasta len Hacer 
		caracterActual <- Subcadena(cadenaTexto,i,i) 
		
		Si caracterActual>='0' Y caracterActual<='9' Entonces 
			contNumeros <- contNumeros+1
		FinSi 
	FinPara 

	Si contNumeros==len Y len>0 Entonces 
		esNumero <- Verdadero 
	SiNo 
		esNumero <- Falso 
	FinSi 
FinFunción

Funcion val <- TieneUnArroba(correo)
	Definir len, cont Como Entero
	Definir caracterActual Como Caracter
	
	len <- Longitud(correo)
	cont <- 0
	
	Para i<-1 Hasta len Hacer
		caracterActual <- Subcadena(correo,i,i)
		
		Si caracterActual == '@' Entonces
			cont <- cont + 1
		FinSi
	FinPara
	
	Si cont == 1 Entonces
		val <- Verdadero
	SiNo
		val <- Falso
	FinSi
FinFuncion

Funcion val <- TieneUnPuntoCom(correo)
	len <- Longitud(correo)
	sub <- Subcadena(correo, len-4+1, len)
	
	Si sub == '.com' Entonces
		val <- Verdadero
	SiNo
		val <- Falso
	FinSi
FinFuncion

Función RegistrarTramite(contador Por Referencia) 
	Definir dni, nombre, correo, tipoTramite, expedienteGenerado Como Cadena 
	Definir numHojas Como Entero 
	Definir dniValido Como Lógico
	Definir correoValido Como Logico

	Escribir '--- REGISTRO DE TRÁMITE ---' 

	Repetir 
		Escribir 'Ingrese DNI del ciudadano (8 dígitos):' 
		Leer dni 
		
		Si Longitud(dni)==8 Y EsSoloNumeros(dni) Entonces 
			dniValido <- Verdadero 
		SiNo 
			dniValido <- Falso 
			Escribir 'Error: Ingrese exactamente 8 números.' 
		FinSi 
	Hasta Que dniValido==Verdadero 

	Escribir 'Ingrese Nombres Completos:' 
	Leer nombre
	
	Repetir
		Escribir 'Ingrese Correo Electrónico:' 
		Leer correo
		
		Si TieneUnArroba(correo) Y TieneUnPuntoCom(correo) Entonces
			correoValido <- Verdadero
		SiNo
			correoValido <- Falso
			Escribir  'Error: Tu correo no es valido.'
		FinSi
	Hasta Que correoValido==Verdadero
	
	Escribir 'Ingrese Tipo de Trámite:' 
	Leer tipoTramite 
	Escribir 'Ingrese Cantidad de Hojas:' 
	Leer numHojas 
	expedienteGenerado <- Concatenar('EXP-2026-00',ConvertirATexto(contador)) 
	contador <- contador+1 

	Escribir '----------------------------------------' 
	Escribir '¡Trámite registrado con éxito!' 
	Escribir 'Su número de expediente asignado es: ', expedienteGenerado 
	Escribir 'Comprobante digital (cargo) generado para el ciudadano.' 
	Escribir '----------------------------------------' 
FinFunción 



Función GenerarReporte(totalRegistros) 
	Escribir '----------------------------------------' 
	Escribir '=== REPORTE DIARIO DE MESA DE PARTES ===' 
	Escribir 'Total de expediente(s) ingresados hoy: ', totalRegistros 
	Escribir 'Cierre de jornada completado sin demoras operativas.' 
	Escribir '----------------------------------------'
FinFunción 

Algoritmo MesaPartesDigitalONPE 
	Definir opcion, contadorCorrelativo, totalProcesados Como Entero 
	Definir continuar Como Lógico 
	
	contadorCorrelativo <- 1 
	continuar <- Verdadero 
	
	Mientras continuar==Verdadero Hacer 
		Escribir '' 
		Escribir '=== SISTEMA MESA DE PARTES DIGITAL - ONPE ===' 
		Escribir '1. Registrar nuevo trámite' 
		Escribir '2. Generar reporte diario de cierre' 
		Escribir '3. Salir' 
		Escribir 'Seleccione una opción:' 
		
		Leer opcion 
		Según opcion Hacer 
			1: 
				RegistrarTramite(contadorCorrelativo) 
			2: 
				totalProcesados <- contadorCorrelativo-1 
				GenerarReporte(totalProcesados) 
			3: 
				continuar <- Falso 
				Escribir 'Saliendo del sistema...' 
			De Otro Modo: 
				Escribir 'Opción no válida. Intente nuevamente.' 
		FinSegún 
	FinMientras 
FinAlgoritmo 