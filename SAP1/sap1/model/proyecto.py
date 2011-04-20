from sqlalchemy import *
from sqlalchemy.orm import mapper
from sap1.model import metadata

# Database table definition

tabla_proyecto = Table("Proyecto", metadata,
    Column("id", Integer, primary_key=True),
    Column("nombre", Text, unique=True),
    Column("descripcion", Text),
    Column("fechaCreacion", Date),	

)

# Python class definition
class Proyecto(object):
    def __init__(self, nombre,descripcion,fechaCreacion):
       self.nombre = nombre
       self.descripcion = descripcion
       self.fechaCreacion = fechaCreacion


# Mapper
mapper_proyecto = mapper(Proyecto, tabla_proyecto)
