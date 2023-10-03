#***************************************************************************************#
# Programmer: Steve Edmund
# Date: 2023-09-20
# Python Version: 3.11
# Purpose: This script connects to a MySQL database server and creates a new database.
#***************************************************************************************#

# Importing the MySQL Connector module
import mysql.connector

# Connecting to the MySQL server
dataBase = mysql.connector.connect(
    host='localhost',  # Database server host
    user='edmund',      # MySQL user
    passwd='Edmund_project'  # Password for the user
)

# Creating a cursor object for database operations
cursorObject = dataBase.cursor()

# Creating a new database named 'Shelter_Record'
cursorObject.execute("CREATE DATABASE Shelter_Record")

# Printing a success message
print("All Done!")


import mysql.connector

dataBase = mysql.connector.connect(
	host = 'localhost',
	user = 'edmund',
	passwd = 'Edmund_project'

	)

# prepare a cursor object
cursorObject = dataBase.cursor()

# Create a database
cursorObject.execute("CREATE DATABASE Shelter_Record")

print("All Done!")
