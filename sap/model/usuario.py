from sqlalchemy import *
from sqlalchemy.orm import mapper
from sap.model import metadata

# Database table definition

tabla_usuario = Table("Usuario", metadata,
    Column("id", Integer, primary_key=True),
    Column("nombre", Text),
    Column("apellido", Text),
    Column("ci", Integer),
    Column("direccion", Text),
    Column("telefono", Text),

)

# Python class definition
class Usuario(object):
    def __init__(self, nombre= " " ,apellido="  ", ci=0,direccion=" ",telefono=" "):
       self.nombre = nombre
       self.apellido = apellido
       self.ci = ci
       self.direccion = direccion
       self.telefono = telefono


# Mapper
mapper_usuario = mapper(Usuario, tabla_usuario)
