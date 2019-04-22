## CspReport
记录浏览器触发CSP拦截规则的服务端


Apache端csp规则配置示例:  
`Header set Content-Security-Policy "default-src * data: blob:; script-src 'self' 'unsafe-inline' 'unsafe-eval' *.google.com ga-dev-tools.appspot.com maps.googleapis.com api.map.baidu.com *.map.bdimg.com; style-src data: blob: 'unsafe-inline' *; child-src 'self' index.baidu.com accounts.google.com content.googleapis.com *.testdomain.cn *.testdomain.com; object-src 'none'; img-src * data:; report-uri http://www.testdomain.com/csp-report.php"`

* csp-report.php 接收端文件
* csp_info.sql 存储数据的表结构