# Clases que representan los datos principales del sistema.
# Cada clase incluye los metodos que trabajan con sus propios datos.
# El campo "id" lo asigna operaciones.py cuando el objeto se guarda en su lista.

from dataclasses import dataclass, field


@dataclass
class Producto:
    categoria: str
    nombre: str
    compra: float
    venta: float
    stock: int
    stock_minimo: int
    margen: float = field(init=False)
    id: int = field(default=0, init=False)

    def __post_init__(self):
        self.compra = float(self.compra)
        self.venta = float(self.venta)
        self.stock = int(self.stock)
        self.stock_minimo = int(self.stock_minimo)
        self.margen = self.calcular_margen()

    # Ganancia que deja cada unidad vendida.
    def calcular_margen(self):
        return self.venta - self.compra

    # Indica si el producto necesita reabastecerse.
    def estado_stock(self):
        if self.stock <= self.stock_minimo:
            return "Stock bajo"
        return "Disponible"

    # Comprueba que los precios y cantidades sean validos.
    def validar(self):
        if self.compra < 0 or self.venta < 0:
            raise ValueError("Los precios no pueden ser negativos.")

        if self.stock < 0 or self.stock_minimo < 0:
            raise ValueError("Las cantidades no pueden ser negativas.")


@dataclass
class Venta:
    cliente: str
    producto: str
    cantidad: int
    precio_unitario: float
    fecha: str = ""
    total: float = field(init=False)
    id: int = field(default=0, init=False)

    def __post_init__(self):
        self.cantidad = int(self.cantidad)
        self.precio_unitario = float(self.precio_unitario)
        self.total = self.calcular_total()

    # Total a cobrar por la venta.
    def calcular_total(self):
        return self.cantidad * self.precio_unitario

    # Comprueba que la cantidad vendida sea correcta.
    def validar(self, stock_disponible):
        if self.cantidad <= 0:
            raise ValueError("La cantidad debe ser mayor que cero.")

        if self.cantidad > stock_disponible:
            raise ValueError("No hay suficiente producto en inventario.")


@dataclass
class Gasto:
    categoria: str
    descripcion: str
    monto: float
    fecha: str
    id: int = field(default=0, init=False)

    def __post_init__(self):
        self.monto = float(self.monto)

    # Comprueba que el monto del gasto sea correcto.
    def validar(self):
        if self.monto <= 0:
            raise ValueError("El monto debe ser mayor que cero.")


@dataclass
class Credito:
    cliente: str
    producto: str
    cantidad: int
    monto: float
    interes_mensual: float = 0.05
    plazo_dias: int = 30
    fecha: str = ""
    estado: str = field(default="Pendiente", init=False)
    id: int = field(default=0, init=False)

    def __post_init__(self):
        self.cantidad = int(self.cantidad)
        self.monto = float(self.monto)
        self.interes_mensual = float(self.interes_mensual)
        self.plazo_dias = int(self.plazo_dias)

    def calcular_interes(self):
        return self.monto * self.interes_mensual

    def calcular_total(self):
        return self.monto + self.calcular_interes()

    # Comprueba que los datos del credito sean correctos.
    def validar(self, stock_disponible):
        if self.cantidad <= 0 or self.monto <= 0:
            raise ValueError("Cantidad y monto deben ser mayores que cero.")

        if self.cantidad > stock_disponible:
            raise ValueError("No hay suficiente producto en inventario.")

        if self.interes_mensual < 0 or self.plazo_dias <= 0:
            raise ValueError("Revisa el interes y el plazo.")

    # Cambia el estado cuando el cliente termina de pagar.
    def marcar_pagado(self):
        self.estado = "Pagado"

    # Un credito esta pendiente mientras no se haya pagado.
    def esta_pendiente(self):
        return self.estado != "Pagado"


@dataclass
class Cliente:
    nombre: str
    cedula: str = ""
    direccion: str = ""
    telefono: str = ""
    origen: str = "REAL"
    id: int = field(default=0, init=False)

    def __post_init__(self):
        self.nombre = self.nombre.strip()
        self.cedula = self.cedula.strip()
        self.direccion = self.direccion.strip()
        self.telefono = self.telefono.strip()

    # Comprueba que el cliente tenga nombre.
    def validar(self):
        if self.nombre == "":
            raise ValueError("Debes escribir el nombre del cliente.")

    # Los clientes de demostracion se identifican por su origen.
    def es_demostracion(self):
        return self.origen == "DEMO"

    # Indica si ya se registraron los datos personales del cliente.
    def tiene_datos_completos(self):
        return self.cedula != "" and self.direccion != ""


@dataclass
class Movimiento:
    producto_id: int
    tipo: str
    cantidad: int
    descripcion: str = ""
    fecha: str = ""
    producto: str = ""
    stock_anterior: int = 0
    stock_nuevo: int = field(default=0, init=False)
    id: int = field(default=0, init=False)

    def __post_init__(self):
        self.tipo = self.tipo.strip().lower()
        self.cantidad = int(self.cantidad)
        self.stock_anterior = int(self.stock_anterior)
        self.stock_nuevo = self.stock_anterior

    # Comprueba el tipo de movimiento y la cantidad.
    def validar(self):
        if self.tipo not in ("entrada", "salida", "ajuste"):
            raise ValueError("Tipo de movimiento no valido.")

        if self.cantidad < 0 or (self.cantidad == 0 and self.tipo != "ajuste"):
            raise ValueError(
                "La cantidad debe ser mayor que cero, excepto en ajustes."
            )

    # Calcula como queda el stock despues del movimiento.
    def calcular_stock_nuevo(self):
        if self.tipo == "entrada":
            self.stock_nuevo = self.stock_anterior + self.cantidad

        elif self.tipo == "salida":
            if self.cantidad > self.stock_anterior:
                raise ValueError("No hay suficientes unidades en inventario.")

            self.stock_nuevo = self.stock_anterior - self.cantidad

        else:
            # En un ajuste, cantidad representa el nuevo stock real.
            self.stock_nuevo = self.cantidad

        return self.stock_nuevo
