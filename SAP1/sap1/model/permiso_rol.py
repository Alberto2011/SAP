from sqlalchemy import *
from sqlalchemy.orm import mapper
from sap1.model import metadata
from sap1.model.rol import Rol
from sap1.model.permiso import Permiso

# Database table definition

tabla_permiso_rol = Table("Permiso_Rol", metadata,
    Column("idPermiso", Integer, ForeignKey("Permiso.id"), primary_key=True),
    Column("idRol", Integer, ForeignKey("Rol.id"), primary_key=True),

)

# Python class definition
class PermisoRol(object):
    def __init__(self, idPermiso, idRol):
       self.idPermiso = idPermiso
       self.idPermiso = idRol


# Mapper
mapper_permiso = mapper(PermisoRol, tabla_permiso_rol) #properties={
#    'permiso': relationship(Permiso), 'rol': relationship(Rol)
#})

