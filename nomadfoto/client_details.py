from pyramid.view import view_config
from .models import User

@view_config(
        name="clients",
        permission="all_users",
        renderer="templates/allusers.pt",
        )
def view_allclients(request):
    all_users = request.root.values()
    users = []
    for user in all_users:
        if isinstance(user, User) and not user.title == 'admin':
            users.append(user)
        else:
            continue
    return {"users": users}
