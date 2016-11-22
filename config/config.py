import ConfigParser
import os

def getDbconfig():
    db={}
    config = ConfigParser.ConfigParser()
    config.read('config.ini')
    db["host"]=config.get("db","host")
    db["dbname"]=config.get("db","dbname")
    db["port"]=config.get("db","port")
    db["username"]=config.get("db","username")
    db["password"]=config.get("db","password")
    return db

