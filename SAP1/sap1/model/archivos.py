from sqlalchemy import *
from sqlalchemy.orm import mapper
from sap1.model import metadata
from sap1.model.item import Item

# Database table definition

tabla_archivos = Table("Archivos", metadata,
    Column("id", Integer, primary_key=True),
    Column("idItem", Integer, ForeignKey("Item.id")),
    Column("nombreArchivo", Text),
    Column("direccion", Text),

)

# Python class definition
class Archivos(object):
    def __init__(self, idItem, nombreArchivo, direccion):
       self.idItem = idItem
       self.nombreArchivo = nombreArchivo
       self.direccion = direccion

# Mapper
mapper_archivos = mapper(Archivos, tabla_archivos)
