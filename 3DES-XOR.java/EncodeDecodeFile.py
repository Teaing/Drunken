#!/usr/bin/env python
# -*- coding: utf_8 -*-
# author: Tea

import os
import sys
import base64
import struct
from Crypto.Cipher import DES3


def main():
    encryptFile()
    decryptFilePath = sys.argv[1]
    decryptFile(decryptFilePath)


def encryptFile():
    desCypherNew = desCypher()  # 将明文字符串先加密
    cypherString = desCypherNew.encrypt(
        '{"username":"******","password":"******","userType":"1","compname":"******","userTypeDesc":"******","isOver":"******","userId":"******","mallId":"******","dogNum":"******","overDate":"2118-12-31 23:59:59","genDate":"2119-02-18 23:59"}')
    resultOver = []
    lengthStr = len(cypherString) / 76  # 特定长度换行
    for num in xrange(lengthStr + 1):
        resultOver.append(cypherString[76 * num:76 * (num + 1)])
        if num != lengthStr:
            resultOver.append('\r\n')  # 执行换行
    cypherStringNew = ''.join(resultOver)  # 转成字符串
    with open("./newKeys.key", 'wb') as FileWrite:
        for line in cypherStringNew:
            FileWrite.write(struct.pack("B", ord(line) ^ 40))  # 异或后写入文件，存储为密文


def decryptFile(filePath):
    if not os.path.exists(filePath):
        sys.exit('File Not Found.')
    resultList = []
    with open(filePath, 'rb') as fileRead:  # 以二进制格式打开
        for line in fileRead.readline():
            resultList.append(struct.pack("B", int(ord(line) ^ (428343592 % 256))))  # 异或
            # resultList.append(struct.pack("B", int(ord(line) ^ 40)))
        cypherString = ''.join(resultList).replace('\r\n', '')
        desCypherNew = desCypher()
        print desCypherNew.decrypt(cypherString)


class desCypher:
    def __init__(self):
        self.key = u'我是加密key'
        BS = DES3.block_size
        self.pad = lambda s: s + (BS - len(s) % BS) * chr(BS - len(s) % BS)
        self.unpad = lambda s: s[0:-ord(s[-1])]

    def encrypt(self, text):
        text = self.pad(text)
        cipher = DES3.new(self.key, DES3.MODE_ECB)
        m = cipher.encrypt(text)
        m = base64.b64encode(m)
        return m.decode('utf-8')

    def decrypt(self, decrypted_text):
        text = base64.b64decode(decrypted_text)
        cipher = DES3.new(self.key, DES3.MODE_ECB)
        s = cipher.decrypt(text)
        s = self.unpad(s)
        return s.decode('utf-8')


if __name__ == '__main__':
    main()
