#coding=utf-8
"""
Create On 2017/3/24

@author: Ron2
"""


import traceback
import json

# /usr/bin/python
# coding: utf-8

global_ip_dict = [[[] for col in range(256)] for row in range(256)]


# input:apnic|CN|ipv4|112.0.0.0|4194304|20081215|allocated
# output:addr1,addr2,addr3,addr4,ip_num
def analyseLine(ip_line):
    ip_str_list = ip_line.split('|')
    if len(ip_str_list) < 7:
        return 0, 0, 0, 0, 0
    ip_nation, ip_version, ip_str, ip_num = ip_str_list[1], ip_str_list[2], ip_str_list[3], int(ip_str_list[4])
    if ip_nation != 'HK' or ip_version != 'ipv4':
        return 0, 0, 0, 0, 0
    ip_addr = ip_str.split('.')
    if len(ip_addr) < 4:
        return 0, 0, 0, 0, 0
    addr1, addr2, addr3, addr4 = int(ip_addr[0]), int(ip_addr[1]), int(ip_addr[2]), int(ip_addr[3])
    return addr1, addr2, addr3, addr4, ip_num


# input:file delegated-apnic-latest
# output:True,init ip dict success;False,init ip dict fail.
def init_ip_dict(frome_file):
    global global_ip_dict
    try:
        filedes = open(frome_file, 'r')
    except:
        return False
    lines = filedes.readlines()
    for line in lines:
        addr1, addr2, addr3, addr4, number_sum = analyseLine(line)
        if number_sum == 0:
            continue

        offset = 0
        while number_sum > 0:
            if number_sum >= 65536:
                start, end, number = 0, 65535, 65536
            else:
                start = addr3 * 256 + addr4
                end = start + number_sum - 1
                number = number_sum
            global_ip_dict[addr1][addr2 + offset].append({'start': start, 'end': end, 'number': number})
            number_sum -= 65536
            offset += 1
    filedes.close()
    return True


# input:ip string,*.*.*.*
# output:True,is china IP;False,is not china IP
def isChinaIP(ip):
    global global_ip_dict
    ip_addr = ip.split('.')
    if len(ip_addr) < 4:
        return False
    addr1, addr2, addr3, addr4 = int(ip_addr[0]), int(ip_addr[1]), int(ip_addr[2]), int(ip_addr[3])

    if len(global_ip_dict[addr1][addr2]) == 0:
        return False
    addr_value = addr3 * 256 + addr4
    for item in global_ip_dict[addr1][addr2]:
        if addr_value >= item['start'] and addr_value <= item['end']:
            return True
    return False


if __name__ == "__main__":
    ret = init_ip_dict('delegated-apnic-latest.txt')
    if not ret:
        print 'open file(delegated-apnic-latest) failed'
        exit(-1)


    # for addr1 in range(100, 256):
    #     for addr2 in range(100, 256):
    #         ip_str = '%s.%s.5.5' % (addr1, addr2)
    #         if isChinaIP(ip_str):
    #             print '%s :china ip' % ip_str
    #         else:
    #             print '%s :not china ip' % ip_str

    fileObj = open("pidForIp.txt", "rb")
    data = fileObj.read()
    fileObj.close()

    pidForIPdic = json.loads(data)
    for pid, ip in pidForIPdic.iteritems():
        ip = ip[1:-1]
        if isChinaIP(ip):
            print pid, ",", ip
