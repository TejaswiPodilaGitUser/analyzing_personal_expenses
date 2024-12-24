import os
from dotenv import load_dotenv
import mysql.connector

load_dotenv()

try:
    connection = mysql.connector.connect(
        host=os.getenv('DB_HOST'),
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASSWORD'),
        database=os.getenv('DB_NAME')
    )
    print("✅ Connected to database successfully!")
    connection.close()
except mysql.connector.Error as err:
    print(f"❌ Database connection failed: {err}")
