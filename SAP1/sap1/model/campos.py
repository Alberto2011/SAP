from sqlalchemy import *
from sqlalchemy.orm import mapper
from sap1.model import metadata
from sap1.model.tipo_de_item import TipoDeItem

# Database table definition

tabla_campos = Table("Campos", metadata,
    Column("id", Integer, primary_key=True),
    Column("idTipoDeItem", Integer, ForeignKey("Tipo_De_Item.id")),
    Column("nombre", Text),
    Column("tipoDeDato", Text),

)

# Python class definition
class Campos(object):
    def __init__(self, idTipoDeItem, nombre, tipoDeDato):
       self.idTipoDeItem = idTipoDeItem
       self.nombre = nombre
       self.tipoDeDato = tipoDeDato


# Mapper
mapper_campos = mapper(Campos, tabla_campos)
