# -*- coding: utf-8 -*-
""" 
@author José Chavéz.
@author Alberto Capli.
@author Nora González.
"""
from sap.model import DeclarativeBase, metadata, DBSession
from sap.model.campos import Campos 
from sap.model.fase import Fase

from tg import expose, flash, redirect, tmpl_context
from sap.model.tipodeitem import TipoDeItem
from sap.model import DeclarativeBase, metadata, DBSession
from tg.decorators import without_trailing_slash, with_trailing_slash
from tg.controllers import RestController
import pylons
#from tgext.crud.decorators import registered_validate, register_validators, catch_errors
#from tg.decorators import registered_validate, register_validators, catch_errors
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

####
import logging
from tg import expose
from repoze.what.predicates import has_permission 
log = logging.getLogger(__name__)

####


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
    def edit(self,*args, **kw):
      
        """Aqui esta el codigo de importacion de tipos de items """
          
          
        log.debug(" kwedit: %s" %kw)
        #log.debug(" fidedit: %s" %fid)        
        pks = self.provider.get_primary_fields(self.model)
        kw = {}
        for i, pk in  enumerate(pks):
            kw[pk] = args[i]
  
        log.debug(" Soy el ID: %s" % kw[pk])
        
        
        
        
        
        redirect('../../importartipodeitem/?fid=22')
        
        
        

    @without_trailing_slash
    @expose("sap.templates.configurar.importartipodeitem.new")
    def new(self,fid=None ,*args, **kw):
        """Display a page to show a new record."""
        tmpl_context.widget = self.new_form
        
        
        log.debug('kwwwwnew: %s' %kw)
        
        
        longitud=len(kw)        
        if longitud==0:
            tiposdeitems=DBSession.query(TipoDeItem.id,TipoDeItem.nombre).filter(TipoDeItem.idFase != fid).all()
            return dict(value={"fid": fid}, model=self.model.__name__ ,importar_options=tiposdeitems)
        else:
           
            ids= kw['TiposDeItemImportar']
            log.debug('ids: %s' %ids)
            longitud= len(ids)
            
                
                
                
            for indice in range(longitud):
                """Hace una copia del tipo de item cambiando el idFase """
                idTipo= ids[indice]
                tipo=DBSession.query(TipoDeItem).filter_by(id=idTipo).first()
                
                
                tipocopia=TipoDeItem()
                tipocopia.nombre=tipo.nombre
                tipocopia.descripcion=tipo.descripcion
                log.debug('tipocopia: %s' %tipocopia)
                tipocopia.idFase=fid
                DBSession.add(tipocopia) #NuevoTipoItem es el nuevo objeto guardado
                
                
                NuevoTipoItem=DBSession.query(TipoDeItem.id).filter_by(nombre=tipocopia.nombre, descripcion=tipocopia.descripcion, idFase=fid).first()
                
                
                #Se copia los los atributos especificos del tipo de item
                campos=DBSession.query(Campos).filter_by(idTipoDeItem=idTipo).all()
                log.debug(campos)
                long2=len(campos)
                log.debug("long2: %s" %long2)
                
                for x in range(long2):
                    #se copia los campos pertenecientes al tipo de item pero con "idTipoDeItem" distinto
                    
                    log.debug("forrrr: %s" %x)
                    campocopia=Campos()
                    campocopia.nombre=campos[x].nombre
                    campocopia.tipoDeDato=campos[x].tipoDeDato
                    campocopia.idTipoDeItem=NuevoTipoItem.id
                    DBSession.add(campocopia) 
                    
                
                
            
        pid=DBSession.query(Fase.idproyec).filter_by(id=fid).first()
            
        redirect("../../fase/?pid="+ str(pid[0]))
        
        
        
            
            
            

        """ids= kw['idFase']
        longitud= len(kw['idFase'])
        for indice in range(longitud):
            kw['idFase']= ids[indice]
            
            msj=DBSession.query(ProyFaseUsuario.idProyecto).filter_by(idProyecto=kw['idProyecto'], iduser=kw['iduser'], idFase=kw['idFase']).first()
            if msj == None:
                self.provider.create(self.model, params=kw)
            else:
                flash("El usuario ya fue adherido a la Fase elegida", "error")
                redirect('new/?pid='+ kw['idProyecto'])
        
        raise redirect('./?pid='+ kw['idProyecto'])
        """     









    @catch_errors(errors, error_handler=new)
    @expose()
    @registered_validate(error_handler=new)
    def post(self, *args, **kw):
        self.provider.create(self.model, params=kw)
        


        log.debug("posImportar: %s" %kw)





        """ids= kw['idFase']
        longitud= len(kw['idFase'])
        for indice in range(longitud):
            kw['idFase']= ids[indice]
            
            msj=DBSession.query(ProyFaseUsuario.idProyecto).filter_by(idProyecto=kw['idProyecto'], iduser=kw['iduser'], idFase=kw['idFase']).first()
            if msj == None:
                self.provider.create(self.model, params=kw)
            else:
                flash("El usuario ya fue adherido a la Fase elegida", "error")
                redirect('new/?pid='+ kw['idProyecto'])
        
        raise redirect('./?pid='+ kw['idProyecto'])"""



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

