from repoze.what.predicates import *
from sap.model import DeclarativeBase, metadata, DBSession
from tg.decorators import without_trailing_slash, with_trailing_slash, paginate
from tw.core import WidgetsList
from tw.forms import CheckBoxList,TableForm, TextField, CalendarDatePicker, SingleSelectField, TextArea
from formencode.validators import Int, NotEmpty, DateConverter, DateValidator
from sprox.tablebase import TableBase
from sprox.formbase import EditableForm, AddRecordForm
from sap.widgets.desarrollar.relacionitem.fillerbase import TableFiller, EditFormFiller, EditFormFiller
from sap.model.relacion_item import RelacionItem
from sap.model.item import Item
from tw.api import WidgetsList
from tw.forms import (TableForm, CalendarDatePicker, Spacer, SingleSelectField,HiddenField, TextField, TextArea,SubmitButton)
from sap.widgets.desarrollar.relacionitem.controller import CrudRestController

#from sap.controllers.root import *
from tg import expose, tmpl_context
from sap.model.auth import *
####
import logging

from repoze.what.predicates import has_permission 
log = logging.getLogger(__name__)

class RelacionItemTable(TableBase):
    __model__ = RelacionItem
    __omit_fields__ = ['id', '__actions__']
relacionitem_table = RelacionItemTable(DBSession) 



class RelacionItemTableFiller(TableFiller):

    __model__ = RelacionItem

    def __actions__(self, obj):
        """Override this function to define how action links should be displayed for the given record."""
        primary_fields = self.__provider__.get_primary_fields(self.__entity__)
        pklist = '/'.join(map(lambda x: str(getattr(obj, x)), primary_fields))
        #if has_permission('manage'):############
        value =  '<div><div><a class="edit_link" href="'+pklist+'/edit" style="text-decoration:none">edit</a>'\
        '</div><div>'\
        '<form method="POST" action="'+pklist+'" class="button-to">'\
        '<input type="hidden" name="_method" value="DELETE" />'\
        '<input class="delete-button" onclick="return confirm(\'Are you sure?\');" value="delete" type="submit" '\
        'style="background-color: transparent; float:left; border:0; color: #286571; display: inline; margin: 0; padding: 0;"/>'\
        '</form>'\
        '</div>'\
        '</div>'
        
        
        return value
    
    def _do_get_provider_count_and_objs(self, **kw):
        limit = kw.get('limit', None)
        offset = kw.get('offset', None)
        order_by = kw.get('order_by', None)
        desc = kw.get('desc', False)
        #objs = DBSession.query(self.__entity__).filter_by(idFase=1).all()
        
        if len(kw) > 0:
            objs = DBSession.query(self.__entity__).filter((RelacionItem.idItem1==kw['iid']) | (RelacionItem.idItem2==kw['iid'])).all()
            listarelaciones = DBSession.query(self.__entity__).filter((RelacionItem.idItem1==kw['iid']) | (RelacionItem.idItem2==kw['iid'])).all() 
            
            for x in range (len(listarelaciones)):
                item1 = DBSession.query(Item).filter_by(id=listarelaciones[x].idItem1).first()
                item2 = DBSession.query(Item).filter_by(id=listarelaciones[x].idItem2).first()
            
                if (int(item1.ultimaversion) !=1) | (int(item2.ultimaversion) !=1):
                    objs.remove(listarelaciones[x])
        else:
            objs = DBSession.query(self.__entity__).all()

        count = len(objs)
        self.__count__ = count
        return count, objs 
    
    

relacionitem_table_filler = RelacionItemTableFiller(DBSession)





class RelacionItemForm(TableForm):
    #action = 'CrearRelacionItem'
    
    
    anterior_options = []
    actual_options = []
    
    fields = [
              HiddenField('idItem1', label_text='Item'),
              
              CheckBoxList('idItem2Anterior', options=anterior_options, label_text='Fase anterior'),
              CheckBoxList('idItem2', options=actual_options, label_text='Fase actual')
              ]
    submit_text = 'Crear Relacion Item'

        

relacionitem_add_form = RelacionItemForm('create_relacionitem_form')


class RelacionItemEditForm(EditableForm):
    __model__ = RelacionItem
    __omit_fields__ = ['id']


relacionitem_edit_form = RelacionItemEditForm(DBSession)



class RelacionItemEditFiller(EditFormFiller):
    __model__ = RelacionItem
relacionitem_edit_filler = RelacionItemEditFiller(DBSession)


class RelacionItemController(CrudRestController):
  
    allow_only = All(not_anonymous(msg='Acceso denegado. Usted no se ha logueado!'),
                         has_any_permission('administrar',
                                            'configurar',
                                            'desarrollar',
                                            msg='Usted no posee los permisos para ingresar a esta pagina!'))
 
        
    model = RelacionItem
    table = relacionitem_table
    table_filler = relacionitem_table_filler
    new_form = relacionitem_add_form
    edit_filler = relacionitem_edit_filler
    edit_form = relacionitem_edit_form

    """
    @expose('sap.templates.desarrollar.relacionitem.new_form')
    def new(self, **kw):
       
        tmpl_context.form = create_relacionitem_form
        return dict(modelname='RelacionItem', value=kw)
    """
    
    
    """ 
    @with_trailing_slash
    @expose("sap.templates.desarrollar.relacionitem.get_all")
    @expose('json')
    @paginate('value_list', items_per_page=7)
    def get_all(self, fid=None,*args, **kw):
        result=super(RelacionItemController, self).get_all(*args, **kw)
        result['fid']=fid
        log.debug('resultGetAll=%s' %result)
        return result
        #return super(RelacionItemController, self).get_all(*args, **kw)
    """
    
    @with_trailing_slash
    @expose("sap.templates.desarrollar.relacionitem.get_all")
    @expose('json')
    @paginate('value_list', items_per_page=7)
    def get_all(self, iid=None, *args, **kw):
        kw['iid']=iid
        result=super(RelacionItemController, self).get_all(*args, **kw)
        result['iid']=iid
        return result
#        return super(RelacionItemController, self).get_all(*args, **kw)

