class Usuario:
    id=None
    NombreUsuario=None
    Passwd=None
    NombreCompleto=None
    Estatus=None
    Tipo=None

    def setId(self, id):
        self.id=id
    def getId(self):
        return self.id

    def setNombreUsuario(self, NombreUsuario):
        self.NombreUsuario=NombreUsuario
    def getNombreUsuario(self):
        return self.NombreUsuario

    def setPasswd(self, Passwd):
        self.Passwd=Passwd
    def getPasswd(self):
        return self.Passwd

    def setNombreCompleto(self, NombreCompleto):
        self.NombreCompleto=NombreCompleto
    def getNombreCompleto(self):
        return self.NombreCompleto

    def setEstatus(self, Estatus):
        self.Estatus=Estatus
    def getEstatus(self):
        return self.Estatus

    def setTipo(self, Tipo):
        self.Tipo=Tipo
    def getTipo(self):
        return self.Tipo