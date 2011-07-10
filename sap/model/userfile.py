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
#from sqlalchemy.orm import relation, backref

from sap.model import DeclarativeBase, metadata, DBSession


class UserFile(DeclarativeBase):
    __tablename__ = 'userfile'
        
    id = Column(Integer, primary_key=True)
    filename = Column(Unicode(255), nullable=False)
    filecontent = Column(LargeBinary)
    
    def __init__(self, filename, filecontent):
        self.filename = filename
        self.filecontent = filecontent
