from sqlalchemy import *
from sqlalchemy.orm import mapper
from sap1.model import metadata

# Database table definition

tabla_usuario = Table("Usuario", metadata,
    Column("id", Integer, primary_key=True),
    Column("nombre", Text),
    Column("apellido", Text),
    Column("ci", Integer, unique=True),
    Column("direccion", Text),
    Column("telefono", Text),	

)

# Python class definition
class Usuario(object):
    def __init__(self, nombre,apellido,ci,direccion,telefono):
       self.nombre = nombre
       self.apellido = apellido
       self.ci = ci
       self.direccion = direccion
       self.telefono = telefono


# Mapper
mapper_usuario = mapper(Usuario, tabla_usuario)
