-- Prepares a MySQL server for the project, The script does this in order:
-- Create a  database hbnb_test_db
CREATE DATABASE IF NOT EXISTS hbnb_dev_db;
-- Create a new user hbnb_test (in localhost) and set
-- the password of hbnb_dev to hbnb_dev_pwd
CREATE USER IF NOT EXISTS 'hbnb_dev'@'localhost' IDENTIFIED BY 'hbnb_dev_pwd';
-- Grant hbnb_dev all privileges on the database hbnb_dev_db
GRANT ALL PRIVILEGES ON hbnb_dev_db.* TO 'hbnb_dev'@'localhost';
-- Grant hbnb_dev SELECT privilege on the database performance_schema
GRANT SELECT ON performance_schema.* TO 'hbnb_dev'@'localhost';
FLUSH PRIVILEGES;
