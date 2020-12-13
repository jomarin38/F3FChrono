CREATE DATABASE  IF NOT EXISTS `f3f_chrono` /*!40100 DEFAULT CHARACTER SET utf8mb4 */;
USE `f3f_chrono`;
-- MySQL dump 10.17  Distrib 10.3.25-MariaDB, for debian-linux-gnu (x86_64)
--
-- Host: 127.0.0.1    Database: f3f_chrono
-- ------------------------------------------------------
-- Server version	10.3.25-MariaDB-0ubuntu0.20.04.1

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `chrono`
--

DROP TABLE IF EXISTS `chrono`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `chrono` (
  `chrono_id` int(11) NOT NULL AUTO_INCREMENT,
  `run_time` double DEFAULT NULL,
  `min_wind_speed` double DEFAULT NULL,
  `max_wind_speed` double DEFAULT NULL,
  `mean_wind_speed` double DEFAULT NULL,
  `wind_direction` double DEFAULT NULL,
  `start_date` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  `end_date` timestamp NULL DEFAULT NULL,
  `lap1` double DEFAULT NULL,
  `lap2` double DEFAULT NULL,
  `lap3` double DEFAULT NULL,
  `lap4` double DEFAULT NULL,
  `lap5` double DEFAULT NULL,
  `lap6` double DEFAULT NULL,
  `lap7` double DEFAULT NULL,
  `lap8` double DEFAULT NULL,
  `lap9` double DEFAULT NULL,
  `lap10` double DEFAULT NULL,
  `climbout_time` double DEFAULT NULL,
  PRIMARY KEY (`chrono_id`)
) ENGINE=InnoDB AUTO_INCREMENT=1002 DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `chrono`
--

LOCK TABLES `chrono` WRITE;
/*!40000 ALTER TABLE `chrono` DISABLE KEYS */;
INSERT INTO `chrono` VALUES (281,10.64,0,0,0,0,'2020-04-25 14:37:02','2020-04-25 14:37:13',1.883,1.145,1.024,1.768,0.912,0.792,0.709,0.864,0.685,0.858,NULL),(829,4.266,-1,-1,0,0,'2020-10-31 13:46:47','2020-10-31 13:46:51',0.397,0.401,0.32,0.478,0.432,0.407,0.416,0.459,0.494,0.462,0.761),(904,2.395,-1,-1,0,0,'2020-11-01 08:53:22','2020-11-01 08:53:25',0.254,0.254,0.239,0.234,0.239,0.23,0.234,0.25,0.22,0.241,0.661),(913,3.12,-1,-1,0,0,'2020-11-01 09:50:53','2020-11-01 09:50:56',0.235,0.238,0.249,0.234,0.255,0.27,0.311,0.315,0.469,0.544,0.544),(966,2.198,-1,-1,0,0,'2020-11-01 15:42:39','2020-11-01 15:42:42',0.183,0.249,0.199,0.194,0.198,0.2,0.224,0.235,0.245,0.271,0.361);
/*!40000 ALTER TABLE `chrono` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `competitor`
--

DROP TABLE IF EXISTS `competitor`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `competitor` (
  `pilot_id` int(11) NOT NULL,
  `event_id` int(11) NOT NULL,
  `team` int(11) DEFAULT NULL,
  `bib_number` int(11) DEFAULT NULL,
  `present` tinyint(4) DEFAULT NULL,
  PRIMARY KEY (`pilot_id`,`event_id`),
  KEY `fk_competitor_event_idx` (`event_id`),
  CONSTRAINT `fk_competitor_event` FOREIGN KEY (`event_id`) REFERENCES `event` (`event_id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `fk_competitor_pilot` FOREIGN KEY (`pilot_id`) REFERENCES `pilot` (`pilot_id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `competitor`
--

LOCK TABLES `competitor` WRITE;
/*!40000 ALTER TABLE `competitor` DISABLE KEYS */;
INSERT INTO `competitor` VALUES (1,1,NULL,1,1),(2,1,NULL,2,1),(3,1,NULL,3,1),(4,1,NULL,4,1),(5,1,NULL,5,1),(6,1,NULL,6,1),(7,1,NULL,7,1),(8,1,NULL,8,1),(9,1,NULL,9,1),(10,1,NULL,10,1),(11,1,NULL,11,1),(12,1,NULL,12,1),(13,1,NULL,13,1),(14,1,NULL,14,1);
/*!40000 ALTER TABLE `competitor` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `event`
--

DROP TABLE IF EXISTS `event`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `event` (
  `event_id` int(11) NOT NULL AUTO_INCREMENT,
  `begin_date` timestamp NULL DEFAULT NULL,
  `end_date` timestamp NULL DEFAULT NULL,
  `location` varchar(100) DEFAULT NULL,
  `name` varchar(200) DEFAULT NULL,
  `min_allowed_wind_speed` double DEFAULT NULL,
  `max_allowed_wind_speed` double DEFAULT NULL,
  `max_wind_dir_dev` double DEFAULT NULL,
  `max_interruption_time` double DEFAULT NULL,
  `bib_start` int(11) DEFAULT 0,
  `flights_before_refly` int(11) DEFAULT 5,
  `dayduration` int(11) DEFAULT 1,
  `f3x_vault_id` int(11) DEFAULT NULL,
  `groups_number` int(11) DEFAULT NULL,
  PRIMARY KEY (`event_id`)
) ENGINE=InnoDB AUTO_INCREMENT=13 DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `event`
--

LOCK TABLES `event` WRITE;
/*!40000 ALTER TABLE `event` DISABLE KEYS */;
INSERT INTO `event` VALUES (1,'2019-10-25 22:00:00','2019-10-26 22:00:00','Col des Faisses','F3F Puy de Manse / Faisses 2019',3,25,45,1800,8,5,1,1706,1);
/*!40000 ALTER TABLE `event` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `pilot`
--

DROP TABLE IF EXISTS `pilot`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `pilot` (
  `pilot_id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(45) DEFAULT NULL,
  `first_name` varchar(45) DEFAULT NULL,
  `fai_id` varchar(45) DEFAULT NULL,
  `national_id` varchar(45) DEFAULT NULL,
  `f3x_vault_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`pilot_id`)
) ENGINE=InnoDB AUTO_INCREMENT=53 DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `pilot`
--

LOCK TABLES `pilot` WRITE;
/*!40000 ALTER TABLE `pilot` DISABLE KEYS */;
INSERT INTO `pilot` VALUES (1,'Mervelet','Matthieu','FRA1015','9908323',2520),(2,'Hours','Frederic','','',806),(3,'Philippe','Lanes','FRA 1153','',2297),(4,'Krebs','Michaël','FRA-30171','',2508),(5,'VINCENT','Arnaud','','0606738-AD',3541),(6,'MONET','Olivier','0700206-AD','',2558),(7,'Marin','Joel','','FRA 321',2256),(8,'FAURE','Martial','FRA30387','',2327),(9,'DELARBRE','Thomas','FRA-30128','',2252),(10,'Daviet','Sylvain','1601415','FRA30748',3528),(11,'Vaissier','Pascal','','FRA30832',3730),(12,'Delarbre','Serge','FRA795','',2602),(13,'CARLIN','Joël','FRA-30116','FRA-30116',2142),(14,'Rondel','Pierre','FRA23036','',630),(15,'Martinez Nieto','Lazaro','ESP-2739','264720',777),(16,'Arjona','Alfredo','ESP-2658','',783),(17,'Moro','Fernando','ESP-2802','',786),(18,'García','Eduardo','ESP-3225','',787),(19,'Treble','Mark','GBR163952','29373 ',326),(20,'Cantero','Carlos','ESP-2234','',789),(21,'Austen','André','','',788),(22,'Aymat','Carles','FAI 17411','',557),(23,'Kopp','Martin','SUI-51948','SUI-51948',1068),(24,'Del Barrio','Fernando','ESP 2237','',2002),(25,'Treble','John','GBR82099','GBR082099',334),(26,'Robertson','Tony','','',1212),(27,'Gil','Alejandro','','',1721),(28,'Wiklicky','Josef','AUT-3999991639','46012',776),(29,'Fricke','Andréas','FRA-7076','60122',815),(30,'Herrera','Jesus','ESP-2670','',778),(31,'Perlick','Dieter','GER-1868','19509',912),(32,'Salmhofer','Alfred','AUT 330039 0014','44148',2323),(33,'Ingles Elias','Aleix','','272367',3287),(34,'Elizondo','Iñaki','ESP1744','ESP-1744',785),(35,'Schneider','Daniel','GER-3521','19853',1135),(36,'Kowalski','Peter','GER 1873','Ger1873',1353),(37,'Alvarez','José Luis','','ESP 2609',1086),(38,'Hladky','Jiri','SUI-53672','',1793),(39,'Lopez','Angel','ESP-2608','',772),(40,'Silgado','Alvaro','17545','ESP-2661',773),(41,'Alonso','Fernando','ESP-3155','',775),(42,'Muñoz','Felix José','78597','',3149),(43,'Phillips','John','66398','',1362),(44,'Gomez-Mayan','Bernardo','87039','87039',2331),(45,'Dall\'ava','Hervé','78196','FRA30335',2512),(46,'Lanes','Sebastien','FRA-545','FRA-545',2158),(47,'Marty','Pierre','1404895','1404895',3326),(48,'Lafarge','Pascal','','FRA30708',3355),(49,'Foucher','Jean-Luc','','FRA-1006',2321),(50,'MARCAIS','Vincent','','403321',3586),(51,'Delarbre','Marie-Hélène','FRA-','',3295),(52,'Garnier','Laurent','','',3715);
/*!40000 ALTER TABLE `pilot` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `round`
--

DROP TABLE IF EXISTS `round`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `round` (
  `round_number` int(11) NOT NULL,
  `event_id` int(11) NOT NULL,
  `valid` tinyint(4) DEFAULT NULL,
  `flight_order` text DEFAULT NULL,
  `current_group` int(11) DEFAULT 0,
  PRIMARY KEY (`round_number`,`event_id`),
  KEY `fk_round_event_idx` (`event_id`),
  CONSTRAINT `fk_round_event` FOREIGN KEY (`event_id`) REFERENCES `event` (`event_id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `round`
--

LOCK TABLES `round` WRITE;
/*!40000 ALTER TABLE `round` DISABLE KEYS */;
INSERT INTO `round` VALUES (1,1,1,NULL,0),(2,1,1,NULL,0),(3,1,1,NULL,0),(4,1,1,NULL,0),(5,1,1,NULL,0),(6,1,1,NULL,0),(7,1,1,NULL,0),(8,1,1,NULL,0),(9,1,1,NULL,0),(10,1,1,NULL,0),(11,1,1,NULL,0),(12,1,1,NULL,0),(13,1,1,NULL,0),(14,1,1,NULL,0),(15,1,1,NULL,0),(16,1,1,NULL,0),(17,1,1,NULL,0),(18,1,1,NULL,0),(19,1,1,NULL,0),(20,1,1,NULL,0),(21,1,0,'1,2,3,4,5,6,1,7,8,9,10,11,12,13,14',0),(22,1,0,'13,14,1,2,3,4,5,6,7,8,9,10,11,12',0),(23,1,0,'13,14,1,2,3,4,5,6,7,8,9,10,11,12',0),(24,1,0,'13,14,1,2,3,4,5,6,7,8,9,10,11,12',0),(25,1,0,'13,14,1,2,3,4,5,6,7,8,9,10,11,12',0),(26,1,0,'13,14,1,2,3,4,5,6,7,8,9,10,11,12',0),(27,1,0,'13,14,1,2,3,4,5,6,7,8,9,10,11,12',0),(28,1,0,'13,14,1,2,3,4,5,6,7,8,9,10,11,12',0),(29,1,0,'8,9,10,11,12,13,14,1,2,3,4,5,6,7',0);
/*!40000 ALTER TABLE `round` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `roundgroup`
--

DROP TABLE IF EXISTS `roundgroup`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `roundgroup` (
  `event_id` int(11) NOT NULL,
  `round_number` int(11) NOT NULL,
  `group_number` int(11) NOT NULL,
  `start_date` timestamp NULL DEFAULT NULL,
  `end_date` timestamp NULL DEFAULT NULL,
  `flight_order` text DEFAULT NULL,
  `valid` tinyint(4) DEFAULT 0,
  `cancelled` int(11) NOT NULL DEFAULT 0,
  `group_id` int(11) NOT NULL AUTO_INCREMENT,
  PRIMARY KEY (`group_id`),
  KEY `fk_roundgroup_round_idx` (`round_number`,`event_id`),
  CONSTRAINT `fk_roundgroup_round` FOREIGN KEY (`round_number`, `event_id`) REFERENCES `round` (`round_number`, `event_id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB AUTO_INCREMENT=183 DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `roundgroup`
--

LOCK TABLES `roundgroup` WRITE;
/*!40000 ALTER TABLE `roundgroup` DISABLE KEYS */;
INSERT INTO `roundgroup` VALUES (1,1,1,NULL,NULL,NULL,0,0,1),(1,2,1,NULL,NULL,NULL,0,0,6),(1,3,1,NULL,NULL,NULL,0,0,11),(1,4,1,NULL,NULL,NULL,0,0,16),(1,5,1,NULL,NULL,NULL,0,0,21),(1,6,1,NULL,NULL,NULL,0,0,26),(1,7,1,NULL,NULL,NULL,0,0,30),(1,8,1,NULL,NULL,NULL,0,0,34),(1,9,1,NULL,NULL,NULL,0,0,38),(1,10,1,NULL,NULL,NULL,0,0,42),(1,11,1,NULL,NULL,NULL,0,0,46),(1,12,1,NULL,NULL,NULL,0,0,49),(1,13,1,NULL,NULL,NULL,0,0,52),(1,14,1,NULL,NULL,NULL,0,0,55),(1,15,1,NULL,NULL,NULL,0,0,58),(1,16,1,NULL,NULL,NULL,0,0,61),(1,17,1,NULL,NULL,NULL,0,0,64),(1,18,1,NULL,NULL,NULL,0,0,67),(1,19,1,NULL,NULL,NULL,0,0,70),(1,20,1,NULL,NULL,NULL,0,0,73),(1,21,1,NULL,NULL,NULL,0,0,76),(1,22,1,NULL,NULL,NULL,0,0,79),(1,23,1,NULL,NULL,NULL,0,0,82),(1,24,1,NULL,NULL,NULL,0,0,85),(1,25,1,NULL,NULL,NULL,0,0,88),(1,26,1,NULL,NULL,NULL,0,0,91),(1,27,1,NULL,NULL,NULL,0,0,94),(1,28,1,NULL,NULL,NULL,0,0,96),(1,29,1,NULL,NULL,NULL,0,0,98);
/*!40000 ALTER TABLE `roundgroup` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `run`
--

DROP TABLE IF EXISTS `run`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `run` (
  `run_id` int(11) NOT NULL AUTO_INCREMENT,
  `competitor_id` int(11) NOT NULL,
  `chrono_id` int(11) DEFAULT NULL,
  `penalty` double DEFAULT NULL,
  `valid` tinyint(4) NOT NULL,
  `reason` varchar(200) DEFAULT NULL,
  `event_id` int(11) DEFAULT NULL,
  `group_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`run_id`),
  KEY `fk_run_competitor_idx` (`competitor_id`,`event_id`),
  KEY `fk_run_chrono_idx` (`chrono_id`),
  KEY `fk_run_group` (`group_id`),
  CONSTRAINT `fk_run_chrono` FOREIGN KEY (`chrono_id`) REFERENCES `chrono` (`chrono_id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `fk_run_competitor` FOREIGN KEY (`competitor_id`, `event_id`) REFERENCES `competitor` (`pilot_id`, `event_id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `fk_run_group` FOREIGN KEY (`group_id`) REFERENCES `roundgroup` (`group_id`) ON DELETE NO ACTION ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=1019 DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `run`
--

LOCK TABLES `run` WRITE;
/*!40000 ALTER TABLE `run` DISABLE KEYS */;
INSERT INTO `run` VALUES (1,5,1,0,1,'',1,1),(2,8,2,0,1,'',1,1),(3,13,3,0,1,'',1,1),(4,2,4,0,1,'',1,1),(5,7,5,0,1,'',1,1),(6,10,6,0,1,'',1,1),(7,11,7,0,1,'',1,1),(8,3,8,0,1,'',1,1),(9,1,9,0,1,'',1,1),(10,12,10,0,1,'',1,1),(11,9,11,0,1,'',1,1),(12,6,12,0,1,'',1,1),(13,14,13,0,1,'',1,1),(14,4,14,0,1,'',1,1),(15,5,15,0,1,'',1,6),(16,8,16,0,1,'',1,6),(17,13,17,0,1,'',1,6),(18,2,18,0,1,'',1,6),(19,7,19,0,1,'',1,6),(20,10,20,0,1,'',1,6),(21,11,21,0,1,'',1,6),(22,3,22,0,1,'',1,6),(23,1,23,0,1,'',1,6),(24,12,24,0,1,'',1,6),(25,9,25,0,1,'',1,6),(26,6,26,0,1,'',1,6),(27,14,27,0,1,'',1,6),(28,4,28,0,1,'',1,6),(29,5,29,0,1,'',1,11),(30,8,30,0,1,'',1,11),(31,13,31,0,1,'',1,11),(32,2,32,0,1,'',1,11),(33,7,33,0,1,'',1,11),(34,10,34,0,1,'',1,11),(35,11,35,0,1,'',1,11),(36,3,36,0,1,'',1,11),(37,1,37,0,1,'',1,11),(38,12,38,0,1,'',1,11),(39,9,39,0,1,'',1,11),(40,6,40,0,1,'',1,11),(41,14,41,0,1,'',1,11),(42,4,42,0,1,'',1,11),(43,5,43,0,1,'',1,16),(44,8,44,0,1,'',1,16),(45,13,45,0,1,'',1,16),(46,2,46,0,1,'',1,16),(47,7,47,0,1,'',1,16),(48,10,48,0,1,'',1,16),(49,11,49,0,1,'',1,16),(50,3,50,0,1,'',1,16),(51,1,51,0,1,'',1,16),(52,12,52,0,1,'',1,16),(53,9,53,0,1,'',1,16),(54,6,54,0,1,'',1,16),(55,14,55,0,1,'',1,16),(56,4,56,0,1,'',1,16),(57,5,57,0,1,'',1,21),(58,8,58,0,1,'',1,21),(59,13,59,0,1,'',1,21),(60,2,60,0,1,'',1,21),(61,7,61,0,1,'',1,21),(62,10,62,0,1,'',1,21),(63,11,63,0,1,'',1,21),(64,3,64,0,1,'',1,21),(65,1,65,0,1,'',1,21),(66,12,66,0,1,'',1,21),(67,9,67,0,1,'',1,21),(68,6,68,0,1,'',1,21),(69,14,69,0,1,'',1,21),(70,4,70,0,1,'',1,21),(71,5,71,0,1,'',1,26),(72,8,72,0,1,'',1,26),(73,13,73,0,1,'',1,26),(74,2,74,0,1,'',1,26),(75,7,75,0,1,'',1,26),(76,10,76,0,1,'',1,26),(77,11,77,0,1,'',1,26),(78,3,78,0,1,'',1,26),(79,1,79,0,1,'',1,26),(80,12,80,0,1,'',1,26),(81,9,81,0,1,'',1,26),(82,6,82,0,1,'',1,26),(83,14,83,0,1,'',1,26),(84,4,84,0,1,'',1,26),(85,5,85,0,1,'',1,30),(86,8,86,0,1,'',1,30),(87,13,87,0,1,'',1,30),(88,2,88,0,1,'',1,30),(89,7,89,0,1,'',1,30),(90,10,90,0,1,'',1,30),(91,11,91,0,1,'',1,30),(92,3,92,0,0,'',1,30),(93,1,93,0,1,'',1,30),(94,12,94,0,1,'',1,30),(95,9,95,0,1,'',1,30),(96,6,96,0,1,'',1,30),(97,14,97,0,1,'',1,30),(98,4,98,0,1,'',1,30),(99,5,99,0,1,'',1,34),(100,8,100,0,1,'',1,34),(101,13,101,0,1,'',1,34),(102,2,102,0,1,'',1,34),(103,7,103,0,1,'',1,34),(104,10,104,0,1,'',1,34),(105,11,105,0,1,'',1,34),(106,3,106,0,1,'',1,34),(107,1,107,0,1,'',1,34),(108,12,108,0,1,'',1,34),(109,9,109,0,1,'',1,34),(110,6,110,0,1,'',1,34),(111,14,111,0,1,'',1,34),(112,4,112,0,1,'',1,34),(113,5,113,0,1,'',1,38),(114,8,114,0,1,'',1,38),(115,13,115,0,1,'',1,38),(116,2,116,0,1,'',1,38),(117,7,117,0,1,'',1,38),(118,10,118,0,1,'',1,38),(119,11,119,0,1,'',1,38),(120,3,120,0,1,'',1,38),(121,1,121,0,1,'',1,38),(122,12,122,0,1,'',1,38),(123,9,123,0,1,'',1,38),(124,6,124,0,1,'',1,38),(125,14,125,0,1,'',1,38),(126,4,126,0,1,'',1,38),(127,6,127,0,1,'',1,42),(128,9,128,0,1,'',1,42),(129,14,129,0,1,'',1,42),(130,3,130,0,1,'',1,42),(131,8,131,0,1,'',1,42),(132,11,132,0,1,'',1,42),(133,1,133,0,1,'',1,42),(134,12,134,0,1,'',1,42),(135,2,135,0,1,'',1,42),(136,13,136,0,1,'',1,42),(137,10,137,0,1,'',1,42),(138,7,138,0,1,'',1,42),(139,4,139,0,1,'',1,42),(140,5,140,0,1,'',1,42),(141,5,141,0,1,'',1,46),(142,8,142,0,1,'',1,46),(143,13,143,0,1,'',1,46),(144,2,144,0,1,'',1,46),(145,7,145,0,1,'',1,46),(146,10,146,0,1,'',1,46),(147,11,147,0,1,'',1,46),(148,3,148,0,1,'',1,46),(149,1,149,0,1,'',1,46),(150,12,150,0,1,'',1,46),(151,9,151,0,1,'',1,46),(152,6,152,0,1,'',1,46),(153,14,153,0,1,'',1,46),(154,4,154,0,1,'',1,46),(155,5,155,0,1,'',1,49),(156,8,156,0,1,'',1,49),(157,13,157,0,1,'',1,49),(158,2,158,0,1,'',1,49),(159,7,159,0,1,'',1,49),(160,10,160,0,1,'',1,49),(161,11,161,0,1,'',1,49),(162,3,162,0,1,'',1,49),(163,1,163,0,1,'',1,49),(164,12,164,0,1,'',1,49),(165,9,165,0,1,'',1,49),(166,6,166,0,1,'',1,49),(167,14,167,0,1,'',1,49),(168,4,168,0,1,'',1,49),(169,5,169,0,1,'',1,52),(170,8,170,0,1,'',1,52),(171,13,171,0,1,'',1,52),(172,2,172,0,1,'',1,52),(173,7,173,0,1,'',1,52),(174,10,174,0,1,'',1,52),(175,11,175,0,1,'',1,52),(176,3,176,0,1,'',1,52),(177,1,177,0,1,'',1,52),(178,12,178,0,1,'',1,52),(179,9,179,0,1,'',1,52),(180,6,180,0,1,'',1,52),(181,14,181,0,1,'',1,52),(182,4,182,0,1,'',1,52),(183,5,183,0,1,'',1,55),(184,8,184,0,1,'',1,55),(185,13,185,0,1,'',1,55),(186,2,186,0,1,'',1,55),(187,7,187,0,1,'',1,55),(188,10,188,0,1,'',1,55),(189,11,189,0,1,'',1,55),(190,3,190,0,1,'',1,55),(191,1,191,0,1,'',1,55),(192,12,192,0,1,'',1,55),(193,9,193,0,1,'',1,55),(194,6,194,0,1,'',1,55),(195,14,195,0,1,'',1,55),(196,4,196,0,1,'',1,55),(197,5,197,0,1,'',1,58),(198,8,198,0,1,'',1,58),(199,13,199,0,1,'',1,58),(200,2,200,0,1,'',1,58),(201,7,201,0,1,'',1,58),(202,10,202,0,1,'',1,58),(203,11,203,0,1,'',1,58),(204,3,204,0,1,'',1,58),(205,1,205,0,1,'',1,58),(206,12,206,0,1,'',1,58),(207,9,207,0,1,'',1,58),(208,6,208,0,1,'',1,58),(209,14,209,0,1,'',1,58),(210,4,210,0,1,'',1,58),(211,6,211,0,1,'',1,61),(212,9,212,0,1,'',1,61),(213,14,213,0,1,'',1,61),(214,3,214,0,1,'',1,61),(215,8,215,0,1,'',1,61),(216,11,216,0,1,'',1,61),(217,1,217,0,1,'',1,61),(218,12,218,0,1,'',1,61),(219,2,219,0,1,'',1,61),(220,13,220,0,1,'',1,61),(221,10,221,0,1,'',1,61),(222,7,222,0,1,'',1,61),(223,4,223,0,1,'',1,61),(224,5,224,0,1,'',1,61),(225,6,225,0,1,'',1,64),(226,9,226,0,1,'',1,64),(227,14,227,0,1,'',1,64),(228,3,228,0,1,'',1,64),(229,8,229,0,1,'',1,64),(230,11,230,0,1,'',1,64),(231,1,231,0,1,'',1,64),(232,12,232,0,1,'',1,64),(233,2,233,0,1,'',1,64),(234,13,234,0,1,'',1,64),(235,10,235,0,1,'',1,64),(236,7,236,0,1,'',1,64),(237,4,237,0,1,'',1,64),(238,5,238,0,1,'',1,64),(239,6,239,0,1,'',1,67),(240,9,240,0,1,'',1,67),(241,14,241,0,1,'',1,67),(242,3,242,0,1,'',1,67),(243,8,243,0,1,'',1,67),(244,11,244,0,1,'',1,67),(245,1,245,0,1,'',1,67),(246,12,246,0,1,'',1,67),(247,2,247,0,1,'',1,67),(248,13,248,0,1,'',1,67),(249,10,249,0,1,'',1,67),(250,7,250,0,1,'',1,67),(251,4,251,0,1,'',1,67),(252,5,252,0,1,'',1,67),(253,6,253,0,1,'',1,70),(254,9,254,0,1,'',1,70),(255,14,255,0,1,'',1,70),(256,3,256,0,1,'',1,70),(257,8,257,0,1,'',1,70),(258,11,258,0,1,'',1,70),(259,1,259,0,1,'',1,70),(260,12,260,0,1,'',1,70),(261,2,261,0,1,'',1,70),(262,13,262,0,1,'',1,70),(263,10,263,0,1,'',1,70),(264,7,264,0,1,'',1,70),(265,4,265,0,1,'',1,70),(266,5,266,0,1,'',1,70),(267,6,267,0,1,'',1,73),(268,9,268,0,1,'',1,73),(269,14,269,0,1,'',1,73),(270,3,270,0,1,'',1,73),(271,8,271,0,1,'',1,73),(272,11,272,0,1,'',1,73),(273,1,273,0,1,'',1,73),(274,12,274,0,1,'',1,73),(275,2,275,0,1,'',1,73),(276,13,276,0,1,'',1,73),(277,10,277,0,1,'',1,73),(278,7,278,0,1,'',1,73),(279,4,279,0,1,'',1,73),(280,5,280,0,1,'',1,73),(281,1,281,0,1,'',1,76);
/*!40000 ALTER TABLE `run` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2020-12-13 19:18:23
