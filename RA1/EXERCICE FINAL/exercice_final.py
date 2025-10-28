import csv
import os
import re
from datetime import datetime, date
from typing import List, Dict, Tuple, Set

DATA_DIR = "data"
CLIENTES_CSV = os.path.join(DATA_DIR, "clientes.csv")
EVENTOS_CSV = os.path.join(DATA_DIR, "eventos.csv")
VENTAS_CSV = os.path.join(DATA_DIR, "ventas.csv")
INFORME_CSV = os.path.join(DATA_DIR, "informe_resumen.csv")

DATE_FORMAT = "%Y-%m-%d"  # fechas: YYYY-MM-DD

# Clases del dominio
class Cliente:
    def __init__(self, id_: int, nombre: str, email: str, fecha_alta: date):
        self.id = id_
        self.nombre = nombre
        self.email = email
        self.fecha_alta = fecha_alta

    def antiguedad_dias(self) -> int:
        return (date.today() - self.fecha_alta).days

    def __str__(self):
        return f"[{self.id}] {self.nombre} <{self.email}> (alta: {self.fecha_alta})"

    def to_csv_row(self) -> List[str]:
        return [str(self.id), self.nombre, self.email, self.fecha_alta.strftime(DATE_FORMAT)]


class Evento:
    def __init__(self, id_: int, titulo: str, fecha_evento: date, categoria: str):
        self.id = id_
        self.titulo = titulo
        self.fecha_evento = fecha_evento
        self.categoria = categoria

    def dias_hasta_evento(self) -> int:
        return (self.fecha_evento - date.today()).days

    def __str__(self):
        return f"[{self.id}] {self.titulo} ({self.categoria}) - {self.fecha_evento}"

    def to_csv_row(self) -> List[str]:
        return [str(self.id), self.titulo, self.fecha_evento.strftime(DATE_FORMAT), self.categoria]


class Venta:
    def __init__(self, id_: int, cliente_id: int, evento_id: int, fecha_venta: date, cantidad: int, precio_unitario: float):
        self.id = id_
        self.cliente_id = cliente_id
        self.evento_id = evento_id
        self.fecha_venta = fecha_venta
        self.cantidad = cantidad
        self.precio_unitario = precio_unitario

    def total(self) -> float:
        return self.cantidad * self.precio_unitario

    def __str__(self):
        return f"[{self.id}] cliente:{self.cliente_id} evento:{self.evento_id} {self.cantidad}x {self.precio_unitario:.2f} on {self.fecha_venta}"

    def to_csv_row(self) -> List[str]:
        return [str(self.id), str(self.cliente_id), str(self.evento_id),
                self.fecha_venta.strftime(DATE_FORMAT), str(self.cantidad), f"{self.precio_unitario:.2f}"]


# Funciones utilitarias CSV
def ensure_data_files():
    """Crea la carpeta data/ y archivos de ejemplo si no existen."""
    os.makedirs(DATA_DIR, exist_ok=True)

    if not os.path.exists(CLIENTES_CSV):
        with open(CLIENTES_CSV, "w", newline="", encoding="utf-8") as f:
            w = csv.writer(f, delimiter=";", quotechar='"', quoting=csv.QUOTE_MINIMAL)
            w.writerow(["1", "Anaérez", "ana@example.com", "2023-02-10"])
            w.writerow(["2", "Luis Gómez", "luis@example.com", "2024-05-01"])
            w.writerow(["3", "María Ruiz", "maria.ruiz@example.com", "2023-11-20"])

    if not os.path.exists(EVENTOS_CSV):
        with open(EVENTOS_CSV, "w", newline="", encoding="utf-8") as f:
            w = csv.writer(f, delimiter=";", quotechar='"', quoting=csv.QUOTE_MINIMAL)
            today = date.today()
            w.writerow(["1", "Concierto Rock", (today.replace(day=min(28, today.day)) + 
                                               datetime.timedelta(days=10)).strftime(DATE_FORMAT) if False else (today.strftime(DATE_FORMAT)) , "Música"])
            w.writerow(["1", "Concierto Rock", (date.today()).strftime(DATE_FORMAT), "Música"])
            w.writerow(["2", "Feria Tecnología", (date.today()).strftime(DATE_FORMAT), "Tecnología"])
            w.writerow(["3", "Mercado Vintage", (date.today()).strftime(DATE_FORMAT), "Ocio"])

    if not os.path.exists(VENTAS_CSV):
        with open(VENTAS_CSV, "w", newline="", encoding="utf-8") as f:
            w = csv.writer(f, delimiter=";", quotechar='"', quoting=csv.QUOTE_MINIMAL)
            w.writerow(["1", "1", "1", date.today().strftime(DATE_FORMAT), "2", "25.00"])
            w.writerow(["2", "2", "1", date.today().strftime(DATE_FORMAT), "1", "25.00"])
            w.writerow(["3", "3", "2", date.today().strftime(DATE_FORMAT), "3", "10.00"])


def parse_date(s: str) -> date:
    return datetime.strptime(s, DATE_FORMAT).date()


# Gestor principal
class GestorMiniCRM:
    def __init__(self):
        self.clientes: Dict[int, Cliente] = {}
        self.eventos: Dict[int, Evento] = {}
        self.ventas: Dict[int, Venta] = {}
        self.categorias: Set[str] = set()
        self.loaded = False

    def cargar_datos(self):
        """Lee los tres CSV y llena las colecciones (manejo de FileNotFoundError)."""
        try:
            with open(CLIENTES_CSV, newline="", encoding="utf-8") as f:
                r = csv.reader(f, delimiter=";", quotechar='"')
                for fila in r:
                    if not fila:
                        continue
                    id_, nombre, email, fecha_alta = fila
                    try:
                        id_i = int(id_)
                        fecha = parse_date(fecha_alta)
                        self.clientes[id_i] = Cliente(id_i, nombre, email, fecha)
                    except Exception as e:
                        print(f"[WARN] fila clientes inválida {fila}: {e}")
        except FileNotFoundError:
            print(f"[ERROR] No se encontró {CLIENTES_CSV}")

        try:
            with open(EVENTOS_CSV, newline="", encoding="utf-8") as f:
                r = csv.reader(f, delimiter=";", quotechar='"')
                for fila in r:
                    if not fila:
                        continue
                    id_, titulo, fecha_evento, categoria = fila
                    try:
                        id_i = int(id_)
                        fecha = parse_date(fecha_evento)
                        ev = Evento(id_i, titulo, fecha, categoria)
                        self.eventos[id_i] = ev
                        self.categorias.add(categoria)
                    except Exception as e:
                        print(f"[WARN] fila eventos inválida {fila}: {e}")
        except FileNotFoundError:
            print(f"[ERROR] No se encontró {EVENTOS_CSV}")

        try:
            with open(VENTAS_CSV, newline="", encoding="utf-8") as f:
                r = csv.reader(f, delimiter=";", quotechar='"')
                for fila in r:
                    if not fila:
                        continue
                    id_, cliente_id, evento_id, fecha_venta, cantidad, precio_unitario = fila
                    try:
                        id_i = int(id_)
                        clin = int(cliente_id)
                        evn = int(evento_id)
                        fecha = parse_date(fecha_venta)
                        cantidad_i = int(cantidad)
                        precio = float(precio_unitario)
                        self.ventas[id_i] = Venta(id_i, clin, evn, fecha, cantidad_i, precio)
                    except Exception as e:
                        print(f"[WARN] fila ventas inválida {fila}: {e}")
        except FileNotFoundError:
            print(f"[ERROR] No se encontró {VENTAS_CSV}")

        self.loaded = True
        print("✅ Datos cargados.")

    def listar(self, tabla: str):
        """Imprime la tabla formateada: clientes, eventos o ventas."""
        if not self.loaded:
            print("Cargar los datos primero (opción 1).")
            return

        if tabla.lower() == "clientes":
            print("\n--- Clientes ---")
            for c in sorted(self.clientes.values(), key=lambda x: x.id):
                print(c)
        elif tabla.lower() == "eventos":
            print("\n--- Eventos ---")
            for e in sorted(self.eventos.values(), key=lambda x: x.id):
                print(e)
        elif tabla.lower() == "ventas":
            print("\n--- Ventas ---")
            for v in sorted(self.ventas.values(), key=lambda x: x.id):
                print(f"{v} => total: {v.total():.2f}")
        else:
            print("Tabla desconocida. Opciones: clientes, eventos, ventas.")

    def nueva_id(self, colec: Dict[int, object]) -> int:
        """Genera nuevo id entero (1 + max existente)."""
        if not colec:
            return 1
        return max(colec.keys()) + 1

    def validar_email(self, email: str) -> bool:
        """Validación sencilla de email."""
        pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"
        return re.match(pattern, email) is not None

    def alta_cliente(self):
        """Pide datos por input, valida y añade el cliente (y guarda incrementalmente)."""
        nombre = input("Nombre completo: ").strip()
        email = input("Email: ").strip()
        if not self.validar_email(email):
            print("[ERROR] Email no válido.")
            return
        fecha_str = input(f"Fecha de alta (YYYY-MM-DD) [hoy {date.today()}]: ").strip()
        if not fecha_str:
            fecha_alta = date.today()
        else:
            try:
                fecha_alta = parse_date(fecha_str)
            except Exception:
                print("[ERROR] Fecha no válida.")
                return

        nuevo_id = self.nueva_id(self.clientes)
        cliente = Cliente(nuevo_id, nombre, email, fecha_alta)
        self.clientes[nuevo_id] = cliente

        # Guardar incrementalmente al CSV
        try:
            with open(CLIENTES_CSV, "a", newline="", encoding="utf-8") as f:
                w = csv.writer(f, delimiter=";", quotechar='"', quoting=csv.QUOTE_MINIMAL)
                w.writerow(cliente.to_csv_row())
            print(f"✅ Cliente añadido con id {nuevo_id}.")
        except Exception as e:
            print(f"[ERROR] al guardar cliente: {e}")

    def filtrar_ventas_por_rango(self):
        """Pide dos fechas e imprime ventas entre ambas (inclusive)."""
        desde_s = input("Fecha desde (YYYY-MM-DD): ").strip()
        hasta_s = input("Fecha hasta (YYYY-MM-DD): ").strip()
        try:
            desde = parse_date(desde_s)
            hasta = parse_date(hasta_s)
        except Exception:
            print("[ERROR] Formato de fecha inválido.")
            return

        if desde > hasta:
            print("[ERROR] 'desde' mayor que 'hasta'.")
            return

        resultado = [v for v in self.ventas.values() if desde <= v.fecha_venta <= hasta]
        print(f"\nVentas entre {desde} y {hasta}: ({len(resultado)})")
        total = 0.0
        for v in sorted(resultado, key=lambda x: x.fecha_venta):
            cliente_nombre = self.clientes.get(v.cliente_id).nombre if v.cliente_id in self.clientes else f"(id {v.cliente_id})"
            evento_titulo = self.eventos.get(v.evento_id).titulo if v.evento_id in self.eventos else f"(id {v.evento_id})"
            print(f"{v.id}: {v.fecha_venta} - {cliente_nombre} - {evento_titulo} - {v.cantidad}x {v.precio_unitario:.2f} => {v.total():.2f}")
            total += v.total()
        print(f"Total ventas en rango: {total:.2f}")

    def estadisticas(self):
        """Calcula y muestra varias métricas solicitadas."""
        if not self.loaded:
            print("Cargar los datos primero (opción 1).")
            return

        # ingresos totales
        ingresos_totales = sum(v.total() for v in self.ventas.values())

        # ingresos por evento
        ingresos_por_evento: Dict[int, float] = {}
        for v in self.ventas.values():
            ingresos_por_evento.setdefault(v.evento_id, 0.0)
            ingresos_por_evento[v.evento_id] += v.total()

        # set de categorías
        categorias = {e.categoria for e in self.eventos.values()}

        # dias hasta el evento más próximo
        proximos = [e.dias_hasta_evento() for e in self.eventos.values()]
        dias_hasta_mas_proximo = min(proximos) if proximos else None

        # tupla (min, max, media) de precios unitarios en ventas
        precios = [v.precio_unitario for v in self.ventas.values()]
        if precios:
            min_p = min(precios)
            max_p = max(precios)
            avg_p = sum(precios) / len(precios)
            tupla_precios = (min_p, max_p, avg_p)
        else:
            tupla_precios = (None, None, None)

        # mostrar
        print("\n--- Estadísticas ---")
        print(f"Ingresos totales: {ingresos_totales:.2f}")
        print("Ingresos por evento:")
        for ev_id, total in ingresos_por_evento.items():
            titulo = self.eventos.get(ev_id).titulo if ev_id in self.eventos else f"(id {ev_id})"
            print(f"  {titulo} [{ev_id}]: {total:.2f}")
        print(f"Categorías existentes: {', '.join(sorted(categorias)) if categorias else '(ninguna)'}")
        if dias_hasta_mas_proximo is not None:
            print(f"Días hasta el evento más próximo: {dias_hasta_mas_proximo}")
        else:
            print("No hay eventos.")
        print(f"Precios unitarios (min, max, media): {tupla_precios}")

        # devolver una tupla resumen por si se quiere usar programáticamente
        return ingresos_totales, ingresos_por_evento, categorias, dias_hasta_mas_proximo, tupla_precios

    def exportar_informe(self):
        """Genera informe_resumen.csv con totales por evento (id, titulo, ingresos)."""
        ingresos_por_evento: Dict[int, float] = {}
        for v in self.ventas.values():
            ingresos_por_evento.setdefault(v.evento_id, 0.0)
            ingresos_por_evento[v.evento_id] += v.total()

        with open(INFORME_CSV, "w", newline="", encoding="utf-8") as f:
            w = csv.writer(f, delimiter=";", quotechar='"', quoting=csv.QUOTE_MINIMAL)
            w.writerow(["evento_id", "titulo", "ingresos_totales"])
            for ev_id, ingreso in ingresos_por_evento.items():
                titulo = self.eventos.get(ev_id).titulo if ev_id in self.eventos else ""
                w.writerow([ev_id, titulo, f"{ingreso:.2f}"])

        print(f"Informe exportado a {INFORME_CSV}")

# Menú principal
def menu():
    ensure_data_files()  
    gestor = GestorMiniCRM()

    opciones = {
        "1": "Cargar CSV (clientes, eventos, ventas)",
        "2": "Listar tabla (clientes/eventos/ventas)",
        "3": "Alta de cliente",
        "4": "Filtrar ventas por rango de fechas",
        "5": "Estadísticas",
        "6": "Exportar informe resumen (CSV)",
        "7": "Salir"
    }

    while True:
        print("\n=== MINI-CRM DE EVENTOS ===")
        for k, v in opciones.items():
            print(f"{k}. {v}")
        choice = input("Elige una opción: ").strip()

        if choice == "1":
            gestor.cargar_datos()
        elif choice == "2":
            tabla = input("Qué tabla listar? (clientes/eventos/ventas): ").strip()
            gestor.listar(tabla)
        elif choice == "3":
            gestor.alta_cliente()
        elif choice == "4":
            gestor.filtrar_ventas_por_rango()
        elif choice == "5":
            gestor.estadisticas()
        elif choice == "6":
            gestor.exportar_informe()
        elif choice == "7":
            print("Adiós ")
            break
        else:
            print("Opción no válida. Intenta de nuevo.")


if __name__ == "__main__":
    menu()
