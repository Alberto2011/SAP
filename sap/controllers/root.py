# -*- coding: utf-8 -*-
"""Main Controller"""

from tg import expose, flash, require, url, request, redirect,response
from pylons.i18n import ugettext as _, lazy_ugettext as l_
#from tgext.admin.tgadminconfig import TGAdminConfig
from sap.widgets.administrar.tgadminconfig import TGAdminConfig
#from tgext.admin.controller import AdminController
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
    """
    The root controller for the SAP application.

    All the other controllers and WSGI applications should be mounted on this
    controller. For example::

        panel = ControlPanelController()
        another_app = AnotherWSGIApplication()

    Keep in mind that WSGI applications shouldn't be mounted directly: They
    must be wrapped around with :class:`tg.controllers.WSGIAppController`.

    """
            
    
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
        
        
        iid=DBSession.query(Adjuntos.idItem).filter_by(id=fileid).first()
        
        try:
            userfile = DBSession.query(Adjuntos).filter_by(id=fileid).one()
        except:
            return redirect("../../adjuntos/new/?iid="+str(iid[0]) )
        DBSession.delete(userfile)
        return redirect("../../adjuntos/new/?iid="+str(iid[0]))



    """-----------------------------------FIN ADJUNTOS----------------------------- """ 





























    
    @expose('sap.templates.desarrollar.elegirtipo.new')
    def elegirtipo(self,**kw):
        
        tmpl_context.form = create_elegirtipo_form
        
        
        
        if len(kw)>1:
            #return dict(modelname='Item',page='ToscaSample New Movie', tid=kw['tipoitem'] )
            redirect('../item/new/?tid=' + str(kw['tipoitem']))
        else:
            tipoitem = [x for x in (DBSession.query(TipoDeItem.id, TipoDeItem.nombre).filter_by(idFase=kw['fid']))]
            
            return dict(tipoitem_options=tipoitem)
        
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
    @expose()
    def calcularimpacto(self,**kw):
        """ids[] es un vector en el cual se guardaran los 'id' """
        ids=[]
        ids.append(int(kw['iid']))
        impacto = 0
        
        self.recorrerArbol(ids, int(kw['iid']))
        
        idsLong = len(ids)
        
        for x in range(idsLong):
            complejidad = DBSession.query(Item.complejidad).filter_by(id = int(ids[x]), ultimaversion=1).first()
            if complejidad != None:
                impacto = impacto + complejidad[0]
        
        fid=DBSession.query(Item.idFase, Item.nombre).filter_by(id=kw['iid']).first()
        flash("El impacto de modificar el item \"" +str(fid[1]) +"\" es: "+ str(impacto))
        redirect('/item/?fid='+str(fid[0]))
    
    
    """------------------------------ Fin Calculo de Impacto--------------------------- """
    
    
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