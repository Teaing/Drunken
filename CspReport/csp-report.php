<?php
/**
 * Created by PhpStorm.
 * User: Tea
 * Date: 2017/10/25
 * Time: 9:20
 */

@error_reporting(E_ALL);

if ("POST" != $_SERVER["REQUEST_METHOD"]) {
    exit('Failure');
}

$csp_json_data = file_get_contents("php://input");
$scp_data = json_decode($csp_json_data, true);

if (!isset($scp_data["csp-report"])) {
    exit('Failure');
}

$scp_source_array = array(
    "0" => "admin.testdomain.com",
    "1" => "www.testdomain.com",
    "2" => "vip.testdomain.com",
);

$scp_report_data = $scp_data["csp-report"];

if (isset($scp_report_data["document-uri"]) and isset($scp_report_data["violated-directive"]) and isset($scp_report_data["blocked-uri"])) {
    $scp_report_data["csp_source"] = array_search("admin.testdomain.com", $scp_source_array); // get scp source key 0 , 1 , 2
    $scp_report_data["insert_time"] = time();
    $scp_report_data["document-uri"] = $scp_report_data["document-uri"] ? htmlspecialchars($scp_report_data["document-uri"], ENT_QUOTES) : "";
    $scp_report_data["referrer"] = $scp_report_data["referrer"] ? htmlspecialchars($scp_report_data["referrer"], ENT_QUOTES) : "";
    $scp_report_data["violated-directive"] = $scp_report_data["violated-directive"] ? htmlspecialchars($scp_report_data["violated-directive"], ENT_QUOTES) : "";
    $scp_report_data["effective-directive"] = $scp_report_data["effective-directive"] ? htmlspecialchars($scp_report_data["effective-directive"], ENT_QUOTES) : "";
    $scp_report_data["original-policy"] = $scp_report_data["original-policy"] ? htmlspecialchars($scp_report_data["original-policy"], ENT_QUOTES) : "";
    $scp_report_data["disposition"] = $scp_report_data["disposition"] ? htmlspecialchars($scp_report_data["disposition"], ENT_QUOTES) : "";
    $scp_report_data["blocked-uri"] = $scp_report_data["blocked-uri"] ? htmlspecialchars($scp_report_data["blocked-uri"], ENT_QUOTES) : "";
    $scp_report_data["line-number"] = $scp_report_data["line-number"] ? intval($scp_report_data["line-number"]) : -1;
    $scp_report_data["source-file"] = $scp_report_data["source-file"] ? htmlspecialchars($scp_report_data["source-file"], ENT_QUOTES) : "";
    $scp_report_data["status-code"] = $scp_report_data["status-code"] ? intval($scp_report_data["status-code"]) : -1;
    $scp_report_data["script-sample"] = $scp_report_data["script-sample"] ? htmlspecialchars($scp_report_data["script-sample"], ENT_QUOTES) : "";
    sql_insert($scp_report_data);
    echo 'Success';
} else {
    exit('Failure');
}


function sql_insert($scp_report_data)
{
    $mysql_conf = array(
        'host' => 'localhost',
        'db' => 'csp_report',
        'db_user' => 'root',
        'db_pwd' => 'root',
    );
    $pdo = new PDO("mysql:host=" . $mysql_conf['host'] . ";dbname=" . $mysql_conf['db'], $mysql_conf['db_user'], $mysql_conf['db_pwd']);
    $pdo->exec("set names 'utf8'");
    $pdo_sql = "INSERT INTO csp_info (`document_url`, `referrer`, `violated_directive`, `effective_directive`, `original_policy`,`disposition`,`blocked_uri`,`line_number`,`source_file`,`status_code`,`script_sample`,`insert_time`,`csp_source`) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)";
    $pdo_array = array($scp_report_data["document-uri"], $scp_report_data["referrer"], $scp_report_data["violated-directive"], $scp_report_data["effective-directive"], $scp_report_data["original-policy"], $scp_report_data["disposition"], $scp_report_data["blocked-uri"], $scp_report_data["line-number"], $scp_report_data["source-file"], $scp_report_data["status-code"], $scp_report_data["script-sample"], $scp_report_data["insert_time"], $scp_report_data["csp_source"]);
    $sth = $pdo->prepare($pdo_sql);
    $sth->execute($pdo_array);
    $pdo = null;
}

?>
