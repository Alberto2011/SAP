from repoze.what.predicates import *
#from tw.forms.validators import Int, NotEmpty, DateConverter
from sap.model.campos import Campos
from sap.model import DeclarativeBase, metadata, DBSession
from tg.decorators import without_trailing_slash, with_trailing_slash, paginate
from tw.core import WidgetsList
from tw.forms import CheckBoxList,TableForm, TextField, CalendarDatePicker, SingleSelectField, TextArea

"""validadores"""
from formencode.validators import Int, NotEmpty, DateConverter, DateValidator
#from formencode import validators
from formencode.api import FancyValidator
from formencode.api import Invalid
import tw.forms as twf


####################3

#import tw.jquery
#from sprox.jquery.tablebase import JQueryTableBase
#from sprox.jquery.fillerbase import JQueryTableFiller
#    from sprox.jquery.formbase import DojoAddRecordForm, DojoEditableForm
#jquery_loaded = True

######################3





from sprox.tablebase import TableBase
from sprox.formbase import EditableForm, AddRecordForm
from sap.widgets.administrar.adminfillerbase import TableFiller, EditFormFiller, EditFormFiller
from tw.api import WidgetsList
from tw.forms import (TableForm, CalendarDatePicker, Spacer,HiddenField, SingleSelectField, TextField, TextArea,SubmitButton)
#from tgext.crud import CrudRestController
from sap.widgets.desarrollar.item.controller import CrudRestController
from sap.model.item import Item
from sap.model.fase import Fase
from sap.model.proyecto import Proyecto
from sap.model.tipodeitem import TipoDeItem
from sap.model.campos import Campos
from sap.model.lineabase import LineaBase




##################################################
try:
    import tw.dojo
    from sprox.dojo.tablebase import DojoTableBase
    from sprox.dojo.fillerbase import DojoTableFiller
    from sprox.dojo.formbase import DojoAddRecordForm, DojoEditableForm
    dojo_loaded = True
except ImportError:
    pass

try:
    import tw.jquery
    from sprox.jquery.tablebase import JQueryTableBase
    from sprox.jquery.fillerbase import JQueryTableFiller
#    from sprox.jquery.formbase import DojoAddRecordForm, DojoEditableForm
    jquery_loaded = True
except ImportError:
    pass


################################################






    

#from sap.controllers.root import *
from tg import expose, flash, redirect, tmpl_context


from sap.model.auth import *
####
import logging

from repoze.what.predicates import has_permission 
log = logging.getLogger(__name__)

####



class ItemTable(TableBase):
    __model__ = Item
    __omit_fields__ = ['id', 'nrohistorial','ultimaversion']
item_table = ItemTable(DBSession) 



class ItemTableFiller(TableFiller):

    __model__ = Item

    def __actions__(self, obj):
        """Override this function to define how action links should be displayed for the given record."""
        primary_fields = self.__provider__.get_primary_fields(self.__entity__)
        pklist = '/'.join(map(lambda x: str(getattr(obj, x)), primary_fields))
        #if has_permission('manage'):############
        
        estadoItem = DBSession.query(Item.estado).filter_by(id = pklist).first() 
        fase = DBSession.query(Item.idFase).filter_by(id = pklist).first()
        proyecto = DBSession.query(Fase.idproyec).filter_by(id = fase).first()
        estadoProy = DBSession.query(Proyecto.estado).filter_by(id = proyecto).first()
        nrohistorial=DBSession.query(Item.nrohistorial).filter_by(id=pklist).first()
        item = DBSession.query(Item).filter_by(id=pklist).first()
        lineabase = DBSession.query(LineaBase).filter_by(id=item.idLineaBase).first()
        
        value='<div></div>'
        
        if str(estadoProy[0]).__eq__("iniciado"):
            if lineabase != None:
                if str(lineabase.estado).__eq__("cerrada"):
                    value =  '<div><div><a class="loginlogout" href="/revertir/?hid='+str(nrohistorial[0])+'">Historial</a></div><br/>'\
                        '<div><a class="loginlogout" href="/detalleitem/?iid='+pklist+'">  Detalle</a></div><br/>'\
                        '<div><a class="loginlogout" href="/relacionitem/?iid='+pklist+'">Ver relaciones</a></div><br/>'\
                        '<div><a class="loginlogout" href="/abrirlineabaserelacion/?iid='+pklist+'">Crear relaciones</a></div><br/>'\
                        '<div><a class="loginlogout" href="/calcularimpacto/?iid='+pklist+ '">  CalcularImpacto</a></div><br/>'\
                        '<div><a class="edit_link" href="/abrirlineabase/?iid='+pklist+'" style="text-decoration:none">edit</a>'\
                        '</div></div>'
                elif str(lineabase.estado).__eq__("comprometida"):
                    if str(estadoItem[0]).__eq__("aprobado"):
                        value =  '<div><div><a class="loginlogout" href="/revertir/?hid='+str(nrohistorial[0])+'">Historial</a></div><br/>'\
                            '<div><a class="loginlogout" href="/detalleitem/?iid='+pklist+'">  Detalle</a></div><br/>'\
                            '<div><a class="loginlogout" href="/relacionitem/?iid='+pklist+'">Ver relaciones</a></div><br/>'\
                            '<div><a class="loginlogout" href="/abrirlineabaserelacion/?iid='+pklist+'">Crear relaciones</a></div><br/>'\
                            '<div><a class="loginlogout" href="/calcularimpacto/?iid='+pklist+ '">  CalcularImpacto</a></div><br/>'\
                            '<div><a class="edit_link" href="/abrirlineabase/?iid='+pklist+'" style="text-decoration:none">edit</a>'\
                            '</div></div>'
                    else:
                        value =  '<div><div><a class="loginlogout" href="/aprobaritem/?iid='+pklist+ '">Aprobar Item</a></div><br/>'\
                            '<div><a class="loginlogout" href="/revertir/?hid='+str(nrohistorial[0])+'">Historial</a></div><br/>'\
                            '<div><a class="loginlogout" href="/detalleitem/?iid='+pklist+'">  Detalle</a></div><br/>'\
                            '<div><a class="loginlogout" href="/relacionitem/?iid='+pklist+'">Ver relaciones</a></div><br/>'\
                            '<div><a class="loginlogout" href="/abrirlineabaserelacion/?iid='+pklist+'">Crear relaciones</a></div><br/>'\
                            '<div><a class="loginlogout" href="/calcularimpacto/?iid='+pklist+ '">  CalcularImpacto</a></div><br/>'\
                            '<div><a class="edit_link" href="/abrirlineabase/?iid='+pklist+'" style="text-decoration:none">edit</a>'\
                            '</div></div>'
                else:
                    if str(estadoItem[0]).__eq__("aprobado"):
                        value =  '<div><div><a class="loginlogout" href="/revertir/?hid='+str(nrohistorial[0])+'">Historial</a></div><br/>'\
                            '<div><a class="loginlogout" href="/detalleitem/?iid='+pklist+'">  Detalle</a></div><br/>'\
                            '<div><a class="loginlogout" href="/relacionitem/?iid='+pklist+'">Ver relaciones</a></div><br/>'\
                            '<div><a class="loginlogout" href="/relacionitem/new/?iid='+pklist+'">Crear relaciones</a></div><br/>'\
                            '<div><a class="loginlogout" href="/calcularimpacto/?iid='+pklist+ '">  CalcularImpacto</a></div><br/>'\
                            '<div><a class="loginlogout" href="/adjuntos/new/?iid='+pklist+'">  Adjuntos</a></div><br/>'\
                            '<div><a class="edit_link" href="'+pklist+'/edit" style="text-decoration:none">edit</a>'\
                            '</div><div>'\
                            '<form method="POST" action="'+pklist+'" class="button-to">'\
                            '<input type="hidden" name="_method" value="DELETE" />'\
                            '<input class="delete-button" onclick="return confirm(\'Are you sure?\');" value="delete" type="submit" '\
                            'style="background-color: transparent; float:left; border:0; color: #286571; display: inline; margin: 0; padding: 0;"/>'\
                            '</form>'\
                            '</div>'\
                            '</div>'
                    else:
                        value =  '<div><div><a class="loginlogout" href="/aprobaritem/?iid='+pklist+ '">Aprobar Item</a></div><br/>'\
                            '<div><a class="loginlogout" href="/revertir/?hid='+str(nrohistorial[0])+'">Historial</a></div><br/>'\
                            '<div><a class="loginlogout" href="/detalleitem/?iid='+pklist+'">  Detalle</a></div><br/>'\
                            '<div><a class="loginlogout" href="/relacionitem/?iid='+pklist+'">Ver relaciones</a></div><br/>'\
                            '<div><a class="loginlogout" href="/relacionitem/new/?iid='+pklist+'">Crear relaciones</a></div><br/>'\
                            '<div><a class="loginlogout" href="/calcularimpacto/?iid='+pklist+ '">  CalcularImpacto</a></div><br/>'\
                            '<div><a class="loginlogout" href="/adjuntos/new/?iid='+pklist+'">  Adjuntos</a></div><br/>'\
                            '<div><a class="edit_link" href="'+pklist+'/edit" style="text-decoration:none">edit</a>'\
                            '</div><div>'\
                            '<form method="POST" action="'+pklist+'" class="button-to">'\
                            '<input type="hidden" name="_method" value="DELETE" />'\
                            '<input class="delete-button" onclick="return confirm(\'Are you sure?\');" value="delete" type="submit" '\
                            'style="background-color: transparent; float:left; border:0; color: #286571; display: inline; margin: 0; padding: 0;"/>'\
                            '</form>'\
                            '</div>'\
                            '</div>'
            else:
                if str(estadoItem[0]).__eq__("aprobado"):
                    value =  '<div><div><a class="loginlogout" href="/revertir/?hid='+str(nrohistorial[0])+'">Historial</a></div><br/>'\
                        '<div><a class="loginlogout" href="/detalleitem/?iid='+pklist+'">  Detalle</a></div><br/>'\
                        '<div><a class="loginlogout" href="/relacionitem/?iid='+pklist+'">Ver relaciones</a></div><br/>'\
                        '<div><a class="loginlogout" href="/relacionitem/new/?iid='+pklist+'">Crear relaciones</a></div><br/>'\
                        '<div><a class="loginlogout" href="/calcularimpacto/?iid='+pklist+ '">  CalcularImpacto</a></div><br/>'\
                        '<div><a class="loginlogout" href="/adjuntos/new/?iid='+pklist+'">  Adjuntos</a></div><br/>'\
                        '<div><a class="edit_link" href="'+pklist+'/edit" style="text-decoration:none">edit</a>'\
                        '</div><div>'\
                        '<form method="POST" action="'+pklist+'" class="button-to">'\
                        '<input type="hidden" name="_method" value="DELETE" />'\
                        '<input class="delete-button" onclick="return confirm(\'Are you sure?\');" value="delete" type="submit" '\
                        'style="background-color: transparent; float:left; border:0; color: #286571; display: inline; margin: 0; padding: 0;"/>'\
                        '</form>'\
                        '</div>'\
                        '</div>'
                else:
                    value =  '<div><div><a class="loginlogout" href="/aprobaritem/?iid='+pklist+ '">Aprobar Item</a></div><br/>'\
                        '<div><a class="loginlogout" href="/revertir/?hid='+str(nrohistorial[0])+'">Historial</a></div><br/>'\
                        '<div><a class="loginlogout" href="/detalleitem/?iid='+pklist+'">  Detalle</a></div><br/>'\
                        '<div><a class="loginlogout" href="/relacionitem/?iid='+pklist+'">Ver relaciones</a></div><br/>'\
                        '<div><a class="loginlogout" href="/relacionitem/new/?iid='+pklist+'">Crear relaciones</a></div><br/>'\
                        '<div><a class="loginlogout" href="/calcularimpacto/?iid='+pklist+ '">  CalcularImpacto</a></div><br/>'\
                        '<div><a class="loginlogout" href="/adjuntos/new/?iid='+pklist+'">  Adjuntos</a></div><br/>'\
                        '<div><a class="edit_link" href="'+pklist+'/edit" style="text-decoration:none">edit</a>'\
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
        
        if len(kw) > 0:
            objs = DBSession.query(self.__entity__).filter((Item.idFase==kw['fid']) & (Item.ultimaversion==1) & (Item.estado!="borrado")).all()
            for x in range (len(objs)):
                log.debug("obj %s", objs[x].id)
        else:
            objs = DBSession.query(self.__entity__).all()

        count = len(objs)
        self.__count__ = count
        return count, objs    


item_table_filler = ItemTableFiller(DBSession)



class ItemForm(TableForm):
#class ItemForm(DojoAddRecordForm):
        #__model__ = Item
        #__omit_fields__ = ['id','idTipoDeItem','idFase','idLineaBase','version', 'nrohistorial','ultimaversion', 'estado']
        tiid=0
        campotipo= DBSession.query(Campos.tipoDeDato, Campos.nombre).filter_by(idTipoDeItem=13).all()
        comlejidadoptions= [(1, 'Muy Baja (1)'), (2, 'Baja (2)'), (3, 'Media (3)'), (4, 'Alta (4)'), (5, 'Muy Alta (5)')]
        
        log.debug(comlejidadoptions)
        
                         
        #campo_options=[]
        
        #campotipo=campo_options
                
        __require_fields__=['nombre']
        
        fields = [
        
        
        TextField('nombre', label_text='Nombre'),
   	    Spacer(),
		HiddenField('idFase', label_text='idFase'),
        HiddenField('version', label_text='version'),
        HiddenField('estado', label_text='estado'),
        SingleSelectField('complejidad', options=comlejidadoptions, label_text='complejidad'),
        Spacer(),
        CalendarDatePicker('fechaCreacion', date_format='%d-%m-%y'),
        #Spacer(),
        HiddenField('nrohistorial', label_text='nrohistorial'),
        #SingleSelectField('idTipoDeItem', options=tipo_options),
        HiddenField('idTipoDeItem', label_text='idTipoDeItem'), 
		]
        #log.debug(campotipo)
        """
        
        for ct in campotipo:
            #log.debug(ct[1])
            campo1 = TextField(ct[1], label_text= ct[1])
            fields.append(campo1)
            
        """
        submit_text = 'Crear Item'
       
item_add_form = ItemForm('create_item_form')



        
class ItemEditForm(EditableForm):
    __model__ = Item
    __disable_fields__=['nombre']
    comlejidadoptions= [(1, 'Muy Baja (1)'), (2, 'Baja (2)'), (3, 'Media (3)'), (4, 'Alta (4)'), (5, 'Muy Alta (5)')]
    __field_widgets__ = {'nombre':TextField('nombre', label_text='Nombre'),
                         'complejidad':SingleSelectField('complejidad', options=comlejidadoptions, label_text='complejidad')}
    
    __omit_fields__ = ['id','idTipoDeItem','idFase','fechaCreacion','idLineaBase','version', 'nrohistorial','ultimaversion', 'estado']


item_edit_form = ItemEditForm(DBSession)



class ItemEditFiller(EditFormFiller):
    __model__ = Item
item_edit_filler = ItemEditFiller(DBSession)
    
   


class ItemController(CrudRestController):
    
        
    allow_only = All(not_anonymous(msg='Acceso denegado. Usted no se ha logueado!'),
                         has_any_permission('administrar',
                                            'configurar',
                                            'desarrollar',
                                            msg='Usted no posee los permisos para ingresar a esta pagina!'))
 
    
    	
    model = Item
    table = item_table
    table_filler = item_table_filler
    new_form = item_add_form
    edit_filler = item_edit_filler
    edit_form = item_edit_form
    

    
    @with_trailing_slash
    @expose("sap.templates.desarrollar.item.get_all")
    @expose('json')
    @paginate('value_list', items_per_page=50)
    def get_all(self, fid=None,*args, **kw):
        kw['fid']=fid
        result=super(ItemController, self).get_all(*args, **kw)
        result['fid']=fid
        #log.debug('resultGetAll=%s' %result)
        return result
        #return super(ItemController, self).get_all(*args, **kw)
    
    
    """@with_trailing_slash
    @expose("sap.templates.desarrollar.item.get_all")
    @expose('json')
    @paginate('value_list', items_per_page=7)
    def get_all(self, *args, **kw):
        return super(ItemController, self).get_all(*args, **kw)
    """

    """@without_trailing_slash
    @expose('sap.templates.desarrollar.item.new')
    def new(self, *args, **kw):
       
        tmpl_context.widget = self.new_form
        # return dict(value=kw, model=self.model.__name__)
        return super(ItemController, self).new(*args, **kw)        
    """
    @expose('sap.templates.desarrollar.item.edit')
    def edit(self, *args, **kw):
        return super(ItemController, self).edit(*args, **kw)
    
    

