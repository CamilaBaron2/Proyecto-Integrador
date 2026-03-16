import flet as ft
import requests
from views.dashboard_flet import dashboard_view

cliente_http = requests.Session()

def main(page: ft.Page):
    page.theme = ft.Theme(font_family="Verdana")
    page.visual_density = ft.VisualDensity.COMFORTABLE
    page.title = "Renacer Territorial"
    page.window_width = 400
    page.window_height = 600
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    # ---------------- HEADER ----------------
    header = ft.Container(
        content=ft.Text("RENACER TERRITORIAL", size=22, weight="bold"),
        padding=10
    )

    # ---------------- FOOTER ----------------
    footer = ft.Container(
        content=ft.Text("© 2026 Renacer Territorial", size=12),
        padding=10
    )

    # ---------------- CAMPOS (Mantenemos tus variables) ----------------
    correo_login = ft.TextField(label="Correo", width=300)
    password_login = ft.TextField(label="Contraseña", password=True, can_reveal_password=True, width=300)
    mensaje_login = ft.Text()

    nombre = ft.TextField(label="Nombre completo", width=300)
    correo = ft.TextField(label="Correo", width=300)
    password = ft.TextField(label="Contraseña", password=True, can_reveal_password=True, width=300)
    confirmar = ft.TextField(label="Confirmar contraseña", password=True, can_reveal_password=True, width=300)
    mensaje_registro = ft.Text()

    # ---------------- LÓGICA LOGIN ----------------
    def login(e):
        data = {"correo": correo_login.value, "password": password_login.value}
        try:
            r = cliente_http.post("http://127.0.0.1:5000/login", json=data)
            if r.status_code == 200:
                respuesta = r.json()
                nombre_usuario = respuesta.get("fullname", "Usuario")
                # Obtenemos el rol exacto de la DB (Propietario o Administrador)
                rol_usuario = respuesta.get("rol", "Propietario") 
                print(f">>> TRANSFIRIENDO: Nombre: {nombre_usuario}, Rol: {rol_usuario}")
                page.clean()
                # Enviamos el rol a la vista del dashboard
                dashboard_view(page, nombre_usuario, rol_usuario, cliente_http ) 
            else:
                mensaje_login.value = "Credenciales incorrectas"
                mensaje_login.color = "red"
        except Exception as ex:
            mensaje_login.value = f"Error: {ex}"
        page.update()

    # ---------------- LÓGICA REGISTRO ----------------
    def registrar(e):
        if not nombre.value or not correo.value or not password.value:
            mensaje_registro.value = "Por favor, completa todos los campos"
            mensaje_registro.color = "red"
            page.update()
            return

        data = {
            "nombre": nombre.value,
            "correo": correo.value,
            "password": password.value,
            "confirmar_password": confirmar.value
        }

        try:
            r = requests.post("http://127.0.0.1:5000/register", json=data)
            if r.status_code == 201:
                nombre_usuario = nombre.value
                page.clean()
                dashboard_view(page, nombre_usuario, "propietario") 
            else:
                respuesta = r.json()
                mensaje_registro.value = respuesta.get("message", "Error en el registro")
                mensaje_registro.color = "red"
        except Exception as ex:
            mensaje_registro.value = "Error al conectar con el servidor"
            mensaje_registro.color = "red"
        page.update()

    # ---------------- ESTRUCTURA DE VISTAS ----------------
    card_content = ft.Column(horizontal_alignment=ft.CrossAxisAlignment.CENTER)
    card = ft.Card(content=ft.Container(content=card_content, padding=20, width=350))

    def mostrar_login(e=None):
        card_content.controls.clear()
        card_content.controls.extend([
            ft.Text("Login", size=25, weight="bold"),
            correo_login, password_login,
            ft.Button("Iniciar sesión", on_click=login, width=300),
            mensaje_login,
            ft.Row([
                ft.Text("¿No tienes cuenta?"),
                ft.TextButton("Regístrate", on_click=mostrar_registro)
            ], alignment=ft.MainAxisAlignment.CENTER)
        ])
        page.update()

    def mostrar_registro(e=None):
        card_content.controls.clear()
        card_content.controls.extend([
            ft.Text("Registro", size=25, weight="bold"),
            nombre, correo, password, confirmar,
            ft.Button("Registrarse", on_click=registrar, width=300),
            mensaje_registro,
            ft.Row([
                ft.Text("¿Ya tienes cuenta?"),
                ft.TextButton("Inicia sesión", on_click=mostrar_login)
            ], alignment=ft.MainAxisAlignment.CENTER)
        ])
        page.update()

    layout = ft.Column(
        [header, card, footer],
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        alignment=ft.MainAxisAlignment.CENTER
    )

    page.add(layout)
    mostrar_login()

if __name__ == "__main__":
    ft.run(
        main, 
        view=ft.AppView.WEB_BROWSER, 
        port=8550, 
        host="127.0.0.1"
    )