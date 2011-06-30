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
        p3.permission_name = u'leer'
        p3.description = u'leer'
        p3.groups.append(g1)
        model.DBSession.add(p3)
        
        
        p4 = model.Permission()
        p4.permission_name = u'escribir'
        p4.description = u'escribir'
        p4.groups.append(g1)
        model.DBSession.add(p4)
        
      
      
        p5 = model.Permission()
        p5.permission_name = u'aprobar'
        p5.description = u'aprobar'
        p5.groups.append(g1)
        model.DBSession.add(p5)
      
      
        
        model.DBSession.flush()
        transaction.commit()
    except IntegrityError:
        print 'Warning, there was a problem adding your auth data, it may have already been added:'
        import traceback
        print traceback.format_exc()
        transaction.abort()
        print 'Continuing with bootstrapping...'
        

    # <websetup.bootstrap.after.auth>
