import sqlite3

def get_connection():
    """
    Crea y devuelve una conexion a la base de datos
    """
    conn = sqlite3.connect("bd/biblioteca.db")
    # Activa foreign keys
    conn.execute("PRAGMA foreign_keys = ON")
    return conn