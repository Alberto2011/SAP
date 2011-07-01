from sqlalchemy import *
from sqlalchemy.orm import mapper
from sap.model import metadata
#from sap.model.item import Item
from sap.model.fase import Fase
from datetime import datetime

# Database table definition

tabla_linea_base = Table("LineaBase", metadata,
    Column("nombre", Text),
    Column("id", Integer, primary_key=True),
    Column("idFase", Integer, ForeignKey("Fase.id",onupdate="CASCADE", ondelete="CASCADE")),
    Column("estado", Text),
    Column("fechaCreacion", Date, default=datetime.now),
    

)

# Python class definition
class LineaBase(object):
    def __init__(self,nombre="",idFase=0, estado="cerrada", fechaCreacion=" "):
       self.nombre = nombre
       self.idFase = idFase
       #self.idItem = idItem
       self.estado = estado
       #self.fechaCreacion = fechaCreacion

# Mapper
mapper_archivos = mapper(LineaBase, tabla_linea_base)
