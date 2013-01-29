from colander import Schema, SchemaNode, String
from deform import FileData
from deform.widget import PasswordWidget, FileUploadWidget
from deform.interfaces import FileUploadTempStore

class Store(dict):
    def preview_url(self, name):
        return ""

store = Store()

class LoginSchema(Schema):
    username = SchemaNode(String(), title=u"username")
    password = SchemaNode(String(), title=u"password", widget=PasswordWidget())
    
class RegistrationSchema(LoginSchema):
    fullname = SchemaNode(String(), title=u"Full Name")
    email = SchemaNode(String(), title=u"Email")

class UploadSchema(Schema):
    description = SchemaNode(String(), title=u"Description for files")
    items = SchemaNode(FileData(), widget=FileUploadWidget(store))
