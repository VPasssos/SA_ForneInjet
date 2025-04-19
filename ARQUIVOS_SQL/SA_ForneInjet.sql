-- MySQL dump 10.13  Distrib 8.0.40, for Win64 (x86_64)
--
-- Host: localhost    Database: sa_forneinjet
-- ------------------------------------------------------
-- Server version	8.0.40

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
-- Table structure for table `fornece`
--

DROP TABLE IF EXISTS `fornece`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `fornece` (
  `ID_Funcionario` int NOT NULL,
  `ID_Fornecedor` int NOT NULL,
  PRIMARY KEY (`ID_Funcionario`,`ID_Fornecedor`),
  KEY `ID_Fornecedor` (`ID_Fornecedor`),
  CONSTRAINT `fornece_ibfk_1` FOREIGN KEY (`ID_Funcionario`) REFERENCES `funcionario` (`ID_Funcionario`),
  CONSTRAINT `fornece_ibfk_2` FOREIGN KEY (`ID_Fornecedor`) REFERENCES `fornecedor` (`ID_Fornecedor`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `fornece`
--

LOCK TABLES `fornece` WRITE;
/*!40000 ALTER TABLE `fornece` DISABLE KEYS */;
/*!40000 ALTER TABLE `fornece` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `fornecedor`
--

DROP TABLE IF EXISTS `fornecedor`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `fornecedor` (
  `ID_Fornecedor` int NOT NULL AUTO_INCREMENT,
  `NM_Fornecedor` varchar(100) DEFAULT NULL,
  `CNPJ` varchar(14) DEFAULT NULL,
  `Endereco` varchar(255) DEFAULT NULL,
  `Numero` int DEFAULT NULL,
  `Estado` varchar(50) DEFAULT NULL,
  `Cidade` varchar(50) DEFAULT NULL,
  `CEP` varchar(10) DEFAULT NULL,
  PRIMARY KEY (`ID_Fornecedor`),
  UNIQUE KEY `CNPJ` (`CNPJ`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `fornecedor`
--

LOCK TABLES `fornecedor` WRITE;
/*!40000 ALTER TABLE `fornecedor` DISABLE KEYS */;
/*!40000 ALTER TABLE `fornecedor` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `funcionario`
--

DROP TABLE IF EXISTS `funcionario`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `funcionario` (
  `ID_Funcionario` int NOT NULL AUTO_INCREMENT,
  `Rua` varchar(100) DEFAULT NULL,
  `Numero` int DEFAULT NULL,
  `Estado` varchar(50) DEFAULT NULL,
  `Cidade` varchar(50) DEFAULT NULL,
  `CEP` varchar(10) DEFAULT NULL,
  `Cargo` varchar(50) DEFAULT NULL,
  `Situacao` varchar(50) DEFAULT NULL,
  `Telefone` varchar(15) DEFAULT NULL,
  `Email` varchar(100) DEFAULT NULL,
  `Usuario` varchar(50) DEFAULT NULL,
  `Senha` varchar(50) DEFAULT NULL,
  `Data_admissao` date DEFAULT NULL,
  PRIMARY KEY (`ID_Funcionario`),
  UNIQUE KEY `Telefone` (`Telefone`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `funcionario`
--

LOCK TABLES `funcionario` WRITE;
/*!40000 ALTER TABLE `funcionario` DISABLE KEYS */;
/*!40000 ALTER TABLE `funcionario` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `injetoras`
--

DROP TABLE IF EXISTS `injetoras`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `injetoras` (
  `ID_Injetoras` int NOT NULL AUTO_INCREMENT,
  `Fornecedor` int DEFAULT NULL,
  `Forca_de_fechamento` decimal(10,2) DEFAULT NULL,
  `Capacidade_de_injecao` decimal(10,2) DEFAULT NULL,
  `Preco_medio_USD` decimal(10,2) DEFAULT NULL,
  `Preco_medio_BRL` decimal(10,2) DEFAULT NULL,
  `Quantidade` int DEFAULT NULL,
  `Marca` varchar(50) DEFAULT NULL,
  `Modelo` varchar(50) DEFAULT NULL,
  `Tipo_de_controle` varchar(50) DEFAULT NULL,
  `Observacao` text,
  PRIMARY KEY (`ID_Injetoras`),
  KEY `Fornecedor` (`Fornecedor`),
  CONSTRAINT `injetoras_ibfk_1` FOREIGN KEY (`Fornecedor`) REFERENCES `fornecedor` (`ID_Fornecedor`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `injetoras`
--

LOCK TABLES `injetoras` WRITE;
/*!40000 ALTER TABLE `injetoras` DISABLE KEYS */;
/*!40000 ALTER TABLE `injetoras` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-04-01 21:57:17
