CREATE DATABASE IF NOT EXISTS ece140;

USE ece140;

-- DUMP EVERYTHING... YOU REALLY SHOULDN'T DO THIS!
DROP TABLE IF EXISTS users;

CREATE TABLE IF NOT EXISTS users (
  id          integer  AUTO_INCREMENT PRIMARY KEY,
  first_name  VARCHAR(30) NOT NULL,
  last_name   VARCHAR(30) NOT NULL,
  created_at  TIMESTAMP
);

INSERT INTO users (first_name, last_name, created_at) VALUES
  ("Zendaya", "", CURRENT_TIMESTAMP),
  ("Tom", "Holland", CURRENT_TIMESTAMP),
  ("Tobey", "Maguire", CURRENT_TIMESTAMP),
  ("Andrew", "Garfield", CURRENT_TIMESTAMP)
;