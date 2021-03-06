from repoze.what.predicates import *
from sap.model import DeclarativeBase, metadata, DBSession
from tg.decorators import without_trailing_slash, with_trailing_slash, paginate
from tw.core import WidgetsList
from tw.forms import CheckBoxList,TableForm, TextField, CalendarDatePicker, SingleSelectField, TextArea
from formencode.validators import Int, NotEmpty, DateConverter, DateValidator
from sprox.tablebase import TableBase
#from saip.widgets.administrar.tablebase import TableBase
from sprox.formbase import EditableForm, AddRecordForm
from sap.widgets.desarrollar.proyecto.configfillerbase import TableFiller, EditFormFiller, EditFormFiller
from sap.model.proyecto import Proyecto
from tw.api import WidgetsList
from tw.forms import (TableForm, CalendarDatePicker, Spacer, SingleSelectField, TextField, TextArea,SubmitButton)
from tgext.crud import CrudRestController
from sap.model.proyecto import Proyecto
#from sap.controllers.root import *
from sap.widgets.administrar.proyecto import *
from sap.model.auth import User
from sap.model.proyfaseusuario import ProyFaseUsuario

import sqlalchemy
from tg import expose, flash, redirect, tmpl_context, request
####
import logging

from repoze.what.predicates import has_permission 
log = logging.getLogger(__name__)

####







class ProyectoTableFiller(TableFiller):
    __model__ = Proyecto

    def __actions__(self, obj):
        
        
        """Override this function to define how action links should be displayed for the given record."""
        primary_fields = self.__provider__.get_primary_fields(self.__entity__)
        pklist = '/'.join(map(lambda x: str(getattr(obj, x)), primary_fields))
        value = '<div><a class="loginlogout" href="/fasedesarrollo/?pid='+pklist+ '">Fases</a></div>'
                
        return value


    
    def _do_get_provider_count_and_objs(self, **kw):
        limit = kw.get('limit', None)
        offset = kw.get('offset', None)
        order_by = kw.get('order_by', None)
        desc = kw.get('desc', False)
        
        

        idUsuario= [x for x in DBSession.query(User.user_id).filter_by(user_name=request.identity['repoze.who.userid'])]
        
        idProy=[x for x in DBSession.query(ProyFaseUsuario.idProyecto).filter_by(iduser=idUsuario[0]).distinct()] 
        proyectos=[]
        
        longitud=len(idProy)
        for y in range(longitud):
            proyectos.append(DBSession.query(self.__entity__).filter_by(id = idProy[y]).one())

        
        if len(kw) > 0:
            
            for y in range(longitud):
                proyectos.append(DBSession.query(self.__entity__).filter((Proyecto.id == idProy[y]) & (Proyecto.nombre.ilike('%'+str(kw['buscar'])+'%'))).one())
            
            objs =proyectos 
            
        else:
            objs = proyectos
        
        
                
        
        
        count = len(objs)
        self.__count__ = count
        return count, objs    
    
    
    
proyecto_table_filler = ProyectoTableFiller(DBSession)

#.query(Proyecto).filter(Proyecto.liderProyecto.contains("Alberto")).all()
#.query(Proyecto).filter(Proyecto.liderProyecto=='Alberto').all()
#DBSession.query(Proyecto).filter(lider.contains("Alberto")).all()

class ProyectoEditForm(EditableForm):
    __model__ = Proyecto
 
    __field_attrs__ = {'nrofase':{'rows':'2'},  
            			'estado':{'rows':'2'}}
    __omit_fields__ = ['id','nombre','descripcion','liderProyecto', 'fechaCreacion']


proyecto_edit_form = ProyectoEditForm(DBSession)

   


class ProyectoDesarrollo(CrudRestController):
        
        allow_only = All(not_anonymous(msg='Acceso denegado. Usted no se ha logueado!'),
                         has_any_permission('administrar',
                                            'configurar',
                                            'desarrollar',
                                            msg='Usted no posee los permisos para ingresar a esta pagina!'))
        
        model = Proyecto
        table = proyecto_table
        table_filler = proyecto_table_filler
        edit_filler = proyecto_edit_filler
        edit_form = proyecto_edit_form
        
        @with_trailing_slash
        @expose("sap.templates.desarrollar.proyecto.get_all")
        @expose('json')
        @paginate('value_list', items_per_page=7)
        def get_all(self, *args, **kw):
            return super(ProyectoDesarrollo, self).get_all(*args, **kw)





    

