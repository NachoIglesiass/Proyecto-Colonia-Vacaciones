import mysql.connector

def conectar_bdd():
    # Conexiòn
    database = mysql.connector.connect(
    host = "localhost",
    user = "nacho",
    password = "43639241ni",
    database = "colonia_vacaciones",
    port = 3306
    )
    # Cursor
    cursor = database.cursor(buffered=True)
    
    return [database, cursor]