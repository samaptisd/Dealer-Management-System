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
-- Table structure for table `whoms_order_corporate`
--

DROP TABLE IF EXISTS `whoms_order_corporate`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `whoms_order_corporate` (
  `Timestamp` text,
  `Order_Date` text,
  `Order_Number` text,
  `Bill_to_Code` text,
  `Branch` text,
  `Team_Name` text,
  `Bill_to_Client_Name` text,
  `Static_Unique_Id` text,
  `Item_Name` text,
  `Grade` text,
  `Colour` text,
  `Length` text,
  `Width` text,
  `Required_Batch` text,
  `Order_Qty_Sheet` text,
  `Special_Remarks` text,
  `Ship_Add_Diff` text,
  `Ship_to_Address` text,
  `Order_Qty_Sq_Mtrs` text,
  `SAP_Material_Number` text,
  `Alloy_Grade` text,
  `Ship_To_Code` text,
  `Ship_to_Client_Name` text,
  `Aludecorian` text,
  `PI_Reference_No` text,
  `PO_Reference_No` text,
  `Freight` text,
  `Payment_Terms` text,
  `Order_Reconfirmation` text,
  `Nature_of_Urgency` text,
  `Type_of_Order` text,
  `SO_No` text,
  `STO_Number` text,
  `Other_Branch` text,
  `User_Email` text,
  `Archive_Status` text
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

-- Dump completed on 2025-06-24 14:40:16
