from sqlalchemy import *
from sqlalchemy.orm import mapper
from sap1.model import metadata

# Database table definition

tabla_tipo_de_item = Table("Tipo_De_Item", metadata,
    Column("id", Integer, primary_key=True),
    Column("nombre", Text),
    Column("descripcion", Text),
    Column("nom_fase", Text),

)

# Python class definition
class TipoDeItem(object):
    def __init__(self, nombre,descripcion,nom_fase):
       self.nombre = nombre
       self.descripcion = descripcion
       self.nom_fase = nom_fase


# Mapper
mapper_tipo_de_item = mapper(TipoDeItem, tabla_tipo_de_item)
