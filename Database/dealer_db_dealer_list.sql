-- MySQL dump 10.13  Distrib 8.0.41, for Win64 (x86_64)
--
-- Host: 3.111.126.92    Database: dealer_db
-- ------------------------------------------------------
-- Server version	8.0.42-0ubuntu0.24.04.1

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `dealer_list`
--

DROP TABLE IF EXISTS `dealer_list`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `dealer_list` (
  `SAP_Code` varchar(20) DEFAULT NULL,
  `Dealer_Name` varchar(200) DEFAULT NULL,
  `Zone` varchar(50) DEFAULT NULL,
  `Team_Name` varchar(100) DEFAULT NULL,
  `Department` varchar(100) DEFAULT NULL,
  `State` varchar(100) DEFAULT NULL,
  `Branch` varchar(50) DEFAULT NULL,
  `Zone_Org` varchar(50) DEFAULT NULL,
  `Addr1` text,
  `Addr2` text,
  `City` text,
  `Pin_Code` varchar(45) DEFAULT NULL,
  `State_Addr` varchar(100) DEFAULT NULL,
  `Contact_Name` varchar(200) DEFAULT NULL,
  `Contact_No` varchar(100) DEFAULT NULL,
  `Email` varchar(100) DEFAULT NULL,
  `PAN` varchar(45) DEFAULT NULL,
  `GSTIN` varchar(45) DEFAULT NULL,
  KEY `index1` (`Department`,`Branch`,`Zone`),
  KEY `sap_code` (`SAP_Code`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-06-24 14:40:35
