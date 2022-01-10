# This code provides the functions used to hash files
# 
#
# @author  TallPanda
# @version 1.02 10th of January 2022
# @platform   Python 3.10.1
from hashlib import sha1
import os


def chunk(fname: str,gigabytes:int=None):
    if os.path.isfile(fname):
        if gigabytes is None:
            gigabytes=1
        with open(fname,"rb") as f:
            while True:
                curpos = f.tell()
                fbytes = f.read((2**10)*gigabytes)# this is 1 gb if gibaytes is 1
                if(curpos == f.tell()): # if position in file hasnt changed break while true loop
                    break
                else:
                    yield fbytes



def hashing(fname: str,gigabytes:int=None):
    if gigabytes is None:
        gigabytes=1
    byts = chunk(fname,gigabytes)
    h = sha1()
    for b in byts:
        h.update(b)
    return h.hexdigest()

def hashingobj(fname: str,gigabytes:int=None):# 
    if gigabytes is None:
        gigabytes=1
    byts = chunk(fname,gigabytes)
    h = sha1()
    for b in byts:
        h.update(b)
    return h


def hasher(fname: str):# single file
    t = hashing( chunk( fname) )
    return t
