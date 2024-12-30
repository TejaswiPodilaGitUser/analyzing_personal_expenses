import mysql.connector
import os
from dotenv import load_dotenv
import pandas as pd
from backend.database.queries import *

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
        """Establish and return a database connection."""
        return mysql.connector.connect(**self.db_config)

    def clean_data(self, df):
        """Clean the data by ensuring correct formats."""
        if 'expense_date' in df.columns:
            # Convert 'expense_date' to datetime format
            df['expense_date'] = pd.to_datetime(df['expense_date'], errors='coerce')
            df = df.dropna(subset=['expense_date'])
        
        if 'amount_paid' in df.columns:
            # Convert 'amount_paid' to numeric
            df['amount_paid'] = pd.to_numeric(df['amount_paid'], errors='coerce')
            df = df.dropna(subset=['amount_paid'])
        
        if 'total_amount' in df.columns:
            # Convert 'total_amount' to numeric
            df['total_amount'] = pd.to_numeric(df['total_amount'], errors='coerce')
            df = df.dropna(subset=['total_amount'])
        
        return df


    def fetch_user_expenses(self, user_id=None, year=None, month=None):
        """Fetch user expenses filtered by user, year, or month."""
        conn = self.get_db_connection()
        cursor = conn.cursor()
        
        if user_id and year:
            query = FETCH_USER_EXPENSES_YEARLY
            params = (user_id, year)
        elif user_id and month:
            query = FETCH_USER_EXPENSES_MONTHLY
            params = (user_id, month)
        elif year:
            query = FETCH_ALL_USER_EXPENSES_YEARLY
            params = (year,)
        elif month:
            query = FETCH_ALL_USER_EXPENSES_MONTHLY
            params = (month,)
        else:
            query = FETCH_ALL_EXPENSES
            params = ()
        
        cursor.execute(query, params)
        data = cursor.fetchall()
        conn.close()
        
        # Convert the data to a DataFrame
        df = pd.DataFrame(data, columns=['expense_date', 'category_name', 'amount_paid'])
        
        # Clean the data
        return self.clean_data(df)

    def fetch_users(self):
        """Fetch all users from the database."""
        query = FETCH_USERS
        conn = self.get_db_connection()
        cursor = conn.cursor()
        cursor.execute(query)
        users = cursor.fetchall()
        conn.close()
        return {user[1]: user[0] for user in users}

    def fetch_all_categories(self):
        """Fetch all unique categories across all users."""
        query = FETCH_ALL_CATEGORIES
        conn = self.get_db_connection()
        cursor = conn.cursor()
        cursor.execute(query)
        categories = cursor.fetchall()
        conn.close()
        return [category[0] for category in categories]

    def fetch_user_categories(self, user_id):
        """Fetch unique categories for a specific user."""
        query = FETCH_USER_CATEGORIES
        conn = self.get_db_connection()
        cursor = conn.cursor()
        cursor.execute(query, (user_id,))
        categories = cursor.fetchall()
        conn.close()
        return [category[0] for category in categories]

    def fetch_expenses_by_category(self, category_name):
        """Fetch expenses for a specific category or all categories."""
        try:
            if category_name == "All Categories":
                query = FETCH_ALL_EXPENSES_BY_SUBCATEGORY
                params = ()
            else:
                query = FETCH_EXPENSES_BY_CATEGORY
                params = (category_name,)
            
            conn = self.get_db_connection()
            cursor = conn.cursor()
            cursor.execute(query, params)
            data = cursor.fetchall()
            conn.close()
            
            # Convert to DataFrame and clean
            df = pd.DataFrame(data, columns=['subcategory_name', 'total_amount'])
            return self.clean_data(df)
        
        except Exception as e:
            print(f"Error fetching expenses by category: {e}")
            return pd.DataFrame()

    def fetch_user_expenses_by_subcategory(self, user_id=None, year=None, month=None, selected_category=None):
        """Fetch user expenses filtered by user, year, month, or subcategory."""
        try:
            conn = self.get_db_connection()
            cursor = conn.cursor()
            
            if user_id and year and selected_category:
                query = FETCH_SUBCATEGORY_EXPENSES_FOR_USER_YEARLY
                params = (user_id, year, selected_category)
            elif user_id and month and selected_category:
                query = FETCH_EXPENSES_BY_CATEGORY_FOR_MONTH_FOR_USER
                params = (user_id, month, selected_category)
            elif year and selected_category:
                query = FETCH_SUBCATEGORY_EXPENSES_FOR_ALL_USERS_YEARLY
                params = (year, selected_category)
            elif month and selected_category:
                query = FETCH_EXPENSES_BY_CATEGORY_FOR_MONTH_FOR_ALL_USERS
                params = (month, selected_category)
            else:
                query = FETCH_ALL_EXPENSES_BY_SUBCATEGORY
                params = ()
            
            cursor.execute(query, params)
            data = cursor.fetchall()
            conn.close()
            
            # Convert the result into a DataFrame
            df = pd.DataFrame(data, columns=['subcategory_name', 'total_amount'])
            return self.clean_data(df)
        
        except Exception as e:
            print(f"Error fetching expenses by subcategory: {e}")
            return pd.DataFrame()
