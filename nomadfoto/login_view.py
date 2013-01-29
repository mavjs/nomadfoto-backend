from pyramid.security import forget
from pyramid.security import remember
from pyramid_deform import FormView
from pyramid.view import view_config
from pyramid.httpexceptions import HTTPFound

#get_user from __init__.py
from . import get_user
#Schemas
from .myschema import LoginSchema

@view_config(name="login",renderer='templates/login.pt')
class Login(FormView):
    schema = LoginSchema()
    buttons = ('login',)
    title = u"Log In"

    def login_success(self, appstruct):
        user = get_user(self.request, appstruct['username'])
        if user is None:
            return self.bad_login()
        if not user.validate_password(appstruct['password']):
            return self.bad_login()

        headers = remember(self.request, user.__name__)
        self.request.session.flash(
                u"Welcome, {0}!".format(user.title), "success")
        if user.title == 'admin':
            return HTTPFound(location=self.request.application_url,
                    headers=headers)
        else:
            return HTTPFound(location=self.request.resource_url(user),
                headers=headers)

    def bad_login(self):
        self.request.session.flash(
                u"Your username or password combination is incorrect", "error")

@view_config(name="logout", renderer='templates/logout')
def logout(request):
    headers = forget(request)
    request.session.flash(u"You have been logged out!")
    return HTTPFound(location=request.application_url, headers = headers)
