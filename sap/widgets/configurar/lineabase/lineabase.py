from repoze.what.predicates import *
from sap.model import DeclarativeBase, metadata, DBSession
from tg.decorators import without_trailing_slash, with_trailing_slash, paginate
from tw.core import WidgetsList

from formencode.validators import Int, NotEmpty, DateConverter, DateValidator
from sprox.tablebase import TableBase
from sprox.formbase import EditableForm, AddRecordForm
from sap.widgets.configurar.lineabase.fillerbase import TableFiller, EditFormFiller, EditFormFiller
from sap.model.lineabase import LineaBase
from tw.api import WidgetsList
from tw.forms import (TableForm, CalendarDatePicker, Spacer,MultipleSelectField ,SingleSelectField, TextField, TextArea,SubmitButton)

#from tgext.crud import CrudRestController
from sap.widgets.configurar.lineabase.controller import CrudRestController
#from sap.controllers.root import *
from sap.model.fase import Fase
from sap.model.item import Item

from tg import tmpl_context, expose
####
import logging

from repoze.what.predicates import has_permission 
log = logging.getLogger(__name__)

####



class LineaBaseTable(TableBase):
    __model__ = LineaBase
    __omit_fields__ = ['id']
lineabase_table = LineaBaseTable(DBSession) 



class LineaBaseTableFiller(TableFiller):
      __model__ = LineaBase
      
      
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
      """    
      def _do_get_provider_count_and_objs(self ,**kw):
        limit = kw.get('limit', None)
        offset = kw.get('offset', None)
        order_by = kw.get('order_by', None)
        desc = kw.get('desc', False)
        
        if len(kw) > 0:
            
            objs = DBSession.query(self.__entity__).filter_by(idproyec=kw['fid']).all()
        else:
            #objs = DBSession.query(self.__entity__).filter_by(idproyec=kw[result['pid']]).all()
            objs = DBSession.query(self.__entity__).all()
        count = len(objs)
        self.__count__ = count
        return count, objs      

        """
    
    
    
    
        
      
lineabase_table_filler = LineaBaseTableFiller(DBSession)



class LineaBaseForm(TableForm):
    
	#action = 'CrearLineaBase'
    
        
    

        #genre_options = [x for x in (DBSession.query(Group).filter_by(group_name="lider").one()).users]
        item_options = [x for x in (DBSession.query(Item.id, Item.nombre))]


        fields = [
        TextField('nombre', label_text='Nombre'),
		TextField('idFase', label_text='idFase'),
	    Spacer(),
		#TextField('idItem', label_text='idItem'),
        MultipleSelectField('idItem', options=item_options,label_text= 'Items'),
        #SingleSelectField('idItem', options=item_options),
		Spacer(),
        TextField('estado', label_text='estado'),
        Spacer(),
		CalendarDatePicker('fechaCreacion', date_format='%d-%m-%y'),
        Spacer(),
        
        
        #SingleSelectField('liderProyecto', options=genre_options),
        #TextField('liderProyecto', label_text='Lider de Proyecto')

		]
        submit_text = 'Crear LineaBase'

        

        
lineabase_add_form = LineaBaseForm('create_lineabase_form')





        
class LineaBaseEditForm(EditableForm):
    __model__ = LineaBase
    __field_attrs__ = {'idFase':{'rows':'2'},
			'idItem':{'rows':'2'},
			'estado':{'rows':'2'}}
    
    

    __omit_fields__ = ['id']


lineabase_edit_form = LineaBaseEditForm(DBSession)



class LineaBaseEditFiller(EditFormFiller):
    __model__ = LineaBase
lineabase_edit_filler = LineaBaseEditFiller(DBSession)
    
   


class LineaBaseController(CrudRestController):
    

    allow_only = All(not_anonymous(msg='Acceso denegado. Usted no se ha logueado!'),
                         has_any_permission('administrar',
                                            'configurar',
                                            msg='Usted no posee los permisos para ingresar a esta pagina!'))
 
    
    
    
    model = LineaBase
    table = lineabase_table
    table_filler = lineabase_table_filler
    new_form = lineabase_add_form
    edit_filler = lineabase_edit_filler
    edit_form = lineabase_edit_form

   

    
    
    
    @with_trailing_slash
    @expose("sap.templates.configurar.lineabase.get_all")
    @expose('json')
    @paginate('value_list', items_per_page=7)
    def get_all(self, fid=None,*args, **kw):
        log.debug('fide=%s' %fid)
        #kw['fid']=fid
        result=super(LineaBaseController, self).get_all(*args, **kw)
        result['fid']=fid
        return result


    """@with_trailing_slash
    @expose("sap.templates.configurar.lineabase.get_all")
    @expose('json')
    @paginate('value_list', items_per_page=7)
    def get_all(self, *args, **kw):
        return super(LineaBaseController, self).get_all(*args, **kw)
    """



    

