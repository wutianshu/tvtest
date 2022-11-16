# db
CREATE TABLE `mock` (
  `id` int(10) NOT NULL AUTO_INCREMENT COMMENT '主键',
  `key` varchar(255) DEFAULT NULL,
  `head` varchar(2048) DEFAULT NULL,
  `body` text,
  `desc` varchar(255) DEFAULT NULL,
  `owner` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `key` (`key`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8;


CREATE TABLE `api_call_statis` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `endpoint` varchar(64) COLLATE utf8mb4_bin NOT NULL,
  `count` int(11) DEFAULT NULL,
  `module` varchar(32) COLLATE utf8mb4_bin NOT NULL,
  `method` varchar(32) COLLATE utf8mb4_bin NOT NULL,
  `path` varchar(32) COLLATE utf8mb4_bin NOT NULL,
  `last_access_time` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `endpoint` (`endpoint`),
  UNIQUE KEY `path` (`path`)
) ENGINE=InnoDB AUTO_INCREMENT=214 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin;


CREATE TABLE `api_call_statis_items` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `endpoint` varchar(64) COLLATE utf8mb4_bin NOT NULL,
  `module` varchar(32) COLLATE utf8mb4_bin NOT NULL,
  `method` varchar(32) COLLATE utf8mb4_bin NOT NULL,
  `path` varchar(32) COLLATE utf8mb4_bin NOT NULL,
  `create_time` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `endpoint` (`endpoint`),
  KEY `path` (`path`)
) ENGINE=InnoDB AUTO_INCREMENT=114128 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin COMMENT='使用统计明细表';


CREATE TABLE `webform` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `webformKey` varchar(64) COLLATE utf8mb4_bin NOT NULL,
  `webformName` varchar(64) COLLATE utf8mb4_bin DEFAULT NULL,
  `webformDesc` varchar(2048) COLLATE utf8mb4_bin DEFAULT NULL,
  `owner` varchar(128) COLLATE utf8mb4_bin DEFAULT NULL,
  `webformRules` varchar(4096) COLLATE utf8mb4_bin DEFAULT NULL,
  `webformOption` varchar(4096) COLLATE utf8mb4_bin DEFAULT NULL,
  `domain` varchar(64) COLLATE utf8mb4_bin DEFAULT NULL,
  `module` varchar(64) COLLATE utf8mb4_bin NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `webformKey` (`webformKey`)
) ENGINE=InnoDB AUTO_INCREMENT=246 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin;

# 环境变量
TVTEST_USER=root

TVTEST_PASS=root

TVTEST_DB=video

TVTEST_HOST=127.0.0.1

TVTEST_ENV=production/default


# target
\\tvtest\tvtest\__init__.py

