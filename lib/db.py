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
            __pool = PooledDB(MySQLdb,20,host=dbstring['host'],user=dbstring['username'],passwd=dbstring['password'],db=dbstring['dbname'],port=int(dbstring['port']))
            return __pool.connection()

    def getnodeclass(self,node):
        dic={'classes':'','parameters': {'host': '','path':'/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin'},'environment':'production'}
        SQL="select node_group,location from nodes where hostname=\'"+node+"\';"
        self._cursor.execute(SQL)
        nodeinfo = self._cursor.fetchall()
	if len(nodeinfo)==0:
		return 'node not defined!'
	node_group=nodeinfo[0][0]
	location=nodeinfo[0][1]
        SQL="select class_name from class where class_group in (select class_group from class_to_node where node_group=\'"+node_group+"\');"
        count=self._cursor.execute(SQL)
        result=self._cursor.fetchall()
        class_dic={}
        for i in range(len(result)) :
            class_dic[result[i][0]]=''
        dic['classes']=class_dic
        dic['parameters']['host']=node_group
        dic['parameters']['location']=location
        yam=ruamel.yaml.dump(dic,Dumper=ruamel.yaml.RoundTripDumper)
        return yam

    def get_machine_list(self):
        lst = []
        SQL="select hostname,ip,node_group from nodes;"
        self._cursor.execute(SQL)
        result=self._cursor.fetchall()
        for i in range(len(result)):
           lst.append({'hostname':result[i][0],'ip':result[i][1],'group':result[i][2]}) 
        return lst

    def get_all_node_groups(self):
        lst = []
        SQL="select node_group from nodes group by node_group;;"
        self._cursor.execute(SQL)
        result=self._cursor.fetchall()
        for i in range(len(result)):
           lst.append(result[i][0]) 
        return lst

    def add_node(self,hostname,node_group):
        SQL="insert into nodes (hostname,node_group) values (\'"+hostname+"\',\'"+node_group+"\');"
        try:
            self._cursor.execute(SQL)
            self._conn.commit()
        except Exception,ex:
            self._conn.rollback()
            print Exception,":",ex
            return "Add node "+hostname+" failed!"
        return self.__getInsertId(hostname)

    def __getInsertId(self,hostname):
        self._cursor.execute("SELECT * from nodes where hostname=\'"+hostname+"\';")
        result=self._cursor.fetchall()
        print result
        if len(result)==0:
            return "Add node "+hostname+" failed!"
        return "Add node "+hostname+" success!"

    def delnode(self,hostname):
        SQL="delete from nodes where hostname=\'"+hostname+"\';"
        try:
            self._cursor.execute(SQL)
            self._conn.commit()
        except Exception,ex:
            self._conn.rollback()
            print Exception,":",ex
            return "Del node "+hostname+" failed!"
        return "success"

    def getnodetoclass(self):
        nodedic={}
        classes={}

        SQL="select * from class;"
        self._cursor.execute(SQL)
        result=self._cursor.fetchall()
        for theclass in result:
            if not classes.has_key(theclass[1]):
                classes[theclass[1]]=[]
            classes[theclass[1]].append(theclass[0])

        SQL="select * from class_to_node;"
        self._cursor.execute(SQL)
        result=self._cursor.fetchall()
        for node_group in result:
            if not nodedic.has_key(node_group[0]):
                nodedic[node_group[0]]=[]
            nodedic[node_group[0]].append({node_group[1]:classes[node_group[1]]})
        return nodedic
