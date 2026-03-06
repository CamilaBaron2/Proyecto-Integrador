from flask import Blueprint, render_template
from flask_login import login_required, current_user
from extensions import db

propietarios = Blueprint('propietarios', __name__, url_prefix='/propietarios')

@propietarios.route("/", methods=["GET"])
@login_required
def ver_propietarios():
    cursor = db.connection.cursor()
    cursor.execute("SELECT IdPropietario, IdUsuario, NombreCompleto, Cedula, Telefono, CorreoElectronico, FechaRegistro, Ubicacion FROM propietarios")
    propietarios_data = cursor.fetchall()
    cursor.close()
    return render_template('roles/propietario.html', propietarios=propietarios_data)