from sap.model.item import Item
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

#from sap.controllers.root import *
#from tgext.crud import CrudRestController
from sap.widgets.configurar.tipodeitem.controller import CrudRestController
from tg import expose, tmpl_context

from sap.model.tipodeitem import TipoDeItem

####
import logging
from tg import expose
from repoze.what.predicates import has_permission 
log = logging.getLogger(__name__)

####


#from tw.dynforms import  DemoGrowingTableFietw.dynforms.widgets
#from tw.dynforms.widgets import GrowingTableFieldSet


class TipoDeItemTable(TableBase):
    __model__ = TipoDeItem
    __omit_fields__ = ['id']
tipodeitem_table = TipoDeItemTable(DBSession) 



class TipoDeItemTableFiller(TableFiller):
    def __actions__(self, obj):
        """Override this function to define how action links should be displayed for the given record."""
        primary_fields = self.__provider__.get_primary_fields(self.__entity__)
        pklist = '/'.join(map(lambda x: str(getattr(obj, x)), primary_fields))
        
        
        iteminstancia=DBSession.query(Item.id).filter_by(idTipoDeItem=pklist).all()
        cantidadinstancia=len(iteminstancia)
        #log.debug('iteminstancia: %s' %iteminstancia)
        
        if cantidadinstancia>0:
            value = '<div><a class="edit_link" href="'+pklist+'/edit" style="text-decoration:none">edit</a>'\
            '<div><a class="loginlogout" href="/campos/?tid='+pklist+'">AtributosEspecificos</a></div><br/></div>'
            
        else:
            value = '<div><div><a class="edit_link" href="'+pklist+'/edit" style="text-decoration:none">edit</a>'\
            '</div><div>'\
            '<div><a class="loginlogout" href="/campos/?tid='+pklist+'">AtributosEspecificos</a></div><br/>'\
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
            
            objs = DBSession.query(self.__entity__).filter_by(idFase=kw['fid']).all()
        else:
            #objs = DBSession.query(self.__entity__).filter_by(idproyec=kw[result['pid']]).all()
            objs = DBSession.query(self.__entity__).all()
        count = len(objs)
        self.__count__ = count
        return count, objs    

    
    

    __model__ = TipoDeItem
tipodeitem_table_filler = TipoDeItemTableFiller(DBSession)



class TipoDeItemForm(TableForm):
    
        fields = [
        HiddenField('idFase', label_text='idFase'),
        Spacer(),
        TextField('nombre', label_text='Nombre'),
        Spacer(),
        TextField('descripcion', label_text='Descripcion'),
        HiddenField('id')
        ]
        
        
        
        submit_text = 'Crear TipoDeItem'

  
tipodeitem_add_form = TipoDeItemForm('create_tipodeitem_form')





        
class TipoDeItemEditForm(EditableForm):
    __model__ = TipoDeItem
    __field_widgets__ = {'nombre':TextField('nombre', label_text='Nombre'),
            'descripcion':TextField('descripcion', label_text='Descripcion'),}
    
    __omit_fields__ = ['id', 'idFase']


tipodeitem_edit_form = TipoDeItemEditForm(DBSession)



class TipoDeItemEditFiller(EditFormFiller):
    __model__ = TipoDeItem
tipodeitem_edit_filler = TipoDeItemEditFiller(DBSession)
    
   


class TipoDeItemController(CrudRestController):    
    
    
    allow_only = All(not_anonymous(msg='Acceso denegado. Usted no se ha logueado!'),
                         has_any_permission('administrar',
                                            'configurar',
                                            msg='Usted no posee los permisos para ingresar a esta pagina!'))
 
    
    model = TipoDeItem
    table = tipodeitem_table
    table_filler = tipodeitem_table_filler
    new_form = tipodeitem_add_form
    edit_filler = tipodeitem_edit_filler
    edit_form = tipodeitem_edit_form

    @with_trailing_slash
    @expose("sap.templates.configurar.tipodeitem.get_all")
    @expose('json')
    @paginate('value_list', items_per_page=7)
    def get_all(self,fid=None, *args, **kw):
        kw['fid']=fid
        result=super(TipoDeItemController, self).get_all(*args, **kw)
        result['fid']=fid
        return result
	    		



    

