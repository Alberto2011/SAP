from sap.model import DeclarativeBase, metadata, DBSession
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
from sap.widgets.desarrollar.revivir.controller import CrudRestController
from sap.model.item import Item
from sap.model.tipodeitem import TipoDeItem
from sap.model.campos import Campos


####
import logging

from repoze.what.predicates import has_permission 
log = logging.getLogger(__name__)

####

    

#from sap.controllers.root import *
from tg import expose, flash, redirect, tmpl_context


from sap.model.auth import *
####
import logging

from repoze.what.predicates import has_permission 
log = logging.getLogger(__name__)

####



class RevivirTable(TableBase):
    __model__ = Item
    __omit_fields__ = ['id']
revivir_table = RevivirTable(DBSession) 



class RevivirTableFiller(TableFiller):

    __model__ = Item

    def __actions__(self, obj):
        """Override this function to define how action links should be displayed for the given record."""
        primary_fields = self.__provider__.get_primary_fields(self.__entity__)
        pklist = '/'.join(map(lambda x: str(getattr(obj, x)), primary_fields))
        #if has_permission('manage'):############
        value =  '<div><a class="loginlogout" href="'+pklist+'/edit" style="text-decoration:none">Revivir</a></div>'
        
        
        return value
    

    def _do_get_provider_count_and_objs(self, **kw):
        limit = kw.get('limit', None)
        offset = kw.get('offset', None)
        order_by = kw.get('order_by', None)
        desc = kw.get('desc', False)
        #objs = DBSession.query(self.__entity__).filter_by(idFase=1).all()
        
        log.debug('pruebaRevivir: %s' %kw)
        
        if len(kw) > 0:
            
             if len(kw) > 1:
                 objs = DBSession.query(self.__entity__).filter((Item.idFase==kw['fid'])& (Item.estado=="borrado") & (Item.nombre.ilike('%'+str(kw['buscar'])+'%'))).all()
             else:
                 objs = DBSession.query(self.__entity__).filter_by(idFase=kw['fid'],estado="borrado").all()
             #objs = DBSession.query(self.__entity__).filter((Item.nrohistorial==kw['hid'])& (Item.ultimaversion==0) & (Item.nombre.ilike('%'+str(kw['buscar'])+'%'))).all()
             #objs = DBSession.query(self.__entity__).all()
        else:
            objs = DBSession.query(self.__entity__).all()

        count = len(objs)
        self.__count__ = count
        return count, objs    


revivir_table_filler = RevivirTableFiller(DBSession)


#campotipo= DBSession.query(Campos.tipoDeDato, Campos.nombre).filter_by(idTipoDeItem=value['idTipoDeItem']).all()







        
class RevivirEditForm(EditableForm):
    __model__ = Item
    __field_attrs__ = {'nombre':{'rows':'2'},'estado':{'rows':'2'}}
    
    __omit_fields__ = ['id','idTipoDeItem','idFase','fechaCreacion','idLineaBase','version', 'nrohistorial','ultimaversion']


revivir_edit_form = RevivirEditForm(DBSession)



class RevivirEditFiller(EditFormFiller):
    __model__ = Item
revivir_edit_filler = RevivirEditFiller(DBSession)
    
   


class RevivirController(CrudRestController):
    
        
    allow_only = All(not_anonymous(msg='Acceso denegado. Usted no se ha logueado!'),
                         has_any_permission('administrar',
                                            'configurar',
                                            'desarrollar',
                                            msg='Usted no posee los permisos para ingresar a esta pagina!'))
 
    
    	
    model = Item
    table = revivir_table
    table_filler = revivir_table_filler
    edit_filler = revivir_edit_filler
    edit_form = revivir_edit_form
    
    
    
    @with_trailing_slash
    @expose("sap.templates.desarrollar.revivir.get_all")
    @expose('json')
    @paginate('value_list', items_per_page=7)
    def get_all(self, fid=None,*args, **kw):
        kw['fid']=fid
        result=super(RevivirController, self).get_all(*args, **kw)
        result['fid']=fid
        return result
    

