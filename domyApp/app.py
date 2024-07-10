from flask import Flask, render_template, request, redirect, url_for, session
import os
import database as db
import mysql.connector
from datetime import datetime
import pandas as pd
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas

app = Flask(__name__, template_folder='templates')
app.secret_key = "tu_clave_secreta"

config = {
    'user': 'root1',
    'password': 'afpv2023',
    'host': 'localhost',
    'database': 'domy'
}

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        cnx = mysql.connector.connect(**config)
        usuario = request.form['usuario']
        contraseña = request.form['contraseña']
        cursor = cnx.cursor()
        cursor.execute("SELECT * FROM usuarios WHERE usuario = %s AND contraseña = %s", (usuario, contraseña))
        cuenta = cursor.fetchone()

        if cuenta:
            session['usuario'] = cuenta[1]  # Asumiendo que el nombre de usuario está en la segunda columna
            if cuenta[1] == 'admin':  # Verifica si el usuario es 'admin'
                return redirect(url_for('admin_home'))  # Redirige a la página de inicio del admin
            else:
                return redirect(url_for('home'))  # Redirige a la página de inicio normal
        else:
            error = "Usuario o contraseña incorrectos"
            return render_template('login.html', error=error)

    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('usuario', None)
    return redirect(url_for('login'))

@app.route('/')
def home():
    if 'usuario' in session:
        if session['usuario'] == 'admin':
            return redirect(url_for('admin_home')) 
        return render_template('home.html')
    else:
        return redirect(url_for('login'))

@app.route('/admin')
def admin_home():
    if 'usuario' in session and session['usuario'] == 'admin':
        return render_template('admin_home.html')  
    else:
        return redirect(url_for('login'))

@app.route('/contact')
def contact():
    cnx = mysql.connector.connect(**config)
    cursor = cnx.cursor()
    cursor.execute('SELECT * FROM contacto')
    contactos = cursor.fetchall()
    cursor.close()
    cnx.close()
    return render_template('contactos.html', contactos=contactos)

@app.route('/propiedad')
def propiedad():
    cnx = mysql.connector.connect(**config)
    cursor = cnx.cursor()
    cursor.execute('SELECT * FROM propiedades')
    propiedad = cursor.fetchall()
    cursor.close()
    cnx.close()
    return render_template('propiedades.html', propiedad=propiedad)


@app.route('/agenda')
def agenda():
    cnx = mysql.connector.connect(**config)
    cursor = cnx.cursor()
    cursor.execute('SELECT * FROM agenda')
    agendas = cursor.fetchall()
    cursor.close()
    cnx.close()
    return render_template('agenda.html', agendas=agendas)

@app.route('/eventos')
def eventos():
    cnx = mysql.connector.connect(**config)
    cursor = cnx.cursor()
    cursor.execute('SELECT * FROM eventos')
    eventos = cursor.fetchall()
    cursor.close()
    cnx.close()
    return render_template('eventos.html', eventos=eventos)


@app.route('/podcast')
def podcasts():
    cnx = mysql.connector.connect(**config)
    cursor = cnx.cursor()
    cursor.execute('SELECT * FROM podcast')
    podcasts = cursor.fetchall()
    cursor.close()
    cnx.close()
    return render_template('podcast.html', podcasts=podcasts)

@app.route('/biblioteca')
def biblioteca():
    cnx = mysql.connector.connect(**config)
    cursor = cnx.cursor()
    cursor.execute('SELECT * FROM biblioteca')
    biblioteca = cursor.fetchall()
    cursor.close()
    cnx.close()
    return render_template('biblioteca.html', biblioteca=biblioteca)

@app.route('/propiedades')
def propiedades():
    cnx = mysql.connector.connect(**config)
    cursor = cnx.cursor()
    cursor.execute('SELECT * FROM propiedades')
    propiedades = cursor.fetchall()
    cursor.close()
    cnx.close()
    return render_template('propiedad.html', propiedades=propiedades)

@app.route('/asesores')
def asesores():
    cnx = mysql.connector.connect(**config)
    cursor = cnx.cursor()
    cursor.execute('SELECT * FROM usuarios')
    asesores = cursor.fetchall()
    cursor.close()
    cnx.close()
    return render_template('asesores.html', asesores=asesores)

@app.route('/asesor/crear', methods=['GET', 'POST'])
def crearasesores():
    if request.method == 'POST':
        usuario = request.form['usuario']
        contraseña = request.form['contraseña']
        nombres = request.form['nombres']
        apellidos = request.form['apellidos']
        cnx = mysql.connector.connect(**config)
        cursor = cnx.cursor()
        insert_query = "INSERT INTO usuarios SET usuario = %s, contraseña = %s, nombres = %s, apellidos = %s"
        cursor.execute(insert_query, (usuario, contraseña, nombres, apellidos))
        cnx.commit()
        cnx.close()
        return """ 
        <script>
            window.location.href = "/propiedad/crear";  
        </script>
        """
    return render_template('crearasesores.html') 

@app.route('/contact/crear', methods=['GET', 'POST'])
def crearclientes():
    if request.method == 'POST':
        usuario_insertor = session['usuario']
        nombre = request.form['nombre']
        genero = request.form['genero']
        celular = request.form['celular']
        documento = request.form['documento']
        correo = request.form['correo']
        departamento = request.form['departamento']
        provincia = request.form['provincia']
        distrito = request.form['distrito']
        urbanizacion = request.form['urbanizacion']
        direccion = request.form['direccion']
        cnx = mysql.connector.connect(**config)
        cursor = cnx.cursor()
        insert_query = "INSERT INTO contacto SET nombre = %s, genero = %s, celular = %s, documento = %s, correo = %s,departamento = %s, provincia = %s, distrito = %s, urbanizacion = %s, direccion = %s, usuario_insertor = %s"
        cursor.execute(insert_query, (nombre, genero, celular, documento, correo, departamento, provincia, distrito, urbanizacion, direccion, usuario_insertor))
        cnx.commit()
        cnx.close()
        return """ 
        <script>
            window.location.href = "/propiedad/crear";  
        </script>
        """
    return render_template('crearcontactos.html')  

@app.route('/clients/<int:id>/editar', methods=['GET', 'POST'])
def editarclientes(id):
    if request.method == 'POST':
        nombre = request.form['nombre']
        apellido = request.form['apellido']
        direccion = request.form['direccion']
        ciudad = request.form['ciudad']
        estado = request.form['estado']
        codigo_postal = request.form['codigo_postal']
        pais = request.form['pais']
        telefono = request.form['telefono']
        email = request.form['email']
        fecha_registro = request.form['fecha_registro']
        try:
            fecha_registro = datetime.strptime(fecha_registro, '%Y-%m-%d').date()
        except ValueError:
            return """
                <script>
                    alert("Ingrese una fecha válida");
                </script>
            """
        cnx = mysql.connector.connect(**config)
        cursor = cnx.cursor()
        update_query = "UPDATE clientes SET Nombre = %s, Apellido = %s, Direccion = %s, Ciudad = %s, Estado = %s,CodigoPostal = %s, Pais = %s, Telefono = %s, Email = %s, FechaRegistro = %s WHERE ClienteID = %s"
        cursor.execute(update_query, (nombre, apellido, direccion, ciudad, estado, codigo_postal, pais, telefono, email, fecha_registro, id))
        cnx.commit()
        cnx.close()
        return """
            <script>
                alert("Cliente editado exitosamente");
                window.location.href = "/clients"; // Reemplaza esto con la URL deseada
            </script>
        """
    else:
        cnx = mysql.connector.connect(**config)
        cursor = cnx.cursor()
        select_query = "SELECT * FROM clientes WHERE ClienteID = %s"
        cursor.execute(select_query, (id,))
        cliente = cursor.fetchone()
        cnx.close()
        return render_template('editarclientes.html', cliente=cliente)

@app.route('/clients/<int:id>/eliminar', methods=['POST'])
def eliminar_cliente(id):
    cnx = mysql.connector.connect(**config)
    cursor = cnx.cursor()
    cursor.execute('DELETE FROM clientes WHERE ClienteID = %s', (id,))
    cnx.commit()
    cursor.close()
    cnx.close()
    return redirect(url_for('clients'))

@app.route('/propiedad/crear', methods=['GET', 'POST'])
def crearpropiedades():
    if request.method == 'POST':
        usuario_insertor = session['usuario']
        nombre = request.form['nombre']
        genero = request.form['genero']
        celular = request.form['celular']
        documento = request.form['documento']
        correo = request.form['correo']
        departamento = request.form['departamento']
        provincia = request.form['provincia']
        distrito = request.form['distrito']
        urbanizacion = request.form['email']
        direccion = request.form['direccion']
        cnx = mysql.connector.connect(**config)
        cursor = cnx.cursor()
        insert_query = "INSERT INTO contactos SET nombre = %s, genero = %s, celular = %s, documento = %s, correo = %s,departamento = %s, provincia = %s, distrito = %s, urbanizacion = %s, direccion = %s, usuario_insertor = %s"
        cursor.execute(insert_query, (nombre, genero, celular, documento, correo, departamento, provincia, distrito, urbanizacion, direccion, usuario_insertor))
        cnx.commit()
        cnx.close()
        return """ 
        <script>
            window.location.href = "/contrato/crear";  
        </script>
        """
    return render_template('crearpropiedad.html') 

@app.route('/contrato/crear', methods=['GET', 'POST'])
def crearcontratos():
    if request.method == 'POST':
        usuario_insertor = session['usuario']
        departamento = request.form['departamento']
        provincia = request.form['provincia']
        distrito = request.form['distrito']
        direccion = request.form['direccion']
        cnx = mysql.connector.connect(**config)
        cursor = cnx.cursor()
        insert_query = "INSERT INTO contactos SET departamento = %s, provincia = %s, distrito = %s, direccion = %s, usuario_insertor= %s"
        cursor.execute(insert_query, (departamento, provincia, distrito, direccion, usuario_insertor))
        cnx.commit()
        cnx.close()
        return """ 
        <script>
            window.location.href = "/";  
        </script>
        """
    return render_template('crearcontrato.html') 

if __name__ == '__main__':
    app.run(debug=True, port=4000)