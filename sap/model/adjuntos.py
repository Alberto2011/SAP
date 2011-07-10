# -*- coding: utf-8 -*-
""" Clase RootController
@author José Chavéz.
@author Alberto Capli.
@author Nora González.
"""
"""Sample model module."""

from sqlalchemy import *
from sqlalchemy.orm import mapper, relation
from sqlalchemy import Table, ForeignKey, Column
from sqlalchemy.types import Integer, Unicode, BLOB
from sap.model.item import Item
#from sqlalchemy.orm import relation, backref

from sap.model import DeclarativeBase, metadata, DBSession


class Adjuntos(DeclarativeBase):
    __tablename__ = 'Adjuntos'
        
    id = Column(Integer, primary_key=True)
    idItem=Column(Integer,ForeignKey("Item.id"))
    filename = Column(Unicode(255), nullable=False)
    filecontent = Column(LargeBinary)
    
    def __init__(self,idItem=0, filename='', filecontent=''):
        
        self.idItem = idItem
        self.filename = filename
        self.filecontent = filecontent
