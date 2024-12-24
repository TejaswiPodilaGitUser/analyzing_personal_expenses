import os
from dotenv import load_dotenv
import mysql.connector

# Load environment variables from .env
load_dotenv()

class MySQLDatabase:
    def connect(self):
        try:
            connection = mysql.connector.connect(
                host=os.getenv('DB_HOST'),
                user=os.getenv('DB_USER'),
                password=os.getenv('DB_PASSWORD'),
                database=os.getenv('DB_NAME')
            )
            print("✅ Database connection successful!")
            return connection
        except mysql.connector.Error as err:
            print(f"❌ Database connection failed: {err}")
            raise
