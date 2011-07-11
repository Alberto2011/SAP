from repoze.what.predicates import *
from sap.model import DeclarativeBase, metadata, DBSession
from tg.decorators import without_trailing_slash, with_trailing_slash, paginate
from tw.core import WidgetsList
from tw.forms import CheckBoxList,TableForm, TextField, CalendarDatePicker, SingleSelectField, TextArea
from formencode.validators import Int, NotEmpty, DateConverter, DateValidator
from sprox.tablebase import TableBase
from sprox.formbase import EditableForm, AddRecordForm
from sap.widgets.administrar.adminfillerbase import TableFiller, EditFormFiller, EditFormFiller
#from sap.model.proyecto import Proyecto
from tw.api import WidgetsList
from tw.forms import (TableForm, CalendarDatePicker, Spacer,MultipleSelectField, SingleSelectField, TextField,HiddenField ,TextArea,SubmitButton)
from sap.model.proyfaseusuario import ProyFaseUsuario
#from sap.controllers.root import *
from sap.widgets.configurar.fase.controller import CrudRestController
from sap.widgets.configurar.proyfaseusuario.controller import CrudRestController
from sap.model.auth import *
from sap.model.fase import Fase
from sap.model.proyecto import Proyecto
from tg import expose

####
import logging

from repoze.what.predicates import has_permission 
log = logging.getLogger(__name__)

####



class UserProyTable(TableBase):
    __model__ =  ProyFaseUsuario
    __omit_fields__ = ['id', 'idProyecto']
userproy_table = UserProyTable(DBSession) 



class UserProyTableFiller(TableFiller):
    
    __model__ = ProyFaseUsuario
    def __actions__(self, obj):
        """Override this function to define how action links should be displayed for the given record."""
        primary_fields = self.__provider__.get_primary_fields(self.__entity__)
        pklist = '/'.join(map(lambda x: str(getattr(obj, x)), primary_fields))
        #if has_permission('manage'):############
        value = '<div><form method="POST" action="'+pklist+'" class="button-to">'\
        '<input type="hidden" name="_method" value="DELETE" />'\
        '<input class="delete-button" onclick="return confirm(\'Are you sure?\');" value="delete" type="submit" '\
        'style="background-color: transparent; float:left; border:0; color: #286571; display: inline; margin: 0; padding: 0;"/>'\
        '</form>'\
        '</div>'
        
        return value

    def _do_get_provider_count_and_objs(self, **kw):
        limit = kw.get('limit', None)
        offset = kw.get('offset', None)
        order_by = kw.get('order_by', None)
        desc = kw.get('desc', False)
        
        if len(kw) > 0:
            if len(kw) > 1:
                objs=[]
                obj=[]
                fases = DBSession.query(Fase.id, Fase.nombre).filter(Fase.nombre.ilike('%'+str(kw['buscar'])+'%')).all()
                permisos = DBSession.query(Permission.permission_id, Permission.permission_name).filter(Permission.permission_name.ilike('%'+str(kw['buscar'])+'%')).all()
                usuarios = DBSession.query(User.user_id, User.user_name).filter(User.user_name.ilike('%'+str(kw['buscar'])+'%')).all()
                
                for fase in fases:
                    obj = DBSession.query(self.__entity__).\
                            filter((ProyFaseUsuario.idProyecto==kw['pid']) &\
                                   (ProyFaseUsuario.idFase==fase.id)).all()
                                                
                    for objetos in obj:
                        if objetos != None:
                            if objs.count(objetos) < 1:
                                objs.append(objetos)
                          
                obj=[]  
                for permiso in permisos:
                    obj = DBSession.query(self.__entity__).\
                            filter((ProyFaseUsuario.idProyecto==kw['pid']) &\
                                   (ProyFaseUsuario.idPermiso==permiso.permission_id)).all()
                                   
                    for objetos in obj:
                        if objetos != None:
                            if objs.count(objetos) < 1:
                                objs.append(objetos)

                obj=[]  
                for usuario in usuarios:
                    obj = DBSession.query(self.__entity__).\
                            filter((ProyFaseUsuario.idProyecto==kw['pid']) &\
                                   (ProyFaseUsuario.iduser==usuario.user_id)).all()
                                   
                    for objetos in obj:
                        if objetos != None:
                            if objs.count(objetos) < 1:
                                objs.append(objetos)
            else:
                objs = DBSession.query(self.__entity__).filter_by(idProyecto=kw['pid']).all()
        else:
            objs = DBSession.query(self.__entity__).all()
        count = len(objs)
        self.__count__ = count
        return count, objs    

    
userproy_table_filler =  UserProyTableFiller(DBSession)



class UserProyForm(TableForm):

    fases_options = []
    usuarios_options=[]
    permisos_options = [(4, u'ver_item'), (5, u'crear_item'), (6, u'editar_item'),\
                        (7, u'borrar_item'), (8, u'revertir_item'), (9, u'revivir_item'),\
                        (10, u'abm_adjuntos'), (11, u'aprobar_item'), (12, u'crear_relaciones'),\
                        (13, u'crear_linea_base'), (14, u'abrir_linea_base')]
 
    
    #user_options = [x for x in (DBSession.query(User.user_id, User.user_name))]
    #permisos_options = [x for x in enumerate (("aprobar", "leer", "escribir"))]
    
    fields = [
        HiddenField('idProyecto', label_text='IdProyecto'),
        Spacer(),
        SingleSelectField('idFase', options=fases_options, label_text='Fase'),
        Spacer(),
       	SingleSelectField('iduser', options=usuarios_options, label_text='Usuario'),    
        Spacer(),
        CheckBoxList('idPermiso', options=permisos_options, label_text='Permisos'),
        Spacer()     
        ]
    
    submit_text = 'Agregar Usuario'
userproy_add_form =  UserProyForm('create_UserProy_form')



        
class  UserProyEditForm(EditableForm):
    __model__ = ProyFaseUsuario
    __field_attrs__ = {'idproyecto':{'rows':'2'},
			'idfase':{'rows':'2'},
			'user_id':{'rows':'2'}}
			
    
    __omit_fields__ = ['id']

userproy_edit_form =  UserProyEditForm(DBSession)



class  UserProyEditFiller(EditFormFiller):
    __model__ = ProyFaseUsuario
userproy_edit_filler =  UserProyEditFiller(DBSession)
    
   


class ProyFaseUsuarioController(CrudRestController):	
    
    
    allow_only = All(not_anonymous(msg='Acceso denegado. Usted no se ha logueado!'),
                         has_any_permission('administrar',
                                            'configurar',
                                            msg='Usted no posee los permisos para ingresar a esta pagina!'))
 
    model = ProyFaseUsuario
    table = userproy_table
    table_filler = userproy_table_filler
    new_form = userproy_add_form
    edit_filler =userproy_edit_filler
    edit_form = userproy_edit_form

    @with_trailing_slash
    @expose("sap.templates.configurar.proyfaseusuario.get_all")
    @expose('json')
    @paginate('value_list', items_per_page=100)
    def get_all(self,pid=None, *args, **kw):
        kw['pid']=pid
        result= super(ProyFaseUsuarioController, self).get_all(*args, **kw)
        result['pid']=pid
        return result

   


    

        
    
        


