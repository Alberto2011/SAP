from repoze.what.predicates import *
from sap.model import DeclarativeBase, metadata, DBSession
from tg.decorators import without_trailing_slash, with_trailing_slash, paginate
from tw.core import WidgetsList
from tw.forms import CheckBoxList,TableForm, TextField, CalendarDatePicker, SingleSelectField, TextArea
from formencode.validators import Int, NotEmpty, DateConverter, DateValidator
from sprox.tablebase import TableBase
from sprox.formbase import EditableForm, AddRecordForm
from sap.widgets.configurar.fase.fasefillerbase import TableFiller, EditFormFiller, EditFormFiller
from sap.model.proyecto import Proyecto
from tw.api import WidgetsList
from tw.forms import (TableForm, CalendarDatePicker, Spacer, SingleSelectField, TextField, TextArea,SubmitButton,HiddenField)
from sap.model.fase import Fase

from sap.widgets.desarrollar.fase.controller import CrudRestController
from sap.model.auth import *
from sap.model.auth import User
from sap.model.proyfaseusuario import ProyFaseUsuario

####
import logging
from tg import expose, request
from repoze.what.predicates import has_permission 
log = logging.getLogger(__name__)

####



class FaseTable(TableBase):
    __model__ = Fase
    __omit_fields__ = ['id', 'idproyec']
fase_table = FaseTable(DBSession) 



class FaseTableFiller(TableFiller):
    
    __model__ = Fase
    def __actions__(self, obj):
        """Override this function to define how action links should be displayed for the given record."""
        primary_fields = self.__provider__.get_primary_fields(self.__entity__)
        pklist = '/'.join(map(lambda x: str(getattr(obj, x)), primary_fields))
        #if has_permission('manage'):############
        
        proyecto = DBSession.query(Fase.idproyec).filter_by(id = pklist).first()
        estado = DBSession.query(Proyecto.estado).filter_by(id = proyecto).first()
        faseanterior = DBSession.query(Fase).filter((Fase.idproyec == proyecto) & (Fase.id < pklist)).all()
        longitud = len(faseanterior)
        
        if str(estado[0]).__eq__("iniciado"):
            if longitud > 0:
                if (faseanterior[longitud-1].estado == 'inicial') | (faseanterior[longitud-1].estado == 'desarrollo'):
                    value = '<div></div>'
                else:
                    value = '<div><a class="loginlogout" href="/item/?fid='+pklist+ '">Items</a><br/>'\
                        '<a class="loginlogout" href="/revivir/?fid='+pklist+ '">RevivirItem</a><br/>'\
                        '<a class="loginlogout" href="/lineabase/?fid='+pklist+ '">LineaBase</a></div>'
            else:
                value = '<div><a class="loginlogout" href="/item/?fid='+pklist+ '">Items</a><br/>'\
                    '<a class="loginlogout" href="/revivir/?fid='+pklist+ '">RevivirItem</a><br/>'\
                    '<a class="loginlogout" href="/lineabase/?fid='+pklist+ '">LineaBase</a></div>'
        else:
            value = '<div><a class="loginlogout" href="/item/?fid='+pklist+ '">Items</a><br/>'\
                '<a class="loginlogout" href="/lineabase/?fid='+pklist+ '">LineaBase</a></div>'
        
        return value

    def _do_get_provider_count_and_objs(self ,**kw):
        limit = kw.get('limit', None)
        offset = kw.get('offset', None)
        order_by = kw.get('order_by', None)
        desc = kw.get('desc', False)
        
        log.debug('kwwww: %s' %kw)
        
        if len(kw) > 0:
            """Se extrae el id del usuario quien inicio sesion"""
            idUsuario= [x for x in DBSession.query(User.user_id).filter_by(user_name=request.identity['repoze.who.userid'])]

            """Se extrae los id de las fases en la cual el usuario tiene permiso """
            idsfases=[x for x in DBSession.query(ProyFaseUsuario.idFase).filter_by(idProyecto=kw['pid'] , iduser=idUsuario[0]).distinct()]
            
            fases=[]
            longitud=len(idsfases)
            
            
            if len(kw) > 1:
                for y in range(longitud):
                    visualizar=DBSession.query(self.__entity__).filter((Fase.id==idsfases[y])  & (Fase.nombre.ilike('%'+str(kw['buscar'])+'%'))).first()
                    if visualizar != None:
                        fases.append(visualizar)
            else:
                for y in range(longitud):
                    fases.append(DBSession.query(self.__entity__).filter_by(id=idsfases[y]).first())
            objs=fases
            
        else:
            objs = DBSession.query(self.__entity__).all()
        count = len(objs)
        self.__count__ = count
        return count, objs    

    
fase_table_filler = FaseTableFiller(DBSession)





class FaseForm(TableForm):
    
	#action = 'CrearFase'

        fields = [
		TextField('nombre', label_text='Nombre'),
	    Spacer(),
		TextField('descripcion', label_text='Descripcion'),
        Spacer(),
        #HiddenField('idproyec', label_text='idproyec')
        TextField('idproyec', label_text='idproyec')

		]
        
        submit_text = 'Crear Fase'
       
fase_add_form = FaseForm('create_fase_form')



        
class FaseEditForm(EditableForm):
    __model__ = Fase
    __field_attrs__ = {'nombre':{'rows':'2'},
			'descripcion':{'rows':'2'},
			'idproyect':{'rows':'2'}}
    
    __field_widgets__ = {'nombre':TextField('nombre', label_text='Nombre'),
            'descripcion':TextField('descripcion', label_text='Descripcion')}
    
    
    __omit_fields__ = ['id']


fase_edit_form = FaseEditForm(DBSession)



class FaseEditFiller(EditFormFiller):
    __model__ = Fase
fase_edit_filler = FaseEditFiller(DBSession)
    
   


class FaseControllerD(CrudRestController):
    
    
    
    allow_only = All(not_anonymous(msg='Acceso denegado. Usted no se ha logueado!'),
                         has_any_permission('administrar',
                                            'configurar',
                                            'desarrollar',
                                            msg='Usted no posee los permisos para ingresar a esta pagina!'))
 
    	
    model = Fase
    table = fase_table
    table_filler = fase_table_filler
    new_form = fase_add_form
    edit_filler = fase_edit_filler
    edit_form = fase_edit_form

    
    @with_trailing_slash
    @expose("sap.templates.desarrollar.fase.get_all")
    @expose('json')
    @paginate('value_list', items_per_page=100)
    def get_all(self, pid=None,*args, **kw):
        kw['pid']=pid
        result=super(FaseControllerD, self).get_all(*args, **kw)
        #log.debug('Result2=%s' %result['value_list'][2])
        
        result['pid']=pid
        return result

        


