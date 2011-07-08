import copy
from sap.model.detalleitem import DetalleItem
from sap.model.relacion_item import RelacionItem


from sap.model.item import Item
from sap.model import DBSession
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
    @expose('sap.templates.desarrollar.adjuntos.new')
    def new(self,iid=None ,*args, **kw):
        
        """Aqui entra solo para mostrar la vista y para guardar, el descargar
        borrar esta implementado en root"""
        
        
        log.debug('iid: %s' %iid)
        log.debug('adjuntos: %s' %kw)
        longitud=len(kw)
        log.debug('longitud: %s' %longitud)
        if longitud==0:
            #current_files = DBSession.query(Adjuntos).all()
            current_files = DBSession.query(Adjuntos).filter_by(idItem=iid).all()
            
            return dict(current_files=current_files, model=self.model.__name__,iid=iid)
        else:
            if iid=="save":
                iid=kw['idItem']
                
            
            
            idItem=kw['idItem']
            userfile=kw['userfile']
            log.debug('idItem: %s' %idItem)
            if userfile=='':
                flash("No ha selecionado ningun archivo", "error")
                redirect("../new/?iid="+str(iid))
            """
            forbidden_files = [".js", ".htm", ".html"]
            for forbidden_file in forbidden_files:
                if userfile.filename.find(forbidden_file) != -1:
                    return redirect("../adjuntos/new")
            filecontent = userfile.file.read()
            new_file = Adjuntos(filename=userfile.filename, filecontent=filecontent,idItem=idItem )
            DBSession.add(new_file)
            DBSession.flush()
            """
            """Realiza una copia del item cuando se adjunta un archivo y aumenta su version"""
            itemeditado= DBSession.query(Item).filter_by(id=idItem).first()
            itemnuevo=Item()
            itemnuevo.version=itemeditado.version + 1
            itemnuevo.idTipoDeItem=itemeditado.idTipoDeItem
            itemnuevo.idFase=itemeditado.idFase
            itemnuevo.idLineaBase=itemeditado.idLineaBase
            itemnuevo.fechaCreacion=itemeditado.fechaCreacion
            itemnuevo.nrohistorial=itemeditado.nrohistorial
            itemnuevo.ultimaversion=1
            itemeditado.ultimaversion=0
            itemnuevo.estado='modificado'
            itemnuevo.complejidad=itemeditado.complejidad
            itemnuevo.nombre=itemeditado.nombre
            DBSession.add(itemnuevo)
            
            """Realiza copia de los valores de los atributos especificos"""
            
            atributoeditado=DBSession.query(DetalleItem).filter_by(iditem=itemeditado.id).all()
            
            
            for objeto in atributoeditado:
                nuevoDetalle=DetalleItem()
                nuevoDetalle.tipo=objeto.tipo
                nuevoDetalle.nombrecampo=objeto.nombrecampo
                nuevoDetalle.valor=objeto.valor
                nuevoDetalle.iditem=itemnuevo.id
                DBSession.add(nuevoDetalle)
                
                
            """Copia las relaciones """
            relaciones = DBSession.query(RelacionItem.idItem1,RelacionItem.idItem2).filter((RelacionItem.idItem2==itemeditado.id) | (RelacionItem.idItem1==itemeditado.id)).all()
            longitud = len(relaciones)
            
            for x in range(longitud):
                newRelation=RelacionItem()
                log.debug('Creando relaciones')
                if int(itemeditado.id) == int(relaciones[x][0]):
                    newRelation.idItem1=int(itemnuevo.id)
                    newRelation.idItem2=relaciones[x][1]
                    DBSession.add(newRelation)
                    #self.provider.create(RelacionItem, params=newRelation)
                elif int(itemeditado.id) == int(relaciones[x][1]):
                    newRelation.idItem1=relaciones[x][0]
                    newRelation.idItem2=int(itemnuevo.id)
                    DBSession.add(newRelation)
                
        
                
            """Realiza copia de los adjuntos"""
            adjuntositemeditado=DBSession.query(Adjuntos).filter_by(idItem=itemeditado.id).all()

            for adj in adjuntositemeditado:
                itemnuevoadjunto=Adjuntos()
                
                log.debug("adj: %s" %adj)
                itemnuevoadjunto=Adjuntos()
                itemnuevoadjunto.idItem=itemnuevo.id
                itemnuevoadjunto.filename=adj.filename
                itemnuevoadjunto.filecontent=adj.filecontent
                DBSession.add(itemnuevoadjunto)
            
            
            
            forbidden_files = [".js", ".htm", ".html"]
            for forbidden_file in forbidden_files:
                if userfile.filename.find(forbidden_file) != -1:
                    return redirect("../adjuntos/new")
            filecontent = userfile.file.read()
            
            log.debug('itemnuevo: %s' %itemnuevo.id)
            
            new_file = Adjuntos(filename=userfile.filename, filecontent=filecontent,idItem=itemnuevo.id )
            DBSession.add(new_file)
            #DBSession.flush()
            
            
            
                
            #self.provider.create(self.model, params=nuevo)
            
            log.debug('adjuntositemeditado: %s' %adjuntositemeditado)
                
           
                
            
            
            
            
            redirect("../new/?iid="+str(itemnuevo.id))
            #return dict(current_files=current_files ,model=self.model.__name__,iid=iid)
            
        
        
        
        
        
        
        #tmpl_context.widget = self.new_form
        #return dict(value=kw, model=self.model.__name__)

    @catch_errors(errors, error_handler=new)
    @expose()
    @registered_validate(error_handler=new)
    def post(self, *args, **kw):
        
        userfile=kw['userfile']
        log.debug("kwwww: %s" %kw)
        
        forbidden_files = [".js", ".htm", ".html"]
        for forbidden_file in forbidden_files:
            if userfile.filename.find(forbidden_file) != -1:
                return redirect("/adjuntos/new")
        filecontent = userfile.file.read()
        new_file = Adjuntos(filename=userfile.filename, filecontent=filecontent)
        DBSession.add(new_file)
        DBSession.flush()
        redirect("/adjuntos/new")
        
        
        #self.provider.create(self.model, params=kw)
        
        
        raise redirect('/adjuntos/new')
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
        """
        pks = self.provider.get_primary_fields(self.model)
        d = {}
        for i, arg in enumerate(args):
            d[pks[i]] = arg
        self.provider.delete(self.model, d)
        redirect('./' + '../' * (len(pks) - 1))
        """
        log.debug("Estoy en el PostDelete")
        
        """
        def delete(self, fileid):
            try:
                userfile = DBSession.query(Adjuntos).filter_by(id=fileid).one()
            except:
                    return redirect("/adjuntos/new")
            DBSession.delete(userfile)
            return redirect("/adjuntos/new")
        """
        return redirect("/adjuntos/new")
        
        
        

    @expose('tgext.crud.templates.get_delete')
    def get_delete(self, *args, **kw):
        """This is the code that creates a confirm_delete page"""
        return dict(args=args)

