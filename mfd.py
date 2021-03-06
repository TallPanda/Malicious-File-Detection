# This code provides provides the main method for use in interaction with the
# Malicious File detection provided by this package
#
# @author  TallPanda
# @version 1.03 10th of January 2022
# @platform   Python 3.10.1

from MFD.hashing import hasher,hashing
from MFD.fileretrieval import dictviewtodict, dirscan,recursivescan
import json
import os
import string
from progressbar import ProgressBar
from MFD.sql import sql

def taskmanager(fnames:list, func) -> dict:# runs a function on items in a list
    tasks = {}
    flen = len(fnames)
    with ProgressBar(max_value=flen) as pb:
        for n,fname in enumerate(fnames):
            pb.update(n)
            tasks[fname] = func(fname)
        return tasks

def fileincr(ftype: str = None,file: str=None, n:int = None):# incrementally generates file names if the file already exists
    if ftype == None:
        ftype = ".log"
    if file == None:
        file = "MFD_Log"
    if n == None:
        if not os.path.isfile(file+ftype):
            return file+ftype
        else:
            n = 1
            return fileincr(ftype,file,n)
    else:
        if not os.path.isfile(file+str(n)+ftype):
            return file+str(n)+ftype
        else:
            n += 1
            return fileincr(ftype,file,n)

def _main(dirname:list):
    filestats = recursivescan(dirname)
    files = []
    for _files in dictviewtodict(filestats.values()):
        files.append(_files["Path"])
    tasks = taskmanager(files,hashing)
    log = fileincr()
    print(log)
    print(tasks)
    with open(log,"x") as f:
        f.writelines(json.dumps(tasks))

def main(dirname:str):
    if dirname[-1] not in ["/","\\"]:
        dirname =input("Please enter a directory, ending with '/'. Eg: 'C:/', 'D:/test/', '/root/'\n")
        main(dirname)
    else:
        _main(dirname)

def scansystem():# Scans the file system
    # drives = [_+":/" for _ in string.ascii_uppercase if os.path.exists(_+":/")]
    drives =["D:/test/"]
    for drive in drives:
        output= fileincr(".json",drive.replace(":/","_").replace("/","")+"_drive_files_on_system")

        files = recursivescan(drive)
        print(output)
        filelist = []
        for _files in dictviewtodict(files.values()):
            filelist.append(_files["Path"])
        tasks = taskmanager(filelist,hashing)

        with open(output,"x") as f:
            f.writelines(json.dumps(tasks))
        hashes = {hash:[0,fname] for fname,hash in tasks.items()}
        print(hashes)
        output= fileincr(".json",drive.replace(":/","_").replace("/","")+"_unknown_hashes_on_system")
        print(output)
        with open(output, "x") as f:
            f.writelines(json.dumps(sql(hashes)))

if __name__ == "__main__":
    scansystem()
