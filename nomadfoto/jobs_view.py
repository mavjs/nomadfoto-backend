from pyramid.view import view_config
from .models import User

@view_config(
        context=User,
        name="jobs",
        permission="users",
        renderer="templates/jobs.pt")
def jobs_view(context, request):
    return {}

@view_config(
        context=User,
        permission="users",
        renderer="templates/user.pt")
def user_view(context, request):
    return {}
