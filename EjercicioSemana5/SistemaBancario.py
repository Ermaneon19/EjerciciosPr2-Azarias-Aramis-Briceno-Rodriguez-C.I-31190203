class Cliente:
    def __init__(self, nombre, cedula):
        self.__nombre = nombre
        self.__cedula = cedula

    def obtener_nombre(self):
        return self.__nombre

    def obtener_cedula(self):
        return self.__cedula

class CuentaBancaria(Cliente):
    def __init__(self, nombre, cedula, numero_cuenta, saldo_inicial=0):

        super().__init__(nombre, cedula)

        self.__numero_cuenta = numero_cuenta

        if saldo_inicial >= 0:
            self.__saldo = saldo_inicial
        else:
            self.__saldo = 0
            print("El saldo inicial no puede ser negativo. Se asignó 0.")

    def obtener_saldo(self):
        return self.__saldo

    def obtener_numero_cuenta(self):
        return self.__numero_cuenta

    def depositar(self, monto):
        if monto > 0:
            self.__saldo += monto
            print(f"Depósito exitoso. Nuevo saldo: {self.__saldo}")
        else:
            print("El monto debe ser mayor que 0.")

    def retirar(self, monto):
        if monto <= 0:
            print("El monto debe ser mayor que 0.")
        elif monto > self.__saldo:
            print("Fondos insuficientes. Operación cancelada.")
        else:
            self.__saldo -= monto
            print(f"Retiro exitoso. Nuevo saldo: {self.__saldo}")

cuenta = CuentaBancaria("Carlos Pérez", "0102030405", "001-2024", 1000)

print("Cliente:", cuenta.obtener_nombre())
print("Cédula:", cuenta.obtener_cedula())
print("Saldo actual:", cuenta.obtener_saldo())

cuenta.depositar(500)
cuenta.retirar(200)
cuenta.retirar(5000)  

print("Saldo actual:", cuenta.obtener_saldo)