import mysql.connector

def conectar_bdd():
    # Conexión a AWS RDS
    database = mysql.connector.connect(
        host="colonia-vacaciones.ct4yuku0u905.us-east-2.rds.amazonaws.com",
        user="nacho",
        password="43639241ni",
        database="colonia_vacaciones",
        port=3306
    )
    # Cursor
    cursor = database.cursor(buffered=True)
    
    return [database, cursor]
