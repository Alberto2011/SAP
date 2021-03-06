"""
"""
from sap.model import DeclarativeBase, metadata, DBSession
from sap.model.item import Item
from sap.model.campos import Campos
from sap.model.detalleitem import DetalleItem
from sap.model.adjuntos import Adjuntos
from sap.model.relacion_item import RelacionItem

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

####
import logging

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

    @expose('sap.templates.desarrollar.detalleitem.edit')
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
    @expose('sap.templates.desarrollar.detalleitem.new')
    def new(self,iid=None ,*args, **kw):
        
        """Se obtiene el id del tipo de item elegido para el item"""
        idtipo=DBSession.query(Item.idTipoDeItem).filter_by(id=iid).first()
        
        atributos= [x for x in (DBSession.query(Campos.nombre, Campos.nombre).filter_by(idTipoDeItem=idtipo))]
        
        
        
        tmpl_context.widget = self.new_form
        return dict(value={'iditem':iid}, model=self.model.__name__, atributos_options=atributos)

    @catch_errors(errors, error_handler=new)
    @expose()
    @registered_validate(error_handler=new)
    def post(self, *args, **kw):
        
        
        
        yaExiste= DBSession.query(DetalleItem.nombrecampo).filter_by(nombrecampo=kw['nombrecampo'],iditem=kw['iditem']).first()
        
        #log.debug("yaExite: %s" %yaExite)
        #longitud= len(yaExite)
        #log.debug("longitud= %s" %longitud)
        
        if yaExiste == None:
            self.provider.create(self.model, params=kw)
        else:
            flash("Atributo cargado", 'error')
            redirect('/detalleitem/new/?iid='+ kw['iditem'])
       
       
               
        raise redirect('/detalleitem/?iid='+ kw['iditem'])
    @expose()
    @registered_validate(error_handler=edit)
    @catch_errors(errors, error_handler=edit)
    def put(self, *args, **kw):
        """update"""
        pks = self.provider.get_primary_fields(self.model)
        for i, pk in enumerate(pks):
            if pk not in kw and i < len(args):
                kw[pk] = args[i]

        #self.provider.update(self.model, params=kw)
        
        log.debug('detalleEditado: %s' %kw)
        detalleitem = DBSession.query(DetalleItem).filter_by(id=kw['id']).first()
        
        if str(detalleitem.tipo).__eq__('integer'):
            try:
                int(kw['valor'])
            except:
                flash('\"' + str(detalleitem.nombrecampo) + '\". Debe ingresar un entero', 'error')
                redirect('../'+kw['id']+'/edit')
        elif str(detalleitem.tipo).__eq__('date'):
            """False = fecha no valida
                True = fecha valida"""
            if not (self.fechaValida(kw['valor'])):
                flash('\"' + str(detalleitem.nombrecampo) + '\" Fecha no valida. Formato: dd/mm/aaaa', 'error')
                redirect('../'+kw['id']+'/edit')
        else:
            if kw['valor'].__eq__(''):
                flash('\"' + str(detalleitem.nombrecampo) + '\" no puede ser vacio', 'error')
                redirect('../'+kw['id']+'/edit')
                
        """-----------Se obtiene el ID item a editado-------------"""
        iid=DBSession.query(DetalleItem.iditem).filter_by(id=kw[pk]).first()
        
        """Se crea un nuevo item"""
        itemeditado=DBSession.query(Item).filter_by(id=iid).first()
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
            
            if str(objeto.id)==str(kw[pk]):
                nuevoDetalle.valor=kw['valor']
            else:
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
        relaciones = DBSession.query(RelacionItem.idItem1,RelacionItem.idItem2).filter((RelacionItem.idItem2==itemeditado.id) | (RelacionItem.idItem1==itemeditado.id)).all()
        longitud = len(relaciones)
        newRelation=RelacionItem()
        for x in range(longitud):
            if int(itemeditado.id) == int(relaciones[x][0]):
                newRelation.idItem1=int(itemnuevo.id)
                newRelation.idItem2=relaciones[x][1]
                DBSession.add(newRelation)
                #self.provider.create(RelacionItem, params=newRelation)
            elif int(itemeditado.id) == int(relaciones[x][1]):
                newRelation.idItem1=relaciones[x][0]
                newRelation.idItem2=int(itemnuevo.id)
                DBSession.add(newRelation)
        
        
        #detalleitem/?iid=113
        
        redirect('../?iid=' + str(itemnuevo.id) )

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

    def fechaValida (self, fecha):
        if fecha.__eq__(''):
            return False
        
        longfecha = len(fecha)
        
        if longfecha != 10:
            return False
        
        if str(fecha[2]) != '/':
            return False
        
        if str(fecha[5]) != '/':
            return False
        
        dia = fecha[0] + fecha[1]
        mes = fecha [3] + fecha [4]
        anho = fecha [6] + fecha [7] + fecha [8] + fecha [9]
        
        try:
            dia = int(dia)
            mes = int(mes)
            anho = int(anho)
        except:
            return False

        meses = {'1':31, '2':28, '3':31, '4':30, '5':31, '6':30, 
                 '7':31, '8':31, '9':30, '10':31, '11':30, '12':31}
        
        if 1900 < anho < 9999:
            if (anho % 4) == 0:
                meses['2'] = 29
            
            if 0 < mes < 13:
                if 0 < dia <= meses[str(mes)]:
                    return True
                else:
                    return False
            else:
                return False
        else:
            return False