ADMIVEN – Sistema de administración 

Prototipo desarrollado en Python con Flet para la gestión de: inventario, ventas, gastos, créditos y clientes.

Características

- Inicio de sesión con pantalla de presentación (splash).
- Registro y consulta de **productos** con búsqueda en vivo y alerta de stock bajo.
- Movimientos de inventario: entradas, salidas y ajustes.
- Ventas y créditos (con interés y plazo) que descuentan automáticamente el inventario.
- Registro de gastos por categoría.
- Directorio de clientes (nombre, cédula, dirección, teléfono) y consulta de su historial.
- Reportes** con resumen financiero: ventas, gastos, créditos pendientes y cobrados.
- Historial de acciones implementado con una pila (LIFO).

Conceptos aplicados

- Clases con `@dataclass` y métodos propios (validación y cálculos).
- Funciones, listas, diccionarios, tuplas y una pila.
- Validación de datos y manejo de excepciones (`try/except`, `ValueError`).
- Búsqueda secuencial y ordenamiento con `sorted()`.
- Programación modular: cada archivo tiene una única responsabilidad.

Estructura del proyecto

ADMIVEN/
├── main.py            # Punto de entrada
├── entidades.py       # Clases dataclass (Producto, Venta, Gasto, Credito, Cliente, Movimiento)
├── estructuras.py     # Listas de datos en memoria y clase Pila
├── operaciones.py     # Lógica del negocio (registrar, buscar, calcular)
├── funciones.py       # Validaciones, componentes y pantallas de la interfaz
├── datos.py           # Categorías, menú, credenciales y datos de demostración
├── requirements.txt   # Dependencias
└── arquitectura_logica.txt


Instalación y ejecución

Requiere **Python 3.10 o superior**.

bash
# 1. Clonar el repositorio
git clone <URL-DEL-REPOSITORIO>
cd ADMIVEN

# 2. Crear y activar un entorno (ejemplo con conda)
conda create -n admiven python=3.12
conda activate admiven

# 3. Instalar Flet
pip install flet

# 4. Ejecutar
python main.py
`

Para abrir la aplicación en el navegador en lugar de una ventana de escritorio:

flet run --web main.py


En Linux, si la ventana de escritorio no abre, instala las librerías del sistema:

bash
sudo apt install libgtk-3-0 libmpv-dev


Acceso (demostración)

| Usuario | Clave |
|---------|-------|
| `admin` | `1234` |

Son credenciales genéricas de demostración, definidas en `datos.py`.

Datos

La aplicación **no usa base de datos**: toda la información se guarda en memoria y se pierde al cerrar el programa. Cada vez que se abre, se cargan productos y clientes de demostración (los que empiezan con `DEMO -`).
