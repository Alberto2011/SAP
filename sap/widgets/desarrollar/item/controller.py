"""
"""
from sap.widgets.desarrollar.item.item import *

from tw.forms import (TableForm, CalendarDatePicker, Spacer,HiddenField, SingleSelectField, TextField, TextArea,SubmitButton)
from sap.model.campos import Campos
from sap.model import DeclarativeBase, metadata, DBSession
from sap.model.item import Item
from sap.model.fase import Fase
from sap.model.tipodeitem import TipoDeItem
from sap.model.lineabase import LineaBase
from sap.model.relacion_item import RelacionItem
from tg import expose, flash, redirect, tmpl_context
from tg.decorators import without_trailing_slash, with_trailing_slash
from tg.controllers import RestController
import pylons

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
            
        longitud=len(values)
        for fila in range(longitud):
            complejidad = int(values[fila]['complejidad'])
            values[fila]['idFase'] = DBSession.query(Fase.nombre).filter_by(id = values[fila]['idFase']).first()
            lineabase = values[fila]['idLineaBase']
            
            if lineabase != 'None':
                values[fila]['idLineaBase'] = DBSession.query(LineaBase.nombre)\
                                                .filter_by(id=lineabase).first()
            else:
                values[fila]['idLineaBase'] = 'Sin linea base'
            
            if (complejidad == 1):
                values[fila]['complejidad'] = 'Muy baja (1)'
            elif (complejidad == 2):
                values[fila]['complejidad'] = 'Baja (2)'
            elif (complejidad == 3):
                values[fila]['complejidad'] = 'Media (3)'
            elif (complejidad == 4):
                values[fila]['complejidad'] = 'Alta (4)'
            else:
                values[fila]['complejidad'] = 'Muy alta (5)'
                

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
    #@expose("sap.templates.desarrollar.item.get_all")
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
    #@expose('tgext.crud.templates.new')
    @expose('sap.templates.desarrollar.item.new')
    def new(self,tid=None ,*args, **kw):
        """Display a page to show a new record."""
        
        
        
        fid= DBSession.query(TipoDeItem.idFase).filter_by(id=tid).first()
        """Extra los campos del tipo de Item elegido """
        
        
        """fields=[]
        campotipo= DBSession.query(Campos.tipoDeDato, Campos.nombre).filter_by(idTipoDeItem=13).all()
        for ct in campotipo:
            #log.debug(ct[1])
            campo1 = TextField(ct[1], label_text= ct[1])
            fields.append(campo1)
        
        item_add_form = ItemForm('create_item_form', fields)
        
        tmpl_context.widget = item_add_form
        """
        tmpl_context.widget = self.new_form
        #return dict(value=kw, model=self.model.__name__)
        
        #child_args=dict(child_args=form_fields_dict)
        
        
        return dict(value={'idTipoDeItem':tid, 'idFase':fid,  },model=self.model.__name__)

    @catch_errors(errors, error_handler=new)
    @expose()
    @registered_validate(error_handler=new)
    def post(self, *args, **kw):
        """extrae el numhistorial ordenado sin repetir, para luego tomar el mayor valor y asi 
        poder asignarle un numhistorial mayor
        """
        num=[x for x in (DBSession.query(Item.nrohistorial).order_by(Item.nrohistorial.desc()).distinct())]
        
        """Por cada Item creado, aumenta el nrohistorial en una unidad """
        
        if num != None  and len(num)>0:
            kw['nrohistorial']=int(num[0][0]) + 1
        else:
            kw['nrohistorial']=1
            
        fase = DBSession.query(Fase).filter_by(id=kw['idFase']).first()
        
        if str(fase.estado).__eq__('inicial'):
            fase.estado = 'desarrollo'
        elif str(fase.estado).__eq__('lineaBaseTotal'):
            fase.estado = 'lineaBaseParcial'
        
        self.provider.create(self.model, params=kw)
        
        raise redirect('./?fid='+kw['idFase'])
        

    @expose()
    @registered_validate(error_handler=edit)
    @catch_errors(errors, error_handler=edit)
    def put(self, *args, **kw):
        """update"""
       
        pks = self.provider.get_primary_fields(self.model)
        for i, pk in enumerate(pks):
            if pk not in kw and i < len(args):
                kw[pk] = args[i]
        
        
        """Extrae todos los valores del item a modificar, para luego crear un nuevo tipo"""
        
        valoresItem=DBSession.query(Item.version ,Item.idTipoDeItem ,Item.idFase ,Item.idLineaBase ,Item.fechaCreacion ,Item.nrohistorial,Item.ultimaversion).filter_by(id=kw['id']).first()
        
        """Se crea una lista, y se le agrega los valores que tendra el item. """
        nuevo={}
        nuevo['version']=valoresItem[0]+1
        nuevo['idTipoDeItem']=valoresItem[1]
        nuevo['idFase']=valoresItem[2]
        nuevo['idLineaBase']=valoresItem[3]
        nuevo['fechaCreacion']=str(valoresItem[4])
        nuevo['nrohistorial']=valoresItem[5]
        nuevo['ultimaversion']=valoresItem[6]
        nuevo['estado']='modificado'
        nuevo['complejidad']=kw['complejidad']
        nuevo['nombre']=kw['nombre']
        self.provider.create(self.model, params=nuevo)
        
        itemeditado=DBSession.query(Item).filter_by(id=kw['id']).first()
        itemeditado.ultimaversion=0
        itemnuevo=DBSession.query(Item.id).filter_by(nrohistorial=nuevo['nrohistorial'], ultimaversion=1).first()
        relaciones = DBSession.query(RelacionItem.idItem1,RelacionItem.idItem2).filter((RelacionItem.idItem2==itemeditado.id) | (RelacionItem.idItem1==itemeditado.id)).all()
        
        longitud = len(relaciones)
        newRelation = {}
        
        for x in range(longitud):
            if int(itemeditado.id) == int(relaciones[x][0]):
                newRelation['idItem1']=int(itemnuevo[0])
                newRelation['idItem2']=relaciones[x][1]
                self.provider.create(RelacionItem, params=newRelation)
            elif int(itemeditado.id) == int(relaciones[x][1]):
                newRelation['idItem1']=relaciones[x][0]
                newRelation['idItem2']=int(itemnuevo[0])
                self.provider.create(RelacionItem, params=newRelation)

        ids=[]
        ids.append(int(itemnuevo[0]))
        self.recorrerArbol(ids, int(itemnuevo[0]))
        ids.remove(int(itemnuevo[0]))
        longitud = len(ids)

        for x in range(longitud):
            itemrevision = DBSession.query(Item).filter_by(id=ids[x], ultimaversion=1).first()
            
            if itemrevision != None:
                if itemrevision.estado != 'modificado':
                    itemrevision.estado = 'revision'
                    if itemrevision.idLineaBase != None:
                        lineabase = DBSession.query(LineaBase).filter_by(id=itemrevision.idLineaBase).first()
                        if lineabase.estado == 'cerrada':
                            lineabase.estado = 'comprometida'
                            listalineabase = DBSession.query(LineaBase).filter_by(idFase = lineabase.idFase).all()
                            desarrollo = True
                            longitud = len(listalineabase)
                            
                            for x in range (longitud):
                                if str(listalineabase[x].estado).__eq__('cerrada'):
                                    desarrollo = False
                                    
                            if desarrollo:
                                fase = DBSession.query(Fase).filter_by(id = lineabase.idFase).first()
                                fase.estado = 'desarrollo'
                                allFaseSgte = DBSession.query(Fase).filter((Fase.idproyec == fase.idproyec) & (Fase.id > fase.id)).all()
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

        flash("El item \"" +kw['nombre'] +"\" ha sido modificado correctamente")
            
        redirect('../' +'../item/?fid=' + str(nuevo['idFase']))
    
    """------------------------------ Recorrer Arbol-----------------------------------
    Uso:
        self.recorrerArbol (ids, iid)
        ids: un vector que contiene primeramente al nodo inicial
        iid: nodo inicial
        Todos los nodos del arbol quedaran guardados en ids---------------------------"""
    def recorrerArbol (self, *args):
        ids = args[0]
        iid = args[1]

        """-------------Obtiene de la BD la tabla relacion completa----------------"""
        relaciones = DBSession.query(RelacionItem.idItem1,RelacionItem.idItem2).filter((RelacionItem.idItem2==iid) | (RelacionItem.idItem1==iid)).all()
        """------------------------------------------------------------------------"""
        
        """-----------Obtiene la cantidad de filas(cantidad de relaciones) ---------"""
        longitud=len(relaciones)
        """ ------------------------------------------------------------------------"""
        
        for x in range (longitud):
            #relaciones[x][0] = idItem1
            #relaciones[x][1] = idItem2
            if (int(iid) == int(relaciones[x][0])):
                if (ids.count(int(relaciones[x][1])) < 1):
                    ids.append(int(relaciones[x][1]))
                    self.recorrerArbol(ids, int(relaciones[x][1]))
            elif (int(iid) == int(relaciones[x][1])):
                if (ids.count(int(relaciones[x][0])) < 1):
                    ids.append(int(relaciones[x][0]))
                    self.recorrerArbol(ids, int(relaciones[x][0]))
    """------------------------------ Fin Recorrer Arbol-----------------------------------"""

    @expose()
    def post_delete(self, *args, **kw):
        """This is the code that actually deletes the record"""
        pks = self.provider.get_primary_fields(self.model)
        d = {}
        for i, arg in enumerate(args):
            d[pks[i]] = arg
            
        """extraer el idFase para poder retornar en el estado anterior """
        idfase= DBSession.query(Item.idFase).filter_by(id=d['id']).first()
        """------------------------------------------------------------"""
        
        """Se crea objeto y cambia de estado """
        itemeDelete=DBSession.query(Item).filter_by(id=d['id']).first()
        itemeDelete.estado="borrado"
        itemeDelete.ultimaversion=0
        
        DBSession.add(itemeDelete)
        
        """---------Se borra las relaciones del Item Borrado--------------"""
        
        relaciones= DBSession.query(RelacionItem).filter((RelacionItem.idItem1==d['id']) | (RelacionItem.idItem2==d['id'])).all()
        
        longitud=len(relaciones)
        log.debug("longitud: %s" %longitud)
        for x in range(longitud):
            log.debug("relaciones: %s" %relaciones[x])
            DBSession.delete(relaciones[x])
        
        """---------------------------------------------------------------"""
        
        #self.provider.delete(self.model, d)
        
        #self.provider.delete(self.model, d)
        
        #redirect('./' + '../' * (len(pks) - 1))
        raise redirect('/item/?fid='+str(idfase[0]))

    @expose('tgext.crud.templates.get_delete')
    def get_delete(self, *args, **kw):
        """This is the code that creates a confirm_delete page"""
        return dict(args=args)

