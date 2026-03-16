import flet as ft

def restitucion_view():
    # Campos del formulario
    predio = ft.TextField(label="Nombre del Predio", border_color="blue800", expand=True)
    hectareas = ft.TextField(label="Hectáreas", border_color="blue800", expand=True)

    # Tabla de datos (DataGrid)
    tabla = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("Predio")),
            ft.DataColumn(ft.Text("Tamaño")),
            ft.DataColumn(ft.Text("Fase Legal")),
        ],
        rows=[
            ft.DataRow(cells=[ft.DataCell(ft.Text("Finca La Esperanza")), ft.DataCell(ft.Text("5 Ha")), ft.DataCell(ft.Text("Notificación"))]),
            ft.DataRow(cells=[ft.DataCell(ft.Text("Lote San José")), ft.DataCell(ft.Text("12 Ha")), ft.DataCell(ft.Text("Sentencia"))]),
        ],
    )

    return ft.Container(
        content=ft.Column([
            ft.Card(
                content=ft.Container(
                    padding=20,
                    content=ft.Column([
                        ft.Text("Restitución de Tierras", size=22, weight="bold", color="blue800"),
                        ft.Row([predio, hectareas], spacing=10),
                        ft.ElevatedButton("Iniciar Proceso", bgcolor="blue700", color="white"),
                    ])
                )
            ),
            ft.Text("Casos en Seguimiento", size=18, weight="bold", color="white"),
            ft.Container(content=tabla, bgcolor="white", border_radius=10, padding=10)
        ], scroll="auto"),
        width=800,
        alignment=ft.Alignment(0, 0)
    )