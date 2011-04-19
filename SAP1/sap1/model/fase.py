from sqlalchemy import *
from sqlalchemy.orm import mapper
from sap1.model import metadata

# Database table definition

tabla_fase = Table("Fase", metadata,
    Column("id", Integer, primary_key=True),
    Column("nombre", Text, unique=True),
    Column("descripcion", Text),

)

# Python class definition
class Fase(object):
    def __init__(self, nombre, descripcion):
       self.nombre = nombre
       self.descripcion = descripcion

# Mapper
mapper_fase = mapper(Fase, tabla_fase)

