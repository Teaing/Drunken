#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-
# Author:Tea

from itsdangerous import base64_encode, base64_decode
from pbkdf2 import PBKDF2
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad


def main():
    cipher = AESWithPBKDF2SHA1(key=pwd)
    decriptData = cipher.decrypt(b64EncData=encData)
    cipher = AESWithPBKDF2SHA1(key=pwd)
    cipher.encrypt(textData=decriptData)


class AESWithPBKDF2SHA1:
    def __init__(self, key, iv=b'\0' * 16):
        # iv=b'\0' * 16 ok
        # iv='\0' * error
        self.iv = iv
        self.key = self.getPBKDF2Key(key)
        self.cipher = AES.new(self.key, AES.MODE_CBC, IV=self.iv)

    def getPBKDF2Key(self, key):
        PBKDF2Salt = b'\0' * 16  # Pbkdf2 Salt value
        print('PBKDF2Hash:',
              PBKDF2(passphrase=key, salt=PBKDF2Salt, iterations=1000).hexread(16))  # show the encrypt key HASH
        return PBKDF2(key, PBKDF2Salt).read(16)

    def encrypt(self, textData):  # encrypt data method
        padData = pad(textData.encode('utf-8'), AES.block_size)
        encData = self.cipher.encrypt(padData)
        b64EncData = str(base64_encode(encData), 'utf-8')
        print('encryptData:', b64EncData)
        return b64EncData

    def decrypt(self, b64EncData):  # decrypt data method
        encData = base64_decode(b64EncData)
        decData = unpad(self.cipher.decrypt(encData), AES.block_size)
        enCodeData = str(decData, 'utf-8')
        print('decryptData:', enCodeData)
        return enCodeData


if __name__ == '__main__':
    main()
