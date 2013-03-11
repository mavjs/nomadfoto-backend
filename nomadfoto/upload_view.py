from pyramid.security import Allow
from pyramid.view import view_config
from pyramid.httpexceptions import HTTPFound
from StringIO import StringIO
from .models import ImageStore
import os
import zipfile
import hashlib
import Image

@view_config(
        name="upload",
        permission="add_upload",
        request_method="POST"
        )
def upload_view(request):
    user = request.POST['username']
    jobid = request.POST['jobid']
    collection = request.POST['collection']
    uploadfile = request.POST['upload']
    return_url = request['HTTP_REFERER']
    if uploadfile == '':
        request.session.flash(u"Please select a file to upload!", "error")
        return HTTPFound(location=return_url)
    elif collection == '':
        request.session.flash(u"Please type in a name for your collection!", "error")
        return HTTPFound(location=return_url)
    else:
        filetype = uploadfile.type
        filezip = StringIO(uploadfile.file.read())
        if not filetype == 'application/zip':
            request.session.flash(u"Please upload a zip file.", "error")
            return HTTPFound(location=return_url)
        elif filetype == 'application/zip':
            zip_list = zipfile.ZipFile(filezip, 'r')
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
                finished_image = "data:image/png;base64,"+im_string.getvalue().encode('base64')
                source = ImageStore(
                        uid=user,
                        jobid=jobid,
                        image_name=split_name,
                        image_file=finished_image,
                        tag="tag",
                        collection=collection,
                        )
                source.__acl__ = [
                        (Allow, user, 'view'),
                        (Allow, user, 'share'),
                        (Allow, request.user.title, 'view'),
                        ]
                request.root['images'][file_uid] = source
                request.root['jobs'][jobid].status = 'completed'
            request.session.flash(u"Upload job done. The job has been marked complete.", "success")
            return HTTPFound(location=request.application_url)

@view_config(
        name="mark",
        permission="add_upload",
        request_method="POST"
        )
def mark_job(request):
    jobid = request.POST['jobid']
    request.root['jobs'][jobid].status = 'completed'
    request.session.flash(u"The job has been marked complete.", "success")
    return HTTPFound(location=request.application_url)
