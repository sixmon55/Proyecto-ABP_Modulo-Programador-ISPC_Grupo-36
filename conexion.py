# database.py
import mysql.connector
from mysql.connector import Error

def get_connection():
    """Retorna una conexión activa a la base de datos"""
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",      
            password="",
            database="skyroute_grupo36"
        )
        return connection
    except Error as e:
        print(f"Error al conectar a MySQL: {e}")
        return None