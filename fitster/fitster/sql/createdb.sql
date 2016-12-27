CREATE USER 'fitsterdb'@'localhost' IDENTIFIED BY 'fitsterdb';
    CREATE DATABASE fitsterdb
      DEFAULT CHARACTER SET utf8
      DEFAULT COLLATE utf8_general_ci;
    GRANT ALL ON fitsterdb.* TO 'fitsterdb'@'localhost';
	GRANT ALL ON test_fitsterdb.* TO 'fitsterdb'@'localhost';