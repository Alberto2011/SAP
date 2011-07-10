# -*- coding: utf-8 -*-
""" Clase RootController
@author José Chavéz.
@author Alberto Capli.
@author Nora González.
"""

from sqlalchemy import *
from sqlalchemy.orm import mapper
from sap.model import metadata
from datetime import datetime

# Database table definition

tabla_proyecto = Table("Proyecto", metadata,
    Column("id", Integer, primary_key=True),
    Column("nombre", Text, unique=True,nullable=False),
    Column("descripcion", Text,nullable=True ),
    Column("fechaCreacion", Date, default=datetime.now),
    Column("liderProyecto", Text, nullable=False),
    Column("nrofase", Integer, nullable=True),
    Column("estado", Text, nullable=True)
		

)

# Python class definition
class Proyecto(object):
    def __init__(self, nombre= " " , descripcion=" ",fechaCreacion= " ", liderProyecto=" ", nrofase= 0, estado ="nuevo"):
       self.nombre = nombre
       self.descripcion = descripcion
       #self.fechaCreacion = fechaCreacion
       self.liderProyecto = liderProyecto
       self.nrofase = nrofase
       self.estado = estado


# Mapper
mapper_proyecto = mapper(Proyecto, tabla_proyecto)
