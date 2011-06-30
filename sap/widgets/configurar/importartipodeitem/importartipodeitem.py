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
from tw.forms import (TableForm, CalendarDatePicker, Spacer, SingleSelectField, TextField, TextArea,SubmitButton,HiddenField)


from sap.widgets.configurar.importartipodeitem.controller import CrudRestController
from tg import expose, tmpl_context

from sap.model.tipodeitem import TipoDeItem

####
import logging
from tg import expose
from repoze.what.predicates import has_permission 
log = logging.getLogger(__name__)

####


class ImportarTipoDeItemTable(TableBase):
    __model__ = TipoDeItem
    __omit_fields__ = ['id']
importartipodeitem_table = ImportarTipoDeItemTable(DBSession) 



class ImportarTipoDeItemTableFiller(TableFiller):
    def __actions__(self, obj):
        """Override this function to define how action links should be displayed for the given record."""
        primary_fields = self.__provider__.get_primary_fields(self.__entity__)
        pklist = '/'.join(map(lambda x: str(getattr(obj, x)), primary_fields))
        value = '<div><a class="loginlogout" href="'+pklist+'/edit" style="text-decoration:none">Importar</a></div>'
        
        return value
    
    def _do_get_provider_count_and_objs(self ,**kw):
        limit = kw.get('limit', None)
        offset = kw.get('offset', None)
        order_by = kw.get('order_by', None)
        desc = kw.get('desc', False)
        
        if len(kw) > 0:
            
            #objs = DBSession.query(self.__entity__).filter_by(idFase=kw['fid']).all()
            objs = DBSession.query(self.__entity__).all()
        else:
            #objs = DBSession.query(self.__entity__).filter_by(idproyec=kw[result['pid']]).all()
            objs = DBSession.query(self.__entity__).all()
        count = len(objs)
        self.__count__ = count
        return count, objs    

    
    

    __model__ = TipoDeItem
importartipodeitem_table_filler = ImportarTipoDeItemTableFiller(DBSession)



class ImportarTipoDeItemForm(TableForm):
    
    
        importar_options=[]
        
        fields = [
        HiddenField('fid', label_text='fid'),
        CheckBoxList('TiposDeItemImportar', options=importar_options),
        
        
        ]
        
        
        
        submit_text = 'Importar'

  
importartipodeitem_add_form = ImportarTipoDeItemForm('create_importartipodeitem_form')





        
class ImportarTipoDeItemEditForm(EditableForm):
    __model__ = TipoDeItem
    __field_attrs__ = {'nombre':{'rows':'2'},
            'descripcion':{'rows':'2'},}
    
    __omit_fields__ = ['id']


importartipodeitem_edit_form = ImportarTipoDeItemEditForm(DBSession)



class ImportarTipoDeItemEditFiller(EditFormFiller):
    __model__ = TipoDeItem
importartipodeitem_edit_filler = ImportarTipoDeItemEditFiller(DBSession)
    
   


class ImportarTipoDeItemController(CrudRestController):    
    
    
    allow_only = All(not_anonymous(msg='Acceso denegado. Usted no se ha logueado!'),
                         has_any_permission('administrar',
                                            'configurar',
                                            msg='Usted no posee los permisos para ingresar a esta pagina!'))
 
    
    model = TipoDeItem
    table = importartipodeitem_table
    table_filler = importartipodeitem_table_filler
    new_form = importartipodeitem_add_form
    edit_filler = importartipodeitem_edit_filler
    edit_form = importartipodeitem_edit_form

    
    @with_trailing_slash
    @expose("sap.templates.configurar.importartipodeitem.get_all")
    @expose('json')
    @paginate('value_list', items_per_page=7)
    def get_all(self,fid=None, *args, **kw):
        kw['fid']=fid
        result=super(ImportarTipoDeItemController, self).get_all(*args, **kw)
        result['fid']=fid
        return result
	    		
    


    

