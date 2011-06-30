from repoze.what.predicates import *
from sap.model import DeclarativeBase, metadata, DBSession
from tg.decorators import without_trailing_slash, with_trailing_slash, paginate
from tw.core import WidgetsList
from tw.forms import CheckBoxList,TableForm, TextField, CalendarDatePicker, SingleSelectField, TextArea
from formencode.validators import Int, NotEmpty, DateConverter, DateValidator
from sprox.tablebase import TableBase
from sprox.formbase import EditableForm, AddRecordForm
from sap.widgets.administrar.adminfillerbase import TableFiller, EditFormFiller, EditFormFiller
from sap.model.adjuntos import Adjuntos
from tw.api import WidgetsList
from tw.forms import (TableForm, CalendarDatePicker, Spacer, SingleSelectField, TextField, TextArea,SubmitButton,FileField)
from tg import expose, flash, redirect, tmpl_context
from sap.widgets.desarrollar.adjuntos.controller import CrudRestController

from sap.model.auth import *
####
import shutil
import os
from pkg_resources import resource_filename




#import logging
#from repoze.what.predicates import has_permission 
#log = logging.getLogger(__name__)

####



class AdjuntosTable(TableBase):
    __model__ = Adjuntos
    __omit_fields__ = ['id', 'filecontent','filename']
adjuntos_table = AdjuntosTable(DBSession) 


class AdjuntosTableFiller(TableFiller):
        __model__ = Adjuntos
adjuntos_table_filler = AdjuntosTableFiller(DBSession)



class AdjuntosForm(TableForm):
        

        """fields = [
        
        TextField('adjuntos_filename', label_text='Nombre'),
        Spacer(),          
		FileField('adjuntos_file', label_text='Adjunto'),
        Spacer(),
        TextField('idItem', label_text='idItem')
		]
        """
        #http://www.turbogears.org/2.1/docs/main/ToscaWidgets/forms.html
        
        #public_dirname = os.path.j'filecontent'oin(os.path.abspath(resource_filename('/sap/widgets/configurar/adjuntos/adjuntos', 'public')))
        #public_dirname = os.path.join(os.path.abspath(resource_filename('/sap/widgets/configurar/adjuntos/adjuntos','/sap/widgets/configurar/adjuntos/adjuntos2')))
        #adjuntos_dirname = os.path.join(public_dirname, '/sap/widgets/configurar/adjuntos/adjuntos')

        ###submit_text = 'Guardar Adjunto'
 
        
    
adjuntos_add_form = AdjuntosForm('create_adjuntos_form')

       
       
       
       
       
       
 
class AdjuntosEditForm(EditableForm):
    __model__ = Adjuntos
    
 
    __omit_fields__ = ['id','filecontent','filename']


adjuntos_edit_form = AdjuntosEditForm(DBSession)



class AdjuntosEditFiller(EditFormFiller):
    __model__ = Adjuntos
adjuntos_edit_filler = AdjuntosEditFiller(DBSession)
   


class AdjuntosController(CrudRestController):	

    allow_only = All(not_anonymous(msg='Acceso denegado. Usted no se ha logueado!'),
                         has_any_permission('administrar',
                                            'configurar',
                                            'generarlineabase',
                                            msg='Usted no posee los permisos para ingresar a esta pagina!'))
 
    model = Adjuntos
    table = adjuntos_table
    table_filler = adjuntos_table_filler
    new_form = adjuntos_add_form
    edit_filler = adjuntos_edit_filler
    edit_form = adjuntos_edit_form
    
    
    
    @with_trailing_slash
    @expose("sap.templates.desarrollar.adjuntos.get_all")
    @expose('json')
    @paginate('value_list', items_per_page=7)
    def get_all(self, *args, **kw):
        
        return super(AdjuntosController, self).get_all(*args, **kw)
    
