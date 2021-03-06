"""
"""
from sap.model import DeclarativeBase, metadata, DBSession
from sap.model.fase import Fase
from sap.model.item import Item
from sap.model.lineabase import LineaBase
from tg import expose, flash, redirect, tmpl_context
from tg.decorators import without_trailing_slash, with_trailing_slash
from tg.controllers import RestController
import pylons

from tgext.crud.decorators import registered_validate, register_validators, catch_errors
from sprox.providerselector import ProviderTypeSelector
from sap.model.auth import *
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
#else:
    # if dojo ist installed, we don't need pagination
    #use_paginate = False
    #def paginate(*args, **kw):
    #    return lambda f: f


####
import logging
from tg import expose
from repoze.what.predicates import has_permission 
log = logging.getLogger(__name__)

####
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
        #pks = self.provider.get_primary_fields(self.model)
        
        log.debug("soyRomperLB= %s" %kw)

        ###########################################
        pks = self.provider.get_primary_fields(self.model)
        
        ###########################################
        kw = {}
        for i, pk in  enumerate(pks):
            kw[pk] = args[i]
        value = self.edit_filler.get_value(kw)
        value['_method'] = 'PUT'
        return dict(value=value, model=self.model.__name__, pk_count=len(pks))
    
    
    

    @without_trailing_slash
    @expose('sap.templates.desarrollar.lineabase.new')
    #@expose('tgext.crud.templates.new')
    def new(self,fid=None, *args, **kw):
        """Display a page to show a new record."""
        tmpl_context.widget = self.new_form
        #return dict(value=kw, model=self.model.__name__)
        """obtiene los id y nombre de los items, de la fase actual """
        #items = [x for x in (DBSession.query(Item.id, Item.nombre).filter_by(idFase=fid))]
        itemfaseactual= [x for x in DBSession.query(Item.id, Item.nombre).filter_by(idFase=fid, idLineaBase=None, estado='aprobado', ultimaversion=1).all()]
        #return dict(value={'idFase':fid}, model=self.model.__name__, item_options=items)
        longitud=len(itemfaseactual)
        
        if (longitud == 0):
            flash("No existen items aprobados en la fase actual", "error")
            redirect('../?fid='+fid)
        else:
            return dict(value={'idFase':fid}, model=self.model.__name__, items_options=itemfaseactual)
        
        
    

    @catch_errors(errors, error_handler=new)
    @expose()
    @registered_validate(error_handler=new)
    def post(self, *args, **kw):
        ids=kw['items']
        longitud = len(ids)
        
        items = DBSession.query(Item).filter_by(idFase=kw['idFase'], ultimaversion=1).all()
        
        if (longitud > 0):
            fase = DBSession.query(Fase).filter_by(id=kw['idFase']).first()
 
            if longitud == len(items):
                fase.estado = 'lineaBaseTotal'
            else:
                fase.estado = 'lineaBaseParcial'
                
            lineabase = self.provider.create(self.model, params=kw)
            
            for indice in range(longitud):
                item = DBSession.query(Item).filter_by(id=ids[indice]).first()
                item.idLineaBase = lineabase.id

            raise redirect('./?fid='+kw['idFase'])
        else:
            flash("No ha seleccionado ningun item", "error")
            raise redirect('./new/?fid='+kw['idFase'])  
            
        
    @expose()
    @registered_validate(error_handler=edit)
    @catch_errors(errors, error_handler=edit)
    def put(self, *args, **kw):
        """update"""
        pks = self.provider.get_primary_fields(self.model)
        for i, pk in enumerate(pks):
            if pk not in kw and i < len(args):
                kw[pk] = args[i]
        
        log.debug('putLineaBase= %s' %kw)
        #lineabase/?fid=21
        
        self.provider.update(self.model, params=kw)
        redirect('../' + '../lineabase/?fid=' + str(kw['idFase']))

    @expose()
    def post_delete(self, *args, **kw):
        """This is the code that actually deletes the record"""
        pks = self.provider.get_primary_fields(self.model)
        d = {}
        
        for i, arg in enumerate(args):
            d[pks[i]] = arg
            
            
        """extraer el idFase para poder retornar en el estado anterior """
        idfase= DBSession.query(LineaBase.idFase).filter_by(id=d['id']).first()
        
        self.provider.delete(self.model, d)
        
        
        
        redirect('/lineabase/?fid='+str(idfase[0]))

    @expose('tgext.crud.templates.get_delete')
    def get_delete(self, *args, **kw):
        """This is the code that creates a confirm_delete page"""
        return dict(args=args)

