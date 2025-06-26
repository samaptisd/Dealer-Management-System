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
-- Table structure for table `pi_corp_logs`
--

DROP TABLE IF EXISTS `pi_corp_logs`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `pi_corp_logs` (
  `PI_No` varchar(50) NOT NULL,
  `Version_No` int NOT NULL,
  `Timestamp` datetime DEFAULT NULL,
  `Order_Id` varchar(50) DEFAULT NULL,
  `Customer_Id` varchar(15) DEFAULT NULL,
  `Customer_Name` varchar(100) DEFAULT NULL,
  `Actual_Branch` varchar(100) DEFAULT NULL,
  `Invoicing_Branch` varchar(50) DEFAULT NULL,
  `Billing_Address` varchar(255) DEFAULT NULL,
  `Billing_Address_City` varchar(100) DEFAULT NULL,
  `Billing_Address_State` varchar(100) DEFAULT NULL,
  `Billing_Address_Pin` varchar(50) DEFAULT NULL,
  `Billing_Address_Contact_P` varchar(100) DEFAULT NULL,
  `Billing_Address_Mob` varchar(50) DEFAULT NULL,
  `Billing_Address_Email` varchar(200) DEFAULT NULL,
  `Delivery_Address_Same` varchar(45) DEFAULT NULL,
  `Delivery_Address` varchar(255) DEFAULT NULL,
  `Delivery_Address_City` varchar(100) DEFAULT NULL,
  `Delivery_Address_State` varchar(100) DEFAULT NULL,
  `Delivery_Address_Pin` varchar(50) DEFAULT NULL,
  `Delivery_Address_Contact_P` varchar(100) DEFAULT NULL,
  `Delivery_Address_Mob` varchar(50) DEFAULT NULL,
  `Sales_Person` varchar(100) DEFAULT NULL,
  `Sales_Person_Mob` varchar(50) DEFAULT NULL,
  `Client_PAN` varchar(50) DEFAULT NULL,
  `Client_GSTIN` varchar(15) DEFAULT NULL,
  `PO_No` varchar(255) DEFAULT NULL,
  `PO_Date` varchar(50) DEFAULT NULL,
  `Total_Sheets` varchar(50) DEFAULT NULL,
  `Total_SQM` varchar(50) DEFAULT NULL,
  `Total_SQF` varchar(50) DEFAULT NULL,
  `Sub_Total` varchar(50) DEFAULT NULL,
  `Less_CD` varchar(50) DEFAULT NULL,
  `Less_CD_Amount` varchar(50) DEFAULT NULL,
  `Sub_Total1` varchar(50) DEFAULT NULL,
  `Freight_Amount` varchar(50) DEFAULT NULL,
  `Packaging_Amount` varchar(50) DEFAULT NULL,
  `Sub_Total2` varchar(50) DEFAULT NULL,
  `GST_Percentage` varchar(50) DEFAULT NULL,
  `GST_Amount` varchar(50) DEFAULT NULL,
  `TCS_Required` varchar(45) DEFAULT NULL,
  `TCS_Amount` varchar(50) DEFAULT NULL,
  `Round_Off` varchar(50) DEFAULT NULL,
  `Final_Amount` varchar(50) DEFAULT NULL,
  `Freight_Note` varchar(50) DEFAULT NULL,
  `Special_Note` varchar(200) DEFAULT NULL,
  `Payment_Terms` varchar(200) DEFAULT NULL,
  `Outstanding_Amount` varchar(50) DEFAULT NULL,
  `Username` varchar(45) DEFAULT NULL,
  `Status` varchar(45) DEFAULT NULL,
  `Customer_Remarks` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`PI_No`,`Version_No`)
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

-- Dump completed on 2025-06-24 14:40:08
