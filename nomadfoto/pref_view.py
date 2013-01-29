from pyramid.view import view_config

@view_config(name='preferences', renderer='templates/pref.pt')
def pref(request):
    return {}
