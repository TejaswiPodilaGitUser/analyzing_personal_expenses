import mysql.connector
import calendar
import os
from dotenv import load_dotenv
import pandas as pd
from backend.database.queries import *
import logging

load_dotenv()

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

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
            df['expense_date'] = pd.to_datetime(df['expense_date'], errors='coerce')
            df = df.dropna(subset=['expense_date'])
        
        if 'amount_paid' in df.columns:
            df['amount_paid'] = pd.to_numeric(df['amount_paid'], errors='coerce')
            df = df.dropna(subset=['amount_paid'])
        
        if 'total_amount' in df.columns:
            df['total_amount'] = pd.to_numeric(df['total_amount'], errors='coerce')
            df = df.dropna(subset=['total_amount'])
        
        return df
    

    def fetch_users(self):
        """Fetch all users from the database."""
        query = FETCH_USERS
        try:
            with self.get_db_connection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute(query)
                    users = cursor.fetchall()
                    return {user[1]: user[0] for user in users}
        except Exception as e:
            logger.error(f"Error fetching users: {e}")
            return {}

    def fetch_all_categories(self):
        """Fetch all unique categories across all users."""
        query = FETCH_ALL_CATEGORIES
        try:
            with self.get_db_connection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute(query)
                    categories = cursor.fetchall()
                    return [category[0] for category in categories]
        except Exception as e:
            logger.error(f"Error fetching categories: {e}")
            return []

    def fetch_user_expenses(self, user_id=None, year=None, month=None):
        """Fetch user expenses filtered by user, year, month"""
        try:
            query, params = self.build_expenses_query(user_id, year, month)
            if not query:
                logger.error("Invalid query parameters for fetch_user_expenses.")
                return pd.DataFrame()

            with self.get_db_connection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute(query, params)
                    data = cursor.fetchall()

            if not data:
                logger.info(f"No data available for user_id: {user_id}.")
                return pd.DataFrame()
            
            df = pd.DataFrame(data, columns=['expense_date', 'category_name', 'amount_paid'])
            df.dropna(subset=['category_name'], inplace=True)
            df = df[df['category_name'] != 'Uncategorized']
            return self.clean_data(df.sort_values(by='amount_paid', ascending=False).head(10))

        except Exception as e:
            logger.error(f"Error fetching expenses: {e}")
            return pd.DataFrame()

    def build_expenses_query(self, user_id, year, month):
        """Construct the query based on input parameters for expenses."""
        base_query = FETCH_ALL_EXPENSES_BASE_QUERY
        
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
        if month:
            try:
                if isinstance(month, str):
                    month_number = list(calendar.month_name).index(month)
                    if month_number == 0:
                        raise ValueError(f"Invalid month name: {month}")
                    month = month_number
                where_clauses.append("MONTH(e.expense_date) = %s")
                params.append(month)
            except ValueError as e:
                logger.error(f"Error: {e}")
                return None, None

        # Add where conditions if any
        if where_clauses:
            base_query += " WHERE " + " AND ".join(where_clauses)

        base_query += """
        ORDER BY amount_paid DESC
        """

        logger.debug(f"Constructed Query: {base_query}")
        return base_query, params

    def fetch_expenses_by_category(self, category_name):
        """Fetch expenses for a specific category or all categories."""
        try:
            if category_name == "All Categories":
                query = FETCH_ALL_EXPENSES_BY_ALL_CATEGORIES
                params = ()
            else:
                query = FETCH_EXPENSES_BY_CATEGORY
                params = (category_name,)

            with self.get_db_connection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute(query, params)
                    data = cursor.fetchall()

            if not data:
                logger.info(f"No data available for category: {category_name}.")
                return pd.DataFrame()

            df = pd.DataFrame(data, columns=['subcategory_name', 'total_amount'])
            df.dropna(subset=['subcategory_name'], inplace=True)
            df = df[df['subcategory_name'] != 'Uncategorized']
            return self.clean_data(df)
        except Exception as e:
            logger.error(f"Error fetching expenses by category: {e}")
            return pd.DataFrame()

    def fetch_user_expenses_by_subcategory(self, user_id=None, year=None, month=None, selected_category=None):
        """Fetch user expenses filtered by user, year, month, or category."""
        try:
            query, params = self.build_subcategory_query(user_id, year, month, selected_category)
            if not query:
                logger.error("Failed to build query for subcategory expenses.")
                return pd.DataFrame()

            with self.get_db_connection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute(query, params)
                    data = cursor.fetchall()

            if not data:
                logger.info(f"No subcategory data available for '{selected_category}'.")
                return pd.DataFrame()

            df = pd.DataFrame(data, columns=['category_name', 'subcategory_name', 'total_amount'])
            df.dropna(subset=['subcategory_name'], inplace=True)
            df = df[df['subcategory_name'] != 'Uncategorized']
            return self.clean_data(df.sort_values(by='total_amount', ascending=False).head(10))

        except Exception as e:
            logger.error(f"Error fetching expenses by subcategory: {e}")
            return pd.DataFrame()

    def build_subcategory_query(self, user_id, year, month, selected_category):
        """Construct the query for subcategory expenses."""
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
        if month:
            try:
                if isinstance(month, str):
                    month_number = list(calendar.month_name).index(month)
                    if month_number == 0:
                        raise ValueError(f"Invalid month name: {month}")
                    month = month_number
                where_clauses.append("MONTH(e.expense_date) = %s")
                params.append(month)
            except ValueError as e:
                logger.error(f"Error: {e}")
                return None, None

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

        base_query += """
        GROUP BY c.category_name, s.subcategory_name
        ORDER BY total_amount DESC
        """

        logger.debug(f"Constructed Subcategory Query: {base_query}")
        return base_query, params
