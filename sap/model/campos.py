from sqlalchemy import *
from sqlalchemy.orm import mapper
from sap.model import metadata
from sap.model.tipodeitem import TipoDeItem

# Database table definition

tabla_campos = Table("Campos", metadata,
    Column("id", Integer, primary_key=True),
    Column("idTipoDeItem", Integer, ForeignKey("TipoDeItem.id",onupdate="CASCADE", ondelete="CASCADE")),
    Column("nombre", Text),
    Column("tipoDeDato", Text),

)

# Python class definition
class Campos(object):
    def __init__(self, idTipoDeItem= 0, nombre="", tipoDeDato=""):
    #def __init__(self,  nombre=" ", tipoDeDato=" "):    
       self.idTipoDeItem = idTipoDeItem
       self.nombre = nombre
       self.tipoDeDato = tipoDeDato


# Mapper
mapper_campos = mapper(Campos, tabla_campos)
