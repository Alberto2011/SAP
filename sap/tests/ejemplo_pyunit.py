import unittest
from sap import model
import transaction
from tg import config
from sqlalchemy import *
from sqlalchemy.orm import mapper, relation, backref, synonym, sessionmaker
from sqlalchemy import Table, ForeignKey, Column
from sqlalchemy.types import Unicode, Integer, DateTime
from sap.model import DeclarativeBase, metadata, DBSession
from sap.model.auth import User
from sap.model.item import Item

class utilTestCase(unittest.TestCase):

	def setUp(self):
		#self.obj = Proyecto()
		db = create_engine('postgresql://admin:admin@localhost:5432/SAP')
		Session = sessionmaker(bind=db)
		self.session = Session()
		#self.un_proyecto = session.query(Proyecto).get(1)
		
		#configuraciones para las pruebas
		# 
		#por ej. 
		#	self.obj = miModel()
		#
		#
		#conexion a BD
		#db = create_engine('postgresql://postgres:postgres@localhost:5432/tuBD')
		#Session = sessionmaker(bind=db)
		#self.session = Session()
		#self.un_proyecto = session.query(Proyecto).get(1)
	
	#este es el metodo que se ejecuta al darle desde la 
	#consola "python ejemplo_pyunit.py"
	#asi mismo se tiene que llamar runTest(self):
	def runTest(self):
		self.test_1()
		self.test_2()
		#self.test_3()

	def test_1(self):
		"""Nombre de usuario debe ser unico"""
		usuarios = self.session.query(User).all()
		lista = []
		
		for usr in usuarios:
			lista.append(usr.user_name)
			
		assert len(lista) == len(set(lista)), 'No son iguales'
		#~ 
		#~ aca lo que quieras probar
		#~ 
		#~ no te olvides del assert para comparar el resultado 
		#~ de tu prueba con algun valor esperado
		#~ ej:
		#~ resultado = algun_proceso_de_tu_aplicacion()
		#~ assert valor_esperado == resultado, 'No son iguales'
		
	def test_2(self):
		"""Nombre de item debe ser unico"""
		cod = self.session.query(Item).filter_by(ultimaversion=1).all()
		cant = []
		
		for i in cod:
			cant.append(i.nombre)
			
		assert len(cant) == len(set(cant)), 'No se repiten los codigos de Item'
	#def test_3(self):
		"""Poner algun nombre significativo a la prueba aca"""
		

if __name__ == "__main__":
	unittest.main()
