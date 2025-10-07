# 1) Datos de ejemplo: Diccionario con nombre: (hora_entrada, hora_salida)

horarios = {
    'María':  ('08', '16'),
    'Juan':   ('09', '17'),
    'Lucía':  ('07', '15'),
    'Diego':  ('10', '18'),
    # Ampliación: nuevos empleados añadidos
    'Ana':    ('08', '14'),
    'Raúl':   ('12', '20'),
    'Sofía':  ('06', '14'),
    'Pablo':  ('11', '19'),
}


# 2) Función: mostrar_registros()

def mostrar_registros():
    """
    Muestra por pantalla todos los registros de horarios.
    Utiliza enumerate() para numerar desde 1 (o desde 0 si se desea probar).
    """
    print("\n--- LISTADO DE HORARIOS ---")
    for i, (nombre, (entrada, salida)) in enumerate(horarios.items(), start=1):
        print(f"{i}. {nombre:10s} -> Entrada: {entrada}h | Salida: {salida}h")
    print("----------------------------\n")


# 3) Función: validar_hora(hora_str)

def validar_hora(hora_str):
    """
    Valida y convierte una hora introducida por el usuario.
    Acepta tanto formato '08' como '08:30'.
    Devuelve la hora en formato decimal (por ejemplo, 8.5 para 08:30)
    o None si no es válida.
    """
    try:
        partes = hora_str.split(':')
        hora = int(partes[0])
        minutos = int(partes[1]) if len(partes) == 2 else 0

        if 0 <= hora <= 23 and 0 <= minutos < 60:
            return hora + minutos / 60
        else:
            return None
    except ValueError:
        return None


# 4) Función: contar_entradas()

def contar_entradas():
    """
    Solicita al usuario una hora y cuenta cuántos empleados
    han llegado antes o a esa hora.
    """
    while True:
        hora_usuario = input("Introduce una hora (0–23 o con minutos, ej. 08:30): ").strip()
        hora_valida = validar_hora(hora_usuario)

        if hora_valida is None:
            print("⚠️  Error: hora no válida. Intenta de nuevo.\n")
            continue
        else:
            break

    contador = 0

    for nombre, (hora_entrada, _) in horarios.items():
        # Convertir hora de entrada de cadena a número decimal
        entrada_valida = validar_hora(hora_entrada)
        if entrada_valida is not None and entrada_valida <= hora_valida:
            contador += 1

    print(f"\nA las {hora_usuario} han llegado {contador} empleado(s).\n")


# 5) Función: menu()

def menu():
    """
    Menú principal repetitivo (bucle while) para elegir acciones:
      1) Mostrar registros
      2) Contar entradas
      3) Salir
    """
    while True:
        print("========== MENÚ ==========")
        print("1) Mostrar registros")
        print("2) Contar entradas")
        print("3) Salir")
        opcion = input("Elige una opción (1-3): ").strip()

        if opcion == '1':
            mostrar_registros()
        elif opcion == '2':
            contar_entradas()
        elif opcion == '3':
            print("¡Hasta luego!")
            break
        else:
            print("⚠️  Opción no válida. Intenta de nuevo.\n")


# 6) Punto de entrada

if __name__ == '__main__':
    # Consejo de depuración:
    # Descomenta las líneas siguientes para pausar en este punto con debugpy.
    # import debugpy
    # debugpy.breakpoint()
    menu()
