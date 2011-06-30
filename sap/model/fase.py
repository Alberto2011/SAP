from sqlalchemy import *
from sqlalchemy.orm import mapper
from sap.model import metadata

# Database table definition

tabla_fase = Table("Fase", metadata,
    Column("id", Integer, primary_key=True),
    Column("idproyec", Integer, ForeignKey("Proyecto.id",
        onupdate="CASCADE", ondelete="CASCADE")),
    Column("nombre", Text, unique=False),
    Column("descripcion", Text),
    Column("estado", Text),

)

# Python class definition
class Fase(object):
    def __init__(self, nombre=" ", descripcion=" ", estado="inicial"):
       self.nombre = nombre
       self.descripcion = descripcion
       self.estado = estado

# Mapper
mapper_fase = mapper(Fase, tabla_fase)

