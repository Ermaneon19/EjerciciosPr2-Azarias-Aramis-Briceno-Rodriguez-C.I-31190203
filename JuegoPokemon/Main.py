import random

TIPO_FUEGO = "Fuego"
TIPO_AGUA = "Agua"
TIPO_PLANTA = "Planta"
TIPO_NORMAL = "Normal"

tabla_tipos = {
    TIPO_FUEGO: {TIPO_PLANTA: 2.0, TIPO_AGUA: 0.5},
    TIPO_AGUA: {TIPO_FUEGO: 2.0, TIPO_PLANTA: 0.5},
    TIPO_PLANTA: {TIPO_AGUA: 2.0, TIPO_FUEGO: 0.5}
}

def multiplicador_elemental(tipo_ataque, tipo_defensor):
    return tabla_tipos.get(tipo_ataque, {}).get(tipo_defensor, 1.0)


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

    def reset(self):
        self.hp = self.hp_max
        self.mp = self.mp_max

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
                        print("No tienes suficiente MP para ese movimiento.")
                        continue
                    return mov
            except ValueError:
                pass
            print("Opción inválida.")


def calcular_dano(atacante, defensor, movimiento):
    mult = multiplicador_elemental(movimiento.tipo, defensor.tipo)

    stab = 1.5 if movimiento.tipo == atacante.tipo else 1.0

    if movimiento.tipo == TIPO_NORMAL:
        defensa_objetivo = defensor.defensa
    else:
        defensa_objetivo = defensor.defensa_esp

    dano = (movimiento.dano_base * mult * stab / defensa_objetivo) * 10
    return int(max(1, dano)), mult


def ejecutar_ataque(atacante, defensor, movimiento):
    atacante.mp -= movimiento.costo_mp

    prec_ef = movimiento.precision_efectiva(atacante)
    tiro = random.randint(1, 100)

    if tiro > prec_ef:
        print(f"¡{movimiento.nombre} de {atacante.nombre} falló!")
        return

    dano, mult = calcular_dano(atacante, defensor, movimiento)
    defensor.hp = max(0, defensor.hp - dano)

    print(f"¡{atacante.nombre} usó {movimiento.nombre} e infligió {dano} de daño!")

    if mult > 1:
        print("¡Es súper efectivo!")
    elif mult < 1:
        print("No es muy efectivo...")

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

lanzallamas = Movimiento("Lanzallamas", TIPO_FUEGO, 35, 10, 3, 90)
nitrocarga = Movimiento("Nitrocarga", TIPO_FUEGO, 25, 6, 5, 100)
golpe_cuerpo = Movimiento("Golpe Cuerpo", TIPO_NORMAL, 35, 10, 3, 100)
ataque_rapido = Movimiento("Ataque Rápido", TIPO_NORMAL, 15, 5, 8, 100)

surf = Movimiento("Surf", TIPO_AGUA, 35, 10, 3, 95)
rayo_burbuja = Movimiento("Rayo Burbuja", TIPO_AGUA, 25, 7, 4, 100)

energibola = Movimiento("Energibola", TIPO_PLANTA, 35, 10, 3, 100)
hoja_afilada = Movimiento("Hoja Afilada", TIPO_PLANTA, 25, 6, 4, 95)

arcanine = Pokemon("Arcanine", TIPO_FUEGO, 180, 50, 12, 10,
                   [lanzallamas, nitrocarga, golpe_cuerpo, ataque_rapido])

blastoise = Pokemon("Blastoise", TIPO_AGUA, 200, 45, 18, 18,
                    [surf, rayo_burbuja, golpe_cuerpo, ataque_rapido])

venusaur = Pokemon("Venusaur", TIPO_PLANTA, 220, 50, 15, 20,
                   [energibola, hoja_afilada, golpe_cuerpo, ataque_rapido])

def batalla(p1, p2):
    p1.reset()
    p2.reset()

    print(f"\n¡Comienza el duelo entre {p1.nombre} y {p2.nombre}!")
    turno = 1

    while p1.esta_vivo() and p2.esta_vivo():
        input(f"\n--- Turno {turno} --- (Enter)")

        mov1 = p1.elegir_movimiento() if p1.puede_usar_algo() else None
        mov2 = p2.elegir_movimiento() if p2.puede_usar_algo() else None

        if mov1 and mov2:
            resolver_turno(p1, mov1, p2, mov2)
        elif mov1:
            ejecutar_ataque(p1, p2, mov1)
        elif mov2:
            ejecutar_ataque(p2, p1, mov2)
        else:
            print("Ambos se quedaron sin MP. ¡Empate!")
            return

        turno += 1

    if p1.esta_vivo():
        print(f"\n¡{p1.nombre} gana el combate!")
    else:
        print(f"\n¡{p2.nombre} gana el combate!")


if __name__ == "__main__":
    lista_pokemon = [arcanine, blastoise, venusaur]

    print("Selecciona el Pokémon 1:")
    for i, p in enumerate(lista_pokemon, start=1):
        print(f"{i}. {p.nombre} ({p.tipo})")

    idx1 = int(input("Número de Pokémon 1: ")) - 1
    idx2 = int(input("Número de Pokémon 2: ")) - 1

    if idx1 == idx2:
        print("No puedes elegir el mismo Pokémon.")
    else:
        batalla(lista_pokemon[idx1], lista_pokemon[idx2])

