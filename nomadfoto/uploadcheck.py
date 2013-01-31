import os
import zipfile
import tarfile
import hashlib
import StringIO
import tempfile

class CheckFileType():
    def __init__(self, filename):
        self.filename = filename
        self.filedict = {}

    def unzip(self):
        self.zipfile_list = zipfile.ZipFile(self.filename)
        for item in self.zipfile_list.namelist():
            if not os.path.basename(item):
                continue
            self.filedict[str(hashlib.md5(item).hexdigest())] = repr(self.zipfile_list.read(item))
        return self.filedict
    
    def untar(self):
        self.tarfile_list = tarfile.open(self.filename, mode='r:*')
        for item in self.tarfile_list:
            self.filedict[hashlib.md5(item).hexdigest()] = item
        return self.filedict
