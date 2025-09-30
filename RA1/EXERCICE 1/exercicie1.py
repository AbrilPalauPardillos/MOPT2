# Practica 1 - Empleados y horarios

# Solicitar número de empleados y validar
while True:
    try:
        num_trabajadores = int(input("¿Cuántos empleados vas a introducir? "))
        if num_trabajadores > 0:
            break
        else:
            print("El número debe ser mayor que 0.")
    except ValueError:
        print("Introduce un número válido.")

# Solicitar hora de referencia y validar
while True:
    try:
        hora_referencia = int(input("Introduce la hora de referencia (0-23): "))
        if 0 <= hora_referencia <= 23:
            break
        else:
            print("La hora debe estar entre 0 y 23.")
    except ValueError:
        print("Introduce una hora válida.")

contador_entradas = 0
salida_mas_temprana = 24  # Valor imposible como inicialización
nombre_salida_temprana = ""

contador = 0
while contador < num_trabajadores:
    nombre_empleado = input(f"Nombre del empleado {contador+1}: ")

    # Validar hora de entrada
    while True:
        try:
            hora_entrada = int(input("Hora de entrada (0-23): "))
            if 0 <= hora_entrada <= 23:
                break
            else:
                print("La hora debe estar entre 0 y 23.")
        except ValueError:
            print("Introduce una hora válida.")

    # Validar hora de salida
    while True:
        try:
            hora_salida = int(input("Hora de salida (0-23): "))
            if 0 <= hora_salida <= 23 and hora_salida > hora_entrada:
                break
            else:
                print("La hora de salida debe estar entre 0 y 23 y ser mayor que la de entrada.")
        except ValueError:
            print("Introduce una hora válida.")

    # Contar empleados que entran antes o a la hora de referencia
    if hora_entrada <= hora_referencia:
        contador_entradas += 1

    # Determinar la salida más temprana
    if hora_salida < salida_mas_temprana:
        salida_mas_temprana = hora_salida
        nombre_salida_temprana = nombre_empleado

    contador += 1

print(f"\nEmpleados que entraron antes o a la hora de referencia: {contador_entradas}")
if nombre_salida_temprana != "":
    print(f"El empleado que salió más temprano fue {nombre_salida_temprana} a las {salida_mas_temprana}.")
else:
    print("No se registraron salidas.")