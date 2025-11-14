
from flask import Flask, request, render_template, redirect, url_for
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
@app.route('/seleccion_cursos/<id>')
def seleccion_cursos(id):
    return render_template('seleccion_cursos.html', curso_id=id)

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
@app.route('/inicio_campus')
def inicio_campus():
    return render_template("inicio_campus.html")
@app.route('/indexcampus')
def indexcampus():
    return render_template("indexcampus.html")
@app.route('/mis_cursos')
def mis_cursos():
    return render_template("mis_cursos.html")
@app.route('/campus_python')
def campus_python():
    return render_template("campus_python.html")
    
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

@app.route("/inscribirse", methods=["POST"])
def inscribirse():
    print(">>> La función inscribirse() fue llamada")
    print(">>> Datos del formulario:", request.form)

    nombre = request.form["nombre"]
    apellido = request.form["apellido"]
    email = request.form["email"]
    dni = request.form["dni"]
    telefono = request.form["telefono"]
    password = request.form["password"]
    fecha_nac = request.form["fecha_nacimiento"]
    curso_id = request.form["curso"]
    precio = request.form["precio"]

    conn = get_conection()
    cursor = conn.cursor()

    
    cursor.execute("""
        SELECT id_usuario FROM usuarios 
        WHERE email=%s OR dni=%s
    """, (email, dni))
    usuario = cursor.fetchone()

    if usuario:
        user_id = usuario[0]
    else:
        
        cursor.execute("""
            INSERT INTO usuarios (nombre, apellido, email, telefono, dni, password, fecha_nacimiento)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (nombre, apellido, email, telefono, dni, password, fecha_nac))
        conn.commit()
        user_id = cursor.lastrowid

   
    cursor.execute("""
        SELECT id_inscripcion FROM inscripciones
        WHERE id_usuario=%s AND id_curso=%s
    """, (user_id, curso_id))
    insc = cursor.fetchone()

    if insc:
        cursor.close()
        conn.close()
        return redirect("/pago")

    titulo_curso = request.form["curso"]

    cursor.execute("""
        SELECT id_curso FROM cursos WHERE titulo = %s
    """, (titulo_curso,))
    curso_row = cursor.fetchone()

    if not curso_row:
        print("❌ Error: No se encontró un curso con ese título:", titulo_curso)
        cursor.close()
        conn.close()
        return "Error: Curso inexistente"


    id_curso_real = curso_row[0]
    print("✔️ ID del curso encontrado:", id_curso_real)

    cursor.execute("""
        INSERT INTO inscripciones (id_usuario, id_curso, fecha_inscripcion, estado)
        VALUES (%s, %s, NOW(), %s)
    """, (user_id, id_curso_real, "Inscripto"))


    conn.commit()

    cursor.close()
    conn.close()

   
    return redirect(url_for(
    "pago",
    nombre=nombre,
    apellido=apellido,
    fecha_nacimiento=fecha_nac,
    email=email,
    dni=dni,
    telefono=telefono,
    curso=curso_id,
    precio=precio
    ))




if __name__ == '__main__':
    import os
    port = int(os.environ.get("PORT", 5000))  # Usa el puerto que Render da
    app.run(host="0.0.0.0", port=port)
    app.run(debug=True)