from sqlalchemy import *
from sqlalchemy.orm import mapper
from sap.model import metadata
from sap.model.rol import Rol
from sap.model.permiso import Permiso

# Database table definition

tabla_permiso_rol = Table("Permiso_Rol", metadata,
    Column("idPermiso", Integer, ForeignKey("Permiso.id",onupdate="CASCADE", ondelete="CASCADE"), primary_key=True),
    Column("idRol", Integer, ForeignKey("Rol.id",onupdate="CASCADE", ondelete="CASCADE"), primary_key=True),

)

# Python class definition
class PermisoRol(object):
    def __init__(self, idPermiso, idRol):
       self.idPermiso = idPermiso
       self.idPermiso = idRol


# Mapper
mapper_permiso_rol = mapper(PermisoRol, tabla_permiso_rol)
