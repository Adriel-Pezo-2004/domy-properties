from flask import Flask, render_template, request, redirect, url_for, session, flash
import os
import database as db
import mysql.connector
from datetime import datetime
import pandas as pd
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas
import base64

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
            session['usuario'] = cuenta[1] 
            if cuenta[1] == 'admin':  
                return redirect(url_for('admin_home'))  
            else:
                return redirect(url_for('home'))  
        else:
            error = "Usuario o contraseña incorrectos"
            return render_template('login.html', error=error)
    else:
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
    usuario = session['usuario']
    if usuario == 'admin':  
        with mysql.connector.connect(**config) as cnx:
            with cnx.cursor() as cursor:
                cursor.execute("SELECT * FROM propiedades")
                propiedades = cursor.fetchall() 
    else:
        with mysql.connector.connect(**config) as cnx:
            with cnx.cursor() as cursor:
                cursor.execute("SELECT * FROM propiedades WHERE usuario_insertor = %s", (usuario,))
                propiedades = cursor.fetchall()
    
    propiedata = []
    if propiedades:
        for propiedad in propiedades:
            task_dict = {
                'analisis': propiedad[2],
                'tipo_pro': propiedad[3],
                'subtipo': propiedad[4],
                'antiguedad': propiedad[5],
                'area_terreno': propiedad[6],
                'area_construida': propiedad[7],
                'tipo_negocio': propiedad[8],
                'imagen': base64.b64encode(propiedad[9]).decode('utf-8') if propiedad[9] else None,
                'usuario_insertor': propiedad[10],
            }
            propiedata.append(task_dict)
    else:
        return """ 
        <script>
            alert("No tienes propiedades");
            window.location.href = "/";  
        </script>
        """
    
    return render_template('propiedades.html', propiedad=propiedata)


@app.route('/contratos')
def contratos():
    usuario = session['usuario']
    if usuario == 'admin':  
        with mysql.connector.connect(**config) as cnx:
            with cnx.cursor() as cursor:
                cursor.execute("SELECT * FROM contrato")
                contratos = cursor.fetchall() 
    else:
        with mysql.connector.connect(**config) as cnx:
            with cnx.cursor() as cursor:
                cursor.execute("SELECT * FROM contrato WHERE usuario_insertor = %s", (usuario,))
                contratos = cursor.fetchall()
                
    return render_template('contratos.html', contratos=contratos)

@app.route('/agenda/crear', methods=['GET', 'POST'])
def crearagenda():
    if request.method == 'POST':
        tarea = request.form['tarea']
        fecha_ini = request.form['fecha_ini']
        fecha_fin = request.form['fecha_fin']
        descripcion = request.form['descripcion']

        cnx = mysql.connector.connect(**config)
        cursor = cnx.cursor()
        insert_query = "INSERT INTO agenda SET tarea = %s, fecha_ini = %s, fecha_fin = %s, descripcion = %s"
        cursor.execute(insert_query, (tarea, fecha_ini, fecha_fin, descripcion))
        cnx.commit()
        cnx.close()
        return """ 
        <script>
            window.location.href = "/agenda";  
        </script>
        """
    return render_template('creartarea.html') 

@app.route('/agenda')
def agenda():
    cnx = mysql.connector.connect(**config)
    cursor = cnx.cursor()
    cursor.execute('SELECT * FROM agenda')
    agendas = cursor.fetchall()
    cursor.close()
    cnx.close()
    return render_template('agenda.html', agendas=agendas)

@app.route('/eventos/crear', methods=['GET', 'POST'])
def creareventos():
    if request.method == 'POST':
        evento = request.form['evento']
        fecha_ini = request.form['fecha_ini']
        fecha_fin = request.form['fecha_fin']
        descripcion = request.form['descripcion']
        imagen = request.files.get('imagen')
        if imagen:
            imagen_data = imagen.read()
        else:
            imagen_data = None

        cnx = mysql.connector.connect(**config)
        cursor = cnx.cursor()
        insert_query = "INSERT INTO eventos SET evento = %s, fecha_ini = %s, fecha_fin = %s, descripcion = %s, imagen=%s"
        cursor.execute(insert_query, (evento, fecha_ini, fecha_fin, descripcion, imagen_data))
        cnx.commit()
        cnx.close()
        return """ 
        <script>
            window.location.href = "/eventos";  
        </script>
        """
    return render_template('crearevento.html') 

@app.route('/eventos')
def eventos():
    cnx = mysql.connector.connect(**config)
    cursor = cnx.cursor()
    cursor.execute('SELECT * FROM eventos')
    task_data = cursor.fetchall()
    cursor.close()
    cnx.close()
    formatted_data = []
    for task in task_data:
        task_dict = {
            'evento': task[0],
            'fecha_ini': task[1],
            'fecha_fin': task[2],
            'descripcion': task[3],
            'imagen': base64.b64encode(task[4]).decode('utf-8') if task[4] else None
        }
    formatted_data.append(task_dict)

    return render_template('eventos.html', eventos=formatted_data)


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
    asesore = cursor.fetchall()
    cursor.close()
    asesores = []
    for asesor in asesore:
        asesor_dict = {
            'user_id': asesor[0],
            'usuario': asesor[1],
            'contraseña': asesor[2],
            'nombres': asesor[3],
            'apellidos': asesor[4],
            'tipo_documento': asesor[5],
            'numero_documento': asesor[6],
            'ruc': asesor[7],
            'genero': asesor[8],
            'sesion': asesor[9],
            'imagen': base64.b64encode(asesor[10]).decode('utf-8') if asesor[10] else None,
            'celular': asesor[11],
            'departamento': asesor[12],
            'provincia': asesor[13],
            'distrito': asesor[14]
        }
    asesores.append(asesor_dict)
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
            window.location.href = "/homer";  
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
        nrodocumento = request.form['nrodocumento']
        correo = request.form['correo']
        departamento = request.form['departamento']
        provincia = request.form['provincia']
        distrito = request.form['distrito']
        urbanizacion = request.form['urbanizacion']
        direccion = request.form['direccion']
        cnx = mysql.connector.connect(**config)
        cursor = cnx.cursor()
        insert_query = "INSERT INTO contacto SET nombre = %s, genero = %s, celular = %s, documento = %s, nrodocumento = %s, correo = %s,departamento = %s, provincia = %s, distrito = %s, urbanizacion = %s, direccion = %s, usuario_insertor = %s"
        cursor.execute(insert_query, (nombre, genero, celular, documento, nrodocumento, correo, departamento, provincia, distrito, urbanizacion, direccion, usuario_insertor))
        cnx.commit()
        session['id_contacto'] = cursor.lastrowid
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
        id_contacto = session.get('id_contacto')
        usuario_insertor = session['usuario']
        analisis = request.form['analisis']
        tipo_pro = request.form['tipo_pro']
        subtipo = request.form['subtipo']
        antiguedad = request.form['antiguedad']
        area_terreno = request.form['area_terreno']
        area_construida = request.form['area_construida']
        tipo_negocio = request.form['tipo_negocio']
        imagen = request.files.get('imagen')
        if imagen:
            imagen_data = imagen.read()
        else:
            imagen_data = None
        cnx = mysql.connector.connect(**config)
        cursor = cnx.cursor()
        insert_query = "INSERT INTO propiedades SET id_contacto = %s, analisis = %s, tipo_pro = %s, subtipo = %s, antiguedad = %s, area_terreno = %s,area_construida = %s, tipo_negocio = %s,  imagen = %s, usuario_insertor = %s"
        cursor.execute(insert_query, (id_contacto, analisis, tipo_pro, subtipo, antiguedad, area_terreno, area_construida, tipo_negocio, imagen_data, usuario_insertor))
        cnx.commit()
        session['id_propiedad'] = cursor.lastrowid
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
        id_propiedad = session.get('id_propiedad')
        usuario_insertor = session['usuario']
        departamento = request.form['departamento']
        provincia = request.form['provincia']
        distrito = request.form['distrito']
        direccion = request.form['direccion']
        cnx = mysql.connector.connect(**config)
        cursor = cnx.cursor()
        insert_query = "INSERT INTO contrato SET id_propiedad = %s, departamento = %s, provincia = %s, distrito = %s, direccion = %s, usuario_insertor= %s"
        cursor.execute(insert_query, (id_propiedad, departamento, provincia, distrito, direccion, usuario_insertor))
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