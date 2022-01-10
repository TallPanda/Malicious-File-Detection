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

def asynchandler(tasks:dict) -> dict:
    taskdict = {}
    for task, func in tasks.items():
        taskdict[task] = func
    return taskdict

def asyncrunner(taskdict:dict):
    taskr={}
    for taskn,task in taskdict.items():
        task = task
        taskr[taskn]= task
    return taskr

def taskmanager(fnames:list) -> dict:
    tasks = {}
    for fname in fnames:
        tasks[fname] = hashing(fname)
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
    tasks = taskmanager(files)
    taskdict = asynchandler(tasks)
    fin = asyncrunner(taskdict)
    log = fileincr()
    print(log)
    print(fin)
    with open(log,"x") as f:
        f.writelines(json.dumps(fin))

def main(dirname:str):
    if dirname[-1] not in ["/","\\"]:
        dirname =input("Please enter a directory, ending with '/'. Eg: 'C:/', 'D:/test/', '/root/'\n")
        main(dirname)
    else:
        _main(dirname)
    
# print(asyncio.run(hashing("D:/test/signatures.txt")))
# main("D:/test/")