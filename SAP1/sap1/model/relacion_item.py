from sqlalchemy import *
from sqlalchemy.orm import mapper
from sap1.model import metadata
from sap1.model.item import Item

# Database table definition

tabla_relacion_item = Table("Relacion_Item", metadata,
    Column("idItem1", Integer, ForeignKey("Item.id"), primary_key=True),
    Column("idItem2", Integer, ForeignKey("Item.id"), primary_key=True),

)

# Python class definition
class RelacionItem(object):
    def __init__(self, idItem1, idItem2):
       self.idItem1 = idItem1
       self.idItem2 = idItem2


# Mapper
mapper_relacion_item = mapper(RelacionItem, tabla_relacion_item)
