# This code retrives and retuns files from a directory
# 
#
# @author  TallPanda
# @version 1.02 10th of January 2022
# @platform   Python 3.10.1
from datetime import date
class fileman:
    
    def __init__(self, filename, fhash, vtstatus, malicious, dhistory=None) -> None:
        self.filename = filename
        self.lastaccessed = str(date.today())
        if dhistory is not None and isinstance(dhistory, list) :
            self.dhistory = dhistory
        elif dhistory is not None:
            raise Exception(TypeError, f"dhistory must be a list or None Type\ndhistory type is: {type(dhistory)}")
        self.fhash = fhash
        self.vtstatus = vtstatus
        self.malicious = malicious
        self.filename = filename

    def __repr__(self) -> str:
        return(f"{self.__class__.__name__}({str(list(self.__dict__.values()))[1:-1]})")

    def __str__(self) -> str:
        return(f"{str(dict(self.__dict__.items()))[1:-1]}")

    def __iter__(self):
        for k,v in self.__dict__.items():
            yield k,v


class pending(fileman):
    pass


class malicious(fileman):
    pass


if __name__ == "__main__":
    a = malicious("test","example","Not Uploaded","Unknown")
    print(f"{list(a)}\n{dict(a)}\n{a}\n{repr(a)}")