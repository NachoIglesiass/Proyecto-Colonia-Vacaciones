import mysql.connector
import os

def conectar_bdd():
    # Conexión
    database = mysql.connector.connect(
        host=os.environ.get('DB_HOST'),  # Cambia esto por el host de tu base de datos en la nube
        user=os.environ.get('DB_USER'),  # Cambia esto por tu usuario
        password=os.environ.get('DB_PASSWORD'),  # Cambia esto por tu contraseña
        database=os.environ.get('DB_NAME'),  # Cambia esto por el nombre de tu base de datos
        port=3306  # Asegúrate de que el puerto sea correcto
    )
    # Cursor
    cursor = database.cursor(buffered=True)
    
    return [database, cursor]