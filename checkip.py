#coding=utf-8
"""
Create On 2017/3/23

@author: Ron2
"""


import requests
import httplib
import json
import traceback
import time


def checkIP(pid, ip):
    """
    IP查询
    :param ip:
    :return:
    """
    try:
        headers = {'Accept-Language': 'zh-CN,zh;q=0.8,en;q=0.6'}
        url = "http://www.ip138.com/ips138.asp?ip=%s&action=2" % ip
        r = requests.get(url, headers=headers)
        # print "r.status => ", r.status_code

        ronCode = requests.utils.get_encodings_from_content(r.content)
        # print "ronCode ==> ", ronCode
        _content = r.content.decode(ronCode[0], 'replace').encode('utf8', 'replace')

        subStr = '''<td align="center"><ul class="ul1"><li>'''
        index = _content.find(subStr)
        if index < 0:
            # print u"error ==> ", _content
            # exit(1)
            # return
            print "er=> ", pid, " ip=> ", ip
            return

        beginIndex = index + len(subStr)
        endIndex = _content.find("<li>", beginIndex)

        target = _content[beginIndex: endIndex-len("<li>")-1]

        ''' 最后写入 '''
        dic = {}
        dic["pid"] = pid
        dic["ip"] = ip
        dic["target"] = target
        data = json.dumps(dic)
        if len(data) >= 500:
            print "da=> ", pid, " ip=> ", ip
            return

        fileObj = open("./register.txt", "a")
        fileObj.write(data)
        fileObj.write("\n")
        fileObj.close()

    except:
        traceback.print_exc()
        print "ex=> ", pid, " ip=> ", ip
        # print _content
        exit(1)


def handle_read_pid_ip():
    """
    读取pid对应的ip
    :return:
    """
    pidForIpDic = {}

    path = "/Users/Ron2/ip.txt"
    fileObj = open(path, "rb")
    while 1:
        data = fileObj.readline()
        if not data:
            break

        subStr = "INSERT INTO `register` VALUES"
        if data.find(subStr) == 0:
            # print "data size =>", len(data)
            beginIndex = len(subStr)
            data = data[beginIndex: -2]

            ar = data.split("),")
            for record in ar:
                record = record[1:]
                colArray = record.split(",")
                pid = colArray[1]
                fromIP = colArray[-2]
                pidForIpDic[pid] = fromIP

    fileObj.close()

    data = json.dumps(pidForIpDic)
    fileObj = open("/Users/Ron2/pidForIp.txt", "wb")
    fileObj.write(data)
    fileObj.close()





if __name__ == "__main__":
    # checkIP("174.70.153.130")
    # checkIP("61.140.62.246")

    # handle_read_pid_ip()



    # fileObj = open("./pidForIp.txt", "rb")
    # data = fileObj.read()
    # fileObj.close()
    #
    # dic = json.loads(data)
    # print "total => ", len(dic)
    #
    # ''' got pid '''
    # pidCount = 0
    # pidSet = set()
    # fileObj = open("./register.txt", "rb")
    # while 1:
    #     data = fileObj.readline()
    #     if not data:
    #         break
    #
    #     pidCount += 1
    #     try:
    #         ipDic = json.loads(data)
    #         pid = ipDic.get("pid")
    #         pidSet.add(pid)
    #     except:
    #         print pidCount, " ==> ", data
    #
    # fileObj.close()
    #
    # print "pidSet ==> ", len(pidSet)
    #
    # ''' 启动之后先写一个换行 '''
    # fileObj = open("./register.txt", "a")
    # fileObj.write("\n")
    # fileObj.close()
    #
    # countNum = 0
    # for pid, ip in dic.iteritems():
    #     if pid in pidSet:
    #         continue
    #
    #     countNum += 1
    #     checkIP(pid, ip[1:-1])
    #
    #     if countNum % 100 == 0:
    #         print "countNum => ", countNum, time.time()
    #
    #

    fileObj = open("/Users/Ron2/Desktop/IPData.txt", "rb")
    while 1:
        data = fileObj.readline()
        if not data:
            break



    fileObj.close()


