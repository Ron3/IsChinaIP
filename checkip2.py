#coding=utf-8
"""
Create On 2017/3/23

@author: Ron2
"""


import requests
import httplib
import json
import traceback


def handleIP():
    """
    读取IP出来
    :return:
    """
    pidSet = set()
    fileObj = open("./hk_pid", "rb")
    while True:
        data = fileObj.readline()
        if not data:
            break

        data = data.strip()
        if len(data) <= 0:
            continue

        ar = data.split(",")
        pidSet.add(ar[0])


    fileObj.close()

    fileObj = open("./hkPidSet", "wb")
    fileObj.write(str(pidSet))
    fileObj.close()

    print len(pidSet)

if __name__ == "__main__":
    handleIP()


