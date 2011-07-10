# -*- coding: utf-8 -*-
""" Clase RootController
@author José Chavéz.
@author Alberto Capli.
@author Nora González.
"""

from sqlalchemy import *
from sqlalchemy.orm import mapper
from sap.model import metadata
from sap.model.proyecto import Proyecto
from sap.model.fase import Fase
from sap.model.usuario import Usuario
from sap.model.auth import User
from sap.model.auth import Permission

# Database table definition

tabla_proy_fase_usuario = Table("ProyFaseUsuario", metadata,
    Column("idProyecto", Integer, ForeignKey("Proyecto.id", 
        onupdate="CASCADE", ondelete="CASCADE"), primary_key=True),
    Column("idFase", Integer, ForeignKey("Fase.id",
        onupdate="CASCADE", ondelete="CASCADE"), primary_key=True),
    Column("iduser", Integer, ForeignKey("tg_user.user_id",
       onupdate="CASCADE", ondelete="CASCADE"), primary_key=True),
    Column("idPermiso", Integer, ForeignKey("tg_permission.permission_id",
       onupdate="CASCADE", ondelete="CASCADE"), primary_key=True)
                                

)




# Python class definition
class ProyFaseUsuario(object):
    def __init__(self, idProyecto=0, idFase=0,iduser=0):
       self.idProyecto = idProyecto
       self.idFase = idFase
       self.iduser = iduser
       


# Mapper
mapper_proy_fase_usuario = mapper(ProyFaseUsuario, tabla_proy_fase_usuario)
