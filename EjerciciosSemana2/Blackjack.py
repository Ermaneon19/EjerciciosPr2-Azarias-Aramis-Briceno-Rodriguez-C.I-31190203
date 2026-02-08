import random

class Carta:
    def __init__(self, palo, valor):
        self.palo = palo
        self.valor = valor

    def valor_juego(self):
        if self.valor > 10:
            return 10
        if self.valor == 1:
            return 11
        return self.valor

    def __str__(self):
        nombres = {1: "As", 11: "J", 12: "Q", 13: "K"}
        valor = nombres.get(self.valor, self.valor)
        return f"{valor} de {self.palo}"


class Mazo:
    def __init__(self):
        self.cartas = []
        palos = ["Corazones", "Diamantes", "Picas", "Tréboles"]

        for palo in palos:
            for valor in range(1, 14):
                self.cartas.append(Carta(palo, valor))

    def repartir_carta(self):
        return self.cartas.pop(random.randrange(len(self.cartas)))


def calcular_puntos(mano):
    total = 0
    ases = 0

    for carta in mano:
        total += carta.valor_juego()
        if carta.valor == 1:
            ases += 1

    while total > 21 and ases:
        total -= 10
        ases -= 1

    return total


def mostrar_mano(nombre, mano, ocultar=False):
    print(f"\nMano de {nombre}:")
    for i, carta in enumerate(mano):
        if ocultar and i == 0:
            print("Carta oculta")
        else:
            print(carta)
    if not ocultar:
        print("Puntos:", calcular_puntos(mano))


if __name__ == "__main__":

    mazo = Mazo()

    jugador = []
    crupier = []

    for _ in range(2):
        jugador.append(mazo.repartir_carta())
        crupier.append(mazo.repartir_carta())

    while True:
        mostrar_mano("Jugador", jugador)
        mostrar_mano("Crupier", crupier, ocultar=True)

        puntos_jugador = calcular_puntos(jugador)
        if puntos_jugador > 21:
            print("\nTe pasaste de 21. Pierdes ")
            exit()

        opcion = input("\n¿Pedir carta (p) o plantarse (s)? ").lower()
        if opcion == "p":
            jugador.append(mazo.repartir_carta())
        elif opcion == "s":
            break
        else:
            print("Opción inválida")

    print("\nTurno del crupier...")
    mostrar_mano("Crupier", crupier)

    while calcular_puntos(crupier) < 17:
        crupier.append(mazo.repartir_carta())
        mostrar_mano("Crupier", crupier)

    puntos_jugador = calcular_puntos(jugador)
    puntos_crupier = calcular_puntos(crupier)

    print("\nResultado final:")
    print("Jugador:", puntos_jugador)
    print("Crupier:", puntos_crupier)

    if puntos_crupier > 21 or puntos_jugador > puntos_crupier:
        print("¡Ganaste!")
    elif puntos_jugador < puntos_crupier:
        print("Gana el crupier")
    else:
        print("Empate")
