## DLL Hijack Tools

#### Dll 劫持工具收集  

##### 下面为后面参考文章的核心内容

##### 调用LoadLibrary或者LoadLibraryEx函数时可以使用DLL的相对路径也可以使用绝对路径，但是很多情况下，开发人员都是使用了相对路径来进行DLL的加载。那么，在这种情况下，Windows系统会按照特定的顺序去搜索一些目录，来确定DLL的完整路径

##### 调用LoadLibrary函数时，系统会依次从下面几个位置去查找所需要调用的DLL文件
```
1.程序所在目录。
2.加载 DLL 时所在的当前目录。
3.系统目录即 SYSTEM32 目录。
4.16位系统目录即 SYSTEM 目录。
5.Windows目录。
6.PATH环境变量中列出的目录
```

##### 微软为了防止DLL劫持漏洞的产生，在XP SP2之后，添加了一个SafeDllSearchMode的注册表属性

##### 注册表路径如下：
```
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Control\Session Manager\SafeDllSearchMode
```

##### 当SafeDllSearchMode的值设置为1，即安全DLL搜索模式开启时，查找DLL的目录顺序如下：
```
1.程序所在目录
2.系统目录即 SYSTEM32 目录。
3.16位系统目录即 SYSTEM 目录。
4.Windows目录。
5.加载 DLL 时所在的当前目录。
6.PATH环境变量中列出的目录。
```

#### XP系统之后发布的Windows操作系统中，默认情况下并未开启安全DLL搜索模式。

##### 微软为了更进一步的防御系统的DLL被劫持，将一些容易被劫持的系统DLL写进了一个注册表项中，那么凡是此项下的DLL文件就会被禁止从EXE自身所在的目录下调用，而只能从系统目录即SYSTEM32目录下调用

##### 注册表路径如下：
```
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Control\Session Manager\KnownDLLs
```

##### 以前经常使用的一些劫持DLL已经被加入了KnownDLLs注册表项，这就意味着使用诸如usp10.dll，lpk.dll，ws2_32.dll去进行DLL劫持已经失效

##### Windows操作系统通过“DLL路径搜索目录顺序”和“KnownDLLs注册表项”的机制来确定应用程序所要调用的DLL的路径，之后，应用程序就将DLL载入了自己的内存空间，执行相应的函数功能

##### 不过，微软又莫名其妙的允许用户在上述注册表路径中添加“ExcludeFromKnownDlls”注册表项，排除一些被“KnownDLLs注册表项”机制保护的DLL。也就是说，只要在“ExcludeFromKnownDlls”注册表项中添加你想劫持的DLL名称就可以对该DLL进行劫持，不过修改之后需要重新启动电脑才能生效

##### 在上述描述加载DLL的整个过程中，DLL劫持漏洞就是在系统进行安装“DLL路径搜索目录顺序”搜索DLL的时候发生的。无论安全DLL搜索模式是否开启，系统总是首先会从程序所在目录加载DLL，如果没有找到就按照上面的顺序依次进行搜索。那么，利用这个特性，攻击者就可以伪造一个相同名称，相同导出函数表的一个“假”DLL，并将每个导出函数转向到“真”DLL。将这个“假”DLL放到程序的目录下，当程序调用DLL中的函数时就会首先加载“假”DLL，在“假”DLL中攻击者已经加入了恶意代码，这时这些恶意代码就会被执行，之后，“假”DLL再将DLL调用流程转向“真”DLL，以免影响程序的正常执行

##### 编写一个用于劫持指定DLL的DLL文件，需要两个步骤：
```
1.查看被劫持的DLL的导出函数表。
2.编程实现劫持DLL向原DLL的导出函数的转发，并加入你的“恶意代码”。
```

##### DLL劫持漏洞测试步骤
```
1.启动应用程序
2.使用Process Explorer等类似软件查看该应用程序启动后加载的动态链接库。
3.从该应用程序已经加载的DLL列表中，查找在上述“KnownDLLs注册表项”中不存在的DLL。
4.编写第三步中获取到的DLL的劫持DLL。
5.将编写好的劫持DLL放到该应用程序目录下，重新启动该应用程序，检测是否劫持成功。
```

#### 防御方法
```
1.将所有需要使用到的DLL放在应用程序所在的目录，不放到系统目录或者其他目录
2.调用LoadLibrary，LoadLibraryEx等会进行模块加载操作的函数时，使用模块的绝对路径作为参数
3.在程序调用DLL时使用“白名单”+ “签名”进行DLL的验证
4.在开发应用程序时，在代码开头调用SetDllDirectory函数，把当前目录从DLL的搜索顺序列表中删除(这个API只能在打了KB2533623补丁的Windows7，2008上使用)
```

##### 工具地址(截止写此README的时候已经删除,通过找寻fork找到)：

https://github.com/coca1ne/DLL_Hijacker  
https://github.com/coca1ne/DLLHijack_Detecter/  

参考：[https://www.freebuf.com/articles/78807.html](https://www.freebuf.com/articles/78807.html)