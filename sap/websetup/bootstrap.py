# -*- coding: utf-8 -*-
"""Setup the SAP application"""

import logging
from tg import config
from sap import model

import transaction


def bootstrap(command, conf, vars):
    """Place any commands to setup sap here"""

    # <websetup.bootstrap.before.auth
    from sqlalchemy.exc import IntegrityError
    try:
        u = model.User()
        u.user_name = u'manager'
        u.display_name = u'Example manager'
        u.email_address = u'manager@somedomain.com'
        u.password = u'managepass'
    
        model.DBSession.add(u)
    
        g = model.Group()
        g.group_name = u'managers'
        g.display_name = u'Managers Group'
    
        g.users.append(u)
    
        model.DBSession.add(g)
        ######
        g1 = model.Group()
        g1.group_name = u'lider'
        g1.display_name = u'lider'
    
        #g1.users.append(u)
    
        model.DBSession.add(g1)
        ######
    
        p = model.Permission()
        p.permission_name = u'manage'
        p.description = u'This permission give an administrative right to the bearer'
        p.groups.append(g)
    
        model.DBSession.add(p)

               
        p1 = model.Permission()
        p1.permission_name = u'configurar'
        p1.description = u'configurar'
        p1.groups.append(g1)
        model.DBSession.add(p1)

        p2 = model.Permission()
        p2.permission_name = u'desarrollar'
        p2.description = u'desarrollar'
        p2.groups.append(g1)
        model.DBSession.add(p2)
        
        p3 = model.Permission()
        p3.permission_name = u'ver_item'
        p3.description = u'Ver Item'
        p3.groups.append(g1)
        model.DBSession.add(p3)
        
        p4 = model.Permission()
        p4.permission_name = u'crear_item'
        p4.description = u'Crear Item'
        p4.groups.append(g1)
        model.DBSession.add(p4)
            
        p5 = model.Permission()
        p5.permission_name = u'editar_item'
        p5.description = u'Editar Item'
        p5.groups.append(g1)
        model.DBSession.add(p5)
        
        p6 = model.Permission()
        p6.permission_name = u'borrar_item'
        p6.description = u'Borrar Item'
        p6.groups.append(g1)
        model.DBSession.add(p6)
        
        p7 = model.Permission()
        p7.permission_name = u'revertir_item'
        p7.description = u'Revertir Item'
        p7.groups.append(g1)
        model.DBSession.add(p7)
        
        p8 = model.Permission()
        p8.permission_name = u'revivir_item'
        p8.description = u'Revivir Item'
        p8.groups.append(g1)
        model.DBSession.add(p8)
        
        p9 = model.Permission()
        p9.permission_name = u'abm_adjuntos'
        p9.description = u'Alta Baja Modificacion Adjuntos'
        p9.groups.append(g1)
        model.DBSession.add(p9)
        
        p10 = model.Permission()
        p10.permission_name = u'aprobar_item'
        p10.description = u'Aprobar Item'
        p10.groups.append(g1)
        model.DBSession.add(p10)
        
        p11 = model.Permission()
        p11.permission_name = u'crear_relaciones'
        p11.description = u'Crear Relaciones'
        p11.groups.append(g1)
        model.DBSession.add(p11)
        
        p12 = model.Permission()
        p12.permission_name = u'crear_linea_base'
        p12.description = u'Crear Linea Base'
        p12.groups.append(g1)
        model.DBSession.add(p12)
        
        p13 = model.Permission()
        p13.permission_name = u'abrir_linea_base'
        p13.description = u'Abrir Linea Base'
        p13.groups.append(g1)
        model.DBSession.add(p13)
        
        model.DBSession.flush()
        transaction.commit()
    except IntegrityError:
        print 'Warning, there was a problem adding your auth data, it may have already been added:'
        import traceback
        print traceback.format_exc()
        transaction.abort()
        print 'Continuing with bootstrapping...'
        

    # <websetup.bootstrap.after.auth>
