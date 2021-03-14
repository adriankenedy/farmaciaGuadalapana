from flask import Flask, render_template, request, url_for, flash, session
from Datos.productoDAO import ProductoDAO
from Datos.usuarioDAO import UsuarioDAO
from flask_mysqldb import MySQL

from Modelo.Producto import Producto
from Modelo.Usuario import Usuario
import json

app = Flask(__name__)
app.secret_key=b'yangars'

app.config['MYSQL_HOST']='localhost'
app.config['MYSQL_USER']='root'
app.config['MYSQL_PASSWORD']='yangars'
app.config['MYSQL_DB']='Farmacia'
mysql=MySQL(app)



#Direcciona a la pagina de login
@app.route('/')
def index():
    return render_template('Farmacia.html')




#Acceso al Sistema
@app.route('/login', methods=['POST'])
def login():
    try:
        udao=UsuarioDAO()
        nombreUsuario=request.form['Usuario']
        passwd=request.form['Contraseña']
        u=udao.validar(nombreUsuario,passwd)
        if u['id']!=None:
            session['user']= u
            return render_template('Comunes/MenuInicio.html', user=session.get('user'))
        else:
            return render_template('Farmacia.html')
    except:
        return 'NO HAY REGISTRO DE UN USUARIO'



#lista los productos en la ventana Productos
@app.route('/Productos')
def listarProductos():
    cur=mysql.connection.cursor()
    cur.execute('select idP,Codigo,Descripcion,PrecioCompra,PrecioVenta,Existencia from Productos')
    data=cur.fetchall()
    return render_template('Productos/Productos.html', productos=data)


#Direcciona a la pagina de registrar usuario
@app.route('/Usuario')
def usuario():
    return render_template('Usuarios/registrarUsuario.html')




 #Creacion de nuevo usuario
@app.route('/insertarUsuario', methods=['POST'])
def agregarUsuario():
    if request.method == 'POST':
        nombreUser=request.form['NombreUsuario']
        passwd=request.form['Contraseña']
        nombreComp=request.form['NombreCompleto']
        estatus=request.form['Estatus']
        tipo=request.form['Tipo']
        cur = mysql.connection.cursor()
        cur.execute('INSERT INTO Usuarios (NombreUsuario, Passwd, NombreCompleto, Estatus, Tipo) VALUES (%s, %s, %s, %s, %s)',
                    (nombreUser,passwd,nombreComp,estatus,tipo))
        mysql.connection.commit()
        return render_template('Farmacia.html')




#Direcciona a la pagina nuevo producto para crear nuevo producto
@app.route('/nuevoProducto')
def nuevoProducto():
    return render_template('Productos/NuevoProducto.html')




#Creacion de un nuevo producto
@app.route('/insertarProducto', methods=['POST'])
def añadirProducto():
    if request.method == 'POST':
        codigoProducto=request.form['codigo']
        descripcion=request.form['descripcion']
        nombreProducto=request.form['nombreProducto']
        ingredienteActivo=request.form['ingredienteActivo']
        dosis=request.form['dosis']
        fechaCaducidad=request.form['fechaCaducidad']
        precioVenta=request.form['precioVenta']
        precioCompra=request.form['precioCompra']
        existencias=request.form['existencias']
        cur=mysql.connection.cursor()
        cur.execute('INSERT INTO Productos (Codigo, Descripcion, NombreP, IngredienteActivo, Dosis, FechaCaducidad, PrecioVenta, PrecioCompra, Existencia) '
                    'VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)',
                    (codigoProducto,descripcion,nombreProducto,ingredienteActivo,dosis,fechaCaducidad, precioVenta, precioCompra, existencias))
        mysql.connection.commit()
        return render_template('Productos/Productos.html')




#Direcciona a la pagina de productos
@app.route('/Productos')
def productos():
    return render_template('Productos/Productos.html', user=session.get('user'))



"""
#lista los productos en la ventana Productos
@app.route('/listarProductos')
def listarProductos():
    cur=mysql.connection.cursor()
    cur.execute('select idP,Codigo,Descripcion,PrecioCompra,PrecioVenta,Existencia from Productos')
    data=cur.fetchall()
    return render_template('Productos/Productos.html', productos=data)
"""



#Elimina un registro de los productos
@app.route('/eliminarProducto/<string:id>')
def eliminarProducto(id):
    cur=mysql.connection.cursor()
    cur.execute('Delete from Productos where idP={0}'.format(id))
    mysql.connection.commit()
    return render_template('Productos/Productos.html')




#toma el registro para editar un producto de productos
@app.route('/editarProducto/<id>')
def editarProducto(id):
    cur=mysql.connection.cursor()
    cur.execute('select Codigo,Descripcion,NombreP,IngredienteActivo,Dosis,FechaCaducidad,PrecioVenta,PrecioCompra,Existencia from Productos where idP={0}'.format(id))
    data=cur.fetchall()
    return render_template('Productos/editarProducto.html', producto=data[0])




#editar/actualizar registro de la tabla de productos
@app.route('/actualizarProducto/<id>', methods=['POST'])
def actualizarProducto(id):
    if request.method == 'POST':
        codigo=request.form['codigo']
        descripcion=request.form['descripcion']
        nombreP=request.form['nombreProducto']
        ingredienteA=request.form['ingredienteActivo']
        dosis=request.form['dosis']
        fechaCaducidad=request.form['fechaCaducidad']
        precioVenta=request.form['precioVenta']
        precioCompra=request.form['precioCompra']
        existencia=request.form['existencias']
    cur=mysql.connection.cursor()
    cur.execute('Update Productos set Codigo=%s,'
                'Descripcion=%s,'
                'NombreP=%s,'
                'IngredienteActivo=%s,'
                'Dosis=%s,'
                'FechaCaducidad=%s,'
                'PrecioVenta=%s,'
                'PrecioCompra=%s,'
                'Existencia=%s'
                'where idP=%s',(codigo,descripcion,nombreP,ingredienteA,dosis,fechaCaducidad,precioVenta,precioCompra,existencia,id))
    mysql.connection.commit()
    print('Contacto Actualizado')
    return render_template('Productos/Productos.html')




#lista los usuarios en la ventana usuarios
@app.route('/listaUsuarios')
def listarUsuarios():
    cur=mysql.connection.cursor()
    cur.execute('select idUsuario, NombreUsuario, NombreCompleto, Tipo from Usuarios')
    data=cur.fetchall()
    return render_template('Usuarios/ListaUsuarios.html', usuarios=data)




#editar usuario
@app.route('/actualizarUsuario')
def actualizarUsuario():
    return render_template('Usuarios/modificarUsuario.html', user=session.get('user'))




#actualizar usuario
@app.route('/modificarUsuario', methods=['POST'])
def guardarPerfil():
    usuario = Usuario()
    usuario.setId(request.form['id'])
    usuario.setNombreUsuario(request.form['NombreUsuario'])
    usuario.setPasswd(request.form['Contraseña'])
    usuario.setNombreCompleto(request.form['NombreCompleto'])
    usuario.setEstatus(request.form['Estatus'])
    usuario.setTipo(request.form['Tipo'])
    udao=UsuarioDAO()
    ban=udao.actualizar(usuario)
    if ban==True:
        udao = UsuarioDAO()
        session['user'] = udao.consultar(usuario.getId())
    return render_template('Comunes/MenuInicio.html', user=session.get('user'))




#Eliminar algun usuario de la BD
@app.route('/eliminarUsuario/<string:id>')
def eliminarUsuario(id):
    cur=mysql.connection.cursor()
    cur.execute('Delete from Usuarios where idUsuario={0}'.format(id))
    mysql.connection.commit()
    return render_template('Usuarios/ListaUsuarios.html')




#MUESTRA LAS VENTAS QUE SE AÑADIRAN AL CARRITO
@app.route('/seleccionVenta', methods=['POST'])
def listaVentas():
    codigo=request.form['codigoBarras']
    cur = mysql.connection.cursor()
    cur.execute('select idP,Codigo,NombreP,PrecioVenta,PrecioCompra from Productos where Codigo={0}'.format(codigo))
    data = cur.fetchall()
    return render_template('Ventas/Crear_Venta.html', ventas=data)




#Añade un producto al carrito
@app.route('/añadirVenta/<id>')
def añadirVenta(id):
    cur=mysql.connection.cursor()
    cur.execute('insert into ventas(nombreProducto,Total,idUser) select p.NombreP, p.PrecioVenta, u.idUsuario from Productos p join Usuarios u where idP={0}'.format(id))
    mysql.connection.commit()
    return render_template('Ventas/Crear_Venta.html')




#Muestra la lista de registros del carro
@app.route('/listarCarrito')
def listarCarro():
    cur=mysql.connection.cursor()
    cur.execute('select idV, nombreProducto, Fecha, Total from Ventas ')
    data=cur.fetchall()
    return render_template('Ventas/Crear_Venta.html', carro=data)




#Elimina algun registro del carro
@app.route('/eliminarCarro/<string:id>')
def eliminarCarrito(id):
    cur=mysql.connection.cursor()
    cur.execute('Delete from Ventas where idV={0}'.format(id))
    mysql.connection.commit()
    return render_template('Ventas/Crear_Venta.html')




#Inserta los registros generados y le suma los que se añan comprado
@app.route('/guardarCarro', methods=['POST'])
def guardarCarro():
    carro=request.form['carro']
    cur = mysql.connection.cursor()
    cur.execute('insert into Productos_Vendidos(idVenta, NombreProducto,Fecha,Total) select v.idV, v.nombreProducto, v.Fecha, v.Total from Ventas v'.format(carro))
    mysql.connection.commit()
    data = cur.fetchall()
    return render_template('CorteCaja/ListaVentas.html', carro=data)




#Muestra los registros de las ventas generadas
@app.route('/corteCaja')
def listarCorte():
   # carro=request.form['corte']
    cur = mysql.connection.cursor()
    cur.execute('Select idVenta, NombreProducto, Fecha, sum(Total)Total_Calculado from Productos_Vendidos')
    mysql.connection.commit()
    data = cur.fetchall()
    return render_template('CorteCaja/ListaVentas.html', cortes=data)




#Elimina un registro de las ventas generadas
@app.route('/eliminarCorte/<string:id>')
def eliminarCorte(id):
    cur=mysql.connection.cursor()
    cur.execute('Delete from Productos_Vendidos'.format(id))
    mysql.connection.commit()
    return render_template('CorteCaja/ListaVentas.html')



#>>>>>DIRECCIONAMIENTO DE PAGINAS<<<<<

#Direcciona a la pantalla del carro
@app.route('/carrito')
def carrito():
    return render_template('Ventas/Carrito.html')

#Direcciona a la pagina crear venta
@app.route('/venta')
def venta():
    return render_template('Ventas/Crear_Venta.html')

#Direcciona a la pagina de corte de caja
@app.route('/corteCaja')
def corteCaja():
    return render_template('CorteCaja/ListaVentas.html')

#Direcciona a la pagina de Historial de ventas
@app.route('/historialVentas')
def historialVenatas():
    return render_template('HistorialVentas/Consultar_Ganancias.html')

#Direcciona a la pagina editar usuario
@app.route('/editarUsuario')
def editarUser():
    return render_template('Usuarios/modificarUsuario.html')

#Direcciona a la pagina Principal del programa
@app.route('/mandarInicio')
def mandarInicio():
    return render_template('Comunes/MenuInicio.html', user=session.get('user'))

#Direcciona a la pagina de usuarios
@app.route('/listaUsuarios')
def listaUsuarios():
    return render_template('Usuarios/ListaUsuarios.html')

 #Cierra sesion del sistema
@app.route('/cerrarSesion')
def cerrarSesion():
    return render_template('Farmacia.html')

#<<<<<DIRECCIONAMIENTO DE PAGINAS>>>>>>

if __name__ == '__main__':
    app.run(debug=True)
