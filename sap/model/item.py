from sqlalchemy import *
from sqlalchemy.orm import mapper
from sap.model import metadata
from sap.model.tipodeitem import TipoDeItem
from sap.model.fase import Fase
from sap.model.lineabase import LineaBase

from sap.model import DeclarativeBase, metadata, DBSession
from sqlalchemy import *
from sqlalchemy.orm import *
from sqlalchemy.types import *
from sqlalchemy.ext.declarative import declarative_base



__all__ = [ 'Item' ]

Base = declarative_base()

class Item(DeclarativeBase):
    __tablename__ = 'Item'

    id = Column(Integer, primary_key=True)
    nombre = Column(Unicode, nullable=False)
    idTipoDeItem=Column(Integer, ForeignKey("TipoDeItem.id"))
    idFase=Column(Integer, ForeignKey("Fase.id"))
    idLineaBase=Column(Integer,ForeignKey("LineaBase.id"))
    version=Column(Integer,default=0)
    estado=Column(Text, default='nuevo')
    complejidad=Column(Integer,default=0,nullable=False)
    fechaCreacion=Column(Date)
    nrohistorial=Column(Integer,default=0)
    ultimaversion=Column(Integer,default=1)
    







