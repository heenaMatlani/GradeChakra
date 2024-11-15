import mysql.connector
from backend.config import Config

def get_connection():
    connection = None
    try:
        connection = mysql.connector.connect(
            host= Config.MYSQL_HOST,
            user= Config.MYSQL_USER,
            password= Config.MYSQL_PASSWORD,
            database= Config.MYSQL_DB
        )
    except mysql.connector.Error as e:
        print(f"Error connecting to database: {e}")
    return connection

def close_connection(connection):
    if connection:
        connection.close()
