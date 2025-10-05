# getdata.py
from flask import Flask, request, render_template, redirect
from app import get_conection
import pymysql

def fetch_cursosOnline():
    print("Iniciando fetch de usuarios...")
    connection = get_conection()

    if connection is None:
        print("No se pudo conectar a la base de datos")
        return
    
    try:
        cursor = connection.cursor()
        query = "SELECT * FROM usuarios"
        cursor.execute(query)
        results = cursor.fetchall()

        if results:
            print(f"Se encontraron {len(results)} registros:")
            for row in results:
                print(row)
        else:
            print("No se encontraron registros en la tabla usuarios.")

    except pymysql.MySQLError as err:
        print(f"Error al ejecutar la consulta: {err}")
    
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()
        print("Conexión cerrada.")

if __name__ == "__main__":
    fetch_cursosOnline()
