from werkzeug.security import check_password_hash
from flask_login import UserMixin

class User(UserMixin):
    def __init__(self, id, correo, password, fullname=None, rol=None):
        self.id = id                # 🔹 minúscula
        self.correo = correo        # usamos correo en lugar de username
        self.password = password
        self.fullname = fullname
        self.rol = rol

    def check_password(self, password):
        return check_password_hash(self.password, password)
    
