from sap.model import DeclarativeBase, metadata, DBSession
from tw.forms import (TableForm, CalendarDatePicker, Label,
    SingleSelectField, Spacer, TextField, TextArea)

from tg import expose,tmpl_context
from sap.model.tipodeitem import TipoDeItem
from tw.forms import CheckBoxList, CheckBox, CheckBoxTable,SingleSelectionMixin,SingleSelectField,HiddenField 


####
import logging

from repoze.what.predicates import has_permission 
log = logging.getLogger(__name__)

####
from tw.api import WidgetsList


class AbrirLineaBaseForm(TableForm):
    
    
    
    
    class fields(WidgetsList):
        tipoitem_options = []

        lineaBase = SingleSelectField(options=tipoitem_options)
        #submit =HiddenField()
        
create_abrirlineabase_form = AbrirLineaBaseForm("create_abrirlineabase_form")






