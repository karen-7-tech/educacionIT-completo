
from flask import Flask, request, render_template, redirect
import pymysql
config = {
    
        "host" :"localhost",
        "user" :"root",
        "password":"",
        "database":"cursos_online"
    }
app = Flask(__name__)
def get_conection():
    
 try:
    connection = pymysql.connect(**config)
    print("Conexión exitosa a MySQL")
    return connection
    
 except pymysql.MySQLError as err:
    print("No se pudo conectar a la base de datos")
    print("Detalles del error:", err)
    print(f"Error: {err}")
    return None
@app.route('/')
def index():
    return render_template('index.html')
@app.route('/seleccion_cursos')
def seleccion_cursos():
    curso_id = request.args.get('id')  # Recupera ?id=ia
    return render_template('seleccion_cursos.html', curso_id=curso_id)
@app.route('/nosotros')
def nosotros():
    return render_template('nosotros.html')

@app.route('/profesores')
def profesores():
    return render_template('profesores.html')

@app.route('/cursos')
def cursos():
    return render_template('cursos.html')

@app.route('/contacto')
def contacto():
    return render_template('contacto.html')
@app.route("/pago", methods=["GET", "POST"])
def pago():
    if request.method == "GET":
        # Recibir datos del alumno y del curso vía query params
        return render_template("pago_cursos.html")

    if request.method == "POST":
        # Recibir datos del formulario
        nombre = request.form['nombre']
        apellido = request.form['apellido']
        email = request.form['email']
        dni = request.form['dni']
        telefono = request.form['telefono']
        curso = request.form['curso']
        precio = request.form['precio']
        metodo_pago = request.form['metodo-pago']
        request.form.get('metodo-pago')
        direccion = request.form['direccion']

        # Aquí podrías validar o simular el pago según método
        pago_exitoso = True  # Cambiar según la lógica real de pago

        if pago_exitoso:
            conn = get_conection()
            if conn:
                try:
                    cursor = conn.cursor()
                    # Insertar en tabla usuarios
                    cursor.execute(
                        "INSERT INTO usuarios (nombre, apellido, documento, edad, email, password, fecha_registro) VALUES (%s,%s,%s,%s,%s,%s,NOW())",
                        (nombre, apellido, dni, 0, email, "")
                    )
                    conn.commit()
                    cursor.close()
                    conn.close()
                except pymysql.MySQLError as e:
                    print("Error al insertar:", e)
                    return "Error al registrar usuario después del pago"

            return f"¡Pago completado! Usuario registrado: {nombre} {apellido} - Curso: {curso} - Método: {metodo_pago}"

        else:
            return "Pago fallido. Intente nuevamente."
@app.route('/pago_form')
def pago_form():
    return render_template('pago_cursos.html')


if __name__ == '__main__':
    app.run(debug=True)