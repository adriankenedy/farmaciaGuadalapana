from Datos.Conexion import Conexion
from Modelo.Usuario import Usuario
import mysql

class UsuarioDAO():
    db=None

    def __init__(self):
        cn=Conexion()
        self.db=cn.getDB()

    def validar(self,nombreUsuario, Password):
        sql="select idUsuario, NombreUsuario, Passwd, NombreCompleto, Estatus, Tipo from Usuarios where NombreUsuario=%s "\
        "and Passwd=%s and Estatus='1' "

        try:
            cursor = self.db.cursor()
            cursor.execute(sql, (nombreUsuario, Password, ))
            rs=cursor.fetchone()
            u={"id":rs[0],"NombreUsuario":rs[1],"Passwd":rs[2],"NombreCompleto":rs[3],
               "Estatus":rs[4],"Tipo":rs[5]}

            cursor.close()
            self.db.close()

        except(ValueError):
                 print("Error al ejecutar la consola "+ ValueError)
        return u

    def insertar(self, usuario):
        usuario=Usuario()
        sql="insert into Usuarios values(%s,%s,%s,%s,%s,%s)"
        ban=False
        try:
            cursor=self.db.cursor()
            cursor.execute(sql,(usuario.getId(),
                                usuario.getNombreUsuario(),
                                usuario.getPasswd(),
                                usuario.getNombreCompleto(),
                                usuario.getEstatus(),
                                usuario.getTipo(),))
            cursor.close()
            self.db.commit()
            self.db.close()
            ban=True
        except(ValueError):
            print('Error al ejecutar la consosla')
        return ban



    def agregar(self, usuario):
        try:
            salida=None
            cursor=self.db.cursor()
            salida=cursor.callproc('sp_agregarUsuario', (
                                                         usuario.NombreUsuario,
                                                         usuario.Passwd,
                                                         usuario.NombreCompleto,salida))
            cursor.close()
            self.db.close()
            print(salida)
            return salida[3]
        except mysql.connector.Error as e:
            print(e)
        return 'Error'

    def actualizar(self,usuario):
        sql = "update Usuarios set NombreUsuario=%s, Passwd=%s, " \
              "NombreCompleto=%s, Estatus=%s, Tipo=%s where idUsuario=%s"
        ban = False
        try:
            cursor = self.db.cursor()
            cursor.execute(sql, (usuario.getNombreUsuario(),
                                 usuario.getPasswd(),
                                 usuario.getNombreCompleto(),
                                 usuario.getEstatus(),
                                 usuario.getTipo(),
                                 usuario.getId(),))
            cursor.close()
            self.db.commit()
            self.db.close()
            ban = True
        except:
            print('Error al actualizar usuario')
        return ban

    def consultar(self,id):
        sql = "select idUsuario, NombreUsuario, Passwd, NombreCompleto, Estatus, Tipo from Usuarios where idUsuario=%s"
        u=None
      #  try:
        cursor = self.db.cursor()
        cursor.execute(sql, (id,))
        rs = cursor.fetchone()
        u = {"id": rs[0], "NombreUsuario": rs[1], "Passwd": rs[2], "NombreCompleto": rs[3], "Estatus": rs[4], "Tipo": rs[5]}
        cursor.close()
        self.db.close()

       # except:
         #   print("Error al ejecutar la consulta")
        return u












