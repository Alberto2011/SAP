from sqlalchemy import *
from sqlalchemy.orm import mapper
from sap.model import metadata
from sap.model.tipodeitem import TipoDeItem
from sap.model.fase import Fase
from sap.model.lineabase import LineaBase

# Database table definition

tabla_historialitem = Table("HistorialItem", metadata,
    Column("id", Integer, primary_key=True),
    Column("idItem", Integer,),
    Column("nombre", Text,unique=False),
    Column("idTipoDeItem", Integer, ForeignKey("TipoDeItem.id",onupdate="CASCADE", ondelete="CASCADE")),
    Column("idFase", Integer, ForeignKey("Fase.id",onupdate="CASCADE", ondelete="CASCADE")),
    Column("idLineaBase", Integer,ForeignKey("LineaBase.id",onupdate="CASCADE", ondelete="CASCADE"),nullable=True),
    Column("version", Integer),
    Column("estado", Text),
    Column("complejidad", Integer),
    Column("fechaCreacion", Date),

)

# Python class definition
class HistorialItem(object):
    def __init__(self,nombre=" ", idTipoDeItem= 0,idLineaBase=0, idFase= 0, version= 0, estado="nuevo", complejidad= 0, fechaCreacion=" "):
    #def __init__(self,nombre=" ", idFase= 0, version= 0, estado="nuevo", complejidad= 0, fechaCreacion=" "):
       self.nombre = nombre 
       self.idTipoDeItem = idTipoDeItem
       self.idFase = idFase
       self.idLineaBase=idLineaBase
       self.version = version
       self.estado = estado
       self.complejidad = complejidad
       self.fechaCreacion = fechaCreacion


# Mapper
mapper_historialitem = mapper(HistorialItem, tabla_historialitem)
