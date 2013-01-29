from pyramid.view import view_config
from pyramid_deform import FormView
from pyramid.httpexceptions import HTTPFound
from .myschema import UploadSchema
from .models import StorageFolder, ImagesFolder
from .uploadcheck import CheckFileType
from cStringIO import StringIO

@view_config(
        context=StorageFolder,
        name="upload",
        permission="add_upload",
        renderer="templates/upload.pt")
class Upload(FormView):
    schema = UploadSchema()
    buttons = ('upload',)
    title = u"Upload"
    
    def upload_success(self, appstruct):
        context = self.request.root['images']
        images = appstruct['items']
        image_files = images['fp'].read()
        image_type = images['mimetype']
        images_dict = {}
        if image_type == 'application/zip':
            images_dict = CheckFileType(StringIO(image_files)).unzip()
        elif image_type == 'application/x-tar':
            images_dict = CheckFileType(StringIO(image_files)).untar()
        for key,value in images_dict.items():
            image_store = ImagesFolder(
                image=value,
                )
            context[key] = image_store 
        self.request.session.flash(u"Your folder was added.", "success")
        return HTTPFound(location=self.request.application_url)
