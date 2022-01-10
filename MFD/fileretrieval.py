# This code provides provides the main method for use in interaction with the
# Malicious File detection provided by this package
#
# @author  TallPanda
# @version 1.02 10th of January 2022
# @platform   Python 3.10.1



import os
import time
import glob
from string import ascii_uppercase as az


def getexempt():
    if os.path.isfile("config/exemptfiles"):
        with open("config/exemptfiles","r") as f:
            return f.readlines()
    else:
        return []

def dirscan(dirname:str):### tbd implement asyc or multiprocessing for file scanning scanned dirs get added to a dict which will process everything added to it filles added to a list and dirs get scanned processed dict elemetns get popped asyncio.Event possibly
    filestats = {}# dictionary of all dirscans in this process ## this will probably be a class in future
    # dirs =[]
    for path in (os.scandir(dirname)):
        if path.is_dir() == True:
            continue
            # dirs.append(path.name)
        else:
            if not dirname in filestats.keys():#create the list for that directory if none exist
                filestats[dirname] = []
            
            filestats[dirname].append({
                "Path":dirname + path.name,
                "Modified":time.ctime(list(path.stat())[-2]),
                "Created":time.ctime(list(path.stat())[-1])
                })

    return filestats

def dictviewtodict(dictview) -> dict:#python doesnt like the dict nesting so this is needed
    _dict = list(dictview)[0]
    return _dict

def recursivescan(dirname:str):
    exempt = getexempt()
    filestats = {}
    for fname in glob.iglob(dirname + '**/*.*', recursive=True):
        for _file in exempt:
            if not _file in fname:
                if not dirname in filestats.keys():#create the list for that directory if none exist
                        filestats[dirname] = []
                if os.path.isdir(fname):# globs return folders so this is needed
                    continue
                filestats[dirname].append({
                    "Path":fname.replace("\\","/")
                    })
    return filestats
# print(recursivescan("D:/test/"))
# print([_+":" for _ in az if os.path.exists(_+":")]) # finds drives