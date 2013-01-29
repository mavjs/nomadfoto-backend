import os
import zipfile
import tarfile
import hashlib

class CheckFileType():
    def __init__(self, filename):
        self.filename = filename
        self.filedict = {}

    def unzip(self):
        self.zipfile_list = zipfile.ZipFile(self.filename).namelist()
        for item in self.zipfile_list:
            if os.path.isfile(item):
                self.filedict[hashlib.md5(item).hexdiget()] = item
        return self.filedict
    
    def untar(self):
        self.tarfile_list = tarfile.open(self.filename, mode='r:*')
        for item in self.tarfile_list:
            self.filedict[hashlib.md5(item).hexdigest()] = item
        return self.filedict
