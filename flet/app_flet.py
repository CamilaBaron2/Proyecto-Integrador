import flet as ft
import requests
import subprocess
import sys


def main(page: ft.Page):

    page.title = "Renacer Territorial"
    page.window_width = 400
    page.window_height = 600
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    # ---------------- HEADER ----------------

    header = ft.Container(
        content=ft.Text(
            "RENACER TERRITORIAL",
            size=22,
            weight="bold"
        ),
        padding=10
    )

    # ---------------- FOOTER ----------------

    footer = ft.Container(
        content=ft.Text(
            "© 2026 Renacer Territorial",
            size=12
        ),
        padding=10
    )

    # ---------------- LOGIN CAMPOS ----------------

    correo_login = ft.TextField(label="Correo", width=300)

    password_login = ft.TextField(
        label="Contraseña",
        password=True,
        can_reveal_password=True,
        width=300
    )

    mensaje_login = ft.Text()

    # ---------------- REGISTRO CAMPOS ----------------

    nombre = ft.TextField(label="Nombre completo", width=300)
    correo = ft.TextField(label="Correo", width=300)

    password = ft.TextField(
        label="Contraseña",
        password=True,
        can_reveal_password=True,
        width=300
    )

    confirmar = ft.TextField(
        label="Confirmar contraseña",
        password=True,
        can_reveal_password=True,
        width=300
    )

    mensaje_registro = ft.Text()

    # ---------------- LOGIN ----------------

    def login(e):

        data = {
            "correo": correo_login.value,
            "password": password_login.value
        }

        try:

            r = requests.post(
                "http://127.0.0.1:5000/login",
                json=data
            )

            if r.status_code == 200:
                mensaje_login.value = "Login correcto"
                mensaje_login.color = "green"
                page.update()

                subprocess.Popen([sys.executable, "flet/dashboard_flet.py"])
                page.window.destroy()
            else:
                mensaje_login.value = "Usuario o contraseña incorrecta"
                mensaje_login.color = "red"

        except:
            mensaje_login.value = "Error conectando con servidor"

        page.update()

    # ---------------- REGISTRO ----------------

    def registrar(e):

        data = {
            "nombre": nombre.value,
            "correo": correo.value,
            "password": password.value,
            "confirmar_password": confirmar.value
        }

        try:

            r = requests.post(
                "http://127.0.0.1:5000/register",
                json=data
            )

            if r.status_code == 201:

                mensaje_registro.value = "Usuario registrado"
                mensaje_registro.color = "green"
                page.update()

                subprocess.Popen([sys.executable, "flet/dashboard_flet.py"])
                page.window.destroy()

                nombre.value = ""
                correo.value = ""
                password.value = ""
                confirmar.value = ""

            else:

                respuesta = r.json()
                mensaje_registro.value = respuesta.get("message", "Error")
                mensaje_registro.color = "red"

        except:
            mensaje_registro.value = "Error conectando con servidor"

        page.update()

    # ---------------- CARD CONTENIDO ----------------

    card_content = ft.Column(
        horizontal_alignment=ft.CrossAxisAlignment.CENTER
    )

    card = ft.Card(
        content=ft.Container(
            content=card_content,
            padding=20,
            width=350
        )
    )

    # ---------------- LOGIN VIEW ----------------

    def mostrar_login(e=None):

        card_content.controls.clear()

        card_content.controls.extend([

            ft.Text("Login", size=25, weight="bold"),

            correo_login,
            password_login,

            ft.Button(
                "Iniciar sesión",
                on_click=login,
                width=300
            ),

            mensaje_login,

            ft.Row(
                [
                    ft.Text("¿No tienes cuenta?"),
                    ft.TextButton(
                        "Regístrate",
                        on_click=mostrar_registro
                    )
                ],
                alignment=ft.MainAxisAlignment.CENTER
            )

        ])

        page.update()

    # ---------------- REGISTRO VIEW ----------------

    def mostrar_registro(e=None):

        card_content.controls.clear()

        card_content.controls.extend([

            ft.Text("Registro", size=25, weight="bold"),

            nombre,
            correo,
            password,
            confirmar,

            ft.Button(
                "Registrarse",
                on_click=registrar,
                width=300
            ),

            mensaje_registro,

            ft.Row(
                [
                    ft.Text("¿Ya tienes cuenta?"),
                    ft.TextButton(
                        "Inicia sesión",
                        on_click=mostrar_login
                    )
                ],
                alignment=ft.MainAxisAlignment.CENTER
            )

        ])

        page.update()

    # ---------------- LAYOUT ----------------

    layout = ft.Column(
        [
            header,
            card,
            footer
        ],
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        alignment=ft.MainAxisAlignment.CENTER
    )

    page.add(layout)

    mostrar_login()


ft.run(main)