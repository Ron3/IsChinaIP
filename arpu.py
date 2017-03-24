#coding=utf-8
"""
Create On 2017/3/24

@author: Ron2
"""


import pymysql


class DB(object):
    """
    """
    def __init__(self):
        self.conn = None
        self.pidSet = set()


    def start(self):
        """
        开始
        :return:
        """
        self._initConn()
        self._initPidSet()
        self._getPayLog()


    def _getPayLog(self):
        """
        得到付费信息
        :return:
        """
        pidArray = tuple(self.pidSet)
        strPidArray = str(pidArray)
        for sid in xrange(7001, 7028, 1):
            if sid == 7002:
                continue

            serverName = "ron_server_%s" % sid
            cur = self.conn.cursor()
            sql = "use %s" % serverName
            cur.execute(sql)

            sql = "select pid, amount from pay where pid in %s " % strPidArray
            cur.execute(sql)
            for row in cur:
                print "row => ", row

            cur.close()


    def _initConn(self):
        """
        初始化连接
        :return:
        """
        self.conn = pymysql.connect(host='10.8.38.34', port=3306, user='root', passwd='adgjmpdb0', db='mysql')


    def _initPidSet(self):
        """
        初始化pid
        :return:
        """
        fileObj = open("./hkPidSet", "rb")
        data = fileObj.read()
        fileObj.close()

        self.pidSet = eval(data)
        print "len(self.pidSet)==> ", len(self.pidSet)



if __name__=="__main__":
    db = DB()
    db.start()
