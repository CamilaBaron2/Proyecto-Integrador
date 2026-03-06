# import flet as ft
# import requests
# import subprocess
# import sys


# def main(page: ft.Page):

#     page.title = "Renacer Territorial - Registro"
#     page.vertical_alignment = ft.MainAxisAlignment.CENTER
#     page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
#     page.window_width = 400
#     page.window_height = 550

#     nombre = ft.TextField(
#         label="Nombre completo",
#         width=300
#     )

#     correo = ft.TextField(
#         label="Correo",
#         width=300
#     )

#     password = ft.TextField(
#         label="Contraseña",
#         password=True,
#         can_reveal_password=True,
#         width=300
#     )

#     confirmar = ft.TextField(
#         label="Confirmar contraseña",
#         password=True,
#         can_reveal_password=True,
#         width=300
#     )

#     mensaje = ft.Text()

#     # REGISTRO
#     def registrar(e):

#         data = {
#             "nombre": nombre.value,
#             "correo": correo.value,
#             "password": password.value,
#             "confirmar_password": confirmar.value
#         }

#         try:

#             r = requests.post(
#                 "http://127.0.0.1:5000/register",
#                 json=data
#             )

#             if r.status_code == 201:

#                 mensaje.value = "Usuario registrado correctamente"
#                 mensaje.color = "green"

#                 nombre.value = ""
#                 correo.value = ""
#                 password.value = ""
#                 confirmar.value = ""

#             else:

#                 respuesta = r.json()
#                 mensaje.value = respuesta.get("message", "Error")
#                 mensaje.color = "red"

#         except Exception as error:

#             mensaje.value = "Error conectando con el servidor"
#             print(error)

#         page.update()

#     # IR A LOGIN
#     def ir_login(e):

#         subprocess.Popen([sys.executable, "flet/login_flet.py"])
#         page.window.close()

#     page.add(
#         ft.Column(
#             [
#                 ft.Text(
#                     "REGISTRO DE USUARIO",
#                     size=30,
#                     weight="bold"
#                 ),

#                 nombre,
#                 correo,
#                 password,
#                 confirmar,

#                 ft.Button(
#                     "Registrarse",
#                     on_click=registrar,
#                     width=300
#                 ),

#                 mensaje,

#                 ft.Row(
#                     [
#                         ft.Text("¿Ya tienes cuenta?"),
#                         ft.TextButton(
#                             "Inicia sesión",
#                             on_click=ir_login
#                         )
#                     ],
#                     alignment=ft.MainAxisAlignment.CENTER
#                 )
#             ],
#             alignment=ft.MainAxisAlignment.CENTER,
#             horizontal_alignment=ft.CrossAxisAlignment.CENTER
#         )
#     )


# ft.run(main)