from pyramid.view import view_config
from pyramid.security import authenticated_userid
from pyramid.httpexceptions import HTTPFound

@view_config(
        renderer="templates/index.pt")
def index(request):
    authd_user = authenticated_userid(request)
    if not authd_user or authd_user == 'admin':
        return {}
    else:
        return HTTPFound(location=request.resource_url(request.user))
