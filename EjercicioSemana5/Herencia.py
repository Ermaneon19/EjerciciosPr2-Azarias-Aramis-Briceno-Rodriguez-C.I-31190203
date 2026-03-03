class Aventurero:
    def __init__(self, nombre, vida, nivel = 0):

        self.nombre = nombre
        self.__vida = vida
        self.__nivel = nivel

    def atacar(self):
        print ("Ataque de aventurero")

class Guerrero(Aventurero):

    def __init__(self, nombre, vida, furia, nivel = 0):

        super().__init__(nombre, vida)
        self.furia = furia

    def grito_de_guerra(self):

        print("El guerrero grita")

    def atacar(self):
        return ("Ataque de guerrero")
    
class Mago(Aventurero):

    def __init__(self, nombre, vida, mana,  nivel=0):
        super().__init__(nombre, vida, nivel)
        self.mana = mana

    def LanzarHechizos(self):
        self.mana -= 10
        print("Lanzar hechizo")

Guerrero = Guerrero("Aza", 100, 100 )
Aventurero = Aventurero("Luis", 100, 200)
Mago = Mago("Luis", 200, 233,)


Guerrero.atacar()

Guerrero.grito_de_guerra()