

productos = []
ventas = []
gastos = []
creditos = []
clientes = []
movimientos = []


# Devuelve el siguiente id disponible para una lista.
def siguiente_id(lista):
    return len(lista) + 1


# Clase para trabajar con una pila (LIFO)
class Pila:

    def __init__(self):
        self.elementos = []

    # Agregar un elemento a la pila
    def push(self, elemento):
        self.elementos.append(elemento)

    # Retirar el ultimo elemento de la pila
    def pop(self):
        if self.empty():
            return None

        return self.elementos.pop()

    # Comprobar si la pila esta vacia
    def empty(self):
        return len(self.elementos) == 0

    # Mostrar los elementos de la pila
    def mostrar(self):
        return self.elementos.copy()


# Crear la pila del historial
historial = Pila()
