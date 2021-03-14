import mysql

from Datos.Conexion import Conexion
from Modelo.Producto import Producto


class ProductoDAO():
    db=None

    def __init__(self):
        cn = Conexion()
        self.db = cn.getDB()

    def consultaProductos(self):
        sql="select *from Productos"

        lista=[]
        try:
            cursor=self.db.cursor()
            cursor.execute(sql)
            rs=cursor.fetchall()

            for reg in rs:
                p=Producto(reg[0], reg[1], reg[2],reg[7], reg[8], reg[9])
                lista.append(p)
                cursor.close()
                self.db.close()
        except mysql.connector.Error as p:
            print(lista)
        return lista

    def consultaIndividual(self,codigo):
        sql="select Codigo from Productos where Codigo=%s"
        a=None

        try:
            cursor=self.db.cursor()
            cursor.execute(sql,(codigo))
            rs=cursor.fetchone()
            a=Producto(rs[1])
            cursor.close()
            self.db.close()

        except mysql.connector.Error as a:
            print(a)
        return a