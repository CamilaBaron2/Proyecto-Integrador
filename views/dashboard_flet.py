import flet as ft
import requests
try:
    from views.reparacion_view import obtener_reparacion_contenido
    from views.restitucion_view import restitucion_view
except ImportError:

    # Fallback por si los archivos no están creados aún
    reparacion_view = None
    restitucion_view = None

def dashboard_view(page: ft.Page, nombre_usuario, rol_usuario, cliente_http):
    # --- CONFIGURACIÓN DE PÁGINA ---
    page.title = "Dashboard - Renacer Territorial"
    page.bgcolor = "#1a1a1a" 
    page.padding = 0 
    page.spacing = 0

    def cerrar_sesion(e):
        
        try:
            cliente_http.get("http://127.0.0.1:5000/logout", headers={"Accept": "application/json"}, timeout=2)
        except:
            pass
        page.clean()
        
        # Importación local (DENTRO de la función para evitar el bucle infinito)
        from views.app_flet import main 
        
        # Volver a ejecutar el inicio
        main(page)

    def ir_a_modulo(modulo_id):
        page.clean()
        
        btn_volver = ft.ElevatedButton(
            "Volver al Menú", 
            icon="arrow_back",
            on_click=lambda _: dashboard_view(page, nombre_usuario, rol_usuario, cliente_http)
        )

        # Lógica de navegación simplificada
        if modulo_id == "reparacion":
            # Llamamos al archivo externo pasando el rol
            contenido = obtener_reparacion_contenido(page, rol_usuario, cliente_http)
            
        elif modulo_id == "restitucion":
            # Aquí podrías hacer lo mismo con restitucion_view
            contenido = ft.Text(f"Módulo Restitución - Rol: {rol_usuario}", color="white")
        else:
            contenido = ft.Text("Módulo no encontrado", color="red")

        page.add(
            header,
            ft.Container(
                content=ft.Column([
                    btn_volver, 
                    ft.Divider(color="white24"), 
                    contenido
                ], spacing=20),
                padding=30
            )
        )
        page.update()

    def create_module_card(title, color, description, modulo_id):
        return ft.Card(
            content=ft.Container(
                content=ft.Column([
                    ft.Text(title, size=20, weight="bold", text_align="center", color="black"),
                    ft.Text(description, size=13, text_align="center", color="grey700"),
                    ft.ElevatedButton(
                        "Ingresar", 
                        bgcolor=color, 
                        color="white", 
                        width=150,
                        on_click=lambda _: ir_a_modulo(modulo_id) 
                    )
                ], alignment="center", horizontal_alignment="center", spacing=15),
                padding=25, width=300, height=220, bgcolor="white", border_radius=10
            ),
            elevation=10
        )

    # --- COMPONENTES PRINCIPALES ---

    # El Header ahora usa correctamente la variable 'rol' que entra a la función
    header = ft.Container(
        content=ft.Row([
            ft.Text("RENACER TERRITORIAL", size=22, weight="bold", color="white"),
            ft.Row([
                ft.Column([
                    ft.Text(nombre_usuario, size=14, weight="bold", color="white"),
                    ft.Text(f"Rol: {rol_usuario}", size=11, color="white70"),
                ], spacing=0, horizontal_alignment="end"),
                ft.VerticalDivider(color="white24"),
                ft.ElevatedButton("Salir", icon="logout", color="white", bgcolor="red700", on_click=cerrar_sesion)
            ], spacing=15)
        ], alignment="spaceBetween"),
        bgcolor="blue800",
        padding=ft.padding.symmetric(horizontal=20, vertical=10),
        width=float("inf") 
    )

    # Definimos qué tarjetas se muestran según el rol
    if rol_usuario == "Administrador":
        cards = [
            create_module_card("Gestión Viviendas", "green800", "Panel administrativo de inmuebles.", "reparacion"),
            create_module_card("Procesos Legales", "blue800", "Control de restitución nacional.", "restitucion")
        ]
    else:
        cards = [
            create_module_card("Reparación Vivienda", "green700", "Subir evidencias de daños.", "reparacion"),
            create_module_card("Mi Restitución", "blue700", "Consultar estado de solicitud.", "restitucion")
        ]

    modules_layout = ft.Row(cards, alignment="center", spacing=20, wrap=True)

    # --- ENSAMBLAJE FINAL ---
    page.clean() 
    page.add(
        header,
        ft.Column([
            ft.Container(
                content=ft.Column([
                    ft.Text(f"Bienvenido al Sistema {nombre_usuario}", size=28, weight="bold", color="white"),
                    ft.Text("Seleccione un módulo para continuar", size=16, color="bluegrey200"),
                ], horizontal_alignment="center"), 
                margin=ft.margin.only(top=40, bottom=20)
            ),
            modules_layout,
            ft.Container(
                content=ft.Text("© 2026 Renacer Territorial - Gestión Social", size=12, color="white70"), 
                padding=40, 
                alignment=ft.Alignment(0, 0)
            )
        ], expand=True, horizontal_alignment="center", scroll="auto")
    )
        
    page.update()