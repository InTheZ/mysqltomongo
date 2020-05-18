# mysqltomongo
MySQL to MongoDB Example

## Environment Setup
This example is developed to work with MongoDB 4.2.x, Python 3.8.x and MySQL 8.0.x version.
```bash
pip install -r requirements.txt
```

## Configuration

### MySQL Configuration
Please don't use this in a production environment!
```
CREATE USER 'example_api'@'localhost' IDENTIFIED BY 'example_api';
GRANT ALL PRIVILEGES ON *.* TO 'example_api'@'localhost' WITH GRANT OPTION;
DROP DATABASE IF EXISTS example_api;
CREATE DATABASE example_api;
USE example_api;
CREATE TABLE `patients` (
    `id` int(11) NOT NULL AUTO_INCREMENT,
    `patientId` bigint UNSIGNED NOT NULL,
    `fileId` int(11) UNSIGNED NOT NULL,
    `name` varchar(255) COLLATE utf8_bin NOT NULL,
    `address` varchar(255) COLLATE utf8_bin NOT NULL,
    `city` varchar(255) COLLATE utf8_bin NOT NULL,
    `state` varchar(255) COLLATE utf8_bin NOT NULL,
    `zip` varchar(255) COLLATE utf8_bin NOT NULL,
    PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin
AUTO_INCREMENT=1;
CREATE TABLE `files` (
    `id` int(11) NOT NULL AUTO_INCREMENT,
    `fileId` int(11) NOT NULL,
    `created` DATETIME NOT NULL,
    PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin
AUTO_INCREMENT=1;
CREATE INDEX created ON files (created);
CREATE TABLE `services` (
    `id` int(11) NOT NULL AUTO_INCREMENT,
    `pId` int(11) NOT NULL,
    `fileId` int(11) NOT NULL,
    `date` DATETIME NOT NULL,
    `name` varchar(255) COLLATE utf8_bin NOT NULL,
    `code` int(11) NOT NULL,
    `description` TEXT COLLATE utf8_bin NOT NULL,
    `cost` DECIMAL(10,2) NOT NULL,
    PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin
AUTO_INCREMENT=1;
CREATE INDEX pId ON services (pId);
```

### MongoDB Configuration
Please don't use this in a production environment! This should be executed by an admin (root) user over the entire database.
```
use example_api
db.createUser({"user": "example_api", "pwd": "example_api", roles: ["readWrite"]})
```