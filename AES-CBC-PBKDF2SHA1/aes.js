const CryptoJS = require("crypto-js");

const SLAT_IV = CryptoJS.enc.Hex.parse('00000000000000000000000000000000')

class AESDecryptOrEncrypt {
    constructor(passPhrase, salt, iv) {
        this.keySize = 128 / 32
        this.iterationCount = 1000
        this.passPhrase = passPhrase
        this.salt = (salt == null) ? SLAT_IV : CryptoJS.enc.Hex.parse(salt)
        this.iv = (iv == null) ? SLAT_IV : CryptoJS.enc.Hex.parse(iv)
    }

    // 生成key
    generateKey(plainText) {
        var key = CryptoJS.PBKDF2(
            this.passPhrase,
            this.salt,
            {keySize: this.keySize, iterations: this.iterationCount})
        console.log("keyReal:" + key)
        console.log("salt:" + this.salt)
        console.log("keySize:" + this.keySize)
        console.log('passPhrase:' + this.passPhrase)
        console.log("iv:" + this.iv)
        console.log('key:' + key)
        return key
    }

    /**
     * AES加密
     */
    AESEncrypt(plainText) {
        var key = this.generateKey()
        console.log("salt:" + this.salt)
        console.log("keySize:" + this.keySize)
        console.log('passPhrase:' + this.passPhrase)
        console.log("iv:" + this.iv)
        console.log('key:' + key)
        var encrypted = CryptoJS.AES.encrypt(
            plainText,
            key,
            {iv: this.iv})
        return encrypted.ciphertext.toString(CryptoJS.enc.Base64)
    }

    /**
     * 字符串转Base64
     * @param str
     */
    strToBase64(str) {
        var newStr = CryptoJS.enc.Utf8.parse(str)
        var base64 = CryptoJS.enc.Base64.stringify(newStr)
        return base64
    }

    /**
     * AES解密
     */
    AESDecrypt(cipherText) {
        var key = this.generateKey()
        var cipherParams = CryptoJS.lib.CipherParams.create({
            ciphertext: CryptoJS.enc.Base64.parse(cipherText)
        })
        // console.log(cipherParams)
        var decrypted = CryptoJS.AES.decrypt(
            cipherParams,
            key,
            {iv: this.iv})
        console.log("salt:" + this.salt)
        console.log("keySize:" + this.keySize)
        console.log('passPhrase:' + this.passPhrase)
        console.log("iv:" + this.iv)
        console.log('key:' + key)
        return decrypted.toString(CryptoJS.enc.Utf8)
    }
}

module.exports = AESDecryptOrEncrypt;
