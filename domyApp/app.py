from flask import Flask, render_template, request, redirect, url_for, session
import os
import database as db
import mysql.connector
from datetime import datetime

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
            session['usuario'] = cuenta[0]
            return redirect(url_for('home'))
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
        return render_template('home.html')
    else:
        return redirect(url_for('login'))

@app.route('/contact')
def contact():
    cnx = mysql.connector.connect(**config)
    cursor = cnx.cursor()
    cursor.execute('SELECT * FROM contacto')
    clientes = cursor.fetchall()
    cursor.close()
    cnx.close()
    return render_template('clientes.html', clientes=clientes)

@app.route('/contact/crear', methods=['GET', 'POST'])
def crearclientes():
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
        insert_query = "INSERT INTO clientes SET Nombre = %s, Apellido = %s, Direccion = %s, Ciudad = %s, Estado = %s,CodigoPostal = %s, Pais = %s, Telefono = %s, Email = %s, FechaRegistro = %s"
        cursor.execute(insert_query, (nombre, apellido, direccion, ciudad, estado, codigo_postal, pais, telefono, email, fecha_registro))
        cnx.commit()
        cnx.close()
        return """ 
        <script>
            alert("Producto creado exitosamente");
            window.location.href = "/clients";  
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

if __name__ == '__main__':
    app.run(debug=True, port=4000)