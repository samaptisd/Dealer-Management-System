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
-- Table structure for table `orders_corp`
--

DROP TABLE IF EXISTS `orders_corp`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `orders_corp` (
  `Sr_No` int NOT NULL AUTO_INCREMENT,
  `Timestamp` datetime DEFAULT NULL,
  `Order_Id` varchar(255) DEFAULT NULL,
  `Customer_Id` varchar(255) DEFAULT NULL,
  `Order_Type` varchar(255) DEFAULT NULL,
  `Diff_Address` varchar(255) DEFAULT NULL,
  `Address` varchar(255) DEFAULT NULL,
  `State` varchar(255) DEFAULT NULL,
  `Pincode` varchar(255) DEFAULT NULL,
  `Item_Code` varchar(255) DEFAULT NULL,
  `Product_Grade` varchar(255) DEFAULT NULL,
  `Color_Code` varchar(255) DEFAULT NULL,
  `Length` int DEFAULT NULL,
  `Width` int DEFAULT NULL,
  `Matching_Lot` varchar(255) DEFAULT NULL,
  `Order_Qty` int DEFAULT NULL,
  `Record_No` bigint DEFAULT NULL,
  `Customer_Name` text,
  `Branch` text,
  `Contact_Name` text,
  `Contact_No` text,
  `Remarks` text,
  `Color_Category` varchar(100) DEFAULT NULL,
  `Order_Received_Time` datetime DEFAULT NULL,
  `Order_Received_From` varchar(100) DEFAULT NULL,
  `Username` varchar(45) DEFAULT NULL,
  `Version_No` int DEFAULT '1',
  PRIMARY KEY (`Sr_No`)
) ENGINE=InnoDB AUTO_INCREMENT=31907 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-06-24 14:41:00
