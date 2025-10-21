import json
import os

# Clase para gestionar los horarios del personal
class Horarios:
    def __init__(self, archivo=None):
        # Si no se indica archivo, se guarda dentro de la carpeta del script
        if archivo is None:
            archivo = os.path.join(os.path.dirname(__file__), "horarios.json")

        self.archivo = archivo

        # Datos iniciales
        self.datos = {
            "María": ("08", "16"),
            "Juan": ("09", "17"),
            "Lucía": ("07", "15"),
            "Diego": ("10", "18"),
            "Ana": ("08", "14"),
            "Raúl": ("12", "20"),
            "Sofía": ("06", "14"),
            "Pablo": ("11", "19")
        }

        # Si ya existe el archivo, cargamos los datos
        if os.path.exists(self.archivo):
            self.cargar()
        else:
            self.guardar()

    def guardar(self):
        # Guarda los horarios en un archivo JSON
        with open(self.archivo, "w", encoding="utf-8") as f:
            json.dump(self.datos, f, ensure_ascii=False, indent=4)

    def cargar(self):
        # Carga los horarios desde el archivo JSON
        with open(self.archivo, "r", encoding="utf-8") as f:
            self.datos = json.load(f)


# Función para mostrar los registros por pantalla
def mostrar_registros(horarios):
    print("\n=== LISTA DE HORARIOS ===")
    for i, (nombre, (entrada, salida)) in enumerate(horarios.items(), start=1):
        print(f"{i}. {nombre:10s} -> Entrada: {entrada}h | Salida: {salida}h")
    print("==========================\n")


# Convierte una hora tipo "08" o "08:30" en número (8.5, por ejemplo)
def validar_hora(hora_str):
    try:
        partes = hora_str.split(":")
        hora = int(partes[0])
        minutos = int(partes[1]) if len(partes) == 2 else 0

        if 0 <= hora <= 23 and 0 <= minutos < 60:
            return hora + minutos / 60
        else:
            return None
    except ValueError:
        return None


# Cuenta cuántos empleados ya han entrado a cierta hora
def contar_entradas(horarios):
    while True:
        hora_usuario = input("Introduce una hora (ej. 08 o 08:30): ").strip()
        hora_valida = validar_hora(hora_usuario)

        if hora_valida is None:
            print("Hora no válida, prueba otra vez.\n")
            continue
        else:
            break

    contador = 0
    for nombre, (entrada, _) in horarios.items():
        entrada_valida = validar_hora(entrada)
        if entrada_valida is not None and entrada_valida <= hora_valida:
            contador += 1

    print(f"\nA las {hora_usuario} han llegado {contador} empleado(s).\n")


# Menú principal
def menu():
    horarios = Horarios()

    while True:
        print("====== MENÚ PRINCIPAL ======")
        print("1) Mostrar registros")
        print("2) Contar entradas")
        print("3) Salir")
        opcion = input("Elige una opción (1-3): ").strip()

        if opcion == "1":
            mostrar_registros(horarios.datos)
        elif opcion == "2":
            contar_entradas(horarios.datos)
        elif opcion == "3":
            print("¡Hasta luego!")
            break
        else:
            print("Opción no válida, intenta otra vez.\n")


# Punto de entrada del programa
if __name__ == "__main__":
    menu()
