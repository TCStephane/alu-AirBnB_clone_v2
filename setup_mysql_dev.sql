-- Prepares a MySQL server for the project (dev environment)
-- Create the database if it does not exist
CREATE DATABASE IF NOT EXISTS hbnb_dev_db;
-- Create the user if it does not exist
CREATE USER IF NOT EXISTS 'hbnb_dev'@'localhost' IDENTIFIED BY 'hbnb_dev_pwd';
-- Give the user all privileges on its own database only
GRANT ALL PRIVILEGES ON hbnb_dev_db.* TO 'hbnb_dev'@'localhost';
-- Give the user SELECT on performance_schema only
GRANT SELECT ON performance_schema.* TO 'hbnb_dev'@'localhost';
-- Apply the privilege changes
FLUSH PRIVILEGES;
