from sqlalchemy import *
from sqlalchemy.orm import mapper
from sap1.model import metadata

# Database table definition

tabla_rol = Table("Rol", metadata,
    Column("id", Integer, primary_key=True),
    Column("nombre", Text),
    Column("descripcion", Text),

)

# Python class definition
class Rol(object):
    def __init__(self, nombre, descripcion):
       self.nombre = nombre
       self.descripcion = descripcion


# Mapper
mapper_rol = mapper(Rol, tabla_rol)
