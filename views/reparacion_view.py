import flet as ft

def obtener_reparacion_contenido(page: ft.Page, rol_usuario, cliente_http):
    """
    Retorna el control (Column/Row/Container) correspondiente 
    al módulo de reparación según el rol.
    """
    def borrar_propietario(id_propietario):
    # 1. Confirmación simple (Opcional, pero recomendada)
        def confirmar_borrado(e):
            r = cliente_http.delete(f"http://127.0.0.1:5000/propietarios/eliminar/{id_propietario}")
            if r.status_code == 200:
                dlg_conf.open = False
                # 2. Mostrar Alerta
                page.snack_bar = ft.SnackBar(ft.Text("Propietario eliminado"), bgcolor="red")
                page.snack_bar.open = True
                
                # 3. RECARGAR LA VISTA SIN SALIR
                page.clean()
                # IMPORTANTE: Volvemos a inyectar el contenido fresco
                page.add(obtener_reparacion_contenido(page, rol_usuario, cliente_http))
                page.update()

        dlg_conf = ft.AlertDialog(
            title=ft.Text("¿Estás seguro?"),
            content=ft.Text("Esta acción no se puede deshacer."),
            actions=[
                ft.TextButton("No", on_click=lambda _: setattr(dlg_conf, "open", False)),
                ft.ElevatedButton("Sí, eliminar", bgcolor="red", color="white", on_click=confirmar_borrado)
            ]
        )
        page.overlay.append(dlg_conf)
        dlg_conf.open = True
        page.update()

    def abrir_edicion(p):
        # Campos de texto con los datos actuales
        nombre = ft.TextField(label="Nombre Completo", value=p.get('NombreCompleto', ''))
        cedula = ft.TextField(label="Cédula", value=p.get('Cedula', ''), read_only=True)
        tel = ft.TextField(label="Teléfono", value=p.get('Telefono', ''))
        correo = ft.TextField(label="Correo", value=p.get('CorreoElectronico', ''))
        fecha = ft.TextField(label="Fecha Registro", value=p.get('FechaRegistro', ''), read_only=True)
        ubicacion = ft.TextField(label="Ubicación", value=p.get('Ubicacion', ''))

        def guardar_cambios(e):
            payload = {
                "NombreCompleto": nombre.value,
                "Telefono": tel.value,
                "CorreoElectronico": correo.value,
                "Ubicacion": ubicacion.value
            }
            id_pro = p.get('IdPropietario')
            try:
                res = cliente_http.put(f"http://127.0.0.1:5000/propietarios/editar/{id_pro}", json=payload)
                
                if res.status_code == 200:
                    dlg.open = False
                    # En lugar de page.clean(), notificamos y refrescamos el modulo
                    page.snack_bar = ft.SnackBar(ft.Text("¡Propietario actualizado!"), bgcolor="green")
                    page.snack_bar.open = True
                    
                    # Limpiamos los controles actuales y re-añadimos el contenido
                    page.controls.clear()
                    page.add(obtener_reparacion_contenido(page, rol_usuario, cliente_http))
                    page.update()
                else:
                    print(f"Error del servidor: {res.status_code}")
            except Exception as ex:
                print(f"Error al conectar para actualizar: {ex}")

        dlg = ft.AlertDialog(
            title=ft.Text("Editar Propietario"),
            content=ft.Column([nombre, cedula, tel, correo, fecha, ubicacion], tight=True, scroll="auto", width=400),
            actions=[
                ft.TextButton("Cancelar", on_click=lambda _: (setattr(dlg, "open", False), page.update())),
                ft.ElevatedButton("Actualizar", on_click=guardar_cambios)
            ]
        )
        page.overlay.append(dlg)
        dlg.open = True
        page.update()      
    
    def crear_tabla_propietarios():
        filas = []
        try:
            r = cliente_http.get(
                "http://127.0.0.1:5000/propietarios/", 
                headers={"Accept": "application/json"},
                timeout=5
            )
            if r.status_code == 200:
                content = r.text.strip()
                if not content:
                    return ft.Text("No hay propietarios registrados.", color="white70")
                
                datos = r.json()
                for p in datos:
                    id_actual = p['IdPropietario']
                    filas.append(
                        ft.DataRow(
                            cells=[
                                ft.DataCell(ft.Text(p['NombreCompleto'])),
                                ft.DataCell(ft.Text(p['Cedula'])),
                                ft.DataCell(ft.Text(p['Telefono'])),
                                ft.DataCell(ft.Text(p['CorreoElectronico'])),      
                                ft.DataCell(ft.Text(p['FechaRegistro'])), 
                                ft.DataCell(ft.Text(p['Ubicacion'])), 
                                ft.DataCell(
                                    ft.Row([
                                        ft.TextButton("📝", on_click=lambda _, p_data=p: abrir_edicion(p_data)),
                                        ft.TextButton("🗑️", on_click=lambda _, id =id_actual: borrar_propietario(id)),
                                    ])
                                ),
                            ]
                        )
                    )
                
                return ft.Row(
                    controls=[
                        ft.DataTable(
                            bgcolor="white10",
                            border=ft.border.all(1, "white24"),
                            border_radius=10,
                            columns=[
                                ft.DataColumn(ft.Text("Nombre")),
                                ft.DataColumn(ft.Text("Cédula")),
                                ft.DataColumn(ft.Text("Teléfono")),
                                ft.DataColumn(ft.Text("CorreoElectronico")),     
                                ft.DataColumn(ft.Text("FechaRegistro")), 
                                ft.DataColumn(ft.Text("Ubicación")),
                                ft.DataColumn(ft.Text("Acciones")),
                            ],
                            rows=filas
                        )
                    ],
                    scroll="always"
                )
            else:
                return ft.Text(f"Error {r.status_code}", color="red")
        except Exception as e:
            return ft.Text(f"Error de conexión: {e}", color="red")

    # --- LÓGICA DE RETORNO SEGÚN ROL ---
    if rol_usuario == "Administrador":
        return ft.Column([
            ft.Text("PANEL DE CONTROL - VIVIENDAS (ADMIN)", size=20, weight="bold", color="white"),
            crear_tabla_propietarios()
        ], spacing=20)
    else:
        # Vista para Propietario / Estándar
        return ft.Column([
            ft.Text("REGISTRO DE EVIDENCIAS", size=20, weight="bold", color="white"),
            ft.TextField(label="Descripción del daño", multiline=True),
            ft.ElevatedButton("Subir Foto/Archivo", icon="upload")
        ], spacing=20)