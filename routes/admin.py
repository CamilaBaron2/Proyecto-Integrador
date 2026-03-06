from flask import Blueprint, render_template
from flask_login import login_required
from extensions import db

admin = Blueprint('admin', __name__, url_prefix='/admin')

@admin.route('/usuarios')
@login_required
def ver_usuarios():
    cursor = db.connection.cursor()
    cursor.execute("SELECT Id, Username, Fullname, Rol FROM user")
    usuarios = cursor.fetchall()
    return render_template('dashboard/usuarios.html', usuarios=usuarios)