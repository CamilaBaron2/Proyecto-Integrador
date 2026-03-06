from models.entities.User import User
from werkzeug.security import generate_password_hash, check_password_hash

class ModelUser:

    # =========================
    # LOGIN
    # =========================
    @classmethod
    def login(cls, db, user):
        try:
            cursor = db.connection.cursor()
            sql = """
                SELECT Id, Username, Password, Fullname, Rol
                FROM user
                WHERE Username = %s
            """
            cursor.execute(sql, (user.correo,))
            data = cursor.fetchone()

            print("Correo escrito:", user.correo)
            print("Usuario en BD:", data)
            print("Password escrita:", user.password)
            print("Resultado check:", check_password_hash(data[2], user.password))

            if data:
                if check_password_hash(data[2], user.password):
                    return User(
                        id=data[0],
                        correo=data[1],
                        password=data[2],
                        fullname=data[3],
                        rol=data[4]
                    )
                else:
                    return None
            else:
                return None

        except Exception as ex:
            print("ERROR EN MODELUSER.LOGIN:", ex)
            raise

    # =========================
    # OBTENER POR ID (Flask-Login)
    # =========================
    @classmethod
    def get_by_id(cls, db, id):
        try:
            cursor = db.connection.cursor()
            sql = """
                SELECT Id, Username, Password, Fullname, Rol
                FROM user
                WHERE Id = %s
            """
            cursor.execute(sql, (id,))
            row = cursor.fetchone()

            if row:
                return User(
                    id=row[0],
                    correo=row[1],
                    password=row[2],
                    fullname=row[3],
                    rol=row[4]
                )

            return None
        except Exception as ex:
            raise Exception(ex)

    # =========================
    # REGISTRO
    # =========================
    @classmethod
    def register(cls, db, user):
        try:
            cursor = db.connection.cursor()

            # 🔹 usar minúsculas de tu User
            hashed_password = generate_password_hash(user.password)

            sql = """
                INSERT INTO user (Username, Password, Fullname, Rol)
                VALUES (%s, %s, %s, %s)
            """

            cursor.execute(sql, (
                user.correo,       # Username = correo
                hashed_password,
                user.fullname,
                user.rol
            ))

            db.connection.commit()
            return True

        except Exception as ex:
            db.connection.rollback()
            raise Exception(ex)