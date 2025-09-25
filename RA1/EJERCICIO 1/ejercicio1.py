trabajadores = input("trabajadores?")
num_trabajadores = int(trabajadores)
print(trabajadores);

hora_salida = input("hora de salida?")  
print(hora_salida);

x = 5

while num_trabajadores > 0:
    print (num_trabajadores)
    num_trabajadores = num_trabajadores -1
    nombre_empleado = input("nombre empleado?")
    hora_entrada = input("hora entrada?")
    hora_salida = input("hora salida?")

    if hora_entrada > hora_salida:
        print("hora correcta")
    else:
        print("hora incorrecta")
else:
    print("final!");