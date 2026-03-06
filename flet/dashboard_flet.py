import flet as ft
import mysql.connector
from dotenv import load_dotenv
import os
import sys

# ----------------- CARGAR VARIABLES DEL .ENV -----------------
load_dotenv()

DB_HOST = os.getenv("DB_HOST")
DB_USER = os.getenv("DB_USERNAME")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_NAME = os.getenv("DB_DATABASE")


# ----------------- FUNCIONES DE BASE DE DATOS -----------------
def get_user_name(correo):
    """Obtener el nombre del usuario que inició sesión."""
    try:
        db = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME
        )
        cursor = db.cursor()
        cursor.execute("SELECT nombre FROM usuarios WHERE correo=%s", (correo,))
        result = cursor.fetchone()
        cursor.close()
        db.close()
        return result[0] if result else "Usuario"
    except Exception as e:
        print("Error al obtener nombre:", e)
        return "Usuario"


def get_viviendas():
    """Obtener lista de viviendas desde la base de datos."""
    try:
        db = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME
        )
        cursor = db.cursor()
        cursor.execute("SELECT id, direccion, estado FROM viviendas")
        result = cursor.fetchall()
        cursor.close()
        db.close()
        return result
    except Exception as e:
        print("Error al obtener viviendas:", e)
        return []


def get_usuarios():
    """Obtener lista de usuarios desde la base de datos."""
    try:
        db = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME
        )
        cursor = db.cursor()
        cursor.execute("SELECT id, nombre, correo FROM usuarios")
        result = cursor.fetchall()
        cursor.close()
        db.close()
        return result
    except Exception as e:
        print("Error al obtener usuarios:", e)
        return []


# ----------------- DASHBOARD -----------------
def main(page: ft.Page, correo_usuario):
    page.title = "Renacer Territorial - Dashboard"
    page.window_width = 800
    page.window_height = 600
    page.bgcolor = ft.colors.WHITE
    page.padding = 10

    # ----------------- HEADER -----------------
    usuario_nombre = get_user_name(correo_usuario)

    def cerrar_sesion(e):
        page.window_destroy()  # Cierra la ventana
        sys.exit()  # Finaliza el proceso

    header = ft.Row(
        controls=[
            ft.Text("Renacer Territorial", size=24, weight="bold", color=ft.colors.WHITE),
            ft.Spacer(),
            ft.Text(usuario_nombre, color=ft.colors.WHITE),
            ft.ElevatedButton("Cerrar sesión", on_click=cerrar_sesion)
        ],
        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        vertical_alignment=ft.CrossAxisAlignment.CENTER,
        expand=True,
        bgcolor=ft.colors.BLUE_900,
        padding=ft.padding.all(10)
    )

    # ----------------- CARDS -----------------
    # Tabla de viviendas
    table_viviendas = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("ID")),
            ft.DataColumn(ft.Text("Dirección")),
            ft.DataColumn(ft.Text("Estado"))
        ],
        rows=[]
    )

    # Tabla de usuarios
    table_usuarios = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("ID")),
            ft.DataColumn(ft.Text("Nombre")),
            ft.DataColumn(ft.Text("Correo"))
        ],
        rows=[]
    )

    def mostrar_viviendas(e):
        table_viviendas.rows.clear()
        for v in get_viviendas():
            table_viviendas.rows.append(ft.DataRow(cells=[ft.DataCell(ft.Text(str(v[0]))),
                                                           ft.DataCell(ft.Text(v[1])),
                                                           ft.DataCell(ft.Text(v[2]))]))
        page.update()

    def mostrar_usuarios(e):
        table_usuarios.rows.clear()
        for u in get_usuarios():
            table_usuarios.rows.append(ft.DataRow(cells=[ft.DataCell(ft.Text(str(u[0]))),
                                                         ft.DataCell(ft.Text(u[1])),
                                                         ft.DataCell(ft.Text(u[2]))]))
        page.update()

    card_viviendas = ft.Card(
        content=ft.Column(
            controls=[
                ft.Text("Gestión de Viviendas", weight="bold"),
                ft.ElevatedButton("Ver viviendas", on_click=mostrar_viviendas)
            ],
            alignment=ft.MainAxisAlignment.CENTER
        ),
        elevation=5,
        padding=10
    )

    card_usuarios = ft.Card(
        content=ft.Column(
            controls=[
                ft.Text("Usuarios Registrados", weight="bold"),
                ft.ElevatedButton("Ver usuarios", on_click=mostrar_usuarios)
            ],
            alignment=ft.MainAxisAlignment.CENTER
        ),
        elevation=5,
        padding=10
    )

    body = ft.Column(
        controls=[
            ft.Row([card_viviendas, card_usuarios], alignment=ft.MainAxisAlignment.SPACE_EVENLY),
            ft.Column([table_viviendas, table_usuarios], spacing=10)
        ],
        spacing=20
    )

    # ----------------- FOOTER -----------------
    footer = ft.Text("© 2026 Renacer Territorial. Todos los derechos reservados.",
                     color=ft.colors.BLACK,
                     size=12,
                     text_align=ft.TextAlign.CENTER)

    # ----------------- PAGE -----------------
    page.add(
        header,
        ft.Divider(),
        body,
        ft.Divider(),
        footer
    )


# ----------------- EJECUTAR -----------------
# Aquí debes pasar el correo del usuario que inició sesión
correo_usuario = "correo@ejemplo.com"  # <- cambiar por el correo que inicia sesión
ft.app(target=lambda page: main(page, correo_usuario))