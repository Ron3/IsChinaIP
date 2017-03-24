#coding=utf-8
"""
Create On 2017/3/23

@author: Ron2
"""


import requests
import httplib
import json
import traceback


def checkIP(pid, ip):
    """
    IP查询
    :param ip:
    :return:
    """
    try:
        headers = {'Accept-Language': 'zh-CN,zh;q=0.8,en;q=0.6'}
        url = "http://ipapi.ipip.net/find" % ip
        r = requests.get(url, headers=headers)
        dic = json.loads(r.content)
        code = dic.get("code")
        if code != 0:
            print "co=> ", pid, " ip=> ", ip
            return

        dataDic = dic.get("data")
        country = dataDic.get("country")
        country_id = dataDic.get("country_id")

        ''' 最后写入 '''
        dic = {}
        dic["pid"] = pid
        dic["ip"] = ip
        dic["target"] = country
        dic["country_id"] = country_id
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




if __name__ == "__main__":
    # checkIP("174.70.153.130")
    # checkIP("61.140.62.246")

    # handle_read_pid_ip()

    fileObj = open("./pidForIp.txt", "rb")
    data = fileObj.read()
    fileObj.close()

    dic = json.loads(data)
    print "total => ", len(dic)

    ''' got pid '''
    pidSet = set()
    fileObj = open("./register.txt", "rb")
    while 1:
        data = fileObj.readline()
        if not data:
            break

        ipDic = json.loads(data)
        pid = ipDic.get("pid")
        pidSet.add(pid)

    fileObj.close()

    print "pidSet ==> ", len(pidSet)

    ''' 启动之后先写一个换行 '''
    fileObj = open("./register.txt", "a")
    fileObj.write("\n")
    fileObj.close()

    countNum = 0
    for pid, ip in dic.iteritems():
        if pid in pidSet:
            continue

        countNum += 1
        checkIP(pid, ip[1:-1])

        if countNum % 100 == 0:
            print "countNum => ", countNum


