from pyramid.view import view_config
from webhelpers.paginate import Page
from .models import User
from webhelpers.paginate import PageURL_WebOb, Page

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
def user_view(request):
    if not "page" in request.params:
        next_page=1
    else:
        next_page = request.params["page"]
    collection = request.root['images'].values()
    url_for_page = PageURL_WebOb(request)
    images = Page(collection,
            page=next_page,
            items_per_page=30,
            url=url_for_page
            )
    return {"images" : images}
