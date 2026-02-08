import random

TIPO_FUEGO = "Fuego"
TIPO_AGUA = "Agua"
TIPO_PLANTA = "Planta"
TIPO_NORMAL = "Normal"

def multiplicador_elemental(tipo_ataque, tipo_defensor):
    if tipo_ataque == TIPO_FUEGO:
        if tipo_defensor == TIPO_PLANTA:
            return 2.0
        if tipo_defensor == TIPO_AGUA:
            return 0.5
    if tipo_ataque == TIPO_AGUA:
        if tipo_defensor == TIPO_FUEGO:
            return 2.0
        if tipo_defensor == TIPO_PLANTA:
            return 0.5
    if tipo_ataque == TIPO_PLANTA:
        if tipo_defensor == TIPO_AGUA:
            return 2.0
        if tipo_defensor == TIPO_FUEGO:
            return 0.5
    return 1.0

class Movimiento:
    def __init__(self, nombre, tipo, dano_base, costo_mp, velocidad, precision):
        self.nombre = nombre
        self.tipo = tipo
        self.dano_base = dano_base
        self.costo_mp = costo_mp
        self.velocidad = velocidad
        self.precision = precision 

    def precision_efectiva(self, pokemon_usuario):
        if self.tipo != pokemon_usuario.tipo and self.tipo != TIPO_NORMAL:
            return max(0, self.precision - 20)
        return self.precision

class Pokemon:
    def __init__(self, nombre, tipo, hp, mp, defensa, defensa_esp, movimientos):
        self.nombre = nombre
        self.tipo = tipo
        self.hp_max = hp
        self.hp = hp
        self.mp_max = mp
        self.mp = mp
        self.defensa = defensa
        self.defensa_esp = defensa_esp
        self.movimientos = movimientos  

    def esta_vivo(self):
        return self.hp > 0

    def puede_usar_algo(self):
        return any(m.costo_mp <= self.mp for m in self.movimientos)

    def elegir_movimiento(self):
        print(f"\nElige movimiento para {self.nombre} (HP {self.hp}/{self.hp_max}, MP {self.mp}/{self.mp_max}):")
        for i, mov in enumerate(self.movimientos, start=1):
            print(f"{i}. {mov.nombre} ({mov.tipo}) - Daño {mov.dano_base}, MP {mov.costo_mp}, Vel {mov.velocidad}, Prec {mov.precision}%")
        while True:
            try:
                eleccion = int(input("Número de movimiento: "))
                if 1 <= eleccion <= len(self.movimientos):
                    mov = self.movimientos[eleccion - 1]
                    if mov.costo_mp > self.mp:
                        print("No tienes suficiente MP para ese movimiento. Elige otro.")
                        continue
                    return mov
            except ValueError:
                pass
            print("Opción inválida, intenta de nuevo.")

def calcular_dano(atacante, defensor, movimiento):
    mult = multiplicador_elemental(movimiento.tipo, defensor.tipo)
   
    if movimiento.tipo == TIPO_NORMAL:
        defensa_objetivo = defensor.defensa
    else:  
        defensa_objetivo = defensor.defensa_esp
    dano = (movimiento.dano_base * mult / defensa_objetivo) * 10
    return int(max(1, dano))  

def ejecutar_ataque(atacante, defensor, movimiento):
    atacante.mp -= movimiento.costo_mp

    prec_ef = movimiento.precision_efectiva(atacante)
    tiro = random.randint(1, 100)
    if tiro > prec_ef:
        print(f"¡{movimiento.nombre} de {atacante.nombre} falló!")
        return

    dano = calcular_dano(atacante, defensor, movimiento)
    defensor.hp = max(0, defensor.hp - dano)
    print(f"¡{atacante.nombre} usó {movimiento.nombre} e infligió {dano} de daño!")
    print(f"{defensor.nombre} ahora tiene {defensor.hp} HP.")

def resolver_turno(poke1, mov1, poke2, mov2):
    if mov1.velocidad > mov2.velocidad:
        primero, mov_primero, segundo, mov_segundo = poke1, mov1, poke2, mov2
    elif mov2.velocidad > mov1.velocidad:
        primero, mov_primero, segundo, mov_segundo = poke2, mov2, poke1, mov1
    else:
        if random.random() < 0.5:
            primero, mov_primero, segundo, mov_segundo = poke1, mov1, poke2, mov2
        else:
            primero, mov_primero, segundo, mov_segundo = poke2, mov2, poke1, mov1

    ejecutar_ataque(primero, segundo, mov_primero)

    if not segundo.esta_vivo():
        print(f"¡{segundo.nombre} ha sido debilitado!")
        return

    ejecutar_ataque(segundo, primero, mov_segundo)

    if not primero.esta_vivo():
        print(f"¡{primero.nombre} ha sido debilitado!")

llamarada = Movimiento("Llamarada", TIPO_FUEGO, 50, 15, 1, 70)
lanzallamas = Movimiento("Lanzallamas", TIPO_FUEGO, 35, 10, 3, 90)
nitrocarga = Movimiento("Nitrocarga", TIPO_FUEGO, 25, 6, 5, 100)
punio_fuego = Movimiento("Puño Fuego", TIPO_FUEGO, 30, 8, 3, 100)
ascuas = Movimiento("Ascuas", TIPO_FUEGO, 15, 3, 4, 100)

hidrobomba = Movimiento("Hidrobomba", TIPO_AGUA, 55, 18, 1, 75)
surf = Movimiento("Surf", TIPO_AGUA, 35, 10, 3, 95)
rayo_burbuja = Movimiento("Rayo Burbuja", TIPO_AGUA, 25, 7, 4, 100)
pistola_agua = Movimiento("Pistola Agua", TIPO_AGUA, 15, 3, 5, 100)
cascada = Movimiento("Cascada", TIPO_AGUA, 30, 9, 3, 100)

rayo_solar = Movimiento("Rayo Solar", TIPO_PLANTA, 60, 20, 1, 80)
energibola = Movimiento("Energibola", TIPO_PLANTA, 35, 10, 3, 100)
hoja_afilada = Movimiento("Hoja Afilada", TIPO_PLANTA, 25, 6, 4, 95)
latigo_cepa = Movimiento("Látigo Cepa", TIPO_PLANTA, 15, 3, 5, 100)
mazazo = Movimiento("Mazazo", TIPO_PLANTA, 45, 15, 2, 85)

hiperrayo = Movimiento("Hiperrayo", TIPO_NORMAL, 70, 25, 1, 60)
golpe_cuerpo = Movimiento("Golpe Cuerpo", TIPO_NORMAL, 35, 10, 3, 100)
placaje = Movimiento("Placaje", TIPO_NORMAL, 20, 4, 4, 100)
ataque_rapido = Movimiento("Ataque Rápido", TIPO_NORMAL, 15, 5, 8, 100)
aranazo = Movimiento("Arañazo", TIPO_NORMAL, 10, 2, 5, 100)

arcanine = Pokemon(
    "Arcanine", TIPO_FUEGO,
    hp=180, mp=50, defensa=12, defensa_esp=10,
    movimientos=[lanzallamas, nitrocarga, golpe_cuerpo, ataque_rapido]
)

magmar = Pokemon(
    "Magmar", TIPO_FUEGO,
    hp=150, mp=60, defensa=8, defensa_esp=15,
    movimientos=[llamarada, punio_fuego, ascuas, placaje]
)

blastoise = Pokemon(
    "Blastoise", TIPO_AGUA,
    hp=200, mp=45, defensa=18, defensa_esp=18,
    movimientos=[surf, rayo_burbuja, cascada, golpe_cuerpo]
)

starmie = Pokemon(
    "Starmie", TIPO_AGUA,
    hp=140, mp=70, defensa=10, defensa_esp=12,
    movimientos=[hidrobomba, surf, pistola_agua, ataque_rapido]
)

venusaur = Pokemon(
    "Venusaur", TIPO_PLANTA,
    hp=220, mp=50, defensa=15, defensa_esp=20,
    movimientos=[energibola, hoja_afilada, latigo_cepa, golpe_cuerpo]
)

sceptile = Pokemon(
    "Sceptile", TIPO_PLANTA,
    hp=160, mp=65, defensa=10, defensa_esp=14,
    movimientos=[hoja_afilada, mazazo, latigo_cepa, ataque_rapido]
)

def batalla(p1, p2):
    print(f"¡Comienza el duelo entre {p1.nombre} y {p2.nombre}!")

    turno = 1
    while True:
        input(f"\n--- Turno {turno} (pulsa Enter para continuar) ---")

        if not p1.esta_vivo() or not p2.esta_vivo():
            break

        if (not p1.puede_usar_algo()) and (not p2.puede_usar_algo()):
            print("¡Ambos Pokémon se han quedado sin MP para atacar! ¡Es un empate!")
            return
        if not p1.puede_usar_algo() and p1.esta_vivo():
            print(f"{p1.nombre} no puede usar ningún movimiento (sin MP suficientes).")
        if not p2.puede_usar_algo() and p2.esta_vivo():
            print(f"{p2.nombre} no puede usar ningún movimiento (sin MP suficientes).")

        if p1.puede_usar_algo():
            mov1 = p1.elegir_movimiento()
        else:
            mov1 = None

        if p2.puede_usar_algo():
            mov2 = p2.elegir_movimiento()
        else:
            mov2 = None

        if mov1 is None and mov2 is None:
            print("Ninguno puede atacar. ¡Empate!")
            return

        if mov1 is not None and mov2 is not None:
            resolver_turno(p1, mov1, p2, mov2)
        elif mov1 is not None:
            ejecutar_ataque(p1, p2, mov1)
        elif mov2 is not None:
            ejecutar_ataque(p2, p1, mov2)

        if not p1.esta_vivo() and not p2.esta_vivo():
            print("¡Ambos Pokémon fueron debilitados al mismo tiempo! ¡Empate!")
            return
        elif not p1.esta_vivo():
            print(f"¡{p1.nombre} ha caído! ¡{p2.nombre} gana el combate!")
            return
        elif not p2.esta_vivo():
            print(f"¡{p2.nombre} ha caído! ¡{p1.nombre} gana el combate!")
            return

        turno += 1

if __name__ == "__main__":
    print("Selecciona el Pokémon 1:")
    lista_pokemon = [arcanine, magmar, blastoise, starmie, venusaur, sceptile]
    for i, p in enumerate(lista_pokemon, start=1):
        print(f"{i}. {p.nombre} ({p.tipo})")

    idx1 = int(input("Número de Pokémon 1: ")) - 1
    idx2 = int(input("Número de Pokémon 2: ")) - 1

    p1 = lista_pokemon[idx1]
    p2 = lista_pokemon[idx2]

    batalla(p1, p2)