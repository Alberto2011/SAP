from sap.model import DeclarativeBase, metadata, DBSession
from tg.decorators import without_trailing_slash, with_trailing_slash, paginate
from tw.core import WidgetsList
from tw.forms import CheckBoxList,TableForm, TextField, CalendarDatePicker, SingleSelectField, TextArea
from formencode.validators import Int, NotEmpty, DateConverter, DateValidator
from sprox.tablebase import TableBase
from sprox.formbase import EditableForm, AddRecordForm
from sap.widgets.administrar.adminfillerbase import TableFiller, EditFormFiller, EditFormFiller
from sap.model.proyecto import Proyecto
from tw.api import WidgetsList
from tw.forms import (TableForm, CalendarDatePicker, Spacer, SingleSelectField, TextField, TextArea,SubmitButton)
from tgext.crud import CrudRestController
from sap.model.proyecto import Proyecto
from sap.controllers.root import *
from sap.model.auth import *





from tgext.admin.config import AdminConfig, CrudRestControllerConfig
from tg.decorators import without_trailing_slash, with_trailing_slash, paginate
from sprox.formbase import AddRecordForm
from formencode import Schema
from formencode.validators import FieldsMatch
from tw.forms import PasswordField, TextField
from sap.model.auth import *
from sprox.tablebase import TableBase
from sprox.fillerbase import TableFiller

form_validator =  Schema(chained_validators=(FieldsMatch('password',
                                                         'verify_password',
                                                         messages={'invalidNoMatch':
                                                         'Passwords do not match'}),))
class UserTableFormType(TableBase):
    __model__= User

class UserTableFillerType(TableFiller):
    __model__ = User

class UserCrudConfig(CrudRestControllerConfig):
    table_type = UserTableFormType
    table_filler_type = UserTableFillerType
    


class MyUserConfig(AdminConfig):
    user = UserCrudConfig
    """
    @with_trailing_slash
    @expose("sap.templates.configurar.proyecto.get_all")
    @expose('json')
    @paginate('value_list', items_per_page=7)
    def get_all(self, *args, **kw):
        return super(MyUserConfig, self).get_all(*args, **kw)
    """