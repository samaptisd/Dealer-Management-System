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
-- Table structure for table `shade_cards`
--

DROP TABLE IF EXISTS `shade_cards`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `shade_cards` (
  `id` int NOT NULL AUTO_INCREMENT,
  `timestamp` timestamp NULL DEFAULT NULL,
  `username` varchar(100) DEFAULT NULL,
  `fullname` varchar(200) DEFAULT NULL,
  `aluwall_qty` int DEFAULT NULL,
  `msc_regular_qty` int DEFAULT NULL,
  `msc_special_qty` int DEFAULT NULL,
  `al45_qty` int DEFAULT NULL,
  `wabi_sabi_swatch_qty` int DEFAULT NULL,
  `ccp_zcp_qty` int DEFAULT NULL,
  `aludecor_system_qty` int DEFAULT NULL,
  `elevate_qty` int DEFAULT NULL,
  `signex_qty` int DEFAULT NULL,
  `final_aluminum_titanium_catalogue_qty` int DEFAULT NULL,
  `final_metal_dhara_lovers_catalogue_qty` int DEFAULT NULL,
  `wabi_sabi_premium_qty` int DEFAULT NULL,
  `sand_rustic_qty` int DEFAULT NULL,
  `corporate_profile_qty` int DEFAULT NULL,
  `why_aludecor_english_qty` int DEFAULT NULL,
  `why_aludecor_hindi_qty` int DEFAULT NULL,
  `why_aludecor_tamil_qty` int DEFAULT NULL,
  `final_ace_timber_combined_catalogue_qty` int DEFAULT NULL,
  `final_3_mm_classique_catalogue_qty` int DEFAULT NULL,
  `final_4_mm_endura_catalogue_qty` int DEFAULT NULL,
  `aludecor_hanging_qty` int DEFAULT NULL,
  `aluwall_hanging` int DEFAULT NULL,
  `ag_armor_qty` int DEFAULT NULL,
  `nepal_regular_qty` int DEFAULT NULL,
  `nedzink_solid_panel_brochure_qty` int DEFAULT NULL,
  `nedzink_catalogue_nature_neo_noir_qty` int DEFAULT NULL,
  `vi_secure_qty` int DEFAULT NULL,
  `zinco_catalogue_qty` int DEFAULT NULL,
  `final_rugged_metal_catalogue_qty` int DEFAULT NULL,
  `nexcomb_brochure_qty` int DEFAULT NULL,
  `aluwall_relic_qty` int DEFAULT NULL,
  `shades_of_the_year_qty` int DEFAULT NULL,
  `nedzink_catalogue_nuance` int DEFAULT NULL,
  `earth_coat` int DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=19 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-06-24 14:40:03
