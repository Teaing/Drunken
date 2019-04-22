#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author:Tea

import nmap


def main():
    getBannerForNmap('192.1.1.105', '20-4000')


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


if __name__ == '__main__':
    main()




'''
{'192.1.1.105': [{1723: 'pptp linux (Firmware: 1)'}, {873: 'rsync'}, {3306: 'mysql MySQL 5.7.13-log'}, {80: 'http Apache httpd 2.2.15'}, {22: 'ssh OpenSSH 5.3'}, {23: 'telnet Linux telnetd'}, {25: 'smtp Postfix smtpd'}, {443: 'htt
p Apache httpd 2.2.15'}, {3690: 'svnserve Subversion'}]}
'''
