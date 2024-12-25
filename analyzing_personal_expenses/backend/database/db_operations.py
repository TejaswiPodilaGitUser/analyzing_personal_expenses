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
        # Base query
        query = """
        SELECT e.expense_date, c.category_name, e.amount_paid
        FROM expenses e
        JOIN categories c ON e.category_id = c.category_id
        """

        # Modify query if a user_id is provided (excluding the 'All' case)
        if user_id and user_id != "All Users":
            query += " WHERE e.user_id = %s"
        
        # Open database connection
        conn = self.get_db_connection()
        cursor = conn.cursor()

        # Execute the query
        if user_id and user_id != "All Users":
            cursor.execute(query, (user_id,))
        else:
            cursor.execute(query)

        # Fetch data and close connection
        data = cursor.fetchall()
        conn.close()

        # Return the data as a DataFrame
        return pd.DataFrame(data, columns=['expense_date', 'category_name', 'amount_paid'])

    def fetch_users(self):
        query = "SELECT user_id, user_name FROM users"  # Only fetch users
        conn = self.get_db_connection()
        cursor = conn.cursor()
        cursor.execute(query)
        
        # Fetch all users (user_id and user_name)
        users = cursor.fetchall()
        conn.close()
        
        return {user[1]: user[0] for user in users}  # Return a dictionary with user_name as key and user_id as value
