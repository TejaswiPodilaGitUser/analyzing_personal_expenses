import mysql.connector
import calendar
import os
from dotenv import load_dotenv
import pandas as pd
import logging
from backend.database.queries import *  # Import queries from the queries file

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

    def fetch_user_expenses(self, user_id=None):
        """Fetch expenses for a specific user or all users."""
        query = """
        SELECT e.expense_date, c.category_name, e.amount_paid
        FROM expenses e
        JOIN categories c ON e.category_id = c.category_id
        """
        if user_id and user_id != "All Users":
            query += " WHERE e.user_id = %s"

        conn = self.get_db_connection()
        cursor = conn.cursor()
        if user_id and user_id != "All Users":
            cursor.execute(query, (user_id,))
        else:
            cursor.execute(query)

        data = cursor.fetchall()
        conn.close()

        return pd.DataFrame(data, columns=['expense_date', 'category_name', 'amount_paid'])

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
        
    def execute_query(self, query):
        """Execute SQL query and return results as DataFrame."""
        try:
            with self.get_db_connection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute(query)
                    data = cursor.fetchall()
                    columns = [col[0] for col in cursor.description]  # Fetch column names dynamically
            return pd.DataFrame(data, columns=columns)
        except Exception as e:
            logger.error(f"Error executing query: {e}")
            return pd.DataFrame()

    def generate_expense_query(self, user_id='ALL Users', selected_year=None, selected_month=None):
        """Generate SQL query for fetching user expenses dynamically."""
        logger.debug("Generating expense query.")
        
        query = """
        SELECT 
            e.expense_date,
            c.category_name,
            s.subcategory_name,
            e.amount_paid
        FROM expenses e
        JOIN categories c ON e.category_id = c.category_id
        LEFT JOIN subcategories s ON e.subcategory_id = s.subcategory_id AND s.category_id = c.category_id
        WHERE e.amount_paid IS NOT NULL
        AND e.category_id IS NOT NULL
        AND (e.subcategory_id IS NOT NULL OR s.subcategory_name IS NULL)  -- Allow NULL subcategory_id or exclude NULL values
        AND s.subcategory_name != 'Uncategorized'
        """

        # Add year filter if specified
        if selected_year is not None:
            query += f" AND YEAR(e.expense_date) = {selected_year}"
            logger.debug(f"Adding year filter: {selected_year}")
        
        # Add month filter if specified
        if selected_month is not None:
            try:
                month_numeric = list(calendar.month_name).index(selected_month)
                if month_numeric > 0:  # Index 0 is an empty string, so we check > 0
                    query += f" AND MONTH(e.expense_date) = {month_numeric}"
                    logger.debug(f"Adding month filter: {selected_month} ({month_numeric})")
                else:
                    logger.warning(f"Invalid month name provided: {selected_month}")
            except ValueError:
                logger.warning(f"Invalid month name provided: {selected_month}")

        
        # Filter by user_id, or include all users if 'ALL Users' is specified
        if user_id != 'ALL Users' and user_id is not None:
            query += f" AND e.user_id = {user_id}"
            logger.debug(f"Adding user filter: {user_id}")
        
        query += " ORDER BY c.category_name, s.subcategory_name, e.amount_paid DESC;"

        logger.debug(f"Generated query: {query}")

        # Execute the query and return the result as a DataFrame
        return self.execute_query(query)

