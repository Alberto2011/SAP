from sqlalchemy import *
from sqlalchemy.orm import mapper
from sap1.model import metadata
from sap1.model.item import Item
from sap1.model.fase import Fase

# Database table definition

tabla_linea_base = Table("Linea_Base", metadata,
    Column("id", Integer, primary_key=True),
    Column("idFase", Integer, ForeignKey("Fase.id")),
    Column("idItem", Integer, ForeignKey("Item.id")),
    Column("estado", Integer),
    Column("fechaCreacion", Date),

)

# Python class definition
class LineaBase(object):
    def __init__(self, idFase, idItem, estado, fechaCreacion):
       self.idFase = idFase
       self.idItem = idItem
       self.estado = estado
       self.fechaCreacion = fechaCreacion

# Mapper
mapper_archivos = mapper(LineaBase, tabla_linea_base)
