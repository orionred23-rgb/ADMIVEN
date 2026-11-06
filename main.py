import flet as ft

from operaciones import cargar_datos_demostracion
from funciones import configurar_pagina, mostrar_splash, mostrar_login


def main(page: ft.Page):

    # Los datos viven solo en memoria: se pierden al cerrar la app.
    cargar_datos_demostracion()

    configurar_pagina(page)

    mostrar_splash(page)   # pantalla de presentacion
    mostrar_login(page)    # login: usuario admin, clave 1234


if __name__ == "__main__":
    ft.run(main)
