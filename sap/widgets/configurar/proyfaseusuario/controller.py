"""
"""
from sap.model import DeclarativeBase, metadata, DBSession
from sap.model.fase import Fase
from sap.model.proyfaseusuario import ProyFaseUsuario
from tg import expose, flash, redirect, tmpl_context
from tg.decorators import without_trailing_slash, with_trailing_slash
from tg.controllers import RestController
import pylons
from sap.model.proyecto import Proyecto
from sap.model.fase import Fase
from sap.model.usuario import Usuario
from sap.model.auth import User
from sap.model.auth import Permission


from tgext.crud.decorators import registered_validate, register_validators, catch_errors
from sprox.providerselector import ProviderTypeSelector

errors = ()
try:
    from sqlalchemy.exc import IntegrityError, DatabaseError, ProgrammingError
    errors =  (IntegrityError, DatabaseError, ProgrammingError)
except ImportError:
    pass

try:
    import tw.dojo
except ImportError:
    use_paginate = True

from tg.decorators import paginate

import logging 
log = logging.getLogger(__name__)


#else:
    # if dojo ist installed, we don't need pagination
    #use_paginate = False
    #def paginate(*args, **kw):
    #    return lambda f: f


class CrudRestController(RestController):
    """
    :variables:

    session
      database session (drives drop-down menus

    menu_items
      Dictionary of links to other models in the form model_items[lower_model_name] = Model

    title
      Title to be used for each page.  default: Turbogears Admin System

    :modifiers:

    model
      Model this class is associated with

    table
      Widget for the table display

    table_filler
      Class instance with get_value() that defines the JSon stream for the table

    edit_form
      Form to be used for editing the model

    edit_filler
      Class instance with a get_value() that defines how we get information for a single
      existing record

    new_form
      Form that defines how we create a form for new data entry.

    :Attributes:

      menu_items
        Dictionary of associated Models (used for menu)
      provider
        sprox provider for data manipulation
      session
        link to the database
    """

    title = "Turbogears Admin System"

    def _before(self, *args, **kw):
        tmpl_context.title = self.title
        tmpl_context.menu_items = self.menu_items

    def __before__(self, *args, **kw):
        # this will be removed in 2.1.*
        tmpl_context.menu_items = self.menu_items
        tmpl_context.title = self.title

    def __init__(self, session, menu_items=None):
        if menu_items is None:
            menu_items = {}
        self.menu_items = menu_items
        self.provider = ProviderTypeSelector().get_selector(self.model).get_provider(self.model, hint=session)

        self.session = session

        #this makes crc declarative
        check_types = ['new_form', 'edit_form', 'table', 'table_filler', 'edit_filler']
        for type_ in check_types:
            if not hasattr(self, type_) and hasattr(self, type_+'_type'):
                setattr(self, type_, getattr(self, type_+'_type')(self.session))

        if hasattr(self, 'new_form'):
            #register the validators since they are none from the parent class
            register_validators(self, 'post', self.new_form)
        if hasattr(self, 'edit_form'):
            register_validators(self, 'put', self.edit_form)

    @with_trailing_slash
    @expose('tgext.crud.templates.get_all')
    @expose('json')
    @paginate('value_list', items_per_page=7)
    def get_all(self, *args, **kw):
        """Return all records.
           Pagination is done by offset/limit in the filler method.
           Returns an HTML page with the records if not json.
        """
        if pylons.request.response_type == 'application/json':
            return self.table_filler.get_value(**kw)

        if not getattr(self.table.__class__, '__retrieves_own_value__', False):
            values = self.table_filler.get_value(**kw)
        else:
            values = []
       
        
        longitud=len(values)
        for fila in range(longitud):
            values[fila]['idProyecto'] = DBSession.query(Proyecto.nombre).filter_by(id = values[fila]['idProyecto']).one()
            values[fila]['idFase'] = DBSession.query(Fase.nombre).filter_by(id = values[fila]['idFase']).one()    
            values[fila]['iduser'] = DBSession.query(User.user_name).filter_by(user_id = values[fila]['iduser']).one()
            values[fila]['idPermiso'] = DBSession.query(Permission.permission_name).filter_by(permission_id = values[fila]['idPermiso']).one()
        

        tmpl_context.widget = self.table
        return dict(model=self.model.__name__, value_list=values)

    @expose('tgext.crud.templates.get_one')
    @expose('json')
    def get_one(self, *args, **kw):
        """get one record, returns HTML or json"""
        #this would probably only be realized as a json stream
        tmpl_context.widget = self.edit_form
        pks = self.provider.get_primary_fields(self.model)
        kw = {}
        for i, pk in  enumerate(pks):
            kw[pk] = args[i]
        value = self.edit_filler.get_value(kw)
        return dict(value=value,model=self.model.__name__)

    @expose('tgext.crud.templates.edit')
    def edit(self, *args, **kw):
        """Display a page to edit the record."""
        tmpl_context.widget = self.edit_form
        pks = self.provider.get_primary_fields(self.model)
        kw = {}
        for i, pk in  enumerate(pks):
            kw[pk] = args[i]
        value = self.edit_filler.get_value(kw)
        value['_method'] = 'PUT'
        return dict(value=value, model=self.model.__name__, pk_count=len(pks))

    @without_trailing_slash
    @expose('sap.templates.configurar.proyfaseusuario.new')
    def new(self,pid=None ,*args, **kw):
        """Display a page to show a new record."""
        tmpl_context.widget = self.new_form
        
        fases = [x for x in DBSession.query(Fase.id, Fase.nombre).filter_by(idproyec=pid)]
        usuarios = [x for x in (DBSession.query(User.user_id, User.user_name))]
        usuarios.remove(usuarios[0])
        #permisos= [x for x in (DBSession.query(Permission. permission_id ,Permission. permission_name))]

        return dict(value={'idProyecto':pid}, model=self.model.__name__, fases_options=fases, usuarios_options=usuarios)






    @catch_errors(errors, error_handler=new)
    @expose()
    @registered_validate(error_handler=new)
    def post(self, *args, **kw):
    	ids= kw['idPermiso']
    	longitud= len(kw['idPermiso'])
        
    	for indice in range(longitud):
            kw['idPermiso']= ids[indice]
            msj=DBSession.query(ProyFaseUsuario).filter_by(idProyecto=kw['idProyecto'], iduser=kw['iduser'], idFase=kw['idFase'],idPermiso=kw['idPermiso']).first()
            log.debug('msg: %s' %msj)
            if msj == None:
                
                self.provider.create(self.model, params=kw)
            else:
                flash("El usuario ya fue adherido a la Fase elegida", "error")
                redirect('new/?pid='+ kw['idProyecto'])
        raise redirect('./?pid='+ kw['idProyecto'])




    @expose()
    @registered_validate(error_handler=edit)
    @catch_errors(errors, error_handler=edit)
    def put(self, *args, **kw):
        """update"""
        pks = self.provider.get_primary_fields(self.model)
        for i, pk in enumerate(pks):
            if pk not in kw and i < len(args):
                kw[pk] = args[i]

        self.provider.update(self.model, params=kw)
        redirect('../' * len(pks))

    @expose()
    def post_delete(self, *args, **kw):
        """This is the code that actually deletes the record"""
        pks = self.provider.get_primary_fields(self.model)
        d = {}
        for i, arg in enumerate(args):
            d[pks[i]] = arg
        self.provider.delete(self.model, d)
        
        #redirect('./' + '../' * (len(pks) - 1))
        redirect('../../../?pid='+ d['idProyecto'])

    @expose('tgext.crud.templates.get_delete')
    def get_delete(self, *args, **kw):
        """This is the code that creates a confirm_delete page"""
        return dict(args=args)

