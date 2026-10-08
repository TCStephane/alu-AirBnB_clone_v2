-- Prepares a MySQL server for the project (test environment)
-- Create the database if it does not exist
CREATE DATABASE IF NOT EXISTS hbnb_test_db;
-- Create the user if it does not exist
CREATE USER IF NOT EXISTS 'hbnb_test'@'localhost' IDENTIFIED BY 'hbnb_test_pwd';
-- Give the user all privileges on its own database only
GRANT ALL PRIVILEGES ON hbnb_test_db.* TO 'hbnb_test'@'localhost';
-- Give the user SELECT on performance_schema only
GRANT SELECT ON performance_schema.* TO 'hbnb_test'@'localhost';
-- Apply the privilege changes
FLUSH PRIVILEGES;
