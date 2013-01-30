from persistent.mapping import PersistentMapping
from pyramid.security import Allow, ALL_PERMISSIONS
import hashlib

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

class ImagesFolder(StorageFolder):
    def __init__(self, title, description=u""):
        super(ImagesFolder, self).__init__(title=title, description=description)

class ImageStore(StorageFolder):
    def __init__(self, image_file):
        super(StorageFolder, self).__init__()
        self.image = image_file

class User(StorageFolder):
    def __init__(self, username, email, password, fullname=u""):
        super(User, self).__init__(title=username, description=fullname)
        self.email = email
        self.hashed_password = self.hash(password)

    @staticmethod
    def hash(password):
        return hashlib.sha512(password.encode('utf-8')).hexdigest()

    def validate_password(self, password):
        return self.hash(password) == self.hashed_password

def appmaker(zodb_root):
    if not 'app_root' in zodb_root:
        app_root = StorageFolder(
                title=u"Main Storage",
                description=u"Main Storage for Photomanagement",
                )
        app_root['admin'] = User(
                username=u"admin",
                email=u"mavjs@mavjs.org",
                password=u"nomadfoto",
                fullname=u"Nomadfoto admin",
                )
        app_root.__acl__ = [
                (Allow, 'admin', ALL_PERMISSIONS),
                (Allow, 'admin', 'add_upload'),
                (Allow, 'admin', 'all_users'),
                ]
        app_root['images'] = ImagesFolder(
                title=u"digi_roll",
                description=u"Main Storage for Photo Collection",
               )
        zodb_root['app_root'] = app_root
        import transaction
        transaction.commit()
    return zodb_root['app_root']
