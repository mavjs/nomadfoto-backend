from pyramid.security import Allow
from pyramid.view import view_config
from pyramid_deform import FormView
from pyramid.httpexceptions import HTTPFound
#from .uploadcheck import CheckFileType
from StringIO import StringIO
from .models import ImageStore
from .myschema import UploadSchema
from . import get_user
import mimetypes
import os
import zipfile
import hashlib
import Image

choices = [
                ('', '-- Select --')
                ]
@view_config(
        name="upload",
        permission="add_upload",
        renderer="templates/upload.pt")
class Upload(FormView):
    schema = UploadSchema()
    buttons = ('upload',)
    title = u"Upload"

    
    def upload_success(self, appstruct):
        username = appstruct['username']
        jobid = appstruct['jobid']
        user = get_user(self.request, username)
        if user is None:
            self.request.session.flash(
                    u"No such users exist", "error")
            return None
        images = appstruct['items']
        image_files = images['fp'].read()
        image_type = images['mimetype']
        if image_type == 'application/zip':
            zip_list = zipfile.ZipFile(StringIO(image_files), 'r')
            for item in zip_list.namelist():
                if not os.path.basename(item):
                    continue
                split_name = item.split('/')[-1] 
                file_uid = str(hashlib.md5(split_name).hexdigest())
                unzip_image = zip_list.read(item)
                im = Image.open(StringIO(unzip_image))
                im_string = StringIO()
                im2 = im.resize((80, 50), Image.ANTIALIAS)
                im2.save(im_string, "PNG")
                finished_image = "data:"+mimetypes.guess_type(item)[0]+";base64,"+im2.fp.read().encode('base64')
                source = ImageStore(
                        uid=user.title,
                        jobid=jobid,
                        image_name=split_name,
                        image_file=finished_image,
                        )
                source.__acl__ = [
                        (Allow, user.title, 'view'),
                        (Allow, user.title, 'share'),
                        ]
                self.request.root['images'][file_uid] = source
                self.request.root['jobs'][jobid].status = 'completed'
        self.request.session.flash(u"Your folder was added.", "success")
        return HTTPFound(location=self.request.application_url)
