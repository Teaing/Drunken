#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author:Tea

import hashlib
from Crypto.Cipher import AES
from Crypto.Hash import SHA256
import base64
from urllib import unquote


def main():
    aes = AesCrypter()
    decrypt_data_Tmp = unquote('我是密文')
    print 'UrlDecode:', decrypt_data_Tmp
    decrypt_data = aes.decrypt(decrypt_data_Tmp)
    print decrypt_data
    encrypt_data = '我是明文'
    print aes.encrypt(encrypt_data)


class AesCrypter(object):

    def __init__(self):  # 消息摘要
        key = 'HAHAHAHAHAHAHAHA'
        hash = SHA256.new()
        hash.update(key)
        self.key = hash.digest()
        # self.key = hashlib.sha256(key).digest()
        print 'Self.Key:', self.key.encode('hex')  # 这里相等
        self.iv = "\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0"  # 正确
        # self.iv = chr(0) * 16  # 正确
        # self.iv = "0000000000000000" 错误
        print 'Self.iv:', self.iv.encode('hex')

    def encrypt(self, data):  # 加密
        data = self.pkcs7padding(data)
        cipher = AES.new(self.key, AES.MODE_CBC, self.iv)
        encrypted = cipher.encrypt(data)
        return base64.b64encode(encrypted)

    def decrypt(self, data):  # 解密
        data = base64.b64decode(data)
        print 'Base64Decode:', data.encode('hex')
        cipher = AES.new(self.key, AES.MODE_CBC, self.iv)
        decrypted = cipher.decrypt(data)
        decrypted = self.pkcs7unpadding(decrypted)
        return decrypted

    def pkcs7padding(self, data):
        bs = AES.block_size
        padding = bs - len(data) % bs
        padding_text = chr(padding) * padding
        return data + padding_text

    def pkcs7unpadding(self, data):
        lengt = len(data)
        unpadding = ord(data[lengt - 1])
        return data[0:lengt - unpadding]


if __name__ == '__main__':
    main()
