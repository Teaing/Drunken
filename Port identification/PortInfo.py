#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author:Tea

import regex
import socket


def main():
    global regexList
    regexList = readRegexFile()
    BannerInfo.getBanner('192.1.1.105', 23, 'TCP')


def filterStr(bannerStr):  # NMAP banner match use nmap-service-probes
    for regexLine in regexList:
        regexData = regexLine.split('||')
        regexStr = regexData[0]
        regexDes = regexData[1]
        try:
            regexResult = regex.findall(regexStr, bannerStr)[0]
        except:
            regexResult = ''
        if regexResult:
            print '{0}'.format(regexDes)
            break


class BannerInfo(object):

    @staticmethod
    def getBanner(ipAddress, port, mode='TCP'):
        mode = mode.upper()
        if mode not in ['TCP', 'UDP']:
            raise Exception('Invalid mode!', mode)
        socketMode = socket.SOCK_STREAM  # TCP Model
        if mode == 'UDP':
            socketMode = socket.SOCK_DGRAM  # UDP Model
        socket.setdefaulttimeout(1)  # Time out
        try:
            sockets = socket.socket(socket.AF_INET, socketMode)
            sockets.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            sockets.connect((ipAddress, port))
            sockets.send('Tea\r\n')
            banner = sockets.recv(1024)
            sockets.close()
            filterStr(banner)
        except:
            return


def readRegexFile():
    portProbesList = []
    with open('./nmap-service-probes', 'r') as readInfo:
        for line in readInfo.readlines():
            splitData = line.split('|')
            if 'match' in splitData[0] and 'm=' not in splitData[0]:
                try:
                    portProbesList.append('{0}||{1}'.format(splitData[1], splitData[0].split(' ')[1]))
                except:
                    pass
    return portProbesList


if __name__ == '__main__':
    main()
