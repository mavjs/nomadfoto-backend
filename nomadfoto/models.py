from persistent.mapping import PersistentMapping
from pyramid.security import Allow, Deny, ALL_PERMISSIONS
import hashlib

#Main root storage folder class
class StorageFolder(PersistentMapping):
    __parent__ = __name__ = None
    
    def __init__(self, title, description=u''):
        super(StorageFolder, self).__init__()
        self.title = title
        self.description = description

    def __setitem__(self, name, item):
        super(StorageFolder, self).__setitem__(name, item)
        item.__name__ = name
        item.__parent__ = self

#Generic folder class for generic folders under root
class GenericFolder(StorageFolder):
    def __init__(self, title, description=u""):
        super(GenericFolder, self).__init__(title=title, description=description)

#Image folder for each image storing X: use ZODB.Blob()
class ImageStore(StorageFolder):
    def __init__(self, uid, jobid, image_name, image_file):
        super(ImageStore, self).__init__(self)
        self.uid = uid
        self.jobid = jobid
        self.name = image_name
        self.image = image_file

#Job queue folder for each job storing
class JobStore(StorageFolder):
    def __init__(self, clientid, dropboxid, jobid, jobtype, status):
        super(JobStore, self).__init__(self)
        self.uid = clientid
        self.dropboxuid = dropboxid
        self.jobid = jobid
        self.jobtype = jobtype
        self.status = status

#User folder for storing credentials of users
class User(StorageFolder):
    def __init__(self, username, email, password, fullname=u""):
        super(User, self).__init__(title=username, description=fullname)
        self.email = email
        self.hashed_password = self.hash(password)

    @staticmethod
    def hash(password):
        return hashlib.sha512(password.encode('utf-8')).hexdigest() #X: change algo on prod/final demo

    def validate_password(self, password):
        return self.hash(password) == self.hashed_password

def appmaker(zodb_root):
    if not 'app_root' in zodb_root:
        # Main root storage folder
        app_root = StorageFolder(
                title=u"Main Storage",
                description=u"Main Storage for Photomanagement",
                )
        
        #admin account X:to change credentials on prod
        app_root['admin'] = User(
                username=u"admin",
                email=u"mavjs@mavjs.org",
                password=u"nomadfoto",
                fullname=u"Nomadfoto Admin",
                )

        #test user account X: to remove on prod
        app_root['test'] = User(
                username=u"test",
                email=u"test",
                password=u"test",
                fullname=u"test",
                )

        #give permissions X: to check acl on prod/demo
        app_root.__acl__ = [
                (Allow, 'admin', ALL_PERMISSIONS),
                (Allow, 'admin', 'add_upload'),
                (Allow, 'admin', 'all_users'),
                (Allow, 'test', 'order'),
                (Allow, 'test', 'users'),
                (Deny, 'test', 'add_upload'),
                ]

        #unified storage for all images X: change to each user image folder?
        app_root['images'] = GenericFolder(
                title=u"digi_roll",
                description=u"Main Storage for Photo Collection",
               )

        #unified storage for job queues X: change to each user job folder?
        app_root['jobs'] = GenericFolder(
                title=u"Jobs Queues",
                description=u"Folder to store job status queues from clients",
                )

        zodb_root['app_root'] = app_root
        import transaction
        transaction.commit()
    return zodb_root['app_root']
