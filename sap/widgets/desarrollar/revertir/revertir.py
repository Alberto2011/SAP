from repoze.what.predicates import *
from sap.model.campos import Campos
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
from sap.widgets.desarrollar.revertir.controller import CrudRestController
from sap.model.item import Item
from sap.model.tipodeitem import TipoDeItem
from sap.model.campos import Campos
from sap.model.lineabase import LineaBase

    

#from sap.controllers.root import *
from tg import expose, flash, redirect, tmpl_context


from sap.model.auth import *
####
import logging

from repoze.what.predicates import has_permission 
log = logging.getLogger(__name__)

####



class RevertirTable(TableBase):
    __model__ = Item
    __omit_fields__ = ['id', 'nrohistorial','ultimaversion', 'idTipoDeItem']
revertir_table = RevertirTable(DBSession) 



class RevertirTableFiller(TableFiller):

    __model__ = Item

    def __actions__(self, obj):
        """Override this function to define how action links should be displayed for the given record."""
        primary_fields = self.__provider__.get_primary_fields(self.__entity__)
        pklist = '/'.join(map(lambda x: str(getattr(obj, x)), primary_fields))
        #if has_permission('manage'):############
        
        historial = DBSession.query(Item.nrohistorial).filter_by(id=pklist).first()
        idlineabase = DBSession.query(Item.idLineaBase).filter_by(nrohistorial=historial, ultimaversion=1).first()
        lineabase = DBSession.query(LineaBase).filter_by(id=idlineabase).first()
        
        value =  '<div></div>'
        
        if lineabase != None:
            if str(lineabase.estado).__eq__('abierta'):
                value =  '<div><a class="loginlogout" href="'+pklist+'/edit" style="text-decoration:none">Revertir</a></div>'
        else:
            value =  '<div><a class="loginlogout" href="'+pklist+'/edit" style="text-decoration:none">Revertir</a></div>'
        
        return value
    

    def _do_get_provider_count_and_objs(self, **kw):
        limit = kw.get('limit', None)
        offset = kw.get('offset', None)
        order_by = kw.get('order_by', None)
        desc = kw.get('desc', False)
        #objs = DBSession.query(self.__entity__).filter_by(idFase=1).all()
        
        if len(kw) > 0:
            
            objs = DBSession.query(self.__entity__).filter_by(nrohistorial=kw['hid'], ultimaversion=0).all()
            
        else:
            objs = DBSession.query(self.__entity__).all()

        count = len(objs)
        self.__count__ = count
        return count, objs    


revertir_table_filler = RevertirTableFiller(DBSession)


        
class RevertirEditForm(EditableForm):
    __model__ = Item
    __field_attrs__ = {'nombre':{'rows':'2'},'estado':{'rows':'2'}}
    
    __omit_fields__ = ['id','idTipoDeItem','idFase','fechaCreacion','idLineaBase','version', 'nrohistorial','ultimaversion']


revertir_edit_form = RevertirEditForm(DBSession)



class RevertirEditFiller(EditFormFiller):
    __model__ = Item
revertir_edit_filler = RevertirEditFiller(DBSession)
    
   


class RevertirController(CrudRestController):
    
        
    allow_only = All(not_anonymous(msg='Acceso denegado. Usted no se ha logueado!'),
                         has_any_permission('administrar',
                                            'configurar',
                                            'desarrollar',
                                            msg='Usted no posee los permisos para ingresar a esta pagina!'))
 
    
    	
    model = Item
    table = revertir_table
    table_filler = revertir_table_filler
    edit_filler = revertir_edit_filler
    edit_form = revertir_edit_form
    

    
    @with_trailing_slash
    @expose("sap.templates.desarrollar.revertir.get_all")
    @expose('json')
    @paginate('value_list', items_per_page=100)
    def get_all(self, hid=None,*args, **kw):
        kw['hid']=hid
        result=super(RevertirController, self).get_all(*args, **kw)
        result['hid']=hid
        #log.debug('resultGetAll=%s' %result)
        return result
        #return super(RevertirController, self).get_all(*args, **kw)
    
    
    

