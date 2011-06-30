from sap.model import DeclarativeBase, metadata, DBSession
from repoze.what.predicates import *
from sap.model.lineabase import LineaBase
from sap.model.item import Item
from sap.model import DeclarativeBase, metadata, DBSession
from tg.decorators import without_trailing_slash, with_trailing_slash, paginate
from tw.core import WidgetsList
from tw.forms import CheckBoxList,TableForm, TextField, CalendarDatePicker, SingleSelectField, TextArea
from formencode.validators import Int, NotEmpty, DateConverter, DateValidator
from sprox.tablebase import TableBase
from sprox.formbase import EditableForm, AddRecordForm
from sap.widgets.administrar.adminfillerbase import TableFiller, EditFormFiller, EditFormFiller
from tw.api import WidgetsList
from tw.forms import (TableForm, CalendarDatePicker, Spacer,HiddenField, SingleSelectField, TextField, TextArea,SubmitButton)
#from tgext.crud import CrudRestController
from sap.widgets.desarrollar.itemlineabase.controller import CrudRestController




    

#from sap.controllers.root import *
from tg import expose, flash, redirect, tmpl_context


from sap.model.auth import *
####
import logging

from repoze.what.predicates import has_permission 
log = logging.getLogger(__name__)

####



class ItemLineaBaseTable(TableBase):
    __model__ = Item
    __omit_fields__ = ['id','idTipoDeItem','complejidad','nrohistorial','version','ultimaversion','fechaCreacion', '__actions__']
itemlineabase_table = ItemLineaBaseTable(DBSession) 



class ItemLineaBaseTableFiller(TableFiller):

    __model__ = Item
    

    def _do_get_provider_count_and_objs(self, **kw):
        limit = kw.get('limit', None)
        offset = kw.get('offset', None)
        order_by = kw.get('order_by', None)
        desc = kw.get('desc', False)

        objs = DBSession.query(self.__entity__).filter_by(idLineaBase=kw['lid'], ultimaversion=1).all()
        
        count = len(objs)
        self.__count__ = count
        return count, objs    


itemlineabase_table_filler = ItemLineaBaseTableFiller(DBSession)
        
class ItemLineaBaseEditForm(EditableForm):
    __model__ = Item

itemlineabase_edit_form = ItemLineaBaseEditForm(DBSession)



class ItemLineaBaseEditFiller(EditFormFiller):
    __model__ = Item
itemlineabase_edit_filler = ItemLineaBaseEditFiller(DBSession)
    
   


class ItemLineaBaseController(CrudRestController):
    
        
    allow_only = All(not_anonymous(msg='Acceso denegado. Usted no se ha logueado!'),
                         has_any_permission('administrar',
                                            'configurar',
                                            'desarrollar',
                                            msg='Usted no posee los permisos para ingresar a esta pagina!'))
 
    
    	
    model = Item
    table = itemlineabase_table
    table_filler = itemlineabase_table_filler
    edit_filler = itemlineabase_edit_filler
    edit_form = itemlineabase_edit_form
    

    
    @with_trailing_slash
    @expose("sap.templates.desarrollar.itemlineabase.get_all")
    @expose('json')
    @paginate('value_list', items_per_page=7)
    def get_all(self, lid=None,*args, **kw):
        kw['lid']=lid
        result=super(ItemLineaBaseController, self).get_all(*args, **kw)
        result['lid']=lid
        #log.debug('resultGetAll=%s' %result)
        return result
    


