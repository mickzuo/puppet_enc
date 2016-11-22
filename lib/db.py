import MySQLdb
import ruamel.yaml
import time
from DBUtils.PooledDB import PooledDB
from config import getDbconfig

class mydb(object):
    __pool = None

    def __init__(self):
        self._conn = mydb.__getConn()
        self._cursor = self._conn.cursor()
  
    @staticmethod
    def __getConn():
        if mydb.__pool is None:
            dbstring = getDbconfig()
            __pool = PooledDB(MySQLdb,5,host=dbstring['host'],user=dbstring['username'],passwd=dbstring['password'],db=dbstring['dbname'],port=int(dbstring['port']))
            return __pool.connection()

    def getnodeclass(self,node):
        dic={'classes':'','parameters': {'host': '','path':'/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin'},'environment':'production'}
        SQL="select node_group from nodes where hostname=\'"+node+"\';"
        self._cursor.execute(SQL)
        node_group = self._cursor.fetchall()[0][0]
        SQL="select class_name from class where class_group in (select class_group from class_to_node where node_group=\'"+node_group+"\');"
        count=self._cursor.execute(SQL)
        result=self._cursor.fetchall()
        class_dic={}
        for i in range(len(result)) :
            class_dic[result[i][0]]=''
        dic['classes']=class_dic
        dic['parameters']['host']=node_group
        yam=ruamel.yaml.dump(dic,Dumper=ruamel.yaml.RoundTripDumper)
        return yam
