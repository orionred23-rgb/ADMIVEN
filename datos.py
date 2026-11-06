
CATEGORIAS_PRODUCTO = [
    "Alimentos",
    "Bebidas",
    "Lacteos",
    "Carnes",
    "Limpieza",
    "Higiene personal",
    "Electronica",
    "Ropa",
    "Hogar",
    "Papeleria",
    "Snacks",
    "Otros",
]

CATEGORIAS_GASTO = [
    "Servicios (agua, luz, internet)",
    "Alquiler",
    "Transporte",
    "Salarios",
    "Impuestos",
    "Publicidad",
    "Mantenimiento",
    "Insumos",
    "Otros",
]

# Credenciales genericas para iniciar sesion
USUARIO_ADMIN = "admin"
CLAVE_ADMIN = "1234"

OPCIONES_MENU = [
    "Inicio",
    "Productos",
    "Agregar producto",
    "Movimientos de inventario",
    "Clientes",
    "Registrar venta",
    "Gastos",
    "Creditos",
    "Consultar cliente",
    "Reportes",
    "Historial de acciones"
]

# Cada producto: (categoria, nombre, compra, venta, stock, stock_minimo)
PRODUCTOS_DEMO = [
    ("Bebidas", "DEMO - Agua embotellada", 12.00, 18.00, 30, 5),
    ("Bebidas", "DEMO - Refresco", 15.00, 22.00, 25, 5),
    ("Alimentos", "DEMO - Arroz", 18.00, 25.00, 40, 10),
    ("Alimentos", "DEMO - Frijoles", 22.00, 30.00, 35, 10),
    ("Limpieza", "DEMO - Detergente", 35.00, 45.00, 20, 5),
    ("Abarrotes", "DEMO - Aceite", 40.00, 52.00, 15, 5)
]

# Cada cliente: (nombre, cedula, direccion, telefono)
CLIENTES_DEMO = [
    ("DEMO - Cliente Ana", "001-010190-0001A", "Managua, Barrio Altagracia", "8888-1111"),
    ("DEMO - Cliente Carlos", "001-150288-0002B", "Masaya, Calle Central", "8888-2222"),
    ("DEMO - Cliente Maria", "001-200395-0003C", "Granada, Barrio Pantanal", "8888-3333")
]
