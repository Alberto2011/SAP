# -*- coding: utf-8 -*-
""" Clase RootController
@author José Chavéz.
@author Alberto Capli.
@author Nora González.
"""
"""Main Controller"""
import pydot
from tg import expose, flash, require, url, request, redirect,response
from pylons.i18n import ugettext as _, lazy_ugettext as l_
from sap.widgets.administrar.tgadminconfig import TGAdminConfig
from sap.widgets.administrar.controllerUserGroupPremission import AdminController 
from repoze.what import predicates
from sap.lib.base import BaseController
from sap.model import DBSession, metadata
from sap import model
from sap.controllers.secure import SecureController

from sap.controllers.error import ErrorController
from tg import tmpl_context
from tgext.crud import CrudRestController

from sap.widgets.movie_form import create_movie_form
from sap.model import *
from sap.widgets.admin import *
from sap.widgets.usuario import *
from sap.controllers.usuario import UsuarioController
from repoze.what.predicates import has_permission
#from sap.widgets.administrar.proyecto import ProyectoController

from sap.widgets.administrar.proyecto import *
from sap.widgets.configurar.proyecto.proyecto import ProyectoConfig
from sap.widgets.configurar.fase.fase import FaseController
from sap.widgets.configurar.tipodeitem.tipodeitem import TipoDeItemController
from sap.widgets.configurar.campos.campos import CamposController
from sap.widgets.configurar.proyfaseusuario.proyfaseusuario import ProyFaseUsuarioController
#from sap.widgets.configurar.usuario import MyUserConfig



from sap.widgets.desarrollar.proyecto.proyecto import ProyectoDesarrollo
from sap.widgets.desarrollar.fase.fase import FaseControllerD

from sap.widgets.desarrollar.item.item import ItemController


from sap.widgets.desarrollar.adjuntos.adjuntos import AdjuntosController
from sap.widgets.desarrollar.lineabase.lineabase import LineaBaseController
from sap.widgets.desarrollar.relacionitem.relacionitem import RelacionItemController
from sap.widgets.desarrollar.detalleitem.detalleitem import DetalleItemController
from sap.widgets.desarrollar.elegirtipo.elegirtipo import *
from sap.widgets.desarrollar.abrirlineabase.abrirlineabase import *
from sap.widgets.desarrollar.abrirlineabaserelacion.abrirlineabaserelacion import *
from sap.widgets.desarrollar.itemlineabase.itemlineabase import ItemLineaBaseController
from sap.widgets.desarrollar.revertir.revertir import RevertirController
from sap.widgets.desarrollar.revivir.revivir import RevivirController
from sap.widgets.desarrollar.adjuntos.adjuntos import AdjuntosController
from sap.widgets.configurar.importartipodeitem.importartipodeitem import ImportarTipoDeItemController
from sap.controllers.error import ErrorController


from tg.controllers import CUSTOM_CONTENT_TYPE
from sap.controllers.error import ErrorController
#from sap.model.userfile import UserFile
from sap.model.adjuntos import Adjuntos




from repoze.what.predicates import *

#from sap.widgets.desarrollar.usuario import MyUserConfig
####
import logging
from repoze.what.predicates import has_permission 
log = logging.getLogger(__name__)
####


__all__ = ['RootController']


class RootController(BaseController):
              
################Administración########################    
    secc = SecureController()
    admin = AdminController(model, DBSession, config_type=TGAdminConfig)
    
    #admin = AdminController(model, DBSession, config_type=MyAdminConfig)
    error = ErrorController()
    proyectos = ProyectoController(DBSession)
    
#####################################################    
    
################Configuración##########################    
    proyectoconfig=ProyectoConfig(DBSession) 
    fase=FaseController(DBSession)
    tipodeitem=TipoDeItemController(DBSession)
    campos=CamposController(DBSession)
    proyfaseusuario=ProyFaseUsuarioController(DBSession)
    importartipodeitem=ImportarTipoDeItemController(DBSession)
#######################################################
    
##################Desarrollo###########################
    
    proyectodesarrollo=ProyectoDesarrollo(DBSession) 
    fasedesarrollo=FaseControllerD(DBSession)
    item=ItemController(DBSession)
    adjuntos=AdjuntosController(DBSession)
    lineabase=LineaBaseController(DBSession)
    relacionitem=RelacionItemController(DBSession)
    detalleitem=DetalleItemController(DBSession)
    itemlineabase=ItemLineaBaseController(DBSession)
    revertir=RevertirController(DBSession)
    revivir=RevivirController(DBSession)
    

#######################################################


    """-----------------------------Adjuntos------------------------------"""
    error = ErrorController()

    @expose('sap.templates.desarrollar.fileupload.index')
    def indexx(self):
        current_files = DBSession.query(UserFile).all()
        return dict(current_files=current_files)
    
    """    
    @expose()
    def save(self,**kw ):
        
        
        idItem=kw['idItem']
        userfile=kw['userfile']
        
        log.debug("userfile: %s" %userfile)
        forbidden_files = [".js", ".htm", ".html"]
        for forbidden_file in forbidden_files:
            if userfile.filename.find(forbidden_file) != -1:
                return redirect("../../adjuntos/new")
        filecontent = userfile.file.read()
        new_file = Adjuntos(filename=userfile.filename, filecontent=filecontent,idItem=idItem)
        archivoguardado=DBSession.add(new_file)
        DBSession.flush()
        log.debug("archivoguardado: %s" %archivoguardado)
        
        redirect("../../adjuntos/new")
        
      """  
        
        
    
    @expose(content_type=CUSTOM_CONTENT_TYPE)
    def view(self, fileid):
        iid=DBSession.query(Adjuntos.idItem).filter_by(id=fileid).first()
        log.debug("iidssss: %s" %iid)
        try:
            userfile = DBSession.query(Adjuntos).filter_by(id=fileid).one()
        except:
            redirect("../../adjuntos/new/adjuntos/new")
        content_types = {
            'display': {},
            'download': {'.pdf':'application/pdf', '.zip':'application/zip', '.rar':'application/x-rar-compressed','.png': 'image/jpeg', '.jpeg':'image/jpeg', '.jpg':'image/jpeg', '.gif':'image/jpeg', '.txt': 'text/plain'}
        }
        for file_type in content_types['display']:
            if userfile.filename.endswith(file_type):
                response.headers["Content-Type"] = content_types['display'][file_type]
        for file_type in content_types['download']:
            if userfile.filename.endswith(file_type):
                response.headers["Content-Type"] = content_types['download'][file_type]
                response.headers["Content-Disposition"] = 'attachment; filename="'+userfile.filename+'"'
        if userfile.filename.find(".") == -1:
            response.headers["Content-Type"] = "text/plain"
        return userfile.filecontent
    
    @expose()
    def delete(self, fileid):
        
        #log.debug("Soy Archivo Borrado")
        
        """Se extrae el ID del Item que supuestamente se borrará, para crear un nuevo Item """       
        iid=DBSession.query(Adjuntos.idItem).filter_by(id=fileid).first()

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
            nuevoDetalle.valor=objeto.valor
            nuevoDetalle.iditem=itemnuevo.id
            DBSession.add(nuevoDetalle)
                
        """Realiza copia de los adjuntos"""
        adjuntositemeditado=DBSession.query(Adjuntos).filter_by(idItem=itemeditado.id).all()
        
        for adj in adjuntositemeditado:
            log.debug("adjuntoBorraado: %s" %adj.id)
            log.debug("fileid: %s" %fileid)
   
            if str(adj.id) != str(fileid): #No se copiará el archivo "supuestamente" borrado
                log.debug("fileid2: %s" %fileid)
                itemnuevoadjunto=Adjuntos()
                itemnuevoadjunto.idItem=itemnuevo.id
                itemnuevoadjunto.filename=adj.filename
                itemnuevoadjunto.filecontent=adj.filecontent
                DBSession.add(itemnuevoadjunto)
        
 
        
        
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
        
        








        return redirect("../../adjuntos/new/?iid="+str(itemnuevo.id))



    """-----------------------------------FIN ADJUNTOS----------------------------- """ 

    
    @expose('sap.templates.desarrollar.elegirtipo.new')
    def elegirtipo(self,**kw):
        
        tmpl_context.form = create_elegirtipo_form
        
        
        
        if len(kw)>1:
            #return dict(modelname='Item',page='ToscaSample New Movie', tid=kw['tipoitem'] )
            redirect('../item/new/?tid=' + str(kw['tipoitem']))
        else:
            tipoitem = [x for x in (DBSession.query(TipoDeItem.id, TipoDeItem.nombre).filter_by(idFase=kw['fid']))]
            
            return dict(tipoitem_options=tipoitem, fid=kw['fid'])
        
#############################################################
    @expose('sap.templates.desarrollar.abrirlineabase.new')
    def abrirlineabase(self,**kw):
        
        tmpl_context.form = create_abrirlineabase_form

        if len(kw)>1:
            if (int(kw['lineaBase']) == 0):
                item = DBSession.query(Item).filter_by(id = kw['iid']).first()
                lineabase = DBSession.query(LineaBase).filter_by(id = item.idLineaBase).first()
                lineabase.estado = 'abierta'
                item.estado = 'modificado'
                listalineabase = DBSession.query(LineaBase).filter_by(idFase = item.idFase).all()
                desarrollo = True
                longitud = len(listalineabase)
                
                for x in range (longitud):
                    if str(listalineabase[x].estado).__eq__('cerrada'):
                        desarrollo = False
                        
                if desarrollo:
                    fase = DBSession.query(Fase).filter_by(id = item.idFase).first()
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
                
                flash("La linea base \"" + lineabase.nombre + "\" se ha abierto", "warning")
                redirect("../item/"+kw['iid']+'/edit')
            else:
                fid = DBSession.query(Item.idFase).filter_by(id = kw['iid']).first()
                flash("Debe abrir la linea base para editar el item", "error")
                redirect("../item/?fid="+str(fid[0]))
        else:
            lineaBase=[x for x in enumerate(('Abrir', 'No abrir'))]
            return dict(tipoitem_options=lineaBase)
   
#############################################################
    @expose('sap.templates.desarrollar.abrirlineabase.new')
    def abrirlineabaserelacion(self,**kw):
        
        tmpl_context.form = create_abrirlineabaserelacion_form

        if len(kw)>1:
            if (int(kw['lineaBase']) == 0):
                item = DBSession.query(Item).filter_by(id = kw['iid']).first()
                lineabase = DBSession.query(LineaBase).filter_by(id = item.idLineaBase).first()
                lineabase.estado = 'abierta'
                item.estado = 'modificado'
                listalineabase = DBSession.query(LineaBase).filter_by(idFase = item.idFase).all()
                desarrollo = True
                longitud = len(listalineabase)
                
                for x in range (longitud):
                    if str(listalineabase[x].estado).__eq__('cerrada'):
                        desarrollo = False
                        
                if desarrollo:
                    fase = DBSession.query(Fase).filter_by(id = item.idFase).first()
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
                
                flash("La linea base \"" + lineabase.nombre + "\" se ha abierto", "warning")
                redirect("../relacionitem/new/?iid="+kw['iid'])
            else:
                fid = DBSession.query(Item.idFase).filter_by(id = kw['iid']).first()
                flash("Debe abrir la linea base para crear relaciones", "error")
                redirect("../item/?fid="+str(fid[0]))
        else:
            lineaBase=[x for x in enumerate(('Abrir', 'No abrir'))]
            return dict(tipoitem_options=lineaBase)
   
    """------------------------------Calculo de Impacto--------------------------- """
    @expose('sap.templates.desarrollar.item.dibujar')
    def calcularimpacto(self,**kw):
        """ids[] es un vector en el cual se guardaran los 'id' """
        ids=[]
        itemraiz = DBSession.query(Item).filter_by(id=kw['iid']).first()
        ids.append(itemraiz)
        impacto = 0
        relacionesTotal = []
        
        self.recorrerArbolAtras(ids, itemraiz, relacionesTotal)
        self.recorrerArbolAdelante(ids, itemraiz, relacionesTotal)
        
        for item in ids:
            complejidad = int(item.complejidad)
            impacto = impacto + complejidad
        
        nodosporfase = []
        
        while len(ids) != 0:
            aux = []
            
            for item in ids:
                if ids[0].idFase == item.idFase:
                    aux.append(item)
                    
            for item in aux:
                ids.remove(item)
                
            nodosporfase.append(aux)
        
        self.dibujar(relacionesTotal, nodosporfase, itemraiz)
        
        flash("El impacto de modificar el item \"" +itemraiz.nombre+"\" es: "+ str(impacto))
        #redirect('/item/?fid='+str(fid[0]))
        return dict(link={'url':'/item/?fid='+str(itemraiz.idFase)})
    
    """---------------------- Recorrer Arbol Atras -------------------------------------
    Uso:
        self.recorrerArbol (ids, iid)
        ids: un vector que contiene primeramente al nodo inicial
        iid: nodo inicial
        Todos los nodos del arbol quedaran guardados en ids---------------------------"""
    def recorrerArbolAtras (self, *args):
        ids = args[0]
        itemraiz = args[1]
        relacionesTotal = args[2]

        """-------------Obtiene de la BD las relaciones actuales del nodo en cuestion---"""
        relaciones = DBSession.query(RelacionItem.idItem1,RelacionItem.idItem2).\
                        filter((RelacionItem.idItem1==itemraiz.id)).all()
        """------------------------------------------------------------------------"""
        
        for relacion in relaciones:
            itemrelacion = DBSession.query(Item).filter_by(id=relacion.idItem2).first()
            
            if itemrelacion.ultimaversion == 1:
                if (ids.count(itemrelacion) < 1):
                        ids.append(itemrelacion)
                        
                if (relacionesTotal.count(relacion) < 1):
                    relacionesTotal.append(relacion)
                self.recorrerArbolAtras(ids, itemrelacion, relacionesTotal)

    """------------------- Fin Recorrer Arbol Atras -----------------------------------"""
    
    """-------------------- Recorrer Arbol Adelante -------------------------------------
    Uso:
        self.recorrerArbol (ids, iid)
        ids: un vector que contiene primeramente al nodo inicial
        iid: nodo inicial
        Todos los nodos del arbol quedaran guardados en ids---------------------------"""
    def recorrerArbolAdelante (self, *args):
        ids = args[0]
        itemraiz = args[1]
        relacionesTotal = args[2]

        """-------------Obtiene de la BD las relaciones actuales del nodo en cuestion---"""
        relaciones = DBSession.query(RelacionItem.idItem1,RelacionItem.idItem2).\
                        filter((RelacionItem.idItem2==itemraiz.id)).all()
        """------------------------------------------------------------------------"""
        
        for relacion in relaciones:
            itemrelacion = DBSession.query(Item).filter_by(id=relacion.idItem1).first()
            
            if itemrelacion.ultimaversion == 1:
                if (ids.count(itemrelacion) < 1):
                        ids.append(itemrelacion)
                        
                if (relacionesTotal.count(relacion) < 1):
                    relacionesTotal.append(relacion)
                self.recorrerArbolAdelante(ids, itemrelacion, relacionesTotal)
        
    """---------------------- Fin Recorrer Arbol Adelante -----------------------------"""
    
    """------------------------------ Fin Calculo de Impacto--------------------------- """
    
    def dibujar(self, *args):

        """Dibuja un grafo dirigido a partir de una matriz de relaciones
        y una matriz de nodos"""
        
        relaciones=args[0]
        nodosporfase=args[1]
        itemraiz=args[2]
        
        g=self.grafo_de_relaciones(relaciones)
        
        for fase in nodosporfase:
            subg= pydot.Subgraph('', rank='same')
            nombreFase = DBSession.query(Fase.nombre).filter_by(id=fase[0].idFase).first()
            subg.add_node(pydot.Node(nombreFase[0],label=nombreFase[0],\
                                    color='white'))
            
            for nodo in fase:
                if nodo == itemraiz:
                    subg.add_node(pydot.Node(nodo.id,\
                            label=str(nodo.nombre)+"\nPeso: "+str(nodo.complejidad),\
                            color='PaleGreen3', style='filled'))
                else:
                     subg.add_node(pydot.Node(nodo.id,\
                            label=str(nodo.nombre)+"\nPeso: "+str(nodo.complejidad),\
                            color='NavajoWhite1', style='filled'))
                
            g.add_subgraph(subg)
        
        g.write_png('sap/public/images/example2_graph.png')
    
    def grafo_de_relaciones(self, edge_list, node_prefix=''):
        """Crea las relaciones en el grafo a partir de una matriz de relaciones.
        Utilizado por el metodo dibujar(self)"""
    
        graph = pydot.Dot(graph_type='digraph', rankdir='RL')
            
        for edge in edge_list:
            
            if isinstance(edge[0], str):
                src = node_prefix + edge[0]
            else:
                src = node_prefix + str(edge[0])
                
            if isinstance(edge[1], str):
                dst = node_prefix + edge[1]
            else:
                dst = node_prefix + str(edge[1])
    
            e = pydot.Edge( src, dst)
            graph.add_edge(e)
            
        return graph
    
    @expose()
    def aprobaritem(self,**kw):
        item=DBSession.query(Item).filter_by(id=kw['iid']).first()
        item.estado = 'aprobado'
        fid=DBSession.query(Item.idFase, Item.nombre).filter_by(id=kw['iid']).first()
        
        if item.idLineaBase != None:
            listaitem = DBSession.query(Item).filter_by(idLineaBase=item.idLineaBase, ultimaversion=1).all()
            longitud = len(listaitem)
            contadoraprob = 0
            modificado = False
            
            for x in range(longitud):
                #Verificar si todos los item de la linea base estan aprobados
                if str(listaitem[x].estado).__eq__('aprobado'):
                    contadoraprob = contadoraprob + 1
                #Verificar si existe por lo menos un item en estado modificado
                elif str(listaitem[x].estado).__eq__('modificado'):
                    modificado = True
            
            #Entra si todos los item de la linea base estan aprobados
            if contadoraprob == longitud:
                 lineabase = DBSession.query(LineaBase).filter_by(id=item.idLineaBase).first()
                 lineabase.estado = 'cerrada'
                 
                 cantItemLB = DBSession.query(Item).filter_by(idLineaBase=lineabase.id, ultimaversion=1).all()
                 cantItemFase = DBSession.query(Item).filter_by(idFase=fid[0], ultimaversion=1).all()
                 
                 fase = DBSession.query(Fase).filter_by(id=fid[0]).first()
                 
                 if len(cantItemLB) == len(cantItemFase):
                     fase.estado = 'lineaBaseTotal'
                     flash("El item \"" +str(fid[1]) +"\" fue aprobado, "\
                       "la linea base \"" + lineabase.nombre + "\" fue cerrada y "\
                       "la fase \""+fase.nombre+"\" paso al estado de \"Linea Base Total\"")
                     redirect('/item/?fid='+str(fid[0]))
                 else:
                     fase.estado = 'lineaBaseParcial'
                     flash("El item \"" +str(fid[1]) +"\" fue aprobado, "\
                       "la linea base \"" + lineabase.nombre + "\" fue cerrada y "\
                       "la fase \""+fase.nombre+"\" paso al estado de \"Linea Base Parcial\"")
                     redirect('/item/?fid='+str(fid[0]))
                     
            #Entra si no existem item modificados en la linea base"""
            elif not modificado:
                lineabase = DBSession.query(LineaBase).filter_by(id=item.idLineaBase).first()
                lineabase.estado = 'comprometida'
                flash("El item \"" +str(fid[1]) +"\" fue aprobado y "\
                      "la linea base \"" + lineabase.nombre + "\" ahora esta comprometida")
                redirect('/item/?fid='+str(fid[0]))
                
        flash("El item \"" +str(fid[1]) +"\" fue aprobado")
        redirect('/item/?fid='+str(fid[0]))


    @expose('sap.templates.index')
    def index(self):
        """Handle the front-page."""
        return dict(page='index')
    

    @expose("sap.templates.configurar.adjuntos.get_all")
    def create(self, **kw):
            adjuntos = Adjuntos()
                        
            #save the filename to the database
            #adjuntos.idItem= kw['idItem']
            adjuntos.picture_filename = kw['adjuntos_filename'].filename
            #DBSession.add(adjuntos)
            DBSession.flush()
        
            """#write the picture file to the public directory
            adjuntos_path = os.path.join(adjuntos_dirname, str(adjuntos.id))
            try:
                os.makedirs(adjuntos_path)
            except OSError:
                #ignore if the folder already exists
                pass
                
            adjuntos_path = os.path.join(adjuntos_path, adjuntos.adjuntos_filename)
            f = file(adjuntos_path, "w")
            f.write(kw['adjuntos_filename'].value)
            f.close()
            """
            #flash("adjuntos was successfully created.")
            redirect("./adjuntos")


    @expose('sap.templates.user')
    def usuario(self, **kw):
        tmpl_context.form = create_user_form
        return dict(modelname='Usuario', value=kw)


    @expose('sap.templates.configurar.configuracion')
    def configuracion(self):
        """Display some information about auth* on this application."""
        return dict(page='configuracion')


    @expose('sap.templates.about')
    def about(self):
        """Handle the 'about' page."""
        return dict(page='about')

    @expose('sap.templates.environ')
    def environ(self):
        """This method showcases TG's access to the wsgi environment."""
        return dict(environment=request.environ)

    @expose('sap.templates.data')
    @expose('json')
    def data(self, **kw):
        """This method showcases how you can use the same controller for a data page and a display page"""
        return dict(params=kw)

    @expose('sap.templates.authentication')
    def auth(self):
        """Display some information about auth* on this application."""
        return dict(page='auth')

    @expose('sap.templates.index')
    @require(predicates.has_permission('manage', msg=l_('Only for managers')))
    def manage_permission_only(self, **kw):
        """Illustrate how a page for managers only works."""
        return dict(page='managers stuff')

    @expose('sap.templates.index')
    @require(predicates.is_user('editor', msg=l_('Only for the editor')))
    def editor_user_only(self, **kw):
        """Illustrate how a page exclusive for the editor works."""
        return dict(page='editor stuff')

    @expose('sap.templates.login')
    def login(self, came_from=url('/')):
        """Start the user login."""
        login_counter = request.environ['repoze.who.logins']
        if login_counter > 0:
            flash(_('Autenticacion incorrecta'), 'warning')
        return dict(page='login', login_counter=str(login_counter),
                    came_from=came_from)

    @expose()
    def post_login(self, came_from='/'):
        """
        Redirect the user to the initially requested page on successful
        authentication or redirect her back to the login page if login failed.

        """
        if not request.identity:
            login_counter = request.environ['repoze.who.logins'] + 1
            redirect('/login', came_from=came_from, __logins=login_counter)
        userid = request.identity['repoze.who.userid']
        flash(_('Bienvenido %s!') % userid)
        redirect(came_from)

    @expose()
    def post_logout(self, came_from=url('/')):
        """
        Redirect the user to the initially requested page on logout and say
        goodbye as well.

        """
        
        redirect('/login')
