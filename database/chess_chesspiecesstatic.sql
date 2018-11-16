-- MySQL dump 10.13  Distrib 8.0.13, for Win64 (x86_64)
--
-- Host: localhost    Database: chess
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
-- Table structure for table `chesspiecesstatic`
--

DROP TABLE IF EXISTS `chesspiecesstatic`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `chesspiecesstatic` (
  `PieceName` varchar(255) DEFAULT NULL,
  `Points` int(11) DEFAULT NULL,
  `MovementType` int(11) DEFAULT NULL,
  `PlayerColor` int(11) DEFAULT NULL,
  `Image` varchar(255) DEFAULT NULL,
  `HP` int(11) DEFAULT NULL,
  `Attack` int(11) DEFAULT NULL,
  `AttackSet` varchar(255) DEFAULT NULL,
  `MoveSet` varchar(255) DEFAULT NULL,
  `SpecialMove` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `chesspiecesstatic`
--

LOCK TABLES `chesspiecesstatic` WRITE;
/*!40000 ALTER TABLE `chesspiecesstatic` DISABLE KEYS */;
INSERT INTO `chesspiecesstatic` VALUES ('Rook',5,3,-1,'',1,1,'10|20|30|40|50|60|70|-10|-20|-30|-40|-50|-60|-70|01|02|03|04|05|06|07|0-1|0-2|0-3|0-4|0-5|0-6|0-7','10|20|30|40|50|60|70|-10|-20|-30|-40|-50|-60|-70|01|02|03|04|05|06|07|0-1|0-2|0-3|0-4|0-5|0-6|0-7',NULL),('Knight',3,2,-1,'',1,1,'12|21|-12|-21|2-1|1-2|-1-2|-2-1','12|21|-12|-21|2-1|1-2|-1-2|-2-1',NULL),('Bishop',3,1,-1,'',1,1,'11|22|33|44|55|66|77|-1-1|-2-2|-3-3|-4-4|-5-5|-6-6|-7-7|-11|-22|-33|-44|-55|-66|-77|1-1|2-2|3-3|4-4|5-5|6-6|7-7','11|22|33|44|55|66|77|-1-1|-2-2|-3-3|-4-4|-5-5|-6-6|-7-7|-11|-22|-33|-44|-55|-66|-77|1-1|2-2|3-3|4-4|5-5|6-6|7-7',NULL),('Queen',9,4,-1,'',1,1,'10|20|30|40|50|60|70|-10|-20|-30|-40|-50|-60|-70|01|02|03|04|05|06|07|0-1|0-2|0-3|0-4|0-5|0-6|0-7|11|22|33|44|55|66|77|-1-1|-2-2|-3-3|-4-4|-5-5|-6-6|-7-7|-11|-22|-33|-44|-55|-66|-77|1-1|2-2|3-3|4-4|5-5|6-6|7-7','10|20|30|40|50|60|70|-10|-20|-30|-40|-50|-60|-70|01|02|03|04|05|06|07|0-1|0-2|0-3|0-4|0-5|0-6|0-7|11|22|33|44|55|66|77|-1-1|-2-2|-3-3|-4-4|-5-5|-6-6|-7-7|-11|-22|-33|-44|-55|-66|-77|1-1|2-2|3-3|4-4|5-5|6-6|7-7',NULL),('King',0,5,-1,'',1,1,'10|11|01|-11|-10|-1-1|0-1|1-1','10|11|01|-11|-10|-1-1|0-1|1-1',NULL),('WhitePawn',1,0,-1,NULL,1,1,'11|-11','01','02'),('BlackPawn',1,0,-1,NULL,1,1,'1-1|-1-1','0-1','0-2');
/*!40000 ALTER TABLE `chesspiecesstatic` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2018-11-16 16:29:55
