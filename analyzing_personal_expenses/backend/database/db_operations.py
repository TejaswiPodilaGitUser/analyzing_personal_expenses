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
        print(f"In DB Operations, User_id: {user_id}, Year: {year}, Month: {month}")
       
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
        
        # Log the final query to inspect
        print("In db_operations-fetch_user_expenses- Constructed Query:", query)
        print("Query Parameters:", params)

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
        """Fetch user expenses filtered by user, year, month, or category."""
        print("In Db operations", user_id, year, month, selected_category)
        
        try:
            conn = self.get_db_connection()
            cursor = conn.cursor()
            
            # Build the query based on the provided parameters
            query, params = self.build_subcategory_query(user_id, year, month, selected_category)

            # Execute the constructed query
            cursor.execute(query, params)
            data = cursor.fetchall()
            conn.close()

            if not data:
                print(f"No subcategory data available for '{selected_category}'.")
                return pd.DataFrame()

            # Convert the data into a DataFrame and clean it
            df = pd.DataFrame(data, columns=['category_name', 'subcategory_name', 'total_amount'])

            # Remove null and 'Uncategorized' entries
            df = df.dropna(subset=['subcategory_name'])
            df = df[df['subcategory_name'] != 'Uncategorized']

            # Sort by total_amount and limit to the top 10
            df = df.sort_values(by='total_amount', ascending=False).head(10)

            return self.clean_data(df)
        
        except Exception as e:
            print(f"Error fetching expenses by subcategory: {e}")
            return pd.DataFrame()

    def build_subcategory_query(self, user_id, year, month, selected_category):
        """Construct the query based on input parameters for subcategories."""
        base_query = FETCH_ALL_EXPENSES_BY_SUBCATEGORY_BASE_QUERY
        
        where_clauses = []
        params = []

        # User filter
        if user_id and user_id != "ALL Users":
            where_clauses.append("e.user_id = %s")
            params.append(user_id)

        # Year filter (if year is provided)
        if year:
            where_clauses.append("YEAR(e.expense_date) = %s")
            params.append(year)

        # Month filter (if month is provided and year is also provided)
        if month and year:
            where_clauses.append("MONTH(e.expense_date) = %s")
            params.append(month)

        # Category filter
        if selected_category and selected_category != "All Categories":
            where_clauses.append("c.category_name = %s")
            params.append(selected_category)

        # Exclude 'Uncategorized' and NULL subcategories
        where_clauses.append("s.subcategory_name IS NOT NULL")
        where_clauses.append("s.subcategory_name != 'Uncategorized'")

        # Add where conditions if any
        if where_clauses:
            base_query += " WHERE " + " AND ".join(where_clauses)

        # Ensure grouping by both category_name and subcategory_name
        base_query += """
        GROUP BY c.category_name, s.subcategory_name
        ORDER BY total_amount DESC
        """

        # Log the final query to inspect
        print("build_subcategory_query- Constructed Query:", base_query)
        print("Query Parameters:", params)

        # Return the constructed query and parameters
        return base_query, params
