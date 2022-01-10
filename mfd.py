# This code provides provides the main method for use in interaction with the
# Malicious File detection provided by this package
#
# @author  TallPanda
# @version 1.02 10th of January 2022
# @platform   Python 3.10.1

from MFD.hashing import hasher,hashing
from MFD.fileretrieval import dictviewtodict, dirscan,recursivescan
import json
import os
import string

from MFD.sql import sql

def taskmanager(fnames:list, func) -> dict:# rins a function on items in a list
    tasks = {}
    for fname in fnames:
        tasks[fname] = func(fname)
    return tasks

def fileincr(ftype: str = None,file: str=None, n:int = None):
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

def scansystem():
    drives = [_+":" for _ in string.ascii_uppercase if os.path.exists(_+":")]
    for drive in drives:
        output= fileincr(".json",drive.strip(":")+"_drive_files_on_system")

        files = recursivescan(drive)
        filelist = []
        for _files in dictviewtodict(files.values()):
            filelist.append(_files["Path"])
        tasks = taskmanager(filelist,hashing)

        with open(output,"x") as f:
            f.writelines(json.dumps(tasks))
        
        hashes = {hash:0 for hash in tasks.keys()}
        output= fileincr(".json",drive.strip(":")+"_unknown_hashes_on_system")
        with open(output, "x") as f:

            f.writelines(json.dumps(sql(hashes)))

# print(asyncio.run(hashing("D:/test/signatures.txt")))
# main("D:/test/")
scansystem()