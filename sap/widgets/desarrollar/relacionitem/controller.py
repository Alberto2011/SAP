from tw.forms import (CheckBoxList, HiddenField)
from sap.model import DBSession
from tg import expose, flash, redirect, tmpl_context
from tg.decorators import without_trailing_slash, with_trailing_slash
from tg.controllers import RestController
import pylons

from tgext.crud.decorators import registered_validate, register_validators, catch_errors
from sprox.providerselector import ProviderTypeSelector
from sap.model.auth import *
from sap.model.detalleitem import DetalleItem
from sap.model.adjuntos import Adjuntos

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

from sap.model.item import Item
from sap.model.relacion_item import RelacionItem
from sap.model.fase import Fase
from sap.model.proyecto import Proyecto
from sap.model.lineabase import LineaBase
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
    @expose('sap.templates.desarrollar.relacionitem.get_all')
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
            values[fila]['idItem1'] = DBSession.query(Item.nombre).filter_by(id = values[fila]['idItem1']).one()
            values[fila]['idItem2'] = DBSession.query(Item.nombre).filter_by(id = values[fila]['idItem2']).one()

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
    @expose('sap.templates.desarrollar.relacionitem.new')
    def new(self, iid=None, *args, **kw):
        """Display a page to show a new record."""
        tmpl_context.widget = self.new_form
        
        """Cambio de estado del item que se quiere relacionar"""
        item = DBSession.query(Item).filter_by(id = iid).first()
        item.estado = 'modificado'
        
        """Fase a la cual pertenece el item que se quiere relacionar"""
        faseActual = DBSession.query(Item.idFase).filter_by(id = iid).one()
        """Proyecto al cual pertenece la fase que hallamos en la linea anterior"""
        proyecto = DBSession.query(Fase.idproyec).filter_by(id = faseActual).one()
        
        listalineabase = DBSession.query(LineaBase).filter_by(idFase = faseActual).all()
        desarrollo = True
        longitud = len(listalineabase)
        
        for x in range (longitud):
            if str(listalineabase[x].estado).__eq__('cerrada'):
                desarrollo = False
                
        if desarrollo & longitud > 0:
            fase = DBSession.query(Fase).filter_by(id = item.idFase).first()
            fase.estado = 'desarrollo'
            allFaseSgte = DBSession.query(Fase).filter((Fase.idproyec == proyecto) & (Fase.id > faseActual)).all()
            longFaseSgte = len(allFaseSgte)
            
            if (longFaseSgte > 0):
                allFaseSgte[0].estado = 'desarrollo'
                lineabasesgte = DBSession.query(LineaBase).filter_by(idFase=allFaseSgte[0].id).all()
                
                for x in range (len(lineabasesgte)):
                    if str(lineabasesgte[x].estado).__eq__('cerrada'):
                        lineabasesgte[x].estado = 'comprometida'
                        
                        itemlbsgte = DBSession.query(Item).filter_by(idLineaBase=lineabasesgte[x].id, ultimaversion=1).all()
                        for y in range (len(itemlbsgte)):
                            itemlbsgte[y].estado = 'revision'
                

        """Proyecto al cual pertenece la fase que hallamos en la linea anterior"""
        proyecto = DBSession.query(Fase.idproyec).filter_by(id = faseActual).one()

        """Todas las fases que pertenecen al proyecto en cuestion"""
        allFase = DBSession.query(Fase).filter((Fase.idproyec == proyecto) & (Fase.id < faseActual)).all()
        longFase = len(allFase)
        
        """Todos los item de la fase actual"""
        listaActual = DBSession.query(Item.id, Item.nombre).filter_by(idFase=faseActual, ultimaversion=1).all()
        
        """Todas las relaciones existentes"""
        relaciones = DBSession.query(RelacionItem.idItem1, RelacionItem.idItem2).all()
        longRel = len(relaciones)
        
        #La fase inmediatamente inferior es la fase anterior
        listaAnterior=[]
        #Se comprueba que exista una fase anterior
        if (longFase > 0):
            listaAnterior = DBSession.query(Item.id, Item.nombre).filter_by(idFase=allFase[longFase-1].id, ultimaversion=1).all()

        #Eliminar los item ya relacionados de la lista de fase anterior
        for x in range(longRel):
            #relaciones[x][0] = idItem1
            #relaciones[x][1] = idItem2
            longitud = len(listaAnterior)
            if iid.__eq__("%s" %relaciones[x][0]):
                for y in range(longitud):
                    if listaAnterior[y][0] == relaciones[x][1]:
                        listaAnterior.remove(listaAnterior[y])
                        break
            elif iid.__eq__("%s" %relaciones[x][1]):
                for y in range(longitud):
                    if listaAnterior[y][0] == relaciones[x][0]:
                        listaAnterior.remove(listaAnterior[y])
                        break
        """-----------------------------------------------"""
        
        """-------------------FASE ACTUAL-------------------"""
        #Eliminar el item que se quiere relacionar de la lista de fase actual
        longitud = len(listaActual)
        for x in range(longitud):
            if iid.__eq__("%s" %listaActual[x][0]):
                listaActual.remove(listaActual[x])
                break
        
        #Eliminar los item ya relacionados de la lista de fase actual
        for x in range(longRel):
            #relaciones[x][0] = idItem1
            #relaciones[x][1] = idItem2
            longitud = len(listaActual)
            if iid.__eq__("%s" %relaciones[x][0]):
                for y in range(longitud):
                    if listaActual[y][0] == relaciones[x][1]:
                        listaActual.remove(listaActual[y])
                        break

        self.controlCiclo (relaciones, listaActual, iid)

        
        """------------------------------------------------"""
        
        #return dict(value=kw, model=self.model.__name__)
        return dict(value={'idItem1':iid},
                    model=self.model.__name__,
                    actual_options=listaActual,
                    anterior_options=listaAnterior)

    def controlCiclo (self, *args):
        relaciones = args[0]
        listaActual = args[1]
        iid = args[2]
        
        longRel = len(relaciones)
        
        for x in range(longRel):
            #relaciones[x][0] = idItem1
            #relaciones[x][1] = idItem2
            if int(iid) == int(relaciones[x][1]):
                longitud = len(listaActual)
                for y in range(longitud):
                    if listaActual[y][0] == relaciones[x][0]:
                        aux = listaActual[y]
                        self.controlCiclo(relaciones, listaActual, relaciones[x][0])
                        listaActual.remove(aux)
                        break


    @catch_errors(errors, error_handler=new)
    @expose()
    @registered_validate(error_handler=new)
    def post(self, *args, **kw):
        
  
        """Se crea un nuevo item"""
        itemeditado=DBSession.query(Item).filter_by(id=kw['idItem1']).first()
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
        DBSession.flush()
        
        """-------------------------"""
        
        
        """ Crea las nuevas relaciones"""
        
        kw['idItem1']=itemnuevo.id
        """ Se crea las relaciones"""
        ids=kw['idItem2']
        longitud=len(kw['idItem2'])
        for indice in range(longitud):
            kw['idItem2']=ids[indice] 
            self.provider.create(self.model, params=kw)
            
        ids=kw['idItem2Anterior']
        longitud=len(kw['idItem2Anterior'])
        for indice in range(longitud):
            kw['idItem2']=ids[indice] 
            self.provider.create(self.model, params=kw)
    
        
        """Realiza copia de los valores de los atributos especificos"""
            
        atributoeditado=DBSession.query(DetalleItem).filter_by(iditem=itemeditado.id).all()
            
        for objeto in atributoeditado:
            nuevoDetalle=DetalleItem()
            nuevoDetalle.tipo=objeto.tipo
            nuevoDetalle.nombrecampo=objeto.nombrecampo
            nuevoDetalle.valor=objeto.valor
            nuevoDetalle.iditem=itemnuevo.id
            DBSession.add(nuevoDetalle)
                
        """Realiza copia de los adjuntos"""
        adjuntositemeditado=DBSession.query(Adjuntos).filter_by(idItem=itemeditado.id).all()
        
        for adj in adjuntositemeditado:
            itemnuevoadjunto=Adjuntos()
            itemnuevoadjunto.idItem=itemnuevo.id
            itemnuevoadjunto.filename=adj.filename
            itemnuevoadjunto.filecontent=adj.filecontent
            DBSession.add(itemnuevoadjunto)
        
        
        """Copia las relaciones """
        #itemnuevo=DBSession.query(Item.id).filter_by(nrohistorial=nuevo['nrohistorial'], ultimaversion=1).first()
        relaciones = DBSession.query(RelacionItem.idItem1,RelacionItem.idItem2).filter((RelacionItem.idItem2==itemeditado.id) | (RelacionItem.idItem1==itemeditado.id)).all()
        
        longitud = len(relaciones)
        
        
        for x in range(longitud):
            newRelation = {}
            if int(itemeditado.id) == int(relaciones[x][0]):
                newRelation['idItem1']=int(itemnuevo.id)
                newRelation['idItem2']=relaciones[x][1]
                self.provider.create(RelacionItem, params=newRelation)
            elif int(itemeditado.id) == int(relaciones[x][1]):
                newRelation['idItem1']=relaciones[x][0]
                newRelation['idItem2']=int(itemnuevo.id)
                self.provider.create(RelacionItem, params=newRelation)

            
            
        
        
        
        
        
        
        
        
        
        
        raise redirect('./?iid='+str(kw['idItem1']))
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

