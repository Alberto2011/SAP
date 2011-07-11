from sap.model import DeclarativeBase, metadata, DBSession
from sap.model.proyecto import Proyecto
from tg.decorators import without_trailing_slash, with_trailing_slash, paginate
from tw.core import WidgetsList
from tw.forms import CheckBoxList,TableForm, TextField, CalendarDatePicker, SingleSelectField, TextArea
from formencode.validators import Int, NotEmpty, DateConverter, DateValidator
from sprox.tablebase import TableBase
#from saip.widgets.administrar.tablebase import TableBase
from sprox.formbase import EditableForm, AddRecordForm
from sap.widgets.configurar.proyecto.configfillerbase import TableFiller, EditFormFiller, EditFormFiller
from sap.model.proyecto import Proyecto
from tw.api import WidgetsList
from tw.forms import (TableForm, CalendarDatePicker, Spacer, SingleSelectField, TextField, TextArea,SubmitButton)
#from tgext.crud import CrudRestController
#from from sap.widgets.configurar.proyecto.controller import CrudRestController
#from sap.model.proyecto import Proyecto
#from sap.controllers.root import *
from sap.widgets.administrar.proyecto import *
from repoze.what.predicates import *
import sqlalchemy
from tg import expose, flash, redirect, tmpl_context, request
####
import logging

from repoze.what.predicates import has_permission 
log = logging.getLogger(__name__)

####



class ProyectoTable(TableBase):
    __model__ = Proyecto
    __omit_fields__ = ['id', 'nrofase']
proyecto_table = ProyectoTable(DBSession) 



class ProyectoTableFiller(TableFiller):
    __model__ = Proyecto

    def __actions__(self, obj):
        
        
        """Override this function to define how action links should be displayed for the given record."""
        primary_fields = self.__provider__.get_primary_fields(self.__entity__)
        pklist = '/'.join(map(lambda x: str(getattr(obj, x)), primary_fields))

        estado = DBSession.query(Proyecto.estado).filter_by(id = pklist).first()
        
        if str(estado[0]).__eq__("iniciado"):
            value = '<div><div><a class="loginlogout" href="'+pklist+'/edit" style="text-decoration:none">Cambiar estado</a></div><br/>'\
               '<div><a class="loginlogout" href="/fase/?pid='+pklist+ '">Fases</a></div><br/>'\
                '<div><a class="loginlogout" href="/proyfaseusuario/?pid='+pklist+'">AddUserProyec</a></div>'\
                '</div>'
        else:
            value = '<div><div><a class="loginlogout" href="'+pklist+'/edit" style="text-decoration:none">Cambiar estado</a></div><br/>'\
               '<div><a class="loginlogout" href="/fase/?pid='+pklist+ '">Fases</a></div><br/>'\
                '</div>'
                            
        return value


    
    def _do_get_provider_count_and_objs(self, **kw):
        limit = kw.get('limit', None)
        offset = kw.get('offset', None)
        order_by = kw.get('order_by', None)
        desc = kw.get('desc', False)
        
        
        if len(kw) > 0:
            
            objs = DBSession.query(self.__entity__).filter((Proyecto.liderProyecto==request.identity['repoze.who.userid']) & (Proyecto.nombre.ilike('%'+str(kw['buscar'])+'%'))).all()
            
        else:
            objs = DBSession.query(self.__entity__).filter_by(liderProyecto=request.identity['repoze.who.userid']).all()
        
        
        
        count = len(objs)
        self.__count__ = count
        return count, objs    
proyecto_table_filler = ProyectoTableFiller(DBSession)

#.query(Proyecto).filter(Proyecto.liderProyecto.contains("Alberto")).all()
#.query(Proyecto).filter(Proyecto.liderProyecto=='Alberto').all()
#DBSession.query(Proyecto).filter(lider.contains("Alberto")).all()

class ProyectoEditForm(EditableForm):
    __model__ = Proyecto
 
    estado_options = ['iniciado', 'cancelado']
    __field_widgets__ = {'estado':SingleSelectField('estado', options=estado_options)}
    __omit_fields__ = ['id','nrofase','nombre','descripcion','liderProyecto', 'fechaCreacion']


proyecto_edit_form = ProyectoEditForm(DBSession)

class ProyectoEditFiller(EditFormFiller):
    __model__ = Proyecto
proyecto_edit_filler = ProyectoEditFiller(DBSession)
   


class ProyectoConfig(CrudRestController):
    
 
        allow_only = All(not_anonymous(msg='Acceso denegado. Usted no se ha logueado!'),
                         has_any_permission('administrar',
                                            'configurar',
                                             msg='Usted no posee los permisos para ingresar a esta pagina!'))
 
    
    
        model = Proyecto
        table = proyecto_table
        table_filler = proyecto_table_filler
        edit_filler = proyecto_edit_filler
        edit_form = proyecto_edit_form
        
        @with_trailing_slash
        @expose("sap.templates.configurar.proyecto.get_all")
        @expose('json')
        @paginate('value_list', items_per_page=7)
        def get_all(self, *args, **kw):
            return super(ProyectoConfig, self).get_all(*args, **kw)