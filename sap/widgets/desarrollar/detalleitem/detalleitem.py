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
from sap.widgets.desarrollar.detalleitem.controller import CrudRestController
from sap.model.detalleitem import DetalleItem
from sap.model.tipodeitem import TipoDeItem

#from sap.controllers.root import *
from tg import expose, flash, redirect, tmpl_context



"""
import logging

from repoze.what.predicates import has_permission 
log = logging.gEditableFormetLogger(__name__)


"""


class DetalleItemTable(TableBase):
    __model__ = DetalleItem
    __omit_fields__ = ['id', 'iditem']
detalleitem_table = DetalleItemTable(DBSession) 



class DetalleItemTableFiller(TableFiller):

    __model__ = DetalleItem

    def __actions__(self, obj):
        """Override this function to define how action links should be displayed for the given record."""
        primary_fields = self.__provider__.get_primary_fields(self.__entity__)
        pklist = '/'.join(map(lambda x: str(getattr(obj, x)), primary_fields))
        #if has_permission('manage'):############
        value =  '<a class="edit_link" href="'+pklist+'/edit" style="text-decoration:none">edit</a>'
        
        
        
        return value
    
    
    def _do_get_provider_count_and_objs(self, **kw):
        limit = kw.get('limit', None)
        offset = kw.get('offset', None)
        order_by = kw.get('order_by', None)
        desc = kw.get('desc', False)
        #objs = DBSession.query(self.__entity__).filter_by(idFase=1).all()
        
        
        
        if len(kw) > 0:
            objs = DBSession.query(self.__entity__).filter_by(iditem=kw['iid']).all()
        else:
            objs = DBSession.query(self.__entity__).all()

        count = len(objs)
        self.__count__ = count
        return count, objs    

    
     
detalleitem_table_filler = DetalleItemTableFiller(DBSession)





class DetalleItemForm(TableForm):
    
    #action = 'CrearFase'
        
        #genre_options = [x for x in (DBSession.query(TipoDeItem.id, TipoDeItem.nombre))]
        atributos_options=[]
        
        fields = [
        
        #SingleSelectField('idTipoDeItem', options=genre_options),
        HiddenField('tipo', label_text='Tipo de Dato'),
        Spacer(),
        SingleSelectField('nombrecampo',options=atributos_options, label_text='Atributo'),
        TextField('valor', label_text='valor'),
        Spacer(),
        HiddenField('iditem', label_text='iditem'),
          
        ]
        
        

        
        
        submit_text = 'Crear DetalleItem'
       
detalleitem_add_form = DetalleItemForm('create_detalleitem_form')



        
class DetalleItemEditForm(EditableForm):
    __model__ = DetalleItem
    __disable_fields__=['nombrecampo']
    __field_attrs__ = {'valor':{'rows':'2'},'nombrecampo':{'rows':'2'},}
    
    __omit_fields__ = ['id','tipo','iditem']


detalleitem_edit_form = DetalleItemEditForm(DBSession)



class DetalleItemEditFiller(EditFormFiller):
    __model__ = DetalleItem
detalleitem_edit_filler = DetalleItemEditFiller(DBSession)
    
   


class DetalleItemController(CrudRestController):
 
    allow_only = All(not_anonymous(msg='Acceso denegado. Usted no se ha logueado!'),
                         has_any_permission('administrar',
                                            'configurar',
                                            'desarrollar',
                                            msg='Usted no posee los permisos para ingresar a esta pagina!'))
 
    
        
    model = DetalleItem
    table = detalleitem_table
    table_filler = detalleitem_table_filler
    new_form = detalleitem_add_form
    edit_filler = detalleitem_edit_filler
    edit_form = detalleitem_edit_form

    
    @with_trailing_slash
    @expose("sap.templates.desarrollar.detalleitem.get_all")
    @expose('json')
    @paginate('value_list', items_per_page=7)
    def get_all(self, iid=None,*args, **kw):
        kw['iid']=iid
        result=super(DetalleItemController, self).get_all(*args, **kw)
        result['iid']=iid
        #log.debug('resultGetAll=%s' %result)
        return result
        #return super(DetalleItemController, self).get_all(*args, **kw)
    
    


