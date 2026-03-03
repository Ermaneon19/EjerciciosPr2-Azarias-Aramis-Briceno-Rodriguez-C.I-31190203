import random
from abc import ABC, abstractmethod

NOMBRES = ["Carlos", "Maria", "Pedro", "Ana", "Luis", "Elena", "Jorge", "Sofia"]
APELLIDOS = ["Garcia", "Lopez", "Martinez", "Rodriguez", "Hernandez", "Gomez"]

class Aldeano:
    def __init__(self, nombre=None, apellido=None, edad=None):
        self.nombre = nombre or random.choice(NOMBRES)
        self.apellido = apellido or random.choice(APELLIDOS)
        self.edad = edad or random.randint(18, 60)

    def __str__(self):
        return f"{self.nombre} {self.apellido} (edad: {self.edad})"

class Almacen:
    def __init__(self):
        self.__inventario = {
            "Trigo": 0, "Pan": 0, "Madera": 0, "Piedra": 0,
            "Hierro": 0, "Oro": 0, "Monedas": 0
        }
    def agregar_recursos(self, recursos):
        for recurso, cantidad in recursos.items():
            if recurso in self.__inventario:
                self.__inventario[recurso] += cantidad

    def consumir_recursos(self, recursos):
        for recurso, cantidad in recursos.items():
            if self.__inventario.get(recurso, 0) < cantidad:
                return False
        for recurso, cantidad in recursos.items():
            self.__inventario[recurso] -= cantidad
        return True

    def mostrar_inventario(self):
        print("--- Inventario del Almacen ---")
        for recurso, cantidad in self.__inventario.items():
            print(f"  {recurso}: {cantidad}")
        print("------------------------------")

    def obtener_cantidad(self, recurso):
        return self.__inventario.get(recurso, 0)

class Edificio(ABC):
    def __init__(self, nombre, costo_base):
        self.nombre = nombre
        self.nivel = 1
        self.costo_base = costo_base  

    def costo_mejora(self):
        return {r: c * self.nivel for r, c in self.costo_base.items()}

    def mejorar(self, almacen):
        costo = self.costo_mejora()
        if almacen.consumir_recursos(costo):
            self.nivel += 1
            print(f"{self.nombre} mejorado a nivel {self.nivel}.")
            return True
        else:
            print(f"No hay recursos suficientes para mejorar {self.nombre}.")
            return False

    @abstractmethod
    def describir(self):
        pass

class Casa(Edificio):
    _casas_construidas = 0

    def __init__(self):
        Casa._casas_construidas += 1
        nombre = f"Casa #{Casa._casas_construidas}"
        super().__init__(nombre, costo_base={"Madera": 5, "Piedra": 3})
        self.capacidad = 4 

    @staticmethod
    def costo_nueva_casa(cantidad_actual):
        factor = cantidad_actual + 1
        return {"Madera": 5 * factor, "Piedra": 3 * factor}

    def capacidad_total(self):
        return self.capacidad * self.nivel

    def describir(self):
        print(f"{self.nombre} | Nivel: {self.nivel} | Capacidad: {self.capacidad_total()}")


RECETAS = {
    "Granja":     {"costo": {},                          "produce": {"Trigo": 1},     "turnos": 1},
    "Panaderia":  {"costo": {"Trigo": 2},                "produce": {"Pan": 1},       "turnos": 1},
    "Aserradero": {"costo": {"Pan": 2},                  "produce": {"Madera": 3},    "turnos": 2},
    "Cantera":    {"costo": {"Pan": 2},                  "produce": {"Piedra": 3},    "turnos": 2},
    "Herreria":   {"costo": {"Piedra": 2, "Pan": 3},     "produce": {"Hierro": 1},    "turnos": 3},
    "Mina de Oro":{"costo": {"Hierro": 1, "Pan": 5},     "produce": {"Oro": 1},       "turnos": 3},
    "Casa Moneda":{"costo": {"Oro": 1},                  "produce": {"Monedas": 10},  "turnos": 1},
}

class EdificioTrabajo(Edificio):
    def __init__(self, tipo):
        if tipo not in RECETAS:
            raise ValueError(f"Tipo de edificio '{tipo}' no existe en las recetas.")
        receta = RECETAS[tipo]
        super().__init__(tipo, costo_base={"Madera": 3, "Piedra": 2})
        self.tipo = tipo
        self.costo_produccion = receta["costo"]
        self.produccion_base = receta["produce"]
        self.turnos_necesarios = receta["turnos"]
        self.turno_actual = 0
        self.lista_activos = []
        self.lista_espera = []
        self.produciendo = False 

    def agregar_aldeano(self, aldeano):
        self.lista_espera.append(aldeano)
        print(f"  {aldeano} asignado a lista de espera de {self.nombre}.")

    def remover_aldeano(self, aldeano):
        if aldeano in self.lista_espera:
            self.lista_espera.remove(aldeano)
            print(f"  {aldeano} removido de lista de espera de {self.nombre}.")
            return True
        
        if aldeano in self.lista_activos:
            self.lista_activos.remove(aldeano)
            self.turno_actual = 0
            self.produciendo = False
            print(f"  {aldeano} removido de activos de {self.nombre}. Progreso reiniciado.")
            return True
        return False

    def procesar_turno(self, almacen):
        """Ejecuta la logica de un turno para este edificio."""
        if len(self.lista_activos) == 0:
            return
        if not self.produciendo:
            costo_total = {r: c * len(self.lista_activos) for r, c in self.costo_produccion.items()}
            if costo_total:
                if not almacen.consumir_recursos(costo_total):
                    print(f"  [{self.nombre}] Detenido: faltan materiales.")
                    return
            self.produciendo = True
            self.turno_actual = 0

        self.turno_actual += 1

        if self.turno_actual >= self.turnos_necesarios:
            produccion = {}
            for recurso, cantidad in self.produccion_base.items():
                produccion[recurso] = cantidad * len(self.lista_activos) * self.nivel
            almacen.agregar_recursos(produccion)
            print(f"  [{self.nombre}] Produccion completada: {produccion}")
            self.turno_actual = 0
            self.produciendo = False
            if self.lista_espera:
                self.lista_activos.extend(self.lista_espera)
                print(f"  [{self.nombre}] {len(self.lista_espera)} aldeano(s) de espera se unieron a activos.")
                self.lista_espera.clear()
        else:
            restantes = self.turnos_necesarios - self.turno_actual
            print(f"  [{self.nombre}] En progreso... {restantes} turno(s) restantes.")

    def describir(self):
        estado = "Produciendo" if self.produciendo else "Inactivo"
        print(f"{self.nombre} | Nivel: {self.nivel} | Activos: {len(self.lista_activos)} "
              f"| Espera: {len(self.lista_espera)} | Estado: {estado} "
              f"| Progreso: {self.turno_actual}/{self.turnos_necesarios}")

class Asentamiento:
    def __init__(self, nombre):
        self.nombre = nombre
        self.almacen = Almacen()
        self.casas = []
        self.edificios_trabajo = []
        self.poblacion = []
        self.turno = 0

    def capacidad_total(self):
        return sum(c.capacidad_total() for c in self.casas)

    def construir_casa(self):
        costo = Casa.costo_nueva_casa(len(self.casas))
        if self.almacen.consumir_recursos(costo):
            casa = Casa()
            self.casas.append(casa)
            print(f"Casa construida. Capacidad total: {self.capacidad_total()}")
            return casa
        else:
            print(f"No hay recursos para construir casa. Costo: {costo}")
            return None

    def construir_edificio(self, tipo):
        costo = {"Madera": 3, "Piedra": 2}
        if self.almacen.consumir_recursos(costo):
            edificio = EdificioTrabajo(tipo)
            self.edificios_trabajo.append(edificio)
            print(f"Edificio '{tipo}' construido.")
            return edificio
        else:
            print(f"No hay recursos para construir {tipo}. Costo: {costo}")
            return None

    def reclutar_aldeano(self):
        if len(self.poblacion) >= self.capacidad_total():
            print("No hay espacio. Construye mas casas.")
            return None
        aldeano = Aldeano()
        self.poblacion.append(aldeano)
        print(f"Aldeano reclutado: {aldeano}")
        return aldeano

    def asignar_aldeano(self, aldeano, edificio):
        if aldeano not in self.poblacion:
            print("Ese aldeano no pertenece al asentamiento.")
            return False
        for e in self.edificios_trabajo:
            if aldeano in e.lista_activos or aldeano in e.lista_espera:
                print(f"{aldeano} ya esta asignado a {e.nombre}.")
                return False
        edificio.agregar_aldeano(aldeano)
        return True

    def remover_aldeano(self, aldeano, edificio):
        return edificio.remover_aldeano(aldeano)

    def avanzar_turno(self):
        self.turno += 1
        print(f"\n{'='*50}")
        print(f"  TURNO {self.turno}")
        print(f"{'='*50}")
        for edificio in self.edificios_trabajo:
            edificio.procesar_turno(self.almacen)
        print()
        self.almacen.mostrar_inventario()

    def estado(self):
        print(f"\n*** Asentamiento: {self.nombre} | Turno: {self.turno} ***")
        print(f"Poblacion: {len(self.poblacion)}/{self.capacidad_total()}")
        print("\nCasas:")
        for casa in self.casas:
            casa.describir()
        print("\nEdificios de trabajo:")
        for edificio in self.edificios_trabajo:
            edificio.describir()
        print()
        self.almacen.mostrar_inventario()


if __name__ == "__main__":
    print("=" * 50)
    print("SIMULADOR DE ASENTAMIENTO")
    print("=" * 50)

    pueblo = Asentamiento("Age Of Empire")

    pueblo.almacen.agregar_recursos({
        "Madera": 50, "Piedra": 30, "Trigo": 10, "Pan": 20
    })
    print("Recursos iniciales otorgados para la demo.\n")

    pueblo.construir_casa()
    pueblo.construir_casa()

    aldeanos = []
    for _ in range(5):
        a = pueblo.reclutar_aldeano()
        if a:
            aldeanos.append(a)

    granja = pueblo.construir_edificio("Granja")
    panaderia = pueblo.construir_edificio("Panaderia")
    aserradero = pueblo.construir_edificio("Aserradero")

    print("\n--- Asignando aldeanos ---")
    pueblo.asignar_aldeano(aldeanos[0], granja)
    pueblo.asignar_aldeano(aldeanos[1], granja)
    pueblo.asignar_aldeano(aldeanos[2], panaderia)
    pueblo.asignar_aldeano(aldeanos[3], aserradero)

    granja.lista_activos = granja.lista_espera[:]
    granja.lista_espera.clear()
    panaderia.lista_activos = panaderia.lista_espera[:]
    panaderia.lista_espera.clear()
    aserradero.lista_activos = aserradero.lista_espera[:]
    aserradero.lista_espera.clear()

    pueblo.estado()

    for _ in range(6):
        pueblo.avanzar_turno()

    print("\n--- Intentando mejorar la Granja ---")
    granja.mejorar(pueblo.almacen)

    print("\n--- Removiendo aldeano activo del Aserradero ---")
    pueblo.remover_aldeano(aldeanos[3], aserradero)

    for _ in range(3):
        pueblo.avanzar_turno()

    print("\n--- ESTADO FINAL ---")
    pueblo.estado()
