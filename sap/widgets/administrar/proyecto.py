from sap.model import DeclarativeBase, metadata, DBSession
from sap.model.proyecto import Proyecto 
from tg.decorators import without_trailing_slash, with_trailing_slash, paginate
from tw.core import WidgetsList
from tw.forms import CheckBoxList,TableForm, TextField, CalendarDatePicker, SingleSelectField, TextArea
from formencode.validators import Int, NotEmpty, DateConverter, DateValidator
from sprox.tablebase import TableBase
from sprox.formbase import EditableForm, AddRecordForm
from sap.widgets.administrar.adminfillerbase import TableFiller, EditFormFiller, EditFormFiller
from sap.model.proyecto import Proyecto
from tw.api import WidgetsList
from tw.forms import (TableForm, CalendarDatePicker, Spacer, SingleSelectField, TextField, TextArea,SubmitButton)
#from tgext.crud import CrudRestController
from sap.widgets.administrar.controllerAdmin import CrudRestController
from sap.model.proyecto import Proyecto
#from sap.controllers.root import *
from sap.model.auth import *
from tg import expose, flash, redirect, tmpl_context, request
from repoze.what.predicates import *



from tw.api import CSSLink
from tg import url
from tw.forms.validators import Int, NotEmpty, DateConverter


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
    def __actions__(self, obj):
        """Override this function to define how action links should be displayed for the given record."""
        primary_fields = self.__provider__.get_primary_fields(self.__entity__)
        pklist = '/'.join(map(lambda x: str(getattr(obj, x)), primary_fields))
        if has_permission('manage'):############
            value = '<div><div><a class="edit_link" href="'+pklist+'/edit" style="text-decoration:none">edit</a>'\
              '</div><div>'\
              '<form method="POST" action="'+pklist+'" class="button-to">'\
            '<input type="hidden" name="_method" value="DELETE" />'\
            '<input class="delete-button" onclick="return confirm(\'Are you sure?\');" value="delete" type="submit" '\
            'style="background-color: transparent; float:left; border:0; color: #286571; display: inline; margin: 0; padding: 0;"/>'\
        '</form>'\
        '</div></div>'
        
        return value
    
    def _do_get_provider_count_and_objs(self ,**kw):
        limit = kw.get('limit', None)
        offset = kw.get('offset', None)
        order_by = kw.get('order_by', None)
        desc = kw.get('desc', False)
        
        
        if len(kw) > 0:
            #if len(kw) > 1:
            objs = DBSession.query(self.__entity__).filter((Proyecto.nombre.ilike('%'+str(kw['buscar'])+'%'))).all()
            #else:
            #    objs = DBSession.query(self.__entity__).filter_by(idproyec=kw['pid']).all()
        else:
            #objs = DBSession.query(self.__entity__).filter_by(idproyec=kw[result['pid']]).all()
            objs = DBSession.query(self.__entity__).all()
        count = len(objs)
        self.__count__ = count
        return count, objs    

    
    
    
    
    

    __model__ = Proyecto
proyecto_table_filler = ProyectoTableFiller(DBSession)



class ProyectoForm(TableForm):
    

        #template = "toscasample.widgets.templates.table_form"
        #template = "sap.templates.administrar.proyecto.new"
        css = [CSSLink(link=url('/css/tooltips.css'))]
        show_errors = True



        lider_options = []
        fields = [
		TextField('nombre',validator=NotEmpty, label_text='Nombre'),
	        Spacer(),
		TextField('descripcion', label_text='Descripcion'),
		#TextArea('descripcion', attrs=dict(rows=3, cols=10)),
        Spacer(),
        
        
        SingleSelectField('liderProyecto', options=lider_options),
        #TextField('liderProyecto', label_text='Lider de Proyecto')

		]
        
        
        
        submit_text = 'Crear Proyecto'

        

        
proyecto_add_form = ProyectoForm('create_proyecto_form')





        
class ProyectoEditForm(EditableForm):
    __model__ = Proyecto
        
    lider_options = []
    __field_widgets__ = {'nombre':TextField('nombre',validator=NotEmpty, label_text='Nombre'),
                         'descripcion':TextField('descripcion', label_text='Descripcion'),
                         'liderProyecto':CalendarDatePicker('fechaCreacion', date_format='%d-%m-%y'),
                         'estado':SingleSelectField('liderProyecto', options=lider_options)}

    __omit_fields__ = ['id', 'fechaCreacion', 'nrofase']
    submit_text = 'Editar Proyecto'


proyecto_edit_form = ProyectoEditForm(DBSession)



class ProyectoEditFiller(EditFormFiller):
    __model__ = Proyecto
proyecto_edit_filler = ProyectoEditFiller(DBSession)
    
   


class ProyectoController(CrudRestController):
    
    allow_only = All(not_anonymous(msg='Acceso denegado. Usted no se ha logueado!'),
                has_any_permission('manage',
                msg='Solo usuarios con algun permiso de administrador pueden acceder a esta pagina!'))
 
    	
    model = Proyecto
    table = proyecto_table
    table_filler = proyecto_table_filler
    new_form = proyecto_add_form
    edit_filler = proyecto_edit_filler
    edit_form = proyecto_edit_form

   

    @with_trailing_slash
    @expose("sap.templates.administrar.proyecto.get_all")
    @expose('json')
    @paginate('value_list', items_per_page=7)
    def get_all(self, *args, **kw):
        return super(ProyectoController, self).get_all(*args, **kw)






    

