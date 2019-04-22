#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author:Tea

import nmap
import time
import logging
import multiprocessing
from pymongo import MongoClient

logging.basicConfig(
    level=logging.INFO,  # filename='/tmp/LogNew.log',
    format='[%(levelname)s] %(message)s',
)


def main():
    mongodbConn = MongodbOperate()
    bsonData = mongodbConn.GetLastOne()
    singleData = bsonData[0]
    logging.info(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(int(singleData['startTime']))))
    startTime = time.time()
    processNum = 40
    pool = multiprocessing.Pool(processes=processNum)
    for singleLine in singleData['scanResult']:
        ipAddress = convertIpAddress(singleLine)
        portStr = ','.join(singleData['scanResult'][singleLine])
        pool.apply_async(getBannerForNmap, (ipAddress, portStr))
    pool.close()
    pool.join()
    logging.info('{0} second'.format(time.time() - startTime))


def getBannerForNmap(ipAddress, port):
    scanResult = dict.fromkeys([ipAddress], [])
    nmapScan = nmap.PortScanner()
    nmapScan.scan(hosts=ipAddress, ports=port, arguments='-sV --open -Pn -n')
    tcpInfo = nmapScan[ipAddress].get('tcp')
    for port in tcpInfo:
        portInfo = tcpInfo.get(port)
        tmpInfo = dict.fromkeys([port], '{0} {1} {2}'.format(portInfo.get('name'), portInfo.get('product'),
                                                             portInfo.get('version')).strip())
        scanResult[ipAddress].append(tmpInfo)
    print scanResult


def convertIpAddress(ipAddress):  # 这里可没有做正确IP检查
    numToIp = lambda x: '.'.join([str(x / (256 ** i) % 256) for i in range(3, -1, -1)])
    ipToNum = lambda x: sum([256 ** j * int(i) for j, i in enumerate(x.split('.')[::-1])])
    try:
        return numToIp(int(ipAddress))
    except:
        return ipToNum(ipAddress)


class MongodbOperate():
    def __init__(self):
        dbHost = '127.0.0.1'
        dbPort = 17178
        dbName = 'MasscanItem'
        collection = 'PortInfo'
        dbUser = ''
        dbPassword = ''
        try:
            self.conn = MongoClient(dbHost, dbPort)
        except Exception, e:
            logging.info(str(e))
        self.db = self.conn[dbName]
        if dbUser and dbPassword:
            self.db.authenticate(dbUser, dbPassword)
        self.collection = self.db[collection]

    def GetLastOne(self):
        return self.collection.find().sort('_id', -1).limit(1)


if __name__ == '__main__':
    main()
