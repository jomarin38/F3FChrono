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
) ENGINE=InnoDB AUTO_INCREMENT=181 DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

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
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2020-12-13 18:04:57
