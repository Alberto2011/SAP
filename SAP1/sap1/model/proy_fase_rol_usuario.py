from sqlalchemy import *
from sqlalchemy.orm import mapper
from sap1.model import metadata
from sap1.model.rol import Rol
from sap1.model.proyecto import Proyecto
from sap1.model.fase import Fase
from sap1.model.usuario import Usuario

# Database table definition

tabla_proy_fase_rol_usuario = Table("Proy_Fase_Rol_Usuario", metadata,
    Column("id", Integer, primary_key=True),
    Column("idProyecto", Integer, ForeignKey("Proyecto.id")),
    Column("idFase", Integer, ForeignKey("Fase.id")),
    Column("idRol", Integer, ForeignKey("Rol.id")),
    Column("idUsuario", Integer, ForeignKey("Usuario.id")),

)

# Python class definition
class ProyFaseRolUsuario(object):
    def __init__(self, idProyecto, idFase, idRol, idUsuario):
       self.idProyecto = idProyecto
       self.idFase = idFase
       self.idRol = idRol
       self.idUsuario = idUsuario


# Mapper
mapper_proy_fase_rol_usuario = mapper(ProyFaseRolUsuario, tabla_proy_fase_rol_usuario)
