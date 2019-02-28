-- MySQL dump 10.13  Distrib 8.0.13, for Win64 (x86_64)
--
-- Host: localhost    Database: movieweb
-- ------------------------------------------------------
-- Server version	8.0.13

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
 SET NAMES utf8 ;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `admin`
--

DROP TABLE IF EXISTS `admin`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `admin` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) DEFAULT NULL,
  `pwd` varchar(100) DEFAULT NULL,
  `is_super` smallint(6) DEFAULT NULL,
  `role_id` int(11) DEFAULT NULL,
  `addtime` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`),
  KEY `role_id` (`role_id`),
  KEY `ix_admin_addtime` (`addtime`),
  CONSTRAINT `admin_ibfk_1` FOREIGN KEY (`role_id`) REFERENCES `role` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `admin`
--

LOCK TABLES `admin` WRITE;
/*!40000 ALTER TABLE `admin` DISABLE KEYS */;
INSERT INTO `admin` VALUES (1,'zzzzzyk','pbkdf2:sha256:50000$ZOubQmoV$f721a1cf51178ed0e1790998df183835e0e423a5edd1d76f8402983acd7f24e8',0,1,'2019-01-17 23:47:36'),(2,'zzzzzyk1','pbkdf2:sha256:50000$1jXp8hfS$cee467cb1aefe79074bbbc741ca49e43e514c429828b894d30bf17d5819057d8',0,1,'2019-02-13 12:05:27'),(3,'zzzzzyk123','pbkdf2:sha256:50000$j5n7VZqz$99f2c1daf9ca7f3d267b1dc6f94f5dd0adefce264f1452c3d6256e6ddfbc84eb',NULL,1,'2019-02-14 19:35:01'),(4,'zyktag','pbkdf2:sha256:50000$4VJg0bWJ$f5618d9917b5bf0f13587b5672dc9946be365acb2634dc2232f1bf5a407c7bad',1,5,'2019-02-15 15:26:54');
/*!40000 ALTER TABLE `admin` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `adminlog`
--

DROP TABLE IF EXISTS `adminlog`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `adminlog` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `admin_id` int(11) DEFAULT NULL,
  `ip` varchar(100) DEFAULT NULL,
  `addtime` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `admin_id` (`admin_id`),
  KEY `ix_adminlog_addtime` (`addtime`),
  CONSTRAINT `adminlog_ibfk_1` FOREIGN KEY (`admin_id`) REFERENCES `admin` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `adminlog`
--

LOCK TABLES `adminlog` WRITE;
/*!40000 ALTER TABLE `adminlog` DISABLE KEYS */;
/*!40000 ALTER TABLE `adminlog` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `alembic_version`
--

DROP TABLE IF EXISTS `alembic_version`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `alembic_version` (
  `version_num` varchar(32) NOT NULL,
  PRIMARY KEY (`version_num`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `alembic_version`
--

LOCK TABLES `alembic_version` WRITE;
/*!40000 ALTER TABLE `alembic_version` DISABLE KEYS */;
INSERT INTO `alembic_version` VALUES ('ee665c7b9095');
/*!40000 ALTER TABLE `alembic_version` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth`
--

DROP TABLE IF EXISTS `auth`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `auth` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(64) DEFAULT NULL,
  `url` varchar(255) DEFAULT NULL,
  `addtime` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`),
  UNIQUE KEY `url` (`url`),
  KEY `ix_auth_addtime` (`addtime`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth`
--

LOCK TABLES `auth` WRITE;
/*!40000 ALTER TABLE `auth` DISABLE KEYS */;
INSERT INTO `auth` VALUES (1,'添加标签','/tag/add',NULL),(2,'删除标签','/tag/del/<int:id>','2019-02-13 10:04:41'),(3,'修改标签','/tag/edit/<int:id>','2019-02-13 10:04:41'),(4,'查看标签','/tag/list/<int:page>/',NULL);
/*!40000 ALTER TABLE `auth` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `comment`
--

DROP TABLE IF EXISTS `comment`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `comment` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `content` text,
  `movie_id` int(11) DEFAULT NULL,
  `user_id` int(11) DEFAULT NULL,
  `addtime` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `movie_id` (`movie_id`),
  KEY `user_id` (`user_id`),
  KEY `ix_comment_addtime` (`addtime`),
  CONSTRAINT `comment_ibfk_1` FOREIGN KEY (`movie_id`) REFERENCES `movie` (`id`),
  CONSTRAINT `comment_ibfk_2` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=21 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `comment`
--

LOCK TABLES `comment` WRITE;
/*!40000 ALTER TABLE `comment` DISABLE KEYS */;
INSERT INTO `comment` VALUES (2,'棒',1,78,'2019-02-10 21:10:25'),(3,'爽',1,75,'2019-02-10 21:10:25'),(4,'刺激',1,79,'2019-02-10 21:10:25'),(5,'666',1,62,'2019-02-10 21:10:25'),(6,'666',1,NULL,'2019-02-10 21:10:25'),(7,'666',1,NULL,'2019-02-10 21:10:25'),(8,'<p>真香</p>',1,89,'2019-02-20 11:18:58'),(10,'<p>666</p>',1,89,'2019-02-20 11:21:27'),(11,'<p><img src=\"http://img.baidu.com/hi/jx2/j_0001.gif\"/></p>',1,89,'2019-02-20 11:26:08'),(12,'<p><img src=\"http://img.baidu.com/hi/jx2/j_0001.gif\"/></p>',1,89,'2019-02-20 11:33:10'),(13,'<p>234<br/></p>',1,89,'2019-02-20 11:33:10'),(14,'<p>111</p>',1,89,'2019-02-20 11:33:10'),(15,'<p><img src=\"http://img.baidu.com/hi/jx2/j_0004.gif\"/></p>',1,90,'2019-02-20 12:03:56'),(16,'<p><img src=\"http://img.baidu.com/hi/tsj/t_0015.gif\"/>美滋滋</p>',1,90,'2019-02-20 12:13:48'),(17,'<p>666</p>',1,90,'2019-02-20 12:34:23'),(18,'<p><img src=\"http://img.baidu.com/hi/jx2/j_0005.gif\"/></p>',1,90,'2019-02-20 12:34:23'),(19,'<p>真香</p>',1,90,'2019-02-21 08:05:09'),(20,'<p><img src=\"http://img.baidu.com/hi/jx2/j_0002.gif\"/></p>',1,89,'2019-02-21 08:14:08');
/*!40000 ALTER TABLE `comment` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `movie`
--

DROP TABLE IF EXISTS `movie`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `movie` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `title` varchar(128) DEFAULT NULL,
  `url` varchar(255) DEFAULT NULL,
  `info` text,
  `logo` varchar(255) DEFAULT NULL,
  `star` smallint(6) DEFAULT NULL,
  `playnum` bigint(20) DEFAULT NULL,
  `commentnum` bigint(20) DEFAULT NULL,
  `tag_id` int(11) DEFAULT NULL,
  `area` varchar(255) DEFAULT NULL,
  `release_time` date DEFAULT NULL,
  `length` varchar(128) DEFAULT NULL,
  `addtime` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `logo` (`logo`),
  UNIQUE KEY `title` (`title`),
  UNIQUE KEY `url` (`url`),
  KEY `tag_id` (`tag_id`),
  KEY `ix_movie_addtime` (`addtime`),
  CONSTRAINT `movie_ibfk_1` FOREIGN KEY (`tag_id`) REFERENCES `tag` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `movie`
--

LOCK TABLES `movie` WRITE;
/*!40000 ALTER TABLE `movie` DISABLE KEYS */;
INSERT INTO `movie` VALUES (1,'环太平洋','20190210210804ef645b5dd8934c72815b062f366ffc64.mp4','环太平洋','201902102108047f63cf67afe245caace95a62d05eb27c.png',3,236,13,3,'中国','2019-02-06','3','2019-02-10 11:24:35');
/*!40000 ALTER TABLE `movie` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `moviecol`
--

DROP TABLE IF EXISTS `moviecol`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `moviecol` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `movie_id` int(11) DEFAULT NULL,
  `user_id` int(11) DEFAULT NULL,
  `addtime` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `movie_id` (`movie_id`),
  KEY `user_id` (`user_id`),
  KEY `ix_moviecol_addtime` (`addtime`),
  CONSTRAINT `moviecol_ibfk_1` FOREIGN KEY (`movie_id`) REFERENCES `movie` (`id`),
  CONSTRAINT `moviecol_ibfk_2` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `moviecol`
--

LOCK TABLES `moviecol` WRITE;
/*!40000 ALTER TABLE `moviecol` DISABLE KEYS */;
INSERT INTO `moviecol` VALUES (1,1,90,'2019-02-21 03:45:25'),(2,1,75,'2019-02-10 21:35:53'),(3,1,62,'2019-02-10 21:35:53'),(4,1,NULL,'2019-02-10 21:35:53'),(5,1,78,'2019-02-10 21:35:53');
/*!40000 ALTER TABLE `moviecol` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `oplog`
--

DROP TABLE IF EXISTS `oplog`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `oplog` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `admin_id` int(11) DEFAULT NULL,
  `ip` varchar(100) DEFAULT NULL,
  `reason` varchar(600) DEFAULT NULL,
  `addtime` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `admin_id` (`admin_id`),
  KEY `ix_oplog_addtime` (`addtime`),
  CONSTRAINT `oplog_ibfk_1` FOREIGN KEY (`admin_id`) REFERENCES `admin` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `oplog`
--

LOCK TABLES `oplog` WRITE;
/*!40000 ALTER TABLE `oplog` DISABLE KEYS */;
/*!40000 ALTER TABLE `oplog` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `preview`
--

DROP TABLE IF EXISTS `preview`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `preview` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `title` varchar(128) DEFAULT NULL,
  `logo` varchar(255) DEFAULT NULL,
  `addtime` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `logo` (`logo`),
  UNIQUE KEY `title` (`title`),
  KEY `ix_preview_addtime` (`addtime`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `preview`
--

LOCK TABLES `preview` WRITE;
/*!40000 ALTER TABLE `preview` DISABLE KEYS */;
INSERT INTO `preview` VALUES (1,'权利的游戏','2019022011340936e12a27bcb745dd86c6e3d907667c17.jpg','2019-02-20 03:20:29'),(2,'让子弹飞','20190220112836589555cf4cbe4dbcb4e3169526d5e483.jpg','2019-02-20 03:20:29'),(3,'纸牌屋','2019022011360412b7319f59da4e27ad61b10f068fc1af.jpg','2019-02-20 03:20:29'),(4,'千与千寻','2019022011433620d5c9bdea204d939c261df8f719cfe5.jpg','2019-02-20 03:20:29'),(5,'大护法','201902201143430311e224563547068418b9e00e82228d.jpg','2019-02-20 03:20:29');
/*!40000 ALTER TABLE `preview` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `role`
--

DROP TABLE IF EXISTS `role`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `role` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(64) DEFAULT NULL,
  `auths` varchar(512) DEFAULT NULL,
  `addtime` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`),
  KEY `ix_role_addtime` (`addtime`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `role`
--

LOCK TABLES `role` WRITE;
/*!40000 ALTER TABLE `role` DISABLE KEYS */;
INSERT INTO `role` VALUES (1,'超级管理员',NULL,NULL),(5,'标签管理员','1,2,3,4','2019-02-14 07:16:39');
/*!40000 ALTER TABLE `role` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tag`
--

DROP TABLE IF EXISTS `tag`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `tag` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(128) DEFAULT NULL,
  `addtime` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`),
  KEY `ix_tag_addtime` (`addtime`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tag`
--

LOCK TABLES `tag` WRITE;
/*!40000 ALTER TABLE `tag` DISABLE KEYS */;
INSERT INTO `tag` VALUES (1,'恐怖','2019-01-18 04:20:39'),(2,'科幻','2019-01-18 04:20:39'),(3,'动作','2019-01-18 05:14:56'),(4,'爱情','2019-01-18 05:22:24'),(5,'喜剧','2019-02-20 12:34:23');
/*!40000 ALTER TABLE `tag` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user`
--

DROP TABLE IF EXISTS `user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `user` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(64) DEFAULT NULL,
  `pwd` varchar(128) DEFAULT NULL,
  `email` varchar(128) DEFAULT NULL,
  `phone` varchar(11) DEFAULT NULL,
  `info` text,
  `face` varchar(255) DEFAULT NULL,
  `addtime` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `email` (`email`),
  UNIQUE KEY `face` (`face`),
  UNIQUE KEY `name` (`name`),
  UNIQUE KEY `phone` (`phone`),
  KEY `ix_user_addtime` (`addtime`)
) ENGINE=InnoDB AUTO_INCREMENT=93 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user`
--

LOCK TABLES `user` WRITE;
/*!40000 ALTER TABLE `user` DISABLE KEYS */;
INSERT INTO `user` VALUES (62,'狗','1231','123451@123.com','12344445511','狗','222.png','2019-02-10 18:35:00'),(66,'猪2','1236','1234564@123.com','12344445515','猪','777.png','2019-02-10 18:35:00'),(67,'猪3','1237','1234565@123.com','12344445516','猪','888.png','2019-02-10 18:35:00'),(68,'猪5','1239','1234568@123.com','12344445518','猪','000.png','2019-02-10 18:35:00'),(69,'猪6','1240','1234560@123.com','12344445519','猪','5551.png','2019-02-10 18:35:00'),(70,'猪7','1241','1213456@123.com','12344445522','猪','5552.png','2019-02-10 18:35:00'),(71,'猪8','1242','1232456@123.com','12344445523','猪','5553.png','2019-02-10 18:35:00'),(72,'猪9','1243','1234356@123.com','12344445524','猪','5554.png','2019-02-10 18:35:00'),(74,'猪11','1245','2123456@123.com','12344445527','猪','5556.png','2019-02-10 18:35:09'),(75,'猪12','1230','1234567123.com','12344445555','猪','666.png','2019-02-10 21:04:30'),(78,'马','1234','1234562@123.com','12344445513','猪','333.png','2019-02-10 21:04:31'),(79,'猪1','1235','1234563@123.com','12344445514','猪','444.png','2019-02-10 21:04:31'),(87,'猪0','1244','1234536@123.com','12344445525','猪','5555.png','2019-02-10 21:04:31'),(89,'test1','pbkdf2:sha256:50000$qRIijJhf$dbe64803e61f1ecdca6d49be56c4fca5ed52a477cce7861e0cc4cb9f7030e6fa','12312312@qq.com','15412341234','666','timg.jpg','2019-02-18 08:16:58'),(90,'test2','pbkdf2:sha256:50000$vf7fCoAC$81756b1c237e22ac970a7a5d8c647e4dc153f240f08573a44135b8ecb6948627','123@qq.com','14411112222','','logo.png','2019-02-18 08:16:58'),(91,'1234','pbkdf2:sha256:50000$kTjtuE7z$a82ca231934d523289d88d1cba64ded05323c950b95949e97c76590f0a0ea69e','12333@qq.com','13344445555',NULL,NULL,'2019-02-19 08:20:21'),(92,'test5','pbkdf2:sha256:50000$i2SzckGE$5e8c398965595b812b07161a5b19d8fee66ac71476bd1383ea3c2cabd128fb02','111@qq.com','15599990000',NULL,NULL,'2019-02-19 08:24:52');
/*!40000 ALTER TABLE `user` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `userlog`
--

DROP TABLE IF EXISTS `userlog`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `userlog` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) DEFAULT NULL,
  `ip` varchar(128) DEFAULT NULL,
  `addtime` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `user_id` (`user_id`),
  KEY `ix_userlog_addtime` (`addtime`),
  CONSTRAINT `userlog_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=24 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `userlog`
--

LOCK TABLES `userlog` WRITE;
/*!40000 ALTER TABLE `userlog` DISABLE KEYS */;
INSERT INTO `userlog` VALUES (1,89,'127.0.0.1','2019-02-18 10:19:35'),(2,89,'127.0.0.1','2019-02-19 04:57:27'),(3,89,'127.0.0.1','2019-02-19 07:51:19'),(4,89,'127.0.0.1','2019-02-19 08:26:21'),(5,89,'127.0.0.1','2019-02-19 09:07:20'),(6,89,'127.0.0.1','2019-02-19 09:14:46'),(7,89,'127.0.0.1','2019-02-19 09:14:46'),(8,89,'127.0.0.1','2019-02-19 09:14:46'),(9,89,'127.0.0.1','2019-02-19 09:14:46'),(10,89,'127.0.0.1','2019-02-19 09:14:46'),(11,89,'127.0.0.1','2019-02-19 09:27:44'),(12,89,'127.0.0.1','2019-02-19 11:40:57'),(13,89,'127.0.0.1','2019-02-20 08:53:06'),(14,89,'127.0.0.1','2019-02-20 08:53:06'),(15,89,'127.0.0.1','2019-02-20 10:31:14'),(16,90,'127.0.0.1','2019-02-20 12:03:56'),(17,90,'127.0.0.1','2019-02-20 12:34:23'),(18,90,'127.0.0.1','2019-02-21 03:03:09'),(19,89,'127.0.0.1','2019-02-21 08:14:08'),(20,89,'127.0.0.1','2019-02-21 09:16:07'),(21,89,'127.0.0.1','2019-02-24 08:11:37'),(22,89,'127.0.0.1','2019-02-24 15:13:07'),(23,89,'127.0.0.1','2019-02-25 11:43:49');
/*!40000 ALTER TABLE `userlog` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2019-02-28 11:09:57
