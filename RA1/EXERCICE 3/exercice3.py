# Practica 3

import csv;
import os;

# Clase para gestionar los horarios del personal
class RegistroHorario:
    """Representa un registro de horario de un empleado en un día concreto."""

    def __init__(self, empleado: str, dia: str, entrada: int, salida: int):
        self.empleado = empleado
        self.dia = dia
        self.entrada = entrada
        self.salida = salida

    def duracion(self) -> int:
        """Devuelve la cantidad de horas trabajadas en este registro."""
        return self.salida - self.entrada


# Clase Empleado
class Empleado:
    """Almacena los registros de un empleado y permite calcular estadísticas."""

    def __init__(self, nombre: str):
        self.nombre = nombre
        self.registros = []

    def agregar_registro(self, registro: RegistroHorario):
        """Añade un nuevo registro de horario al empleado."""
        self.registros.append(registro)

    def horas_totales(self) -> int:
        """Suma todas las horas trabajadas en la semana."""
        return sum(r.duracion() for r in self.registros)

    def dias_trabajados(self) -> int:
        """Cuenta los días distintos que trabajó el empleado."""
        return len({r.dia for r in self.registros})

    def fila_csv(self):
        """Devuelve una lista con los datos para escribir en el CSV de resumen."""
        return [self.nombre, self.dias_trabajados(), self.horas_totales()]


# Clase GestorHorarios
class GestorHorarios:
    """Clase que gestiona la lectura, análisis y escritura de los horarios."""

    def __init__(self, fichero_entrada: str):
        self.fichero_entrada = fichero_entrada
        self.registros = []
        self.empleados = {}
        self.empleados_por_dia = {}

    def leer_csv(self):
        """Lee el fichero de entrada y crea los objetos RegistroHorario."""
        with open(self.fichero_entrada, newline='', encoding='utf-8') as f:
            lector = csv.reader(f, delimiter=';', quotechar='"')
            for fila in lector:
                nombre, dia, h_entrada, h_salida = fila
                registro = RegistroHorario(nombre, dia, int(h_entrada), int(h_salida))
                self.registros.append(registro)

                # Añadir al diccionario de empleados
                if nombre not in self.empleados:
                    self.empleados[nombre] = Empleado(nombre)
                self.empleados[nombre].agregar_registro(registro)

                # Añadir al conjunto de empleados por día
                if dia not in self.empleados_por_dia:
                    self.empleados_por_dia[dia] = set()
                self.empleados_por_dia[dia].add(nombre)

        print(f"✅ Se han leído {len(self.registros)} registros correctamente.")

    def mostrar_empleados_por_dia(self):
        """Muestra los empleados que trabajaron cada día."""
        print("\n📅 Empleados por día:")
        for dia, empleados in self.empleados_por_dia.items():
            print(f"{dia}: {', '.join(empleados)}")

    def operaciones_conjuntos(self):
        """Ejemplos de operaciones de teoría de conjuntos."""
        if "Lunes" in self.empleados_por_dia and "Viernes" in self.empleados_por_dia:
            inter = self.empleados_por_dia["Lunes"] & self.empleados_por_dia["Viernes"]
            print(f"\n👥 Empleados que trabajaron Lunes y Viernes: {inter}")

        if "Sábado" in self.empleados_por_dia and "Domingo" in self.empleados_por_dia:
            exclusivos = self.empleados_por_dia["Sábado"] - self.empleados_por_dia["Domingo"]
            print(f"🧍 Empleados que trabajaron sólo el Sábado: {exclusivos}")

    def empleados_madrugadores(self, hora_referencia=8):
        """Obtiene empleados que entran antes de una hora dada."""
        madrugadores = {r.empleado for r in self.registros if r.entrada < hora_referencia}
        with open('madrugadores.csv', 'w', newline='', encoding='utf-8') as f:
            escritor = csv.writer(f, delimiter=';', quotechar='"')
            escritor.writerow(["Empleado", "Hora entrada"])
            for r in self.registros:
                if r.entrada < hora_referencia:
                    escritor.writerow([r.empleado, r.entrada])
        print(f"🌅 Archivo 'madrugadores.csv' creado con {len(madrugadores)} empleados.")

    def generar_resumen(self):
        """Crea un archivo con el resumen semanal de cada empleado."""
        with open('resumen_clases.csv', 'w', newline='', encoding='utf-8') as f:
            escritor = csv.writer(f, delimiter=';', quotechar='"')
            escritor.writerow(["Empleado", "Días trabajados", "Horas totales"])
            for empleado in self.empleados.values():
                escritor.writerow(empleado.fila_csv())

        print("📁 Archivo 'resumen_clases.csv' generado correctamente.")


#Función principal
def main():
    gestor = GestorHorarios("horarios.csv")
    gestor.leer_csv()
    gestor.mostrar_empleados_por_dia()
    gestor.operaciones_conjuntos()
    gestor.empleados_madrugadores(hora_referencia=8)
    gestor.generar_resumen()


# Ejecución del programa
if __name__ == "__main__":
    main()