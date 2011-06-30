from repoze.what.predicates import *
from sap.model import DeclarativeBase, metadata, DBSession
from tg.decorators import without_trailing_slash, with_trailing_slash, paginate
from tw.core import WidgetsList
from tw.forms import CheckBoxList,TableForm, TextField, CalendarDatePicker, SingleSelectField, TextArea
from formencode.validators import Int, NotEmpty, DateConverter, DateValidator
from sprox.tablebase import TableBase
from sprox.formbase import EditableForm, AddRecordForm
from sap.widgets.administrar.adminfillerbase import TableFiller, EditFormFiller, EditFormFiller
from tw.api import WidgetsList
from tw.forms import (TableForm, CalendarDatePicker, Spacer, SingleSelectField,HiddenField ,TextField, TextArea,SubmitButton)
#from tgext.crud import CrudRestController
from sap.widgets.configurar.campos.controller import CrudRestController
#from sap.controllers.root import *
from sap.model.campos import Campos
from tg import expose
import logging 
log = logging.getLogger(__name__)


class CamposTable(TableBase):
    __model__ = Campos
    __omit_fields__ = ['id']
campos_table = CamposTable(DBSession) 



class CamposTableFiller(TableFiller):
    __model__ = Campos
    
    def __actions__(self, obj):
        """Override this function to define how action links should be displayed for the given record."""
        primary_fields = self.__provider__.get_primary_fields(self.__entity__)
        pklist = '/'.join(map(lambda x: str(getattr(obj, x)), primary_fields))
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
            objs = DBSession.query(self.__entity__).filter_by(idTipoDeItem=kw['tid']).all()
        else:
            #objs = DBSession.query(self.__entity__).filter_by(idproyec=kw[result['pid']]).all()
            objs = DBSession.query(self.__entity__).all()
        count = len(objs)
        self.__count__ = count
        return count, objs 
    

    
campos_table_filler = CamposTableFiller(DBSession)






class CamposForm(TableForm):
   
        tipo_options = [x for x in (('string', 'integer','date'))]


        fields = [
        TextField('nombre', label_text='Nombre'),
	    HiddenField('idTipoDeItem', label_text='Tipo de Item'),
        Spacer(),
        SingleSelectField('tipoDeDato',options=tipo_options,label_text='Tipo de Dato'),
        ]
        submit_text = 'Crear Atributo'
        
campos_add_form = CamposForm('create_campos_form')



class CamposEditForm(EditableForm):
    __model__ = Campos
    
    tipo_options = [x for x in (('string', 'integer','date'))]
    
    __field_widgets__ = {'nombre':TextField('nombre', label_text='Nombre'),
            'tipoDeDato':SingleSelectField('tipoDeDato',options=tipo_options,label_text='Tipo de Dato'),}
    
    __omit_fields__ = ['id','idTipoDeItem']


campos_edit_form = CamposEditForm(DBSession)




class CamposEditFiller(EditFormFiller):
    __model__ = Campos
campos_edit_filler = CamposEditFiller(DBSession)
    
   


class CamposController(CrudRestController):
    
    allow_only = All(not_anonymous(msg='Acceso denegado. Usted no se ha logueado!'),
                         has_any_permission('administrar',
                                            'configurar',
                                            'desarrollar',
                                            msg='Usted no posee los permisos para ingresar a esta pagina!'))
     
    model = Campos
    table = campos_table
    table_filler = campos_table_filler
    new_form = campos_add_form
    edit_filler = campos_edit_filler
    edit_form = campos_edit_form
    
    @with_trailing_slash
    @expose("sap.templates.configurar.campos.get_all")
    @expose('json')
    @paginate('value_list', items_per_page=7)
    def get_all(self,tid=None ,*args, **kw):
        log.debug("KwGtAll %s" %tid)
        kw['tid']=tid
        result=super(CamposController, self).get_all(*args, **kw)
        result['tid']=tid
        return result




    

