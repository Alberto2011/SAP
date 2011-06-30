from sqlalchemy import *
from sqlalchemy.orm import mapper
from sap.model import metadata

# Database table definition

tabla_tipodeitem = Table("TipoDeItem", metadata,
    Column("id", Integer, primary_key=True),
    Column("idFase", Integer, ForeignKey("Fase.id",onupdate="CASCADE", ondelete="CASCADE")),
    Column("nombre", Text),
    Column("descripcion", Text),
    #Column("nom_fase", Text),

)

# Python class definition
class TipoDeItem(object):
    def __init__(self,idFase=0, nombre=" ",descripcion=" ",nom_fase=" "):
       self.idFase = idFase
       self.nombre = nombre
       self.descripcion = descripcion
       #self.nom_fase = nom_fase


# Mapper
mapper_tipo_de_item = mapper(TipoDeItem, tabla_tipodeitem)
