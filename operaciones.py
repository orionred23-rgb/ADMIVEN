

from datos import PRODUCTOS_DEMO, CLIENTES_DEMO, USUARIO_ADMIN, CLAVE_ADMIN
from entidades import Producto, Venta, Credito, Cliente, Movimiento
from estructuras import (
    productos,
    ventas,
    gastos,
    creditos,
    clientes,
    movimientos,
    siguiente_id
)


# ---------------------------------
# DATOS DE DEMOSTRACION
# ---------------------------------

# Carga productos y clientes de ejemplo al abrir la app.
def cargar_datos_demostracion():

    if len(productos) > 0:
        return

    for datos in PRODUCTOS_DEMO:
        agregar_producto(Producto(*datos))

    for nombre, cedula, direccion, telefono in CLIENTES_DEMO:
        guardar_cliente(nombre, cedula, direccion, telefono, "DEMO")


# ---------------------------------
# PRODUCTOS
# ---------------------------------

def agregar_producto(producto):

    for otro in productos:
        if otro.nombre.lower() == producto.nombre.lower():
            raise ValueError("Ya existe un producto con ese nombre.")

    producto.id = siguiente_id(productos)
    productos.append(producto)


def obtener_producto(producto_id):
    for producto in productos:
        if producto.id == producto_id:
            return producto
    return None


# Devuelve los productos ordenados por nombre.
def obtener_productos():
    return sorted(productos, key=lambda p: p.nombre.lower())


# ---------------------------------
# MOVIMIENTOS DE INVENTARIO
# ---------------------------------

# Registra una entrada, salida o ajuste y devuelve el stock nuevo.
def registrar_movimiento(producto_id, tipo, cantidad, descripcion, fecha):

    movimiento = Movimiento(
        producto_id, tipo, cantidad, descripcion, fecha
    )

    movimiento.validar()

    producto = obtener_producto(producto_id)

    if producto is None:
        raise ValueError("El producto no existe.")

    movimiento.producto = producto.nombre
    movimiento.stock_anterior = producto.stock

    producto.stock = movimiento.calcular_stock_nuevo()

    movimiento.id = siguiente_id(movimientos)
    movimientos.append(movimiento)

    return producto.stock


# Los mas recientes aparecen primero.
def obtener_movimientos():
    return list(reversed(movimientos))


# ---------------------------------
# VENTAS
# ---------------------------------

# Registra la venta, descuenta el stock y devuelve el total.
def registrar_venta(cliente, producto_id, cantidad, fecha):

    producto = obtener_producto(producto_id)

    if producto is None:
        raise ValueError("El producto no existe.")

    venta = Venta(cliente, producto.nombre, cantidad, producto.venta, fecha)

    venta.validar(producto.stock)

    # Esto descuenta el stock y guarda la salida en movimientos.
    registrar_movimiento(
        producto_id, "salida", venta.cantidad, "Salida por venta", fecha
    )

    venta.id = siguiente_id(ventas)
    ventas.append(venta)

    registrar_cliente_si_no_existe(cliente)

    return venta.total


def obtener_ventas():
    return list(reversed(ventas))


# ---------------------------------
# GASTOS
# ---------------------------------

def guardar_gasto(gasto):
    gasto.id = siguiente_id(gastos)
    gastos.append(gasto)


def obtener_gastos():
    return list(reversed(gastos))


# ---------------------------------
# CREDITOS
# ---------------------------------

# Registra un credito: el monto se calcula con el precio del producto,
# se descuenta el stock (igual que una venta) y devuelve el total
# a pagar (con interes).
def registrar_credito(cliente, producto_id, cantidad, interes, plazo, fecha):

    producto = obtener_producto(producto_id)

    if producto is None:
        raise ValueError("El producto no existe.")

    cantidad = int(cantidad)
    monto = cantidad * producto.venta

    credito = Credito(
        cliente, producto.nombre, cantidad, monto, interes, plazo, fecha
    )

    credito.validar(producto.stock)

    # Esto descuenta el stock y guarda la salida en movimientos.
    registrar_movimiento(
        producto_id, "salida", credito.cantidad, "Salida por crédito", fecha
    )

    credito.id = siguiente_id(creditos)
    creditos.append(credito)

    registrar_cliente_si_no_existe(cliente)

    return credito.calcular_total()


def obtener_creditos():
    return list(reversed(creditos))


# Devuelve 0 si el credito no existe, -1 si ya estaba pagado
# y 1 si se marco como pagado.
def marcar_credito_pagado(credito_id):

    for credito in creditos:

        if credito.id == credito_id:

            if not credito.esta_pendiente():
                return -1

            credito.marcar_pagado()
            return 1

    return 0


# ---------------------------------
# CLIENTES
# ---------------------------------

def obtener_cliente_por_nombre(nombre):
    for cliente in clientes:
        if cliente.nombre.lower() == nombre.strip().lower():
            return cliente
    return None


# Guarda un cliente. Devuelve:
#  1 -> cliente nuevo guardado
#  2 -> se completaron los datos de un cliente que ya existia sin datos
#  0 -> el cliente ya estaba registrado
# -1 -> la cedula pertenece a otro cliente
def guardar_cliente(nombre, cedula="", direccion="", telefono="", origen="REAL"):

    cliente = Cliente(nombre, cedula, direccion, telefono, origen)

    cliente.validar()

    if cliente.cedula != "":
        for otro in clientes:
            misma_cedula = otro.cedula.lower() == cliente.cedula.lower()
            otro_nombre = otro.nombre.lower() != cliente.nombre.lower()

            if misma_cedula and otro_nombre:
                return -1

    existente = obtener_cliente_por_nombre(cliente.nombre)

    if existente is not None:

        # Cliente creado automaticamente por una venta: completar sus datos
        if not existente.tiene_datos_completos() and cliente.cedula != "":
            existente.cedula = cliente.cedula
            existente.direccion = cliente.direccion
            existente.telefono = cliente.telefono
            return 2

        return 0

    cliente.id = siguiente_id(clientes)
    clientes.append(cliente)

    return 1


# Las ventas y creditos registran al cliente si todavia no existe.
def registrar_cliente_si_no_existe(nombre):
    guardar_cliente(nombre)


def obtener_clientes():
    return sorted(clientes, key=lambda c: c.nombre.lower())


# Busca clientes por nombre o cedula y sus ventas y creditos.
# Devuelve (clientes_encontrados, filas)
# Cada fila: (fecha, producto, cantidad, total, tipo)
def buscar_cliente(texto):

    texto = texto.strip().lower()

    encontrados = []
    for cliente in clientes:
        if texto in cliente.nombre.lower() or texto in cliente.cedula.lower():
            encontrados.append(cliente)

    nombres = []
    for cliente in encontrados:
        nombres.append(cliente.nombre.lower())

    filas = []

    for venta in ventas:
        if venta.cliente.lower() in nombres:
            filas.append((
                venta.fecha, venta.producto,
                venta.cantidad, venta.total, "Venta"
            ))

    for credito in creditos:
        if credito.cliente.lower() in nombres:
            filas.append((
                credito.fecha, credito.producto,
                credito.cantidad, credito.calcular_total(), "Credito"
            ))

    # Fechas mas recientes primero.
    filas.sort(key=lambda fila: fila[0], reverse=True)

    return encontrados, filas


# ---------------------------------
# INICIO DE SESION
# ---------------------------------

def verificar_credenciales(usuario, clave):
    return usuario.strip() == USUARIO_ADMIN and clave == CLAVE_ADMIN


# ---------------------------------
# REPORTES GENERALES
# ---------------------------------

def obtener_resumen():

    unidades = 0
    inventario = 0
    stock_bajo = 0
    agotados = 0

    for producto in productos:
        unidades += producto.stock
        inventario += producto.compra * producto.stock

        if producto.stock <= 0:
            agotados += 1
        elif producto.stock <= producto.stock_minimo:
            stock_bajo += 1

    total_ventas = 0
    for venta in ventas:
        total_ventas += venta.total

    total_gastos = 0
    for gasto in gastos:
        total_gastos += gasto.monto

    creditos_pendientes = 0
    creditos_cobrados = 0
    for credito in creditos:
        if credito.esta_pendiente():
            creditos_pendientes += credito.calcular_total()
        else:
            creditos_cobrados += credito.calcular_total()

    return {
        "productos": len(productos),
        "unidades": unidades,
        "inventario": inventario,
        "cantidad_ventas": len(ventas),
        "ventas": total_ventas,
        "gastos": total_gastos,
        "creditos": creditos_pendientes,
        "cobrados": creditos_cobrados,
        "resultado": total_ventas + creditos_cobrados - total_gastos,
        "stock_bajo": stock_bajo,
        "agotados": agotados
    }
