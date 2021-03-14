class Producto:
    idP=None
    codigo=None
    descripcion=None
   # nombreP=None
    #ingredienteActivo=None
    #dosis=None
    #fechaCaducidad=None
    precioVenta=None
    precioCompra=None
    existencia=None

    def __init__(self,idP,codigo,descripcion,precioVenta,precioCompra,existencia):
        self.idP=idP
        self.codigo=codigo
        self.descripcion=descripcion
       # self.nombreP=nombreP
      #  self.ingredienteActivo=ingredienteActivo
       # self.dosis=dosis
        #self.fechaCaducidad=fechaCaducidad
        self.precioVenta=precioVenta
        self.precioCompra=precioCompra
        self.existencia=existencia