from flask import Blueprint, request, jsonify, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required
from markupsafe import escape
from flask import Blueprint, request, jsonify, redirect, url_for, flash, render_template


from models.ModelUser import ModelUser
from models.entities.User import User
from extensions import db

auth = Blueprint('auth', __name__)

# =========================
# LOGIN
# =========================
@auth.route('/login', methods=['GET', 'POST'])
def login():
    print("ENTRÓ A AUTH LOGIN")
    if request.method == 'GET':
        return render_template("aplicacion/login.html")  # Mostrar formulario en navegador

    # POST -> procesar formulario HTML
    try:
        correo = escape(request.form.get("correo", "").strip())
        password = request.form.get("password", "")

        if not correo or not password:
            flash("Faltan datos", "danger")
            return render_template("aplicacion/login.html")

        user = User(id=0, correo=correo, password=password)
        print("ANTES DE LLAMAR A MODELUSER")
        logged_user = ModelUser.login(db, user)
        print("DESPUÉS DE LLAMAR A MODELUSER")
       
        if logged_user:
            login_user(logged_user)
            flash(f"Bienvenido {logged_user.fullname}!", "success")
            return redirect(url_for("dashboard.dashboard_view"))  # redirigir al dashboard
        else:
            flash("Usuario o contraseña incorrectos", "danger")
            return render_template("aplicacion/login.html")

    except Exception as ex:
        flash(f"Error: {str(ex)}", "danger")
        return render_template("aplicacion/login.html")

# =========================
# REGISTER
# =========================
@auth.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template("aplicacion/register.html")  # Mostrar formulario

    # POST -> procesar registro JSON
    try:
        data = request.json
        nombre = data.get("nombre", "").strip()
        correo = data.get("correo", "").strip()
        password = data.get("password", "")
        confirmar = data.get("confirmar_password", "")

        if not nombre or not correo or not password or not confirmar:
            return jsonify({"success": False, "message": "Campos incompletos"}), 400

        if password != confirmar:
            return jsonify({"success": False, "message": "Las contraseñas no coinciden"}), 400

        user = User(0, correo, password, nombre, "Propietario")
        ModelUser.register(db, user)

        return jsonify({"success": True, "message": "Usuario registrado correctamente"}), 201

    except Exception as ex:
        return jsonify({"success": False, "message": str(ex)}), 500

# =========================
# LOGOUT
# =========================
@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash("Has cerrado sesión correctamente", "info")
    return redirect(url_for('/')) # Redirige al home