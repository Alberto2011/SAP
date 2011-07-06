"""
"""
from sap.model import DeclarativeBase, metadata, DBSession
from sap.model.item import Item
from sap.model.detalleitem import DetalleItem
from sap.model.adjuntos import Adjuntos


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
        
        """este codigo es ejecutado cuando se revierte un item """
       
        pks = self.provider.get_primary_fields(self.model)
        
        kw = {}
        for i, pk in  enumerate(pks):
            kw[pk] = args[i]
        value = self.edit_filler.get_value(kw)
        
        """-----------Se obtiene el item a revertir -------------"""
        item=DBSession.query(Item).filter_by(id=kw['id']).first()
        """------------------------------------------------------"""
        
        
        """------obtine el numero de la mayor version del item---"""
        versionmayor= DBSession.query(Item.version).filter_by(nrohistorial=item.nrohistorial ,ultimaversion=1).first()
        """------------------------------------------------------"""
        
        """ ---el item con la version mayor, cambia su ultimaversion a cero --- """
        item3=DBSession.query(Item).filter_by(nrohistorial=item.nrohistorial,ultimaversion=1).first()
        log.debug('item3= %s'%item3 )
        item3.ultimaversion=0
        
        
        
        
        log.debug("versionmayor= %s" %versionmayor[0])
        
        item2=Item()
        item2.nombre=item.nombre
        item2.idTipoDeItem=item.idTipoDeItem
        item2.idFase=item.idFase
        item2.idLineaBase=item.idLineaBase
        
        """el item a revertir aumenta su version a la ultima y el
        el item con la ultima version, "ultima version" pasa a 0 """
        item2.version= versionmayor[0]+1
        item2.ultimaversion=1
        item2.estado=item.estado
        item2.complejidad=item.complejidad
        item2.fechaCreacion=item.fechaCreacion
        item2.nrohistorial=item.nrohistorial
        DBSession.add(item2)
        
        """Realiza copia de los valores de los atributos especificos"""
            
        atributoeditado=DBSession.query(DetalleItem).filter_by(iditem=item.id).all()
            
            
        for objeto in atributoeditado:
            nuevoDetalle=DetalleItem()
            nuevoDetalle.tipo=objeto.tipo
            nuevoDetalle.nombrecampo=objeto.nombrecampo
            nuevoDetalle.valor=objeto.valor
            nuevoDetalle.iditem=item2.id #el ID del nuevo item
            DBSession.add(nuevoDetalle)
                
        """Realiza copia de los adjuntos"""
        adjuntositemeditado=DBSession.query(Adjuntos).filter_by(idItem=item.id).all()
            
        for adj in adjuntositemeditado:
                
            log.debug("adj: %s" %adj)
            itemnuevoadjunto=Adjuntos()
            itemnuevoadjunto.idItem=item2.id
            itemnuevoadjunto.filename=adj.filename
            itemnuevoadjunto.filecontent=adj.filecontent
            DBSession.add(itemnuevoadjunto)        
        
        
        redirect('../'+'../item/?fid=' + str(item.idFase))

    @without_trailing_slash
    @expose('tgext.crud.templates.new')
    def new(self, *args, **kw):
        """Display a page to show a new record."""
        tmpl_context.widget = self.new_form
        return dict(value=kw, model=self.model.__name__)

    @catch_errors(errors, error_handler=new)
    @expose()
    @registered_validate(error_handler=new)
    def post(self, *args, **kw):
        self.provider.create(self.model, params=kw)
        #########
        #if len(kw['idproyec']) > 0:
        #   raise redirect('./?pid='+kw['idproyec'])
        #else:
        #    if len(kw['idFase']) > 0:
        #        raise redirect('./?fid='+kw['idFase'])
        #    else:
        #        raise redirect('./')
        #########
        raise redirect('./')
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
        redirect('./' + '../' * (len(pks) - 1))

    @expose('tgext.crud.templates.get_delete')
    def get_delete(self, *args, **kw):
        """This is the code that creates a confirm_delete page"""
        return dict(args=args)

