from sqlalchemy import *
from sqlalchemy.orm import mapper
from sap1.model import metadata

# Database table definition

tabla_permiso = Table("Permiso", metadata,
    Column("id", Integer, primary_key=True),
    Column("nombre", Text, unique=True),

)

# Python class definition
class Permiso(object):
    def __init__(self, nombre):
       self.nombre = nombre


# Mapper
mapper_permiso = mapper(Permiso, tabla_permiso)

