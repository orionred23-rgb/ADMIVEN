
import time
from datetime import date

import flet as ft

from datos import CATEGORIAS_PRODUCTO, CATEGORIAS_GASTO, OPCIONES_MENU
from entidades import Producto, Gasto
from estructuras import historial
from operaciones import (
    agregar_producto,
    obtener_productos,
    registrar_movimiento,
    obtener_movimientos,
    registrar_venta,
    obtener_ventas,
    guardar_gasto,
    obtener_gastos,
    registrar_credito,
    obtener_creditos,
    marcar_credito_pagado,
    buscar_cliente,
    obtener_clientes,
    guardar_cliente,
    obtener_resumen,
    verificar_credenciales
)


# ESTILO: colores, negritas e iconos


# Todo el texto del sistema usa negrita.
NEGRITA = ft.FontWeight.BOLD
MUY_NEGRITA = ft.FontWeight.W_900

# Paleta de colores
COLOR_FONDO = "#EEF2F7"       # fondo general
COLOR_MENU = "#0B2545"        # panel lateral y titulos
COLOR_MENU_BOTON = "#13315C"  # botones del menu
COLOR_ACTIVO = "#14B8A6"      # opcion del menu seleccionada
COLOR_PRIMARIO = "#2563EB"    # botones de accion
TEXTO = "#0F172A"
TEXTO_SUAVE = "#334155"
VERDE = "#16A34A"
ROJO = "#DC2626"
AMBAR = "#D97706"
MORADO = "#7C3AED"
CIAN = "#0891B2"

# Color de algunos textos dentro de las tablas.
COLOR_ESTADO = {
    "Stock bajo": ROJO,
    "Disponible": VERDE,
    "Pendiente": AMBAR,
    "Pagado": VERDE,
    "Entrada": VERDE,
    "Salida": ROJO,
    "Ajuste": COLOR_PRIMARIO,
    "Venta": VERDE,
    "Credito": AMBAR,
}

# Icono de cada opcion del menu.
ICONOS_MENU = {
    "Inicio": ft.Icons.HOME,
    "Productos": ft.Icons.INVENTORY_2,
    "Agregar producto": ft.Icons.ADD_BOX,
    "Movimientos de inventario": ft.Icons.SWAP_VERT,
    "Clientes": ft.Icons.PEOPLE,
    "Registrar venta": ft.Icons.POINT_OF_SALE,
    "Gastos": ft.Icons.RECEIPT_LONG,
    "Creditos": ft.Icons.CREDIT_CARD,
    "Consultar cliente": ft.Icons.PERSON_SEARCH,
    "Reportes": ft.Icons.BAR_CHART,
    "Historial de acciones": ft.Icons.HISTORY,
}



# FUNCIONES DE APOYO


def fecha_actual():
    return date.today().isoformat()


def convertir_numero(valor, nombre):
    try:
        numero = float(valor)
    except (TypeError, ValueError):
        raise ValueError("El campo " + nombre + " debe ser numérico.")
    return numero


def convertir_entero(valor, nombre):
    try:
        numero = int(valor)
    except (TypeError, ValueError):
        raise ValueError("El campo " + nombre + " debe ser un número entero.")
    return numero


def validar_texto(valor: str | None, nombre: str) -> str:
    if valor is None or valor.strip() == "":
        raise ValueError("Debes escribir " + nombre + ".")
    return valor.strip()


def validar_seleccion(valor: str | None, nombre: str) -> str:
    if valor is None:
        raise ValueError("Selecciona " + nombre + ".")
    return valor


# Devuelve el id (numero entero) de la opcion elegida en un desplegable.
def obtener_id(valor: str | None, nombre: str) -> int:
    if valor is None:
        raise ValueError("Selecciona " + nombre + ".")
    return int(valor)


# La fecha debe tener el formato AAAA-MM-DD y ser una fecha real.
def validar_fecha(valor):
    texto = validar_texto(valor, "la fecha")

    try:
        if len(texto) != 10:
            raise ValueError
        date.fromisoformat(texto)
    except ValueError:
        raise ValueError("La fecha debe tener el formato AAAA-MM-DD, "
                         "por ejemplo 2026-11-04.")

    return texto


def dinero(valor):
    return "C$ " + format(float(valor), ",.2f")


# Si un dato esta vacio se muestra un guion.
def texto_o_guion(valor):
    if valor == "":
        return "-"
    return valor



# COMPONENTES DE LA INTERFAZ

# Texto en negrita (todos los textos pasan por aqui).
def crear_texto(texto, tamano=14, color=TEXTO, peso=NEGRITA):
    return ft.Text(texto, size=tamano, color=color, weight=peso)


# Mostrar mensajes en pantalla.
def mensaje(page, texto):
    page.show_dialog(
        ft.SnackBar(content=crear_texto(texto, 14, "white"), bgcolor=COLOR_MENU)
    )


# Crear campos de texto.
def crear_campo(titulo, ancho=300, valor="", clave=False, icono=None):
    return ft.TextField(
        label=titulo,
        width=ancho,
        value=valor,
        password=clave,
        can_reveal_password=clave,
        prefix_icon=icono,
        border_radius=10,
        border_color="#94A3B8",
        focused_border_color=COLOR_PRIMARIO,
        text_style=ft.TextStyle(weight=NEGRITA),
        label_style=ft.TextStyle(weight=NEGRITA),
    )


# Crear listas desplegables.
# opciones: lista de tuplas (texto, clave)
def crear_lista(titulo, opciones, ancho=300, icono=None):
    lista = []
    for texto, clave in opciones:
        lista.append(ft.dropdown.Option(text=texto, key=clave))

    return ft.Dropdown(
        label=titulo,
        width=ancho,
        options=lista,
        leading_icon=icono,
        border_radius=10,
        border_color="#94A3B8",
        focused_border_color=COLOR_PRIMARIO,
        text_style=ft.TextStyle(weight=NEGRITA),
        label_style=ft.TextStyle(weight=NEGRITA),
    )


# Boton de accion (guardar, buscar, etc.)
def crear_boton_accion(texto, accion, color=COLOR_PRIMARIO, ancho=None,
                       icono=None):
    return ft.Button(
        content=crear_texto(texto, 14, "white"),
        icon=icono,
        icon_color="white",
        on_click=accion,
        width=ancho,
        height=42,
        bgcolor=color,
        color="white",
        style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10)),
    )


# Titulo grande de cada pantalla (con icono).
def crear_titulo(texto, icono=None):
    controles: list[ft.Control] = []

    if icono is not None:
        controles.append(ft.Icon(icono, size=30, color=COLOR_ACTIVO))

    controles.append(crear_texto(texto, 24, COLOR_MENU, MUY_NEGRITA))

    return ft.Row(controls=controles, spacing=10)


# Subtitulo de una seccion.
def crear_subtitulo(texto, color=TEXTO_SUAVE):
    return crear_texto(texto, 18, color)


# Tarjeta con un indicador (usada en Inicio y Reportes).
def crear_tarjeta(titulo, valor, color, descripcion="", icono=None):

    textos: list[ft.Control] = [
        crear_texto(titulo, 13, TEXTO_SUAVE),
        crear_texto(valor, 22, color, MUY_NEGRITA),
    ]

    if descripcion != "":
        textos.append(crear_texto(descripcion, 12, TEXTO_SUAVE))

    controles: list[ft.Control] = []

    if icono is not None:
        controles.append(
            ft.Container(
                content=ft.Icon(icono, size=26, color=color),
                width=48,
                height=48,
                border_radius=24,
                bgcolor=ft.Colors.with_opacity(0.12, color),
                alignment=ft.Alignment.CENTER,
            )
        )

    controles.append(ft.Column(controls=textos, spacing=4))

    return ft.Container(
        content=ft.Row(controls=controles, spacing=12),
        width=270,
        padding=16,
        bgcolor="white",
        border_radius=14,
        border=ft.Border.all(1, "#E2E8F0"),
        shadow=ft.BoxShadow(
            blur_radius=10,
            color=ft.Colors.with_opacity(0.08, "black"),
            offset=ft.Offset(0, 3),
        ),
    )


# Crear tablas para mostrar informacion.
def crear_tabla(titulos, registros):

    if len(registros) == 0:
        return crear_texto("No hay registros.")

    columnas = []
    for titulo in titulos:
        columnas.append(
            ft.DataColumn(label=crear_texto(titulo, 14, COLOR_MENU))
        )

    filas = []
    for registro in registros:
        celdas = []
        for dato in registro:
            # Algunos estados se muestran con color.
            color = COLOR_ESTADO.get(str(dato), TEXTO)
            celdas.append(ft.DataCell(crear_texto(str(dato), 13, color)))
        filas.append(ft.DataRow(cells=celdas))

    tabla = ft.DataTable(
        columns=columnas,
        rows=filas,
        heading_row_color="#E2EAF4",
        divider_thickness=0.5,
    )

    return ft.Row(controls=[tabla], scroll=ft.ScrollMode.AUTO)


# Coloca los controles en el panel de contenido y refresca la pantalla.
def mostrar_en_pantalla(page, contenido, controles, espacio=12):
    contenido.content = ft.Column(
        controls=controles,
        spacing=espacio,
        scroll=ft.ScrollMode.AUTO
    )
    page.update()


# Quita todo lo que haya en la ventana (para cambiar de pantalla).
def limpiar_pagina(page):
    page.controls.clear()
    page.update()


# Fondo con degradado usado en el splash y el login.
def crear_fondo_degradado(controles):
    return ft.Container(
        expand=True,
        alignment=ft.Alignment.CENTER,
        gradient=ft.LinearGradient(
            begin=ft.Alignment.TOP_LEFT,
            end=ft.Alignment.BOTTOM_RIGHT,
            colors=["#0B2545", "#134074"],
        ),
        content=ft.Column(
            controls=controles,
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=10,
        ),
    )



# CONVERSION DE OBJETOS A FILAS DE TABLA


def filas_ventas(lista):
    filas = []
    for v in lista:
        filas.append((
            v.id, v.fecha, v.cliente, v.producto,
            v.cantidad, dinero(v.precio_unitario), dinero(v.total)
        ))
    return filas


def filas_gastos(lista):
    filas = []
    for g in lista:
        filas.append((g.id, g.fecha, g.categoria, g.descripcion, dinero(g.monto)))
    return filas


def filas_creditos(lista):
    filas = []
    for c in lista:
        filas.append((
            c.id, c.fecha, c.cliente, c.producto, c.cantidad,
            dinero(c.monto), str(round(c.interes_mensual * 100, 2)) + "%",
            dinero(c.calcular_total()), c.plazo_dias, c.estado
        ))
    return filas


# Lista de productos con stock, para los desplegables.
# El texto muestra el stock y la clave es el id del producto.
def opciones_productos(solo_disponibles=False):
    opciones = []
    for p in obtener_productos():
        if solo_disponibles and p.stock <= 0:
            continue
        opciones.append((p.nombre + " - Stock: " + str(p.stock), str(p.id)))
    return opciones



# INICIO


def mostrar_inicio(page, contenido):

    datos = obtener_resumen()

    tarjetas: list[ft.Control] = [
        crear_tarjeta("Productos registrados", str(datos["productos"]),
                      COLOR_PRIMARIO, "Productos en el sistema",
                      ft.Icons.INVENTORY_2),
        crear_tarjeta("Unidades disponibles", str(datos["unidades"]),
                      CIAN, "Existencias en inventario", ft.Icons.INVENTORY),
        crear_tarjeta("Valor del inventario", dinero(datos["inventario"]),
                      MORADO, "Según precio de compra",
                      ft.Icons.ACCOUNT_BALANCE_WALLET),
        crear_tarjeta("Stock bajo", str(datos["stock_bajo"]),
                      AMBAR, "Productos por reabastecer",
                      ft.Icons.WARNING_AMBER),
        crear_tarjeta("Agotados", str(datos["agotados"]),
                      ROJO, "Productos sin existencias", ft.Icons.ERROR_OUTLINE),
        crear_tarjeta("Ventas registradas", str(datos["cantidad_ventas"]),
                      VERDE, "Operaciones realizadas", ft.Icons.SHOPPING_CART),
        crear_tarjeta("Total de ventas", dinero(datos["ventas"]),
                      VERDE, "Ingresos por ventas", ft.Icons.PAYMENTS),
        crear_tarjeta("Total de gastos", dinero(datos["gastos"]),
                      ROJO, "Gastos registrados", ft.Icons.TRENDING_DOWN),
        crear_tarjeta("Créditos pendientes", dinero(datos["creditos"]),
                      AMBAR, "Monto por cobrar", ft.Icons.CREDIT_CARD),
        crear_tarjeta("Créditos cobrados", dinero(datos["cobrados"]),
                      VERDE, "Créditos ya pagados", ft.Icons.CHECK_CIRCLE),
        crear_tarjeta("Resultado", dinero(datos["resultado"]),
                      COLOR_MENU, "Ventas + cobrados - gastos",
                      ft.Icons.TRENDING_UP),
    ]

    controles: list[ft.Control] = [
        crear_titulo("Panel principal", ft.Icons.HOME),
        crear_texto("Resumen general de la actividad de tu negocio.",
                    14, TEXTO_SUAVE),
        ft.Divider(color="#E2E8F0"),
        ft.Row(controls=tarjetas, wrap=True, spacing=14, run_spacing=14),
    ]

    mostrar_en_pantalla(page, contenido, controles, 15)



# PRODUCTOS


def mostrar_productos(page, contenido):

    filas = []

    for p in obtener_productos():
        filas.append((
            p.id, p.nombre, p.categoria,
            dinero(p.compra), dinero(p.venta), dinero(p.margen),
            p.stock, p.stock_minimo, p.estado_stock()
        ))

    buscar = crear_campo("Buscar producto por nombre", 350,
                         icono=ft.Icons.SEARCH)
    tabla = ft.Column()

    def actualizar_tabla(e=None):

        texto = (buscar.value or "").lower().strip()
        resultado = []

        for fila in filas:
            if texto in str(fila[1]).lower():
                resultado.append(fila)

        tabla.controls.clear()
        tabla.controls.append(
            crear_tabla(
                ["ID", "Producto", "Categoria", "Compra", "Venta",
                 "Margen", "Stock", "Minimo", "Estado"],
                resultado
            )
        )
        page.update()

    buscar.on_change = actualizar_tabla

    mostrar_en_pantalla(page, contenido, [
        crear_titulo("Inventario de productos", ft.Icons.INVENTORY_2),
        buscar,
        tabla
    ])

    actualizar_tabla()


def mostrar_formulario_producto(page, contenido):

    opciones = []
    for categoria_nombre in CATEGORIAS_PRODUCTO:
        opciones.append((categoria_nombre, categoria_nombre))

    categoria = crear_lista("Categoria", opciones, icono=ft.Icons.CATEGORY)
    nombre = crear_campo("Nombre del producto", icono=ft.Icons.LABEL)
    compra = crear_campo("Precio de compra", icono=ft.Icons.ATTACH_MONEY)
    venta = crear_campo("Precio de venta", icono=ft.Icons.SELL)
    stock = crear_campo("Cantidad inicial", icono=ft.Icons.NUMBERS)
    minimo = crear_campo("Stock minimo", icono=ft.Icons.WARNING_AMBER)

    def guardar(e):
        try:
            producto = Producto(
                categoria=validar_seleccion(categoria.value, "la categoria"),
                nombre=validar_texto(nombre.value, "el nombre"),
                compra=convertir_numero(compra.value, "precio de compra"),
                venta=convertir_numero(venta.value, "precio de venta"),
                stock=convertir_entero(stock.value, "cantidad"),
                stock_minimo=convertir_entero(minimo.value, "stock minimo")
            )

            producto.validar()
            agregar_producto(producto)

            historial.push("Se registro el producto: " + producto.nombre)
            mensaje(page, "Producto guardado correctamente.")
            mostrar_productos(page, contenido)

        except ValueError as error:
            mensaje(page, str(error))

    mostrar_en_pantalla(page, contenido, [
        crear_titulo("Agregar producto", ft.Icons.ADD_BOX),
        categoria, nombre, compra, venta, stock, minimo,
        crear_boton_accion("Guardar producto", guardar, icono=ft.Icons.SAVE)
    ], 10)



# MOVIMIENTOS DE INVENTARIO


def mostrar_movimientos(page, contenido):

    producto = crear_lista("Seleccionar producto", opciones_productos(), 350,
                           ft.Icons.INVENTORY_2)
    tipo = crear_lista(
        "Tipo de movimiento",
        [("entrada", "entrada"), ("salida", "salida"), ("ajuste", "ajuste")],
        350, ft.Icons.SWAP_VERT
    )
    cantidad = crear_campo("Cantidad", icono=ft.Icons.NUMBERS)
    descripcion = crear_campo("Descripción", icono=ft.Icons.DESCRIPTION)
    fecha = crear_campo("Fecha (AAAA-MM-DD)", valor=fecha_actual(),
                        icono=ft.Icons.CALENDAR_MONTH)

    def guardar(e):
        try:
            identificador = obtener_id(producto.value, "un producto")
            tipo_movimiento = validar_seleccion(tipo.value, "el tipo de movimiento")

            unidades = convertir_entero(cantidad.value, "cantidad")
            detalle = validar_texto(descripcion.value, "la descripción")
            dia = validar_fecha(fecha.value)

            nuevo_stock = registrar_movimiento(
                identificador, tipo_movimiento, unidades, detalle, dia
            )

            historial.push("Movimiento de inventario: " + tipo_movimiento)
            mensaje(page, "Movimiento registrado. Nuevo stock: "
                    + str(nuevo_stock))
            mostrar_movimientos(page, contenido)

        except ValueError as error:
            mensaje(page, str(error))

    filas = []
    for m in obtener_movimientos():
        filas.append((
            m.id, m.fecha, m.producto, m.tipo.capitalize(),
            m.cantidad, m.stock_anterior, m.stock_nuevo, m.descripcion
        ))

    mostrar_en_pantalla(page, contenido, [
        crear_titulo("Movimientos de inventario", ft.Icons.SWAP_VERT),
        crear_texto("Registra entradas, salidas y ajustes de existencias.",
                    14, TEXTO_SUAVE),
        producto, tipo, cantidad, descripcion, fecha,
        crear_boton_accion("Guardar movimiento", guardar, icono=ft.Icons.SAVE),
        ft.Divider(),
        crear_subtitulo("Historial de movimientos"),
        crear_tabla(
            ["ID", "Fecha", "Producto", "Tipo", "Cantidad",
             "Stock anterior", "Stock nuevo", "Descripción"],
            filas
        )
    ])


# ==============================================================
# CLIENTES
# ==============================================================

def mostrar_clientes(page, contenido):

    nombre = crear_campo("Nombre completo", 350, icono=ft.Icons.PERSON)
    cedula = crear_campo("Número de cédula", 350, icono=ft.Icons.BADGE)
    direccion = crear_campo("Dirección", 350, icono=ft.Icons.LOCATION_ON)
    telefono = crear_campo("Teléfono (opcional)", 350, icono=ft.Icons.PHONE)
    lista_clientes = ft.Column()

    def actualizar_clientes():

        filas = []
        for c in obtener_clientes():
            if c.es_demostracion():
                origen = "Demostración"
            else:
                origen = "Real"

            filas.append((
                c.id, c.nombre, texto_o_guion(c.cedula),
                texto_o_guion(c.direccion), texto_o_guion(c.telefono), origen
            ))

        lista_clientes.controls.clear()
        lista_clientes.controls.append(
            crear_tabla(
                ["ID", "Nombre", "Cédula", "Dirección", "Teléfono", "Origen"],
                filas
            )
        )
        page.update()

    def guardar(e):
        try:
            nom = validar_texto(nombre.value, "el nombre del cliente")
            ced = validar_texto(cedula.value, "el número de cédula")
            direc = validar_texto(direccion.value, "la dirección")
            tel = telefono.value or ""

            resultado = guardar_cliente(nom, ced, direc, tel)

            if resultado == -1:
                mensaje(page, "Esa cédula ya pertenece a otro cliente.")
                return

            if resultado == 0:
                mensaje(page, "Ese cliente ya está registrado.")
                return

            if resultado == 2:
                mensaje(page, "Se completaron los datos del cliente.")
            else:
                mensaje(page, "Cliente registrado correctamente.")

            historial.push("Se registro el cliente: " + nom)

            nombre.value = ""
            cedula.value = ""
            direccion.value = ""
            telefono.value = ""
            actualizar_clientes()

        except ValueError as error:
            mensaje(page, str(error))

    mostrar_en_pantalla(page, contenido, [
        crear_titulo("Directorio de clientes", ft.Icons.PEOPLE),
        crear_texto("Registra y consulta los clientes del negocio.",
                    14, TEXTO_SUAVE),
        nombre, cedula, direccion, telefono,
        crear_boton_accion("Guardar cliente", guardar,
                           icono=ft.Icons.PERSON_ADD),
        ft.Divider(),
        crear_subtitulo("Clientes registrados"),
        lista_clientes
    ], 10)

    actualizar_clientes()


# Consulta un cliente por nombre o cedula y muestra su historial.
def mostrar_cliente(page, contenido):

    texto_busqueda = crear_campo("Nombre o cédula del cliente", 350,
                                 icono=ft.Icons.SEARCH)
    resultado = ft.Column(spacing=10)

    def buscar(e):
        try:
            texto = validar_texto(texto_busqueda.value, "el nombre o la cédula")

            encontrados, movimientos = buscar_cliente(texto)

            resultado.controls.clear()

            if len(encontrados) == 0:
                resultado.controls.append(
                    crear_texto("No se encontró ningún cliente con ese dato.",
                                16, ROJO)
                )
                page.update()
                return

            # Datos personales de cada cliente encontrado
            for c in encontrados:
                resultado.controls.append(
                    crear_subtitulo(c.nombre, COLOR_MENU)
                )
                resultado.controls.append(
                    crear_tabla(
                        ["Cédula", "Dirección", "Teléfono"],
                        [(texto_o_guion(c.cedula),
                          texto_o_guion(c.direccion),
                          texto_o_guion(c.telefono))]
                    )
                )

            # Historial de compras y creditos
            total = 0
            filas = []
            for m in movimientos:
                total += m[3]
                filas.append((m[0], m[1], m[2], dinero(m[3]), m[4]))

            resultado.controls.append(ft.Divider())
            resultado.controls.append(crear_subtitulo("Historial de movimientos"))
            resultado.controls.append(
                crear_tabla(
                    ["Fecha", "Producto", "Cantidad", "Total", "Tipo"],
                    filas
                )
            )
            resultado.controls.append(
                crear_texto("Movimientos: " + str(len(filas)) +
                            "   |   Total: " + dinero(total), 15, COLOR_MENU)
            )

            page.update()

        except ValueError as error:
            mensaje(page, str(error))

    # Al presionar Enter tambien busca.
    texto_busqueda.on_submit = buscar

    mostrar_en_pantalla(page, contenido, [
        crear_titulo("Consultar cliente", ft.Icons.PERSON_SEARCH),
        crear_texto("Busca por nombre o por número de cédula.",
                    14, TEXTO_SUAVE),
        texto_busqueda,
        crear_boton_accion("Buscar", buscar, icono=ft.Icons.SEARCH),
        resultado
    ], 10)


# VENTAS


def mostrar_ventas(page, contenido):

    cliente = crear_campo("Nombre del cliente", icono=ft.Icons.PERSON)
    # Solo se pueden vender productos que tengan stock.
    producto = crear_lista("Producto", opciones_productos(True), 350,
                           ft.Icons.INVENTORY_2)
    cantidad = crear_campo("Cantidad", icono=ft.Icons.NUMBERS)
    fecha = crear_campo("Fecha (AAAA-MM-DD)", valor=fecha_actual(),
                        icono=ft.Icons.CALENDAR_MONTH)

    def guardar(e):
        try:
            nombre_cliente = validar_texto(cliente.value, "el cliente")
            identificador = obtener_id(producto.value, "un producto")

            unidades = convertir_entero(cantidad.value, "cantidad")
            dia = validar_fecha(fecha.value)

            total = registrar_venta(
                nombre_cliente, identificador, unidades, dia
            )

            historial.push("Venta realizada a: " + nombre_cliente)
            mensaje(page, "Venta registrada. Total: " + dinero(total))
            mostrar_ventas(page, contenido)

        except ValueError as error:
            mensaje(page, str(error))

    mostrar_en_pantalla(page, contenido, [
        crear_titulo("Registrar venta", ft.Icons.POINT_OF_SALE),
        cliente, producto, cantidad, fecha,
        crear_boton_accion("Guardar venta", guardar, VERDE,
                           icono=ft.Icons.CHECK_CIRCLE),
        ft.Divider(),
        crear_subtitulo("Historial de ventas"),
        crear_tabla(
            ["ID", "Fecha", "Cliente", "Producto",
             "Cantidad", "Precio", "Total"],
            filas_ventas(obtener_ventas())
        )
    ], 10)


# ==============================================================
# GASTOS
# ==============================================================

def mostrar_gastos(page, contenido):

    opciones = []
    for nombre_categoria in CATEGORIAS_GASTO:
        opciones.append((nombre_categoria, nombre_categoria))

    # La categoria va primero y luego la descripcion.
    categoria = crear_lista("Categoria", opciones, icono=ft.Icons.CATEGORY)
    descripcion = crear_campo("Descripcion", icono=ft.Icons.DESCRIPTION)
    monto = crear_campo("Monto", icono=ft.Icons.ATTACH_MONEY)
    fecha = crear_campo("Fecha (AAAA-MM-DD)", valor=fecha_actual(),
                        icono=ft.Icons.CALENDAR_MONTH)

    def guardar(e):
        try:
            gasto = Gasto(
                validar_seleccion(categoria.value, "la categoria"),
                validar_texto(descripcion.value, "la descripcion"),
                convertir_numero(monto.value, "monto"),
                validar_fecha(fecha.value)
            )

            gasto.validar()
            guardar_gasto(gasto)

            historial.push("Se registro un gasto: " + gasto.descripcion)
            mensaje(page, "Gasto registrado correctamente.")
            mostrar_gastos(page, contenido)

        except ValueError as error:
            mensaje(page, str(error))

    mostrar_en_pantalla(page, contenido, [
        crear_titulo("Registro de gastos", ft.Icons.RECEIPT_LONG),
        categoria, descripcion, monto, fecha,
        crear_boton_accion("Guardar gasto", guardar, icono=ft.Icons.SAVE),
        ft.Divider(),
        crear_tabla(
            ["ID", "Fecha", "Categoria", "Descripcion", "Monto"],
            filas_gastos(obtener_gastos())
        )
    ], 10)


# ==============================================================
# CREDITOS
# ==============================================================

def mostrar_creditos(page, contenido):

    cliente = crear_campo("Nombre del cliente", icono=ft.Icons.PERSON)
    # Solo aparecen los productos que tienen stock disponible.
    producto = crear_lista("Producto", opciones_productos(True), 350,
                           ft.Icons.INVENTORY_2)
    cantidad = crear_campo("Cantidad", icono=ft.Icons.NUMBERS)
    interes = crear_campo("Interes (0.05 equivale a 5%)", valor="0.05",
                          icono=ft.Icons.PERCENT)
    plazo = crear_campo("Plazo en dias", valor="30", icono=ft.Icons.SCHEDULE)
    fecha = crear_campo("Fecha (AAAA-MM-DD)", valor=fecha_actual(),
                        icono=ft.Icons.CALENDAR_MONTH)

    # Lista de creditos pendientes para elegir cual se pago.
    pendientes = []
    for c in obtener_creditos():
        if c.esta_pendiente():
            texto = ("#" + str(c.id) + " - " + c.cliente + " - " +
                     dinero(c.calcular_total()))
            pendientes.append((texto, str(c.id)))

    credito_a_pagar = crear_lista("Credito pendiente", pendientes, 450,
                                  ft.Icons.CREDIT_CARD)

    def guardar(e):
        try:
            nombre_cliente = validar_texto(cliente.value, "el cliente")
            identificador = obtener_id(producto.value, "un producto")

            total = registrar_credito(
                nombre_cliente,
                identificador,
                convertir_entero(cantidad.value, "cantidad"),
                convertir_numero(interes.value, "interes"),
                convertir_entero(plazo.value, "plazo"),
                validar_fecha(fecha.value)
            )

            historial.push("Se registro un credito para: " + nombre_cliente)
            mensaje(page, "Credito registrado. Total a pagar: " + dinero(total))
            mostrar_creditos(page, contenido)

        except ValueError as error:
            mensaje(page, str(error))

    def marcar_pagado(e):
        try:
            identificador = obtener_id(credito_a_pagar.value, "un credito")

            resultado = marcar_credito_pagado(identificador)

            if resultado == 0:
                mensaje(page, "No se encontro ese credito.")
            elif resultado == -1:
                mensaje(page, "Ese credito ya estaba pagado.")
            else:
                historial.push(
                    "Se marco como pagado el credito: " + str(identificador)
                )
                mensaje(page, "Credito marcado como pagado.")

            mostrar_creditos(page, contenido)

        except ValueError as error:
            mensaje(page, str(error))

    mostrar_en_pantalla(page, contenido, [
        crear_titulo("Administrar creditos", ft.Icons.CREDIT_CARD),
        crear_texto("El monto se calcula con el precio de venta del producto "
                    "y la cantidad se descuenta del inventario.",
                    14, TEXTO_SUAVE),
        cliente, producto, cantidad, interes, plazo, fecha,
        crear_boton_accion("Guardar credito", guardar, AMBAR,
                           icono=ft.Icons.SAVE),
        ft.Divider(),
        crear_subtitulo("Marcar credito como pagado"),
        credito_a_pagar,
        crear_boton_accion("Marcar como pagado", marcar_pagado, VERDE,
                           icono=ft.Icons.CHECK_CIRCLE),
        ft.Divider(),
        crear_tabla(
            ["ID", "Fecha", "Cliente", "Producto", "Cantidad",
             "Monto", "Interes", "Total", "Dias", "Estado"],
            filas_creditos(obtener_creditos())
        )
    ], 10)


# ==============================================================
# REPORTES
# ==============================================================

def mostrar_reportes(page, contenido):

    datos = obtener_resumen()

    tarjetas: list[ft.Control] = [
        crear_tarjeta("Valor del inventario", dinero(datos["inventario"]),
                      MORADO, "", ft.Icons.ACCOUNT_BALANCE_WALLET),
        crear_tarjeta("Total de ventas", dinero(datos["ventas"]),
                      VERDE, "", ft.Icons.PAYMENTS),
        crear_tarjeta("Total de gastos", dinero(datos["gastos"]),
                      ROJO, "", ft.Icons.TRENDING_DOWN),
        crear_tarjeta("Créditos pendientes", dinero(datos["creditos"]),
                      AMBAR, "", ft.Icons.CREDIT_CARD),
        crear_tarjeta("Créditos cobrados", dinero(datos["cobrados"]),
                      VERDE, "", ft.Icons.CHECK_CIRCLE),
        crear_tarjeta("Resultado del negocio", dinero(datos["resultado"]),
                      COLOR_MENU, "", ft.Icons.TRENDING_UP),
    ]

    mostrar_en_pantalla(page, contenido, [
        crear_titulo("Reportes del negocio", ft.Icons.BAR_CHART),
        crear_texto("Consulta el resumen financiero y los movimientos registrados.",
                    14, TEXTO_SUAVE),
        ft.Divider(color="#E2E8F0"),

        crear_subtitulo("Resumen financiero"),
        ft.Row(controls=tarjetas, wrap=True, spacing=14, run_spacing=14),
        ft.Divider(color="#E2E8F0"),

        crear_subtitulo("Detalle de ventas", VERDE),
        crear_tabla(
            ["ID", "Fecha", "Cliente", "Producto",
             "Cantidad", "Precio", "Total"],
            filas_ventas(obtener_ventas())
        ),
        ft.Divider(color="#E2E8F0"),

        crear_subtitulo("Detalle de gastos", ROJO),
        crear_tabla(
            ["ID", "Fecha", "Categoria", "Descripcion", "Monto"],
            filas_gastos(obtener_gastos())
        ),
        ft.Divider(color="#E2E8F0"),

        crear_subtitulo("Detalle de créditos", AMBAR),
        crear_tabla(
            ["ID", "Fecha", "Cliente", "Producto", "Cantidad",
             "Monto", "Interes", "Total", "Dias", "Estado"],
            filas_creditos(obtener_creditos())
        ),
    ])


# ==============================================================
# HISTORIAL (usa la Pila)
# ==============================================================

def mostrar_historial(page, contenido):

    lista_historial = ft.Column()

    def actualizar_historial():

        lista_historial.controls.clear()

        if historial.empty():
            lista_historial.controls.append(crear_texto("No hay registros."))
        else:
            # Mostramos primero el ultimo elemento agregado.
            elementos = historial.mostrar()
            elementos.reverse()

            for elemento in elementos:
                lista_historial.controls.append(
                    ft.Row(
                        controls=[
                            ft.Icon(ft.Icons.CHECK_CIRCLE, size=18,
                                    color=COLOR_ACTIVO),
                            crear_texto(elemento),
                        ],
                        spacing=8,
                    )
                )

        page.update()

    def retirar_ultimo(e):
        ultimo = historial.pop()

        if ultimo is None:
            mensaje(page, "No hay datos.")
        else:
            mensaje(page, "Se retiro del historial: " + str(ultimo))

        actualizar_historial()

    mostrar_en_pantalla(page, contenido, [
        crear_titulo("Historial de acciones", ft.Icons.HISTORY),
        crear_boton_accion("Retirar ultima accion", retirar_ultimo, ROJO,
                           icono=ft.Icons.UNDO),
        lista_historial
    ])

    actualizar_historial()


# ==============================================================
# PANTALLA DE PRESENTACION (SPLASH) Y LOGIN
# ==============================================================

# Pantalla de bienvenida con una barra de carga.
def mostrar_splash(page):

    barra = ft.ProgressBar(
        width=300, value=0, color=COLOR_ACTIVO, bgcolor="#1E4A7A"
    )

    page.add(
        crear_fondo_degradado([
            ft.Icon(ft.Icons.STOREFRONT, size=100, color=COLOR_ACTIVO),
            crear_texto("ADMIVEN", 52, "white", MUY_NEGRITA),
            crear_texto(
                "Sistema de administración de inventario y ventas",
                16, "#CBD5E1"
            ),
            ft.Container(height=20),
            barra,
            crear_texto("Cargando sistema...", 13, "#CBD5E1"),
        ])
    )

    # La barra avanza 10 pasos (en total unos 2.5 segundos).
    for paso in range(1, 11):
        time.sleep(0.25)
        barra.value = paso / 10
        page.update()

    limpiar_pagina(page)


# Pantalla de inicio de sesion (usuario: admin, clave: 1234).
def mostrar_login(page):

    usuario = crear_campo("Usuario", 300, icono=ft.Icons.PERSON)
    clave = crear_campo("Clave", 300, clave=True, icono=ft.Icons.LOCK)

    def ingresar(e):
        if verificar_credenciales(usuario.value or "", clave.value or ""):
            limpiar_pagina(page)
            construir_pantalla(page)
        else:
            clave.value = ""
            mensaje(page, "Usuario o clave incorrectos.")
            page.update()

    # Al presionar Enter tambien se inicia sesion.
    usuario.on_submit = ingresar
    clave.on_submit = ingresar

    tarjeta = ft.Container(
        width=400,
        padding=30,
        bgcolor="white",
        border_radius=18,
        shadow=ft.BoxShadow(
            blur_radius=25,
            color=ft.Colors.with_opacity(0.35, "black"),
            offset=ft.Offset(0, 8),
        ),
        content=ft.Column(
            controls=[
                ft.Icon(ft.Icons.STOREFRONT, size=60, color=COLOR_ACTIVO),
                crear_texto("ADMIVEN", 30, COLOR_MENU, MUY_NEGRITA),
                crear_texto("Inicia sesión para continuar", 14, TEXTO_SUAVE),
                ft.Container(height=10),
                usuario,
                clave,
                ft.Container(height=5),
                crear_boton_accion("Ingresar", ingresar, COLOR_PRIMARIO, 300,
                                   ft.Icons.LOGIN),
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=10,
        ),
    )

    page.add(crear_fondo_degradado([tarjeta]))


# ==============================================================
# NAVEGACION Y DISEÑO GENERAL
# ==============================================================

# Cada opcion del menu se asocia con su pantalla.
PANTALLAS = {
    "Inicio": mostrar_inicio,
    "Productos": mostrar_productos,
    "Agregar producto": mostrar_formulario_producto,
    "Movimientos de inventario": mostrar_movimientos,
    "Clientes": mostrar_clientes,
    "Registrar venta": mostrar_ventas,
    "Gastos": mostrar_gastos,
    "Creditos": mostrar_creditos,
    "Consultar cliente": mostrar_cliente,
    "Reportes": mostrar_reportes,
    "Historial de acciones": mostrar_historial,
}


def mostrar_seccion(page, contenido, nombre):
    pantalla = PANTALLAS[nombre]
    pantalla(page, contenido)


# Configuracion basica de la ventana.
def configurar_pagina(page):
    page.title = "ADMIVEN"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.padding = 0
    page.bgcolor = COLOR_FONDO


# Construye el panel lateral y el area de contenido.
def construir_pantalla(page):

    contenido = ft.Container(
        padding=20,
        bgcolor="white",
        border_radius=14,
        shadow=ft.BoxShadow(
            blur_radius=10,
            color=ft.Colors.with_opacity(0.08, "black"),
            offset=ft.Offset(0, 3),
        ),
    )

    # Botones del menu, guardados por nombre para resaltar el activo.
    botones = {}

    def abrir(nombre):
        for otro in botones:
            botones[otro].bgcolor = COLOR_MENU_BOTON

        botones[nombre].bgcolor = COLOR_ACTIVO
        mostrar_seccion(page, contenido, nombre)

    def crear_boton_menu(nombre):

        def accion(e):
            abrir(nombre)

        return crear_boton_accion(
            nombre, accion, COLOR_MENU_BOTON, 230, ICONOS_MENU[nombre]
        )

    for opcion in OPCIONES_MENU:
        botones[opcion] = crear_boton_menu(opcion)

    def cerrar_sesion(e):
        limpiar_pagina(page)
        mostrar_login(page)

    lista_botones: list[ft.Control] = list(botones.values())
    lista_botones.append(ft.Divider(color="#1E4A7A"))
    lista_botones.append(
        crear_boton_accion("Cerrar sesión", cerrar_sesion, ROJO, 230,
                           ft.Icons.LOGOUT)
    )

    panel_lateral = ft.Container(
        content=ft.Column(
            controls=[
                ft.Row(
                    controls=[
                        ft.Icon(ft.Icons.STOREFRONT, size=32,
                                color=COLOR_ACTIVO),
                        crear_texto("ADMIVEN", 26, "white", MUY_NEGRITA),
                    ],
                    spacing=10,
                ),
                crear_texto("Sistema de gestion", 13, "#CBD5E1"),
                ft.Divider(color="#1E4A7A"),
                *lista_botones,
            ],
            spacing=10,
            scroll=ft.ScrollMode.AUTO,
        ),
        width=265,
        padding=15,
        bgcolor=COLOR_MENU,
        border_radius=14,
    )

    area_derecha = ft.Container(
        content=ft.Column(
            controls=[
                crear_texto("Administracion de inventario y ventas",
                            22, COLOR_MENU, MUY_NEGRITA),
                ft.Divider(),
                contenido,
            ],
            expand=True,
            scroll=ft.ScrollMode.AUTO,
        ),
        expand=True,
        padding=10,
    )

    page.add(
        ft.Container(
            expand=True,
            padding=20,
            content=ft.Row(
                controls=[panel_lateral, area_derecha],
                expand=True,
                vertical_alignment=ft.CrossAxisAlignment.START,
            ),
        )
    )

    abrir("Inicio")
