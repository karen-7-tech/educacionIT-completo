# getdata.py+
import pymysql
print("Intentando conectar a MySQL...")

def get_conection():
    """
    Conecta a MySQL usando XAMPP en Windows.
    """
    config = {
        "host": "127.0.0.1",   # importante: 127.0.0.1 en Windows
        "user": "root",
        "password": "",         # si tu root tiene contraseña, colócala aquí
        "database": "cursos_online",
        "port": 3306            # puerto por defecto de XAMPP
    }

    try:
        connection = pymysql.connect(**config)
        print("Conexión exitosa a MySQL")
        return connection
    except pymysql.MySQLError as err:
        print("No se pudo conectar a la base de datos")
        print("Detalles del error:", repr(err))
        return None

def fetch_cursosOnline():
    print("Iniciando fetch de usuarios...")
    connection = get_conection()

    if connection is None:
        print("No se pudo establecer conexión. Revisar MySQL y configuración.")
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
        print(f"Error al ejecutar la consulta: {repr(err)}")

    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()
        print("Conexión cerrada.")

if __name__ == "__main__":
    fetch_cursosOnline()
