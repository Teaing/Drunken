<html>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
<?php
error_reporting(E_ALL);
require_once('./config.php');
$username = "Test";
$content = addslashes($_REQUEST['content']);

if (empty($content)){
	die('Par Empty');
}
if(strpos($content, "<") === false && strpos($content, ">") === false)
{
	exit('不需要做下面的检查');
}
$ra1 = array('javascript', 'vbscript', 'expression', 'applet', 'meta', 'xml', 'blink', 'link', 'style', 'script', 'embed', 'object', 'iframe', 'frame', 'frameset', 'ilayer', 'layer', 'bgsound', 'title', 'base');
$ra2 = array('onabort', 'onactivate', 'onafterprint', 'onafterupdate', 'onbeforeactivate', 'onbeforecopy', 'onbeforecut', 'onbeforedeactivate', 'onbeforeeditfocus', 'onbeforepaste', 'onbeforeprint', 'onbeforeunload', 'onbeforeupdate', 'onblur', 'onbounce', 'oncellchange', 'onchange', 'onclick', 'oncontextmenu', 'oncontrolselect', 'oncopy', 'oncut', 'ondataavailable', 'ondatasetchanged', 'ondatasetcomplete', 'ondblclick', 'ondeactivate', 'ondrag', 'ondragend', 'ondragenter', 'ondragleave', 'ondragover', 'ondragstart', 'ondrop', 'onerror', 'onerrorupdate', 'onfilterchange', 'onfinish', 'onfocus', 'onfocusin', 'onfocusout', 'onhelp', 'onkeydown', 'onkeypress', 'onkeyup', 'onlayoutcomplete', 'onload', 'onlosecapture', 'onmousedown', 'onmouseenter', 'onmouseleave', 'onmousemove', 'onmouseout', 'onmouseover', 'onmouseup', 'onmousewheel', 'onmove', 'onmoveend', 'onmovestart', 'onpaste', 'onpropertychange', 'onreadystatechange', 'onreset', 'onresize', 'onresizeend', 'onresizestart', 'onrowenter', 'onrowexit', 'onrowsdelete', 'onrowsinserted', 'onscroll', 'onselect', 'onselectionchange', 'onselectstart', 'onstart', 'onstop', 'onsubmit', 'onunload');
$ra = array_merge($ra1, $ra2);
$found = true; // keep replacing as long as the previous round replaced something
$val = $content;
while ($found == true) {//循环
	$val_before = $val;// 赋值给$val
        for ($i = 0; $i < sizeof($ra); $i++) {//遍历$ra,也就是上面定义合并的关键字,总共98个值
		$pattern = '/';
                for ($j = 0; $j < strlen($ra[$i]); $j++) {
                    if ($j > 0) {
                        $pattern .= '(';
                        $pattern .= '(&#[xX]0{0,8}([9ab]);)';
                        $pattern .= '|';
                        $pattern .= '|(&#0;{0,8}([9|10|13]);)';
                        $pattern .= ')*';
                    }
                    $pattern .= $ra[$i][$j];
                }
                $pattern .= '/i';
                $replacement = substr($ra[$i], 0, 2) . '<x>' . substr($ra[$i], 2); // //加入<x>到规则关键字中
                $val = preg_replace($pattern, $replacement, $val); //替换掉原先的关键字
                if ($val_before == $val) {////没有更换，进入流程
                    $found = false;
                }
            }
        }
$sql_str = "INSERT INTO faq (`name`,`content`) VALUES ('{$username}','{$val}')";
$conn=mysql_connect($db_host,$db_user,$db_pass);//连接数据库

if(!$conn){
    echo "连接数据库不成功!";
}
mysql_select_db($db_dbname,$conn);//选择数据库
$result = mysql_query($sql_str, $conn) or print(mysql_error());//执行SQL语句
echo "你当前执行的sql语句为："."<br >";
echo $sql_str;
$sql_str = "SELECT id,name,content FROM faq ORDER BY ID DESC LIMIT 0,1";
echo "<br >你当前执行的sql语句为："."<br >";
echo $sql_str."</br>";
$result=mysql_query($sql_str);//执行SQL语句
while($row = mysql_fetch_array($result)){
    echo "用户ID：".$row['id']."<br >";
    echo "用户名：".$row['name']."<br >";
    echo "内容：".$row['content']."<br >";
	echo "------------------------------------------------------------------<br >";
}
mysql_close($conn); //关闭数据库连接
?>
</html>
