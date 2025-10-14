import json
import os


# CLASE Horarios: gestiona la carga y guardado de los datos
class Horarios:
    def __init__(self, archivo="horarios.json"):
        self.archivo = archivo
        self.datos = {
            'María':  ('08', '16'),
            'Juan':   ('09', '17'),
            'Lucía':  ('07', '15'),
            'Diego':  ('10', '18'),
            # Ampliación con nuevos empleados
            'Ana':    ('08', '14'),
            'Raúl':   ('12', '20'),
            'Sofía':  ('06', '14'),
            'Pablo':  ('11', '19'),
        }

        # Si ya existe el archivo, cargarlo. Si no, guardarlo.
        if os.path.exists(self.archivo):
            self.cargar()
        else:
            self.guardar()

    def guardar(self):
        """Guarda los horarios actuales en el archivo JSON."""
        with open(self.archivo, "w", encoding="utf-8") as f:
            json.dump(self.datos, f, ensure_ascii=False, indent=4)

    def cargar(self):
        """Carga los horarios desde el archivo JSON."""
        with open(self.archivo, "r", encoding="utf-8") as f:
            self.datos = json.load(f)


# FUNCIONES PRINCIPALES1

def mostrar_registros(horarios):

    print("\n--- LISTADO DE HORARIOS ---")
    for i, (nombre, (entrada, salida)) in enumerate(horarios.items(), start=1):
        print(f"{i}. {nombre:10s} -> Entrada: {entrada}h | Salida: {salida}h")
    print("----------------------------\n")


def validar_hora(hora_str):
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


def contar_entradas(horarios):

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
        entrada_valida = validar_hora(hora_entrada)
        if entrada_valida is not None and entrada_valida <= hora_valida:
            contador += 1

    print(f"\nA las {hora_usuario} han llegado {contador} empleado(s).\n")


def menu():
    horarios_obj = Horarios()

    while True:
        print("========== MENÚ ==========")
        print("1) Mostrar registros")
        print("2) Contar entradas")
        print("3) Salir")
        opcion = input("Elige una opción (1-3): ").strip()

        if opcion == '1':
            mostrar_registros(horarios_obj.datos)
        elif opcion == '2':
            contar_entradas(horarios_obj.datos)
        elif opcion == '3':
            print("¡Hasta luego!")
            break
        else:
            print("⚠️  Opción no válida. Intenta de nuevo.\n")


# PUNTO DE ENTRADA DEL PROGRAMA
if __name__ == '__main__':
    # Descomenta las líneas siguientes para depurar en VS Code:
    # import debugpy
    # debugpy.breakpoint()
    menu()
