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
    'database': 'farmacia'
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
def homes():
    if 'usuario' in session:
        return render_template('index.html')
    else:
        return redirect(url_for('login'))
    
@app.route('/home')
def home():
    if 'usuario' in session:
        return render_template('home.html')
    else:
        return redirect(url_for('login'))

@app.route('/products')
def products():
    cnx = mysql.connector.connect(**config)
    cursor = cnx.cursor()
    cursor.execute('SELECT * FROM Productos')
    productos = cursor.fetchall()
    cursor.close()
    cnx.close()
    return render_template('productos.html', productos=productos)

@app.route('/clients')
def clients():
    cnx = mysql.connector.connect(**config)
    cursor = cnx.cursor()
    cursor.execute('SELECT * FROM clientes')
    clientes = cursor.fetchall()
    cursor.close()
    cnx.close()
    return render_template('clientes.html', clientes=clientes)

@app.route('/ventas')
def ventas():
    cnx = mysql.connector.connect(**config)
    cursor = cnx.cursor()
    cursor.execute('SELECT * FROM ventas')
    ventas = cursor.fetchall()
    cursor.close()
    cnx.close()
    return render_template('ventas.html', ventas=ventas)

@app.route('/detail')
def detail():
    cnx = mysql.connector.connect(**config)
    cursor = cnx.cursor()
    cursor.execute('SELECT * FROM detalleventa')
    detalles = cursor.fetchall()
    cursor.close()
    cnx.close()
    return render_template('detalle.html', detalles=detalles)

@app.route('/facturas')
def factura():
    cnx = mysql.connector.connect(**config)
    cursor = cnx.cursor()
    cursor.execute('SELECT * FROM facturas' )
    facturas = cursor.fetchall()
    cursor.close()
    cnx.close()
    return render_template('factura.html', facturas=facturas)

@app.route('/productos/crear', methods=['GET', 'POST'])
def crearproductos():
    if request.method == 'POST':
        nombre = request.form['nombre']
        descripcion = request.form['descripcion']
        precio = float(request.form['precio'])
        stock = int(request.form['stock'])
        fecha_entrada = request.form['fecha_entrada']
        try:
            fecha = datetime.strptime(fecha_entrada, '%Y-%m-%d').date()
        except ValueError:
            return "Ingrese Fecha Válida"
        proveedor = request.form['proveedor']
        categoria = request.form['categoria']

        cnx = mysql.connector.connect(**config)
        cursor = cnx.cursor()
        insert_query = "INSERT INTO productos (Nombre, Descripcion, PrecioUnitario, CantidadStock, Proveedor, Categoria, FechaEntradaStock) VALUES (%s, %s, %s, %s, %s, %s)"
        cursor.execute(insert_query, (nombre, descripcion, precio, stock, proveedor, categoria, fecha_entrada))
        cnx.commit()
        cnx.close()
        return """ 
        <script>
            alert("Producto creado exitosamente");
            window.location.href = "/products";  
        </script>
        """
    return render_template('crearproductos.html')    

@app.route('/products/<int:id>/editar', methods=['GET', 'POST'])
def editarproductos(id):
    if request.method == 'POST':
        nombre = request.form['nombre']
        descripcion = request.form['descripcion']
        precio = request.form['precio']
        stock = request.form['stock']
        fecha_entrada = request.form['fecha_entrada']
        try:
            fecha_entrada = datetime.strptime(fecha_entrada, '%Y-%m-%d').date()
        except ValueError:
            return """
        <script>
            alert("Ingrese fecha valida")
        </script>
        """
            
        proveedor = request.form['proveedor']
        categoria = request.form['categoria']
        cnx = mysql.connector.connect(**config)
        cursor = cnx.cursor()
        update_query = "UPDATE productos SET Nombre = %s, Descripcion = %s, PrecioUnitario = %s, CantidadStock = %s, Proveedor = %s, Categoria = %s,FechaEntradaStock = %s WHERE ProductoID = %s"
        cursor.execute(update_query, (nombre, descripcion, precio, stock, proveedor, categoria, fecha_entrada, id))
        cnx.commit()
        cnx.close()
        return """
        <script>
            alert("Producto editado exitosamente");
            window.location.href = "/products";  // Reemplaza esto con la URL deseada
        </script>
        """
    else:
        cnx = mysql.connector.connect(**config)
        cursor = cnx.cursor()
        select_query = "SELECT * FROM productos WHERE ProductoID = %s"
        cursor.execute(select_query, (id,))
        producto = cursor.fetchone()
        cnx.close()
        return render_template('editarproductos.html', producto=producto)

@app.route('/products/<int:id>/eliminar', methods=['POST'])
def eliminar_producto(id):
    cnx = mysql.connector.connect(**config)
    cursor = cnx.cursor()
    cursor.execute('DELETE FROM productos WHERE ProductoID = %s', (id,))
    cnx.commit()
    cursor.close()
    cnx.close()
    return redirect(url_for('products'))

@app.route('/clients/crear', methods=['GET', 'POST'])
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
    return render_template('crearclientes.html') 

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

@app.route('/ventas/crear', methods=['GET', 'POST'])
def crearventas():
    if request.method == 'POST':
        cliente_id = request.form['cliente_id']
        total_venta = request.form['total_venta']
        metodo_pago = request.form['metodo_pago']
        estado = request.form['estado']
        fecha = request.form['fecha']
        try:
            fecha_hora = datetime.strptime(fecha, '%Y-%m-%dT%H:%M')
        except ValueError:
            return """
                <script>
                    alert("Ingrese una fecha válida");
                </script>
            """

        cnx = mysql.connector.connect(**config)
        cursor = cnx.cursor()
        insert_query = "INSERT INTO ventas (FechaHora, Cliente, TotalVenta, MetodoPago, Estado) VALUES (%s, %s, %s, %s, %s)"
        cursor.execute(insert_query, (fecha_hora, cliente_id, total_venta, metodo_pago, estado))
        cnx.commit()
        cursor.close()
        cnx.close()
        return """ 
        <script>
            alert("Venta creada exitosamente");
            window.location.href = "/ventas";  
        </script>
        """

    return render_template('crearventas.html', ventas=ventas)

@app.route('/ventas/<int:id>/editar', methods=['GET', 'POST'])
def editarventas(id):
    if request.method == 'POST':
        cliente_id = request.form['cliente_id']
        total_venta = request.form['total_venta']
        metodo_pago = request.form['metodo_pago']
        estado = request.form['estado']
        fecha = request.form['fecha']
        try:
            fecha_hora = datetime.strptime(fecha, '%Y-%m-%dT%H:%M')
        except ValueError:
            return """
                <script>
                    alert("Ingrese una fecha válida");
                </script>
            """
        cnx = mysql.connector.connect(**config)
        cursor = cnx.cursor()
        update_query = "UPDATE ventas SET FechaHora = %s, Cliente = %s, TotalVenta = %s, MetodoPago = %s, Estado = %s WHERE VentaID = %s"
        cursor.execute(update_query, (fecha_hora, cliente_id, total_venta, metodo_pago, estado, id))
        cnx.commit()
        cnx.close()
        return """ 
        <script>
            alert("Venta editada exitosamente");
            window.location.href = "/ventas";  
        </script>
        """
    else:
        cnx = mysql.connector.connect(**config)
        cursor = cnx.cursor()
        select_query = "SELECT * FROM ventas WHERE VentaID = %s"
        cursor.execute(select_query, (id,))
        venta = cursor.fetchone()
        cnx.close()
        return render_template('editarventas.html', venta=venta)
    
    

@app.route('/ventas/<int:id>/eliminar', methods=['POST'])
def eliminar_ventas(id):
    cnx = mysql.connector.connect(**config)
    cursor = cnx.cursor()
    cursor.execute('DELETE FROM ventas WHERE VentaID = %s', (id,))
    cnx.commit()
    cursor.close()
    cnx.close()
    return redirect(url_for('ventas'))

@app.route('/facturas/crear', methods=['GET', 'POST'])
def crearfacturas():
    if request.method == 'POST':
        venta_id = request.form['venta_id']
        cliente_id = request.form['cliente_id']
        total_venta = request.form['total_venta']
        estado = request.form['estado']
        fecha = request.form['fecha_emision']
        try:
            fecha_emision = datetime.strptime(fecha, '%Y-%m-%d').date()
        except ValueError:
            return """
        <script>
            alert("Ingrese fecha valida")
        </script>
        """

        cnx = mysql.connector.connect(**config)
        cursor = cnx.cursor()
        insert_query = "INSERT INTO facturas (FechaEmision, VentaID, ClienteID, TotalFactura, Estado) VALUES (%s, %s, %s, %s, %s)"
        cursor.execute(insert_query, (fecha_emision, venta_id, cliente_id, total_venta, estado))
        cnx.commit()
        cursor.close()
        cnx.close()
        return """ 
        <script>
            alert("Venta creado exitosamente");
            window.location.href = "/facturas";  
        </script>
        """
    return render_template('crearfacturas.html', factura=factura)

@app.route('/facturas/<int:id>/editar', methods=['GET', 'POST'])
def editarfacturas(id):
    if request.method == 'POST':
        cliente_id = request.form['cliente_id']
        venta_id = request.form['venta_id']
        total_venta = request.form['total_venta']
        estado = request.form['estado']
        fecha = request.form['fecha']
        try:
            fecha_emision = datetime.strptime(fecha, '%Y-%m-%d').date()
        except ValueError:
            return """
        <script>
            alert("Ingrese fecha valida")
        </script>
        """
        cnx = mysql.connector.connect(**config)
        cursor = cnx.cursor()
        update_query = "UPDATE facturas SET FechaEmision = %s, VentaID = %s, ClienteID = %s, TotalFactura = %s, Estado = %s WHERE NumeroFactura = %s"
        cursor.execute(update_query, (fecha_emision, venta_id, cliente_id, total_venta, estado, id))
        cnx.commit()
        cursor.close()
        cnx.close()
        return """ 
        <script>
            alert("Factura editada exitosamente");
            window.location.href = "/facturas";  
        </script>
        """
    else:
        cnx = mysql.connector.connect(**config)
        cursor = cnx.cursor()
        select_query = "SELECT * FROM facturas WHERE NumeroFactura = %s"
        cursor.execute(select_query, (id,))
        factura = cursor.fetchone()
        cnx.close()
        return render_template('editarfacturas.html', factura=factura)

@app.route('/facturas/<int:id>/eliminar', methods=['POST'])
def eliminar_facturas(id):
    cnx = mysql.connector.connect(**config)
    cursor = cnx.cursor()
    cursor.execute('DELETE FROM facturas WHERE NumeroFactura = %s', (id,))
    cnx.commit()
    cursor.close()
    cnx.close()
    return redirect(url_for('facturas'))

@app.route('/detail/crear', methods=['GET', 'POST'])
def creardetalles():
    if request.method == 'POST':
        venta_id = request.form['venta_id']
        product_id = request.form['product_id']
        cantidad = request.form['cantidad']
        precio_unitario = request.form['precio_unitario']

        cnx = mysql.connector.connect(**config)
        cursor = cnx.cursor()
        insert_query = "INSERT INTO detalleventa (VentaID, ProductoID, CantidadVendida, Preciounitario) VALUES (%s, %s, %s, %s)"
        cursor.execute(insert_query, (venta_id, product_id, cantidad, precio_unitario))
        cnx.commit()
        cursor.close()
        cnx.close()
        return """ 
        <script>
            alert("Detalle creado exitosamente");
            window.location.href = "/detail";  
        </script>
        """
    return render_template('creardetalles.html', detail=detail)

@app.route('/detail/<int:id>/editar', methods=['GET', 'POST'])
def editardetalles(id):
    if request.method == 'POST':
        venta_id = request.form['venta_id']
        product_id = request.form['product_id']
        cantidad = request.form['cantidad']
        precio_unitario = request.form['precio_unitario']

        cnx = mysql.connector.connect(**config)
        cursor = cnx.cursor()
        update_query = "UPDATE detalleventa SET VentaID = %s, ProductoID = %s, CantidadVendida = %s, Preciounitario = %s WHERE DetalleVentaID = %s"
        cursor.execute(update_query, (venta_id, product_id, cantidad, precio_unitario, id))
        cnx.commit()
        cursor.close()
        cnx.close()
        return """ 
        <script>
            alert("Detalle editado exitosamente");
            window.location.href = "/detail";  
        </script>
        """
    else:
        cnx = mysql.connector.connect(**config)
        cursor = cnx.cursor()
        select_query = "SELECT * FROM detalleventa WHERE DetalleVentaID = %s"
        cursor.execute(select_query, (id,))
        detail = cursor.fetchone()
        cnx.close()
        return render_template('editardetalles.html', detail=detail)

@app.route('/detail/<int:id>/eliminar', methods=['POST'])
def eliminar_detalles(id):
    cnx = mysql.connector.connect(**config)
    cursor = cnx.cursor()
    cursor.execute('DELETE FROM detalleventa WHERE DetalleVentaID = %s', (id,))
    cnx.commit()
    cursor.close()
    cnx.close()
    return redirect(url_for('detail'))


if __name__ == '__main__':
    app.run(debug=True, port=4000)