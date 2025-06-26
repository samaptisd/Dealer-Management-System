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
-- Table structure for table `w_req_corp`
--

DROP TABLE IF EXISTS `w_req_corp`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `w_req_corp` (
  `Id` bigint NOT NULL AUTO_INCREMENT,
  `W_Req_Id` varchar(100) NOT NULL,
  `Timestamp` datetime DEFAULT NULL,
  `Customer_Id` int DEFAULT NULL,
  `Invoice_Date` varchar(45) DEFAULT NULL,
  `Invoice_No` varchar(45) DEFAULT NULL,
  `Item` varchar(45) DEFAULT NULL,
  `Grade` varchar(45) DEFAULT NULL,
  `Color` varchar(45) DEFAULT NULL,
  `Length` varchar(45) DEFAULT NULL,
  `Width` varchar(45) DEFAULT NULL,
  `Batch_No` varchar(45) DEFAULT NULL,
  `Inv_Qty` varchar(45) DEFAULT NULL,
  `Eligible_Qty` varchar(45) DEFAULT NULL,
  `Req_Qty` varchar(45) DEFAULT NULL,
  `W_Issued_To` varchar(200) DEFAULT NULL,
  `Call_Up_No` varchar(100) DEFAULT NULL,
  `Call_Up_Qty_SQM` varchar(45) DEFAULT NULL,
  `Call_Up_Date` date DEFAULT NULL,
  `PO_No` text,
  `Outlet_Name` varchar(200) DEFAULT NULL,
  `Outlet_Id` varchar(45) DEFAULT NULL,
  `Application_Type` varchar(200) DEFAULT NULL,
  `Installation_Date` date DEFAULT NULL,
  `Contact_Name` varchar(200) DEFAULT NULL,
  `Addr_1` varchar(255) DEFAULT NULL,
  `Addr_2` varchar(255) DEFAULT NULL,
  `City` varchar(200) DEFAULT NULL,
  `Pin_Code` int DEFAULT NULL,
  `State` varchar(255) DEFAULT NULL,
  `Outlet_Img_1` text,
  `Outlet_Img_2` text,
  `Outlet_Img_3` text,
  `D_Name` varchar(255) DEFAULT NULL,
  `D_Contact_Name` varchar(255) DEFAULT NULL,
  `D_Addr_1` varchar(255) DEFAULT NULL,
  `D_Addr_2` varchar(255) DEFAULT NULL,
  `D_City` varchar(100) DEFAULT NULL,
  `D_Pin_Code` varchar(10) DEFAULT NULL,
  `D_State` varchar(100) DEFAULT NULL,
  `C_Name` varchar(255) DEFAULT NULL,
  `C_Contact_Name` varchar(255) DEFAULT NULL,
  `C_Addr_1` varchar(255) DEFAULT NULL,
  `C_Addr_2` varchar(255) DEFAULT NULL,
  `C_City` varchar(100) DEFAULT NULL,
  `C_Pin_Code` varchar(10) DEFAULT NULL,
  `C_State` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`Id`)
) ENGINE=InnoDB AUTO_INCREMENT=84 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-06-24 14:40:56
