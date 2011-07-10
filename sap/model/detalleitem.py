# -*- coding: utf-8 -*-
""" Clase RootController
@author José Chavéz.
@author Alberto Capli.
@author Nora González.
"""

from sqlalchemy import *
from sqlalchemy.orm import mapper
from sap.model import metadata
from sap.model import Item

# Database table definition

tabla_detalleitem = Table("DetalleItem", metadata,
    Column("id", Integer, primary_key=True),
    Column("tipo", Text,nullable=True),
    Column("nombrecampo", Text,nullable=True ),
    Column("valor", Text, nullable=True),
    Column("iditem", Integer, ForeignKey("Item.id", onupdate="CASCADE", ondelete="CASCADE")),
        

)

# Python class definition
class DetalleItem(object):
    def __init__(self, tipo= " " , nombrecampo=" ",valor= " ", iditem=0):
       self.tipo = tipo
       self.nombrecampo = nombrecampo
       self.valor = valor
       self.iditem = iditem
       

# Mapper
mapper_detalleitem = mapper(DetalleItem, tabla_detalleitem)
