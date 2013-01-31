import os
import zipfile
import tarfile
import hashlib

class CheckFileType():
    def __init__(self, filename):
        self.filename = filename
        self.filedict = {}

    def unzip(self):
        self.zipfile_list = zipfile.ZipFile(self.filename, 'r')
        for item in self.zipfile_list.namelist():
            if not os.path.basename(item):
                continue
            #the logic here isn't right, thus upload fails.
            self.filedict[str(hashlib.md5(item).hexdigest())] = self.zipfile_list.open(item).read()
        return self.filedict
    
    def untar(self):
        self.tarfile_list = tarfile.open(self.filename, mode='r:*')
        for item in self.tarfile_list:
            self.filedict[hashlib.md5(item).hexdigest()] = item
        return self.filedict
