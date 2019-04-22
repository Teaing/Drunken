import java.security.MessageDigest;
import java.security.spec.AlgorithmParameterSpec;
import javax.crypto.Cipher;
import javax.crypto.spec.IvParameterSpec;
import javax.crypto.spec.SecretKeySpec;
import java.util.Base64;
import java.security.*;

class AESCrypt {
    private final Cipher cipher;
    private final SecretKeySpec key;
    private AlgorithmParameterSpec spec;

    AESCrypt()
            throws Exception {
        Security.addProvider(new org.bouncycastle.jce.provider.BouncyCastleProvider());
        MessageDigest localMessageDigest = MessageDigest.getInstance("SHA-256");
        localMessageDigest.update("HAHAHAHAHAHAHAHA".getBytes("UTF-8"));
        byte[] arrayOfByte = new byte[32];  //  私钥
        System.arraycopy(localMessageDigest.digest(), 0, arrayOfByte, 0, arrayOfByte.length);
        this.cipher = Cipher.getInstance("AES/CBC/PKCS7Padding", "BC");
        this.key = new SecretKeySpec(arrayOfByte, "AES");   // 第一个参数为私钥字节数，第二个为加密方式
        this.spec = getIV();    // Iv ,python表示这里需要 "\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0"
    }

    public String encrypt(String paramString)
            throws Exception {
        this.cipher.init(1, this.key, this.spec);
        return new String(Base64.getEncoder().encode(this.cipher.doFinal(paramString.getBytes("UTF-8"))), "UTF-8");
    }

    public String decrypt(String paramString)
            throws Exception {
        this.cipher.init(2, this.key, this.spec);
        byte[] arrayOfByte = Base64.getDecoder().decode(paramString);
        return new String(this.cipher.doFinal(arrayOfByte), "UTF-8");
    }

    public AlgorithmParameterSpec getIV() {
        byte[] arrayOfByte = new byte[16];
        arrayOfByte[0] = 0;
        arrayOfByte[1] = 0;
        arrayOfByte[2] = 0;
        arrayOfByte[3] = 0;
        arrayOfByte[4] = 0;
        arrayOfByte[5] = 0;
        arrayOfByte[6] = 0;
        arrayOfByte[7] = 0;
        arrayOfByte[8] = 0;
        arrayOfByte[9] = 0;
        arrayOfByte[10] = 0;
        arrayOfByte[11] = 0;
        arrayOfByte[12] = 0;
        arrayOfByte[13] = 0;
        arrayOfByte[14] = 0;
        arrayOfByte[15] = 0;
        return new IvParameterSpec(arrayOfByte);
    }
}

public class Main {

    public static void main(String[] args) throws Exception {
        String data = "我是密文";
        AESCrypt localAESCrypt = new AESCrypt();
        String decrypt_data = localAESCrypt.decrypt(data);
        System.out.println(decrypt_data);
    }
}
