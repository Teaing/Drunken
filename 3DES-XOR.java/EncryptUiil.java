import java.io.PrintStream;
import java.security.SecureRandom;
import javax.crypto.Cipher;
import javax.crypto.SecretKey;
import javax.crypto.SecretKeyFactory;
import javax.crypto.spec.DESedeKeySpec;
import sun.misc.BASE64Decoder;
import sun.misc.BASE64Encoder;

public class EncryptUtil
{
  public static String EncryptBy3DES(String src, String DES_KEY)
  {
    String result = null;
    try
    {
      SecureRandom secureRandom = new SecureRandom();
      DESedeKeySpec sedeKeySpec = new DESedeKeySpec(DES_KEY.getBytes());
      SecretKeyFactory secretKeyFactory = SecretKeyFactory.getInstance("DESede");
      SecretKey key = secretKeyFactory.generateSecret(sedeKeySpec);
      Cipher cipher = Cipher.getInstance("DESede/ECB/PKCS5Padding");
      cipher.init(1, key, secureRandom);
      byte[] bytesresult = cipher.doFinal(src.getBytes());
      result = new BASE64Encoder().encode(bytesresult);
    }
    catch (Exception e)
    {
      e.printStackTrace();
    }
    return result;
  }
  
  public static String decryptBy3DES(String src, String DES_KEY)
  {
    String deresult = null;
    try
    {
      SecureRandom secureRandom = new SecureRandom();
      DESedeKeySpec sedeKeySpec = new DESedeKeySpec(DES_KEY.getBytes());
      
      SecretKeyFactory secretKeyFactory = SecretKeyFactory.getInstance("DESede");
      SecretKey key = secretKeyFactory.generateSecret(sedeKeySpec);
      
      Cipher cipher = Cipher.getInstance("DESede/ECB/PKCS5Padding");
      cipher.init(2, key, secureRandom);
      
      byte[] bytesresult = cipher.doFinal(new BASE64Decoder().decodeBuffer(src));
      deresult = new String(bytesresult, "UTF-8");
    }
    catch (Exception e)
    {
      e.printStackTrace();
    }
    return deresult;
  }