#SELECT A.* FROM A WHERE ID NOT IN(SELECT ID FROM B) something like this
#
# This code provides provides the the functions necessary with communicationg with the mysql database
# @author  TallPanda
# @version 1.02 10th of January 2022
# @platform   Python 3.10.1
from mysql import connector
import json,os
import uuid,getpass
import time

def getdetails(config:str=None):
    if config == None:
        config = "config/mysql/secure/login.json"
    if not os.path.isfile(config):
        raise(f"Config does not exist at {config}")
    
    with open(config, "r") as details:
        details = json.loads(details.read())
        host = details["host"]
        passw = details["password"]
        user = details["user"]
        database = details["database"]
        port = details["port"]
    id = f"{getpass.getuser()}_{uuid.getnode()}"
    return id,host,passw,user,database,port

def sqlconcur(config:str=None):    
    host,passw,user,database,port = getdetails(config)[1:]

    try:
        con =connector.connect(host=host,user=user,password=passw,database=database,port=port)
        print(f"""
Connected to {con.server_host} as User '{con.user}' on Port: {con.server_port}    
Server Version: {con.get_server_info().replace('-0ubuntu0.',',Ubuntu-').strip(str.join(".",[str(_) for _ in con.get_server_version()])+"-").replace("-",":").split(",")}
Connection ID: {con.connection_id}
""")
        cur = con.cursor(buffered=True)
        return con,cur
    except Exception as e:
        if "Can't connect to MySQL server on" in str(e):
            print(f"Connection Issues on {host}:{port}")
            print("Retrying in 2 minutes")
            time.sleep(120)
            return sqlconcur(config)
        else:
            print(e)
            print("Retrying in 1 minutes")
            raise "Please contact the devloper if the issue cannot be resolved"
def tablexists(cur,table):
    cur.execute("show tables;")
    for x in cur:
        if table in x:
            return True
    return False

def makeusertable(cur,id):# makes a table for the users data
    if not tablexists(cur,id):
        cur.execute(f"create Table {id}(SHA1 VARCHAR(255) UNIQUE not null, vtstatus int not null default 0, primary key (SHA1));")
        print(f"Table {id} created.")
    else:
        inp = input(f"Table: {id} already exists\nDo you want to recreate the table?(Y/N)\n")
        while not inp.lower() in ["y","n"]:
            inp = input(f"Table: {id} already exists\nDo you want to recreate the table?(Y/N)\n")

        match inp.lower():
            case "y":
                cur.execute(f"drop Table {id};")
                cur.execute(f"create Table {id}(SHA1 VARCHAR(255) UNIQUE not null, vtstatus int not null default 0, primary key (SHA1));")
                print(f"Table {id} created.")
            case "n":
                print(f"Skipping table {id}")


def sha1exists(cur,id,key):
    cur.execute(f"select * from {id} where SHA1='{key}'")
    for message in cur:
        if key in message:
            return True
    return False

def uploadata(cur,id,userdata):
    for key,value in userdata.items():
        if not sha1exists(cur,id,key):
            cur.execute(f"insert into {id} (SHA1, vtstatus) values ('{key}',{value})")
            print(f"Uploaded {key}:{value}")

def notfounds(cur,id):
    cur.execute(f"select SHA1 from {id} where (not vtstatus=2 or not vtstatus=3) and SHA1 not in (select SHA1 from uniq);")
    nfs = {}
    for i in cur:
        # for n in i:
        #     nfs.append(n)
        key,value =i
        nfs[key] = value
    return nfs


def sql(userdata,config:str=None):
    id = getdetails(config)[0]
    con, cur = sqlconcur()
    with con as con:
        with cur as cur:
            makeusertable(cur,id)
            uploadata(cur,id,userdata)
            return(notfounds(cur,id))
