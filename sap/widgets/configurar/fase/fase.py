from repoze.what.predicates import *
from sap.model import DeclarativeBase, metadata, DBSession
from tg.decorators import without_trailing_slash, with_trailing_slash, paginate
from tw.core import WidgetsList
from tw.forms import CheckBoxList,TableForm, TextField, CalendarDatePicker, SingleSelectField, TextArea
from formencode.validators import Int, NotEmpty, DateConverter, DateValidator
from sprox.tablebase import TableBase
from sprox.formbase import EditableForm, AddRecordForm
from sap.widgets.configurar.fase.fasefillerbase import TableFiller, EditFormFiller, EditFormFiller
from sap.model.proyecto import Proyecto
from tw.api import WidgetsList
from tw.forms import (TableForm, CalendarDatePicker, Spacer, SingleSelectField, TextField, TextArea,SubmitButton,HiddenField)
from sap.model.fase import Fase
#from sap.controllers.root import *
from sap.widgets.configurar.fase.controller import CrudRestController
from sap.model.auth import *
####
import logging
from tg import expose
from repoze.what.predicates import has_permission 
log = logging.getLogger(__name__)

####



class FaseTable(TableBase):
    __model__ = Fase
    __omit_fields__ = ['id']
fase_table = FaseTable(DBSession) 



class FaseTableFiller(TableFiller):
    
    __model__ = Fase
    def __actions__(self, obj):
        """Override this function to define how action links should be displayed for the given record."""
        primary_fields = self.__provider__.get_primary_fields(self.__entity__)
        pklist = '/'.join(map(lambda x: str(getattr(obj, x)), primary_fields))
        #if has_permission('manage'):############
        proyecto = DBSession.query(Fase.idproyec).filter_by(id = pklist).first()
        estado = DBSession.query(Proyecto.estado).filter_by(id = proyecto).first()
        value='<div></div>'
        
        if str(estado[0]).__eq__("nuevo"):
            value = '<div><a class="edit_link" href="'+pklist+'/edit" style="text-decoration:none">edit</a></div>'
        elif str(estado[0]).__eq__("iniciado"):
            value = '<div><div><a class="edit_link" href="'+pklist+'/edit" style="text-decoration:none">edit</a>'\
            '<div><a class="loginlogout" href="/tipodeitem/?fid='+pklist+ '">TiposItem</a></div><br/>'\
            '<div><a class="loginlogout" href="/importartipodeitem/new/?fid='+pklist+ '">ImportarTipoItem</a></div><br/>'\
            '</div></div>'
        
        return value

    def _do_get_provider_count_and_objs(self ,**kw):
        limit = kw.get('limit', None)
        offset = kw.get('offset', None)
        order_by = kw.get('order_by', None)
        desc = kw.get('desc', False)
        
        log.debug(kw)
        
        if len(kw) > 0:
            if len(kw) > 1:
                objs = DBSession.query(self.__entity__).filter((Fase.idproyec==kw['pid']) & (Fase.nombre.ilike('%'+str(kw['buscar'])+'%'))).all()
            else:
                objs = DBSession.query(self.__entity__).filter_by(idproyec=kw['pid']).all()
        else:
            #objs = DBSession.query(self.__entity__).filter_by(idproyec=kw[result['pid']]).all()
            objs = DBSession.query(self.__entity__).all()
        count = len(objs)
        self.__count__ = count
        return count, objs    

    
fase_table_filler = FaseTableFiller(DBSession)





class FaseForm(TableForm):
    
	#action = 'CrearFase'

        fields = [
		TextField('nombre', label_text='Nombre'),
	    Spacer(),
		TextField('descripcion', label_text='Descripcion'),
        Spacer(),
        HiddenField('idproyec', label_text='idproyec')

		]
        
        submit_text = 'Crear Fase'
       
fase_add_form = FaseForm('create_fase_form')



        
class FaseEditForm(EditableForm):
    __model__ = Fase
       
    __omit_fields__ = ['id','idproyec', 'estado']
   
    
    
    __field_widgets__ = {'nombre':TextField('nombre', label_text='Nombre'),
            'descripcion':TextField('descripcion', label_text='Descripcion')}
    
    
    
    


fase_edit_form = FaseEditForm(DBSession)



class FaseEditFiller(EditFormFiller):
    __model__ = Fase
fase_edit_filler = FaseEditFiller(DBSession)
    
   


class FaseController(CrudRestController):	
    

    allow_only = All(not_anonymous(msg='Acceso denegado. Usted no se ha logueado!'),
                 has_any_permission('administrar','configurar',
                 msg='Usted no posee los permisos para ingresar a esta pagina!'))
 
    
    
    
    model = Fase
    table = fase_table
    table_filler = fase_table_filler
    new_form = fase_add_form
    edit_filler = fase_edit_filler
    edit_form = fase_edit_form

    
    @with_trailing_slash
    @expose("sap.templates.configurar.fase.get_all")
    @expose('json')
    @paginate('value_list', items_per_page=7)
    def get_all(self, pid=None,*args, **kw):
        kw['pid']=pid
        result=super(FaseController, self).get_all(*args, **kw)
        #log.debug('Result2=%s' %result['value_list'][2])
        
        result['pid']=pid
        return result
    
    
    
    """
    @with_trailing_slash
    @expose("sap.templates.configurar.fase.get_all")
    @expose('json')
    @paginate('value_list', items_per_page=7)
    def get_all(self, *args, **kw):
        return super(FaseController, self).get_all(*args, **kw)
   
    """
    
    
    
    @expose('sap.templates.configurar.fase.edit')
    def edit(self, *args, **kw):
        return super(FaseController, self).edit(*args, **kw)
        
    
        


