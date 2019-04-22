/*
Navicat MySQL Data Transfer

Source Server         : 127.0.0.1
Source Server Version : 100108
Source Host           : localhost:3306
Source Database       : csp_report

Target Server Type    : MYSQL
Target Server Version : 100108
File Encoding         : 65001

Date: 2017-10-25 11:36:26
*/

SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for csp_info
-- ----------------------------
DROP TABLE IF EXISTS `csp_info`;
CREATE TABLE `csp_info` (
  `ID` int(11) NOT NULL AUTO_INCREMENT,
  `document_url` varchar(255) DEFAULT NULL,
  `referrer` varchar(255) DEFAULT NULL,
  `violated_directive` varchar(255) DEFAULT NULL,
  `effective_directive` varchar(255) DEFAULT NULL,
  `original_policy` varchar(255) DEFAULT NULL,
  `disposition` varchar(255) DEFAULT NULL,
  `blocked_uri` varchar(255) DEFAULT NULL,
  `line_number` int(11) DEFAULT NULL,
  `source_file` varchar(255) DEFAULT NULL,
  `status_code` int(11) DEFAULT NULL,
  `script_sample` varchar(255) DEFAULT '',
  `insert_time` int(11) DEFAULT NULL COMMENT '请求时间',
  `csp_source` int(11) DEFAULT NULL COMMENT '数据来源',
  PRIMARY KEY (`ID`),
  KEY `ID` (`ID`),
  KEY `document_url` (`document_url`),
  KEY `referrer` (`referrer`),
  KEY `violated_directive` (`violated_directive`),
  KEY `effective_directive` (`effective_directive`),
  KEY `original_policy` (`original_policy`),
  KEY `disposition` (`disposition`),
  KEY `blocked_uri` (`blocked_uri`),
  KEY `line_number` (`line_number`),
  KEY `source_file` (`source_file`),
  KEY `status_code` (`status_code`),
  KEY `script_sample` (`script_sample`),
  KEY `csp_source` (`csp_source`),
  KEY `insert_time` (`insert_time`) USING BTREE
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
