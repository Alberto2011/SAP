from sqlalchemy import *
from sqlalchemy.orm import mapper
from sap1.model import metadata
from sap1.model.tipo_de_item import TipoDeItem
from sap1.model.fase import Fase

# Database table definition

tabla_item = Table("Item", metadata,
    Column("id", Integer, primary_key=True),
    Column("idTipoDeItem", Integer, ForeignKey("Tipo_De_Item.id")),
    Column("idFase", Integer, ForeignKey("Fase.id")),
    Column("version", Integer),
    Column("estado", Integer),
    Column("complejidad", Integer),
    Column("fechaCreacion", Date),

)

# Python class definition
class Item(object):
    def __init__(self, idTipoDeItem, idFase, version, estado, complejidad, fechaCreacion):
       self.idTipoDeItem = idTipoDeItem
       self.idFase = idFase
       self.version = version
       self.estado = estado
       self.complejidad = complejidad
       self.fechaCreacion = fechaCreacion


# Mapper
mapper_item = mapper(Item, tabla_item)
