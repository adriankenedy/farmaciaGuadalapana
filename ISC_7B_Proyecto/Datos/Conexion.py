import mysql.connector

class Conexion:
    db=None

    def __init__(self):
        self.db=mysql.connector.connect(host='localhost', user='root', password='yangars', db='Farmacia')

    def getDB(self):
        return self.db

    def cerrar(self):
        self.db.close()
