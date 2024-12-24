import mysql.connector
import os
from dotenv import load_dotenv
import pandas as pd

load_dotenv()

class DatabaseOperations:
    def __init__(self):
        self.db_config = {
            'host': os.getenv('DB_HOST'),
            'user': os.getenv('DB_USER'),
            'password': os.getenv('DB_PASSWORD'),
            'database': os.getenv('DB_NAME')
        }

    def get_db_connection(self):
        return mysql.connector.connect(**self.db_config)

    def fetch_user_expenses(self, user_id=None):
        query = """
        SELECT e.expense_date, c.category_name, e.amount_paid
        FROM expenses e
        JOIN categories c ON e.category_id = c.category_id
        """
        if user_id:
            query += " WHERE e.user_id = %s"
        
        conn = self.get_db_connection()
        cursor = conn.cursor()
        if user_id:
            cursor.execute(query, (user_id,))
        else:
            cursor.execute(query)
        
        data = cursor.fetchall()
        conn.close()

        return pd.DataFrame(data, columns=['expense_date', 'category_name', 'amount_paid'])
