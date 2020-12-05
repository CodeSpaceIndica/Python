-- Petrol_Prices.Historical definition

CREATE TABLE `Historical` (
  `ID` int NOT NULL AUTO_INCREMENT,
  `DateTime` datetime NOT NULL,
  `City` varchar(100) NOT NULL,
  `StationAddress` varchar(512) DEFAULT NULL,
  `Petrol` float NOT NULL,
  `Diesel` float NOT NULL,
  `PremiumPetrol` float NOT NULL,
  `PremiumDiesel` float NOT NULL,
  `StationName` varchar(256) DEFAULT NULL,
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB AUTO_INCREMENT=237 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
