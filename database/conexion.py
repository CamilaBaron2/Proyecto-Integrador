import mysql.connector

def obtener_usuario(email, password):

    conexion = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="renacer_territorial"
    )

    cursor = conexion.cursor(dictionary=True)

    query = """
        SELECT fullname, Rol
        FROM user
        WHERE email=%s AND password=%s
    """

    cursor.execute(query, (email, password))

    usuario = cursor.fetchone()

    cursor.close()
    conexion.close()

    return usuario