HHA 504 Final Assignment

# Setup and deploy EC2
- Created VM on Azure
- Selected inbound port 22
- Added port 3306 in inbound security rules
- Added auto-shutdown

# Create a user to the ubuntu EC2 instance
- Used SSH so no .pem file needed

# Install mySQL
- Opened CMD
- Logged in with 
  - ssh username@ip address
- sudo apt-get update
- sudo apt install mysql-server mysql-client
- sudo mysql

# Create a mysql user
- CREATE USER ‘DBA'@'%' IDENTIFIED BY ‘ahi2021’;
- GRANT ALL PRIVILEGES ON *.* TO 'dba'@'%' WITH GRANT OPTION;
- show grants with DBA
- \q
- log in with DBA
  - mysql -u DBA -p

# Create a new database called ‘e2e’
- create database e2e;
- show databases;

# Write a python or R script that connects to your SQL instance
- \q
- Need to update mySQL configuration settings to enable external connections
  - sudo nano /etc/mysql/mysql.conf.d/mysqld.cnf
- Set bind-address to 0.0.0.0
- CTRL + O to save
- CTRL + X to exit
- Restart mySQL
  - /etc/init.d/mysql restart
- Write python code to connect to SQL instance and upload CSV file from GITHUB
- Name table 'h1n1'

from sqlalchemy import create_engine
import sqlalchemy

import pandas as pd

MYSQL_HOSTNAME = '40.117.148.146'
MYSQL_USER = 'DBA'
MYSQL_PASSWORD = 'ahi2021'
MYSQL_DATABASE = 'e2e'

connection_string = f'mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOSTNAME}/{MYSQL_DATABASE}'
engine = create_engine(connection_string)

print(engine.table_names())

csvfile = pd.read_csv('https://raw.githubusercontent.com/chelseatwan/datasets/main/H1N1_Flu_Vaccines.csv')
csvfile.to_sql('h1n1', con=engine, if_exists='append')

- Back in mySQL in terminal:
  - show databases;
  - select e2e;
  - show tables;
  - select * from h1n1 limit 5;

# Create a dump (.sql) file
- \q
- sudo mysqldump e2e > database-dump.sql

# Using the SCP command from your terminal, move that file to your own local computer
- scp database-dump.sql chelsea@40.117.148.146:/home/chelsea

# Create a trigger
- Open MySql Workbench
- Set up new connection to VM
- Go to e2e database
- Create trigger

delimiter $$
CREATE TRIGGER H1N1_concern_trigger BEFORE INSERT ON h1n1
FOR EACH ROW
BEGIN
	IF NEW.h1n1_concern >= 3 THEN
		SIGNAL SQLSTATE '45000'
		SET MESSAGE_TEXT = 'H1N1 concern should be a numerical value between 0 and 3. Please try again.';
	END IF;
END; $$
delimiter ;
