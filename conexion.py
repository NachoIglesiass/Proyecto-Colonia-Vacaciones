import mysql.connector
from mysql.connector import Error

def conectar_bdd():
    try:
        # Conexión a AWS RDS
        database = mysql.connector.connect(
            host="colonia-vacaciones.ct4yuku0u905.us-east-2.rds.amazonaws.com",
            user="nacho",
            password="43639241ni",
            database="colonia_vacaciones",
            port=3306
        )
        if database.is_connected():
            cursor = database.cursor(buffered=True)
            return database, cursor
    except Error as e:
        print(f"Error al conectar a la base de datos: {e}")
        return None, None