from pyramid.view import view_config
from .models import User

@view_config(
        renderer="templates/index.pt")
def index(request):
    return {}

@view_config(
        context=User,
        permission="users",
        renderer="templates/user.pt")
def user_view(context, request):
    return {}

