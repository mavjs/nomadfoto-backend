from pyramid.view import view_config
from pyramid.security import authenticated_userid
from pyramid.httpexceptions import HTTPFound
from webhelpers.paginate import PageURL_WebOb, Page

@view_config(
        renderer="templates/index.pt")
def index(request):
    authd_user = authenticated_userid(request)
    if not authd_user or authd_user == 'admin':
        return {}
    else:
        return HTTPFound(location=request.resource_url(request.user))

@view_config(
        name="pricelist",
        renderer="templates/price.pt")
def pricelist(request):
    return {}

@view_config(
        name="collections",
        renderer="templates/collections.pt")
def collections(context, request):
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
