from colander import Schema, SchemaNode, String
from deform.widget import PasswordWidget
import colander
from deform import FileData
from deform.widget import FileUploadWidget, SelectWidget

class LoginSchema(Schema):
    username = SchemaNode(String(), title=u"username")
    password = SchemaNode(String(), title=u"password", widget=PasswordWidget())
    
class RegistrationSchema(LoginSchema):
    fullname = SchemaNode(String(), title=u"Full Name")
    email = SchemaNode(String(), title=u"Email")

class Store(dict):
    def preview_url(self, name):
        return ""

store = Store()

@colander.deferred
def deferred_users_validator(node, kw):
    usernames = kw.get('usernames', [])
    return SelectWidget(values=usernames)

class UploadSchema(Schema):
    username = SchemaNode(String(), title=u"Username")
    items = SchemaNode(FileData(), widget=FileUploadWidget(store))
