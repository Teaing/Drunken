# 某JAVA程序key解密方法

#### 解密算法相关：3DES+XOR

最烦的是早异或的值，数值很大，因为经验不足，后面想到了大于65535的端口号，尝试了一下，道理一样。      

所以 （异或的key % 256） 就是异或的值了，得到40(自己写代码测试的时候，JAVA 可以直接使用这么大的值进行异或)

具体，见代码

最后生成key的方法，也跟原始加密一模一样  

```
➜  3DES-XOR.java git:(master) ✗ md5sum ***.key
da1ac466a99f80a343c3d18f43e444f1  ***.key
➜  3DES-XOR.java git:(master) ✗ md5sum newKeys.key
da1ac466a99f80a343c3d18f43e444f1  newKeys.key
```