# -*- coding: utf-8 -*-
""" 
@author José Chavéz.
@author Alberto Capli.
@author Nora González.
"""

from repoze.what.predicates import *
#from tw.forms.validators import Int, NotEmpty, DateConverter
from sap.model.campos import Campos
from sap.model import DeclarativeBase, metadata, DBSession
from tg.decorators import without_trailing_slash, with_trailing_slash, paginate
from tw.core import WidgetsList
from tw.forms import Form, CheckBoxList,TableForm, TextField, CalendarDatePicker, SingleSelectField, TextArea, FormField, ContainerMixin

"""validadores"""
from formencode.validators import Int, NotEmpty, DateConverter, DateValidator
#from formencode import validators
from formencode.api import FancyValidator
from formencode.api import Invalid
import tw.forms as twf

from sprox.tablebase import TableBase
from sprox.formbase import EditableForm, AddRecordForm
from sap.widgets.administrar.adminfillerbase import TableFiller, EditFormFiller, EditFormFiller
from tw.api import WidgetsList
from tw.forms import (TableForm, CalendarDatePicker, Spacer,HiddenField, SingleSelectField, TextField, TextArea,SubmitButton)
#from tgext.crud import CrudRestController
from sap.widgets.desarrollar.item.controller import CrudRestController
from sap.model.item import Item
from sap.model.fase import Fase
from sap.model.proyecto import Proyecto
from sap.model.tipodeitem import TipoDeItem
from sap.model.campos import Campos
from sap.model.lineabase import LineaBase
from sap.model.detalleitem import DetalleItem

##################################################
try:
    import tw.dojo
    from sprox.dojo.tablebase import DojoTableBase
    from sprox.dojo.fillerbase import DojoTableFiller
    from sprox.dojo.formbase import DojoAddRecordForm, DojoEditableForm
    dojo_loaded = True
except ImportError:
    pass

try:
    import tw.jquery
    from sprox.jquery.tablebase import JQueryTableBase
    from sprox.jquery.fillerbase import JQueryTableFiller
#    from sprox.jquery.formbase import DojoAddRecordForm, DojoEditableForm
    jquery_loaded = True
except ImportError:
    pass


#from sap.controllers.root import *
from tg import expose, flash, redirect, tmpl_context


from sap.model.auth import *
####
import logging

from repoze.what.predicates import has_permission 
log = logging.getLogger(__name__)

####



class ItemTable(TableBase):
    __model__ = Item
    __omit_fields__ = ['id', 'nrohistorial','ultimaversion', 'idTipoDeItem']
item_table = ItemTable(DBSession) 



class ItemTableFiller(TableFiller):

    __model__ = Item

    def __actions__(self, obj):
        """Override this function to define how action links should be displayed for the given record."""
        primary_fields = self.__provider__.get_primary_fields(self.__entity__)
        pklist = '/'.join(map(lambda x: str(getattr(obj, x)), primary_fields))
        #if has_permission('manage'):############
        
        estadoItem = DBSession.query(Item.estado).filter_by(id = pklist).first() 
        fase = DBSession.query(Item.idFase).filter_by(id = pklist).first()
        proyecto = DBSession.query(Fase.idproyec).filter_by(id = fase).first()
        estadoProy = DBSession.query(Proyecto.estado).filter_by(id = proyecto).first()
        nrohistorial=DBSession.query(Item.nrohistorial).filter_by(id=pklist).first()
        item = DBSession.query(Item).filter_by(id=pklist).first()
        lineabase = DBSession.query(LineaBase).filter_by(id=item.idLineaBase).first()
        
        value='<div>'
        
        aprobar_item='<div><a class="loginlogout" href="/aprobaritem/?iid='+pklist+ '">Aprobar Item</a></div><br/>'
        revertir='<div><a class="loginlogout" href="/revertir/?hid='+str(nrohistorial[0])+'">Historial</a></div><br/>'
        detalle='<div><a class="loginlogout" href="/detalleitem/?iid='+pklist+'">  Detalle</a></div><br/>'
        ver_relaciones='<div><a class="loginlogout" href="/relacionitem/?iid='+pklist+'">Ver relaciones</a></div><br/>'
        crear_relaciones_linea_base='<div><a class="loginlogout" href="/abrirlineabaserelacion/?iid='+pklist+'">Crear relaciones</a></div><br/>'
        crear_relaciones='<div><a class="loginlogout" href="/relacionitem/new/?iid='+pklist+'">Crear relaciones</a></div><br/>'
        calcular_impacto='<div><a class="loginlogout" href="/calcularimpacto/?iid='+pklist+ '">  CalcularImpacto</a></div><br/>'
        adjuntos='<div><a class="loginlogout" href="/adjuntos/new/?iid='+pklist+'">  Adjuntos</a></div><br/>'
        editar_linea_base='<div><a class="edit_link" href="/abrirlineabase/?iid='+pklist+'" style="text-decoration:none">edit</a></div>'
        editar='<div><a class="edit_link" href="'+pklist+'/edit" style="text-decoration:none">edit</a></div>'
        borrar='<div><form method="POST" action="'+pklist+'" class="button-to">'\
                '<input type="hidden" name="_method" value="DELETE" />'\
                '<input class="delete-button" onclick="return confirm(\'Are you sure?\');" value="delete" type="submit" '\
                'style="background-color: transparent; float:left; border:0; color: #286571; display: inline; margin: 0; padding: 0;"/>'\
                '</form></div>'
        
        if str(estadoProy[0]).__eq__("iniciado"):
            if lineabase != None:
                if str(lineabase.estado).__eq__("cerrada"):
                    value = value + revertir + detalle + ver_relaciones + crear_relaciones_linea_base +\
                            calcular_impacto + editar
                elif str(lineabase.estado).__eq__("comprometida"):
                    if str(estadoItem[0]).__eq__("aprobado"):
                        value = value + revertir + detalle + ver_relaciones + crear_relaciones_linea_base +\
                            calcular_impacto + editar
                    else:
                        value = value + aprobar_item + revertir + detalle + ver_relaciones +\
                        crear_relaciones_linea_base + calcular_impacto + editar
                else:
                    if str(estadoItem[0]).__eq__("aprobado"):
                        value = value + revertir + detalle + ver_relaciones + crear_relaciones +\
                            calcular_impacto + adjuntos + editar + borrar
                    else:
                        value = value + aprobar_item + revertir + detalle + ver_relaciones + crear_relaciones +\
                            calcular_impacto + adjuntos + editar + borrar
            else:
                if str(estadoItem[0]).__eq__("aprobado"):
                    value = value + revertir + detalle + ver_relaciones + crear_relaciones +\
                            calcular_impacto + adjuntos + editar + borrar
                else:
                    value = value + aprobar_item + revertir + detalle + ver_relaciones + crear_relaciones +\
                            calcular_impacto + adjuntos + editar + borrar
                        
        value=value+'</div>'
        return value
    

    def _do_get_provider_count_and_objs(self, **kw):
        limit = kw.get('limit', None)
        offset = kw.get('offset', None)
        order_by = kw.get('order_by', None)
        desc = kw.get('desc', False)
        
        
        
        if len(kw) > 0:
            
                    
                    
            if len(kw) > 1:
                #objs = DBSession.query(self.__entity__).filter((Fase.idproyec==kw['pid']) & (Fase.nombre.ilike('%'+str(kw['buscar'])+'%'))).all()
                objs = DBSession.query(self.__entity__).\
                    filter((Item.idFase==kw['fid']) &
                        (Item.ultimaversion==1) &
                        (Item.nombre.ilike('%'+str(kw['buscar'])+'%'))&
                        (Item.estado!="borrado")).order_by(Item.nrohistorial).all()    
                
                
            else:
                objs = DBSession.query(self.__entity__).\
                    filter((Item.idFase==kw['fid']) &
                        (Item.ultimaversion==1) &
                        (Item.estado!="borrado")).order_by(Item.nrohistorial).all()        
            
            
                    
        else:
            objs = DBSession.query(self.__entity__).all()


        count = len(objs)
        self.__count__ = count
        return count, objs    


item_table_filler = ItemTableFiller(DBSession)



class ItemForm(TableForm):
#class ItemForm(DojoAddRecordForm):
        #__model__ = Item
        #__omit_fields__ = ['id','idTipoDeItem','idFase','idLineaBase','version', 'nrohistorial','ultimaversion', 'estado']
        tiid=0
        #campotipo= DBSession.query(Campos.tipoDeDato, Campos.nombre).filter_by(idTipoDeItem=13).all()
        comlejidadoptions= [(1, 'Muy Baja (1)'), (2, 'Baja (2)'), (3, 'Media (3)'), (4, 'Alta (4)'), (5, 'Muy Alta (5)')]
        
                         
        #campo_options=[]
        
        #campotipo=campo_options
                
        __require_fields__=['nombre']
        
        
        fields = [
        
        
        TextField('nombre', label_text='Nombre', disabled=True),
   	    Spacer(),
		HiddenField('idFase', label_text='idFase'),
        HiddenField('version', label_text='version'),
        HiddenField('estado', label_text='estado'),
        SingleSelectField('complejidad', options=comlejidadoptions, label_text='Complejidad'),
        Spacer(),
        #CalendarDatePicker('fechaCreacion', date_format='%d-%m-%y'),
        #Spacer(),
        HiddenField('nrohistorial', label_text='nrohistorial'),
        #SingleSelectField('idTipoDeItem', options=tipo_options),
        HiddenField('idTipoDeItem', label_text='idTipoDeItem'),
		]
        #log.debug(campotipo)
        """
        
        for ct in campotipo:
            #log.debug(ct[1])
            campo1 = TextField(ct[1], label_text= ct[1])
            fields.append(campo1)
            
        """
        submit_text = 'Crear Item'
       
item_add_form = ItemForm('create_item_form')



        
class ItemEditForm(EditableForm):
    __model__ = Item
    __disable_fields__=['nombre']
    comlejidadoptions= [(1, 'Muy Baja (1)'), (2, 'Baja (2)'), (3, 'Media (3)'), (4, 'Alta (4)'), (5, 'Muy Alta (5)')]
    __field_widgets__ = {'nombre':HiddenField('nombre', label_text='Nombre'),
                         'complejidad':SingleSelectField('complejidad', options=comlejidadoptions, label_text='complejidad')}
    
    __omit_fields__ = ['id','idTipoDeItem','idFase','fechaCreacion','idLineaBase','version', 'nrohistorial','ultimaversion', 'estado']


item_edit_form = ItemEditForm(DBSession)



class ItemEditFiller(EditFormFiller):
    __model__ = Item
item_edit_filler = ItemEditFiller(DBSession)
    
   


class ItemController(CrudRestController):
    
        
    allow_only = All(not_anonymous(msg='Acceso denegado. Usted no se ha logueado!'),
                         has_any_permission('administrar',
                                            'configurar',
                                            'desarrollar',
                                            msg='Usted no posee los permisos para ingresar a esta pagina!'))
 
    
    	
    model = Item
    table = item_table
    table_filler = item_table_filler
    edit_filler = item_edit_filler
    edit_form = item_edit_form
    
    @with_trailing_slash
    @expose("sap.templates.desarrollar.item.get_all")
    @expose('json')
    @paginate('value_list', items_per_page=50)
    def get_all(self, fid=None,*args, **kw):
        kw['fid']=fid
        result=super(ItemController, self).get_all(*args, **kw)
        result['fid']=fid
        #log.debug('resultGetAll=%s' %result)
        return result
        #return super(ItemController, self).get_all(*args, **kw)
    

    @without_trailing_slash
    #@expose('tgext.crud.templates.new')
    @expose('sap.templates.desarrollar.item.new')
    def new(self,tid=None ,*args, **kw):
        """Display a page to show a new record."""
        

            
        fid= DBSession.query(TipoDeItem.idFase).filter_by(id=tid).first()
    
        comlejidadoptions= [(1, 'Muy Baja (1)'), (2, 'Baja (2)'), (3, 'Media (3)'), (4, 'Alta (4)'), (5, 'Muy Alta (5)')]
        
        campos = [TextField('nombre', label_text='Nombre', disabled=True),
                  Spacer(),
                  HiddenField('idFase', label_text='idFase'),
                  HiddenField('version', label_text='version'),
                  HiddenField('estado', label_text='estado'),
                  SingleSelectField('complejidad', options=comlejidadoptions, label_text='complejidad'),
                  Spacer(),
                  HiddenField('nrohistorial', label_text='nrohistorial'),
                  HiddenField('idTipoDeItem', label_text='idTipoDeItem'),
                  ]
        
        camponombre= DBSession.query(Campos.tipoDeDato, Campos.nombre, Campos.id).filter_by(idTipoDeItem=tid).all()

        for ct in camponombre:
            #log.debug(ct[1])
            if str(ct[0]).__eq__('date'):
                campo1 = CalendarDatePicker(str(ct[2]), label_text= ct[1]+' ('+ct[0]+')', date_format= '%d/%m/%Y')
            else:
                campo1 = TextField(str(ct[2]), label_text= ct[1]+' ('+ct[0]+')')
            
            campos.append(campo1)
            campos.append(Spacer())
        
        #self.new_form = TableForm('tf', fields=campos, submit_text='Guardar')
        #tmpl_context.widget = self.new_form
        
        tmpl_context.widget = TableForm('create_table_form', fields=campos, submit_text='Guardar')
        
        
        
        """El tipo de Item elegido es extraido para  asignar su nombre al item"""
        tipo_item_elegido=DBSession.query(TipoDeItem).filter_by(id=tid).first()
        
        nrogenerado = tipo_item_elegido.nrogeneracion + 1
        
        if int(nrogenerado) < 10:
            nombreitem=tipo_item_elegido.nombre + '-00' + str(nrogenerado)
        elif int(nrogenerado) < 100:
            nombreitem=tipo_item_elegido.nombre + '-0' + str(nrogenerado)
        else:
            nombreitem=tipo_item_elegido.nombre + '-' + str(nrogenerado)
            
        return dict(value={'idTipoDeItem':tid, 'idFase':fid, 'nombre':nombreitem },model=self.model.__name__)
    
    @expose()
    def post(self, *args, **kw):
        """extrae el numhistorial ordenado sin repetir, para luego tomar el mayor valor y asi 
        poder asignarle un numhistorial mayor
        """
        
        campotipo= DBSession.query(Campos.tipoDeDato, Campos.nombre, Campos.id).filter_by(idTipoDeItem=kw['idTipoDeItem']).all()
        #log.debug('a %s', kw)

        for ct in campotipo:
            if str(ct[0]).__eq__('integer'):
                try:
                    int(kw[str(ct[2])])
                except:
                    flash('\"' + str(ct[1]) + '\". Debe ingresar un entero', 'error')
                    redirect('./new/?tid='+kw['idTipoDeItem'])
            elif str(ct[0]).__eq__('date'):
                """False = fecha no valida
                    True = fecha valida"""
                if not (self.fechaValida(kw[str(ct[2])])):
                    flash('\"' + str(ct[1]) + '\" Fecha no valida. Formato: dd/mm/aaaa', 'error')
                    redirect('./new/?tid='+kw['idTipoDeItem'])
            else:
                if kw[str(ct[2])].__eq__(''):
                    flash('\"' + str(ct[1]) + '\" no puede ser vacio', 'error')
                    redirect('./new/?tid='+kw['idTipoDeItem'])
        
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
        
        tipo_item_elegido=DBSession.query(TipoDeItem).filter_by(id=kw['idTipoDeItem']).first()
        kw1= {}
        nrogenerado = tipo_item_elegido.nrogeneracion + 1
        
        if int(nrogenerado) < 10:
            nombreitem=tipo_item_elegido.nombre + '-00' + str(nrogenerado)
        elif int(nrogenerado) < 100:
            nombreitem=tipo_item_elegido.nombre + '-0' + str(nrogenerado)
        else:
            nombreitem=tipo_item_elegido.nombre + '-' + str(nrogenerado)
            
        kw1['nombre'] = nombreitem
        kw1['idTipoDeItem'] = kw['idTipoDeItem']
        kw1['idFase'] = kw['idFase']
        kw1['complejidad'] = kw['complejidad']
        kw1['nrohistorial'] = kw['nrohistorial']
        
        itemnuevo = self.provider.create(self.model, params=kw1)
        tipo_item_elegido.nrogeneracion= tipo_item_elegido.nrogeneracion+1
        
        for ct in campotipo:
            detalle = {}
            detalle['tipo'] = ct[0]
            detalle['nombrecampo'] = ct[1]
            detalle['valor'] = kw[str(ct[2])]
            detalle['iditem'] = itemnuevo.id
            self.provider.create(DetalleItem, params=detalle)
        
        raise redirect('./?fid='+kw['idFase'])

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
        

