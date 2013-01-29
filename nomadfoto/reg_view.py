from pyramid.security import remember, Allow, Deny
from pyramid_deform import FormView
from pyramid.view import view_config
from pyramid.httpexceptions import HTTPFound

#get_user from __init__.py
from . import get_user
#User storage
from .models import User
#Schemas
from .myschema import RegistrationSchema

@view_config(name="register",renderer='templates/register.pt')
class Registration(FormView):
    schema = RegistrationSchema()
    buttons = ('register',)
    title = u"Register"

    def register_success(self, appstruct):
        username = appstruct.pop('username')
        user = get_user(self.request, username)
        if user is not None:
            self.request.session.flash(
                    u"That username is already taken.", "error")
            return None

        user = User(
                username=username,
                email=appstruct['email'],
                password=appstruct['email'],
                fullname=appstruct['fullname'],
                )
        user.__acl__ = [
                (Allow, user.title, 'order'),
                (Allow, user.title, 'users'),
                (Deny, user.title, 'add_upload'),
                ]
        self.request.root[username] = user
        headers = remember(self.request, user.__name__)
        self.request.session.flash(
                u"Welcome to your collections, {0}!".format(user.title),
                "success")
        return HTTPFound(location=self.request.resource_url(user), headers=headers)
