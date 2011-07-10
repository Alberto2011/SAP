# -*- coding: utf-8 -*-
""" Clase RootController
@author José Chavéz.
@author Alberto Capli.
@author Nora González.
"""

from sqlalchemy import *
from sqlalchemy.orm import mapper
from sap.model import metadata

# Database table definition

tabla_tipodeitem = Table("TipoDeItem", metadata,
    Column("id", Integer, primary_key=True),
    Column("idFase", Integer, ForeignKey("Fase.id",onupdate="CASCADE", ondelete="CASCADE")),
    Column("nombre", Text),
    Column("descripcion", Text),
    Column("nrogeneracion", Integer),
    
    #Column("nom_fase", Text),

)

# Python class definition
class TipoDeItem(object):
    def __init__(self,idFase=0, nombre=" ",descripcion=" ",nom_fase=" ", nrogeneracion=0 ):
       self.idFase = idFase
       self.nombre = nombre
       self.descripcion = descripcion
       self.nrogeneracion=nrogeneracion
       #self.nom_fase = nom_fase


# Mapper
mapper_tipo_de_item = mapper(TipoDeItem, tabla_tipodeitem)
