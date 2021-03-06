from persistent.mapping import PersistentMapping
from pyramid.security import Allow, Deny, ALL_PERMISSIONS
import hashlib

# repoze.catalog for catalogging photos
from repoze.catalog.indexes.text import CatalogTextIndex
from repoze.catalog.catalog import Catalog
from repoze.catalog.document import DocumentMap

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

#Image folder for each image storing XXX: use ZODB.Blob()
class ImageStore(StorageFolder):
    def __init__(self, uid, jobid, image_name, image_file, tag=u"",collection=u""):
        super(ImageStore, self).__init__(self)
        self.uid = uid
        self.jobid = jobid
        self.name = image_name
        self.image = image_file
        self.tag = tag
        self.collection = collection

#Job queue folder for each job storing
class JobStore(StorageFolder):
    def __init__(self, clientid, dropboxid, jobid, jobtype, status):
        super(JobStore, self).__init__(self)
        self.uid = clientid
        self.dropboxid = dropboxid
        self.jobid = jobid
        self.jobtype = jobtype
        self.status = status

#User folder for storing credentials of users
class User(StorageFolder):
    def __init__(self, username, email, password, dropboxid=u"", fullname=u"", credit="00.00"):
        super(User, self).__init__(title=username, description=fullname)
        self.email = email
        self.dropboxid = dropboxid
        self.hashed_password = self.hash(password)
        self.credit = credit

    @staticmethod
    def hash(password):
        return hashlib.sha512(password.encode('utf-8')).hexdigest() #XXX: change algo on prod/final demo

    def validate_password(self, password):
        return self.hash(password) == self.hashed_password

def appmaker(zodb_root):
    if not 'app_root' in zodb_root:
        # Main root storage folder
        app_root = StorageFolder(
                title=u"Main Storage",
                description=u"Main Storage for Photomanagement",
                )
        
        #admin account XXX:to change credentials on prod
        app_root['admin'] = User(
                username=u"admin",
                email=u"mavjs@mavjs.org",
                password=u"nomadfoto",
                fullname=u"Nomadfoto Admin",
                )

        #test user account XXX: to remove on prod
        app_root['test'] = User(
                username=u"test",
                email=u"test@example.com",
                password=u"test",
                dropboxid=u"testuser",
                fullname=u"test user",
                credit="00.00",
                )

        #give permissions XXX: to check acl on prod/demo
        app_root.__acl__ = [
                (Allow, 'admin', ALL_PERMISSIONS),
                (Allow, 'admin', 'add_upload'),
                (Allow, 'admin', 'all_users'),
                (Allow, 'test', 'order'),
                (Allow, 'test', 'users'),
                (Deny, 'test', 'add_upload'),
                ]

        #unified storage for all images XXX: change to each user image folder?
        app_root['images'] = GenericFolder(
                title=u"digi_roll",
                description=u"Main Storage for Photo Collection",
               )

        #unified storage for job queues XXX: change to each user job folder?
        app_root['jobs'] = GenericFolder(
                title=u"Jobs Queues",
                description=u"Folder to store job status queues from clients",
                )
        #test user job for digiroll_all
        app_root['jobs']['test-0'] = JobStore(
                clientid='test',
                dropboxid='test',
                jobid='test-0',
                jobtype='digiroll_all',
                status='pending',
                )
        
        #test user job for digiroll_edit
        app_root['jobs']['test-1'] = JobStore(
                clientid='test',
                dropboxid='test',
                jobid='test-1',
                jobtype='digiroll_edit',
                status='pending',
                )
        
        #site root folder
        zodb_root['app_root'] = app_root

        #catalog stuff
        catalog = Catalog()
        catalog['tag'] = CatalogTextIndex('tag')
        catalog['collection'] = CatalogTextIndex('collection')
        app_root.catalog = catalog
        document_map = DocumentMap()
        app_root.document_map = document_map

        import transaction
        transaction.commit()
    return zodb_root['app_root']
