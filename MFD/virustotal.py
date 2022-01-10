import vt,os,json

def getapikey(keyfile: str = None):
    if keyfile == None:
        keyfile = "config/virustotal/vt-api.json"
    if os.path.isfile(keyfile):
        with open(keyfile,"r") as key:
            api = json.loads(key.read())
        return api["apikey"]
    else:
        raise "Keyfile does not exist please check config/virustotal/vt-api.json"

def _getclient():
    api = getapikey()
    with vt.Client(api) as session:
        return session

def getfobj(api, hash:str):
    return api.get_object(f"/files/{hash}")
    


def getmalice(file):
    detected = []
    for key,res in file.last_analysis_results.items():
        if res["category"] == "malicious":
            detected.append(key)

    return detected

def reportgen(hash):
    with _getclient() as api:
        file = getfobj(api, hash)
        malice =getmalice(file)
        newline ="\n"
        if len(malice)>0:
            return f"File deemd malicious by the following sources:\n{str.join(newline,malice)}"

with open("test.json","a+") as f:
    f.writelines(reportgen("b0fab49496d7566de454d3251966afb2e990ef5f"))