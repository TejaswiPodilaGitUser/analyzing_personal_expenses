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
        """Fetch all expenses for a specific user or all users, without dropping null values."""
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

    def fetch_user_categories(self, user_id='ALL Users', selected_year=None, selected_month=None):
        """Fetch distinct expense categories for a specific user or all users."""
        query = FETCH_USER_CATEGORIES

        # Add year filter if specified
        if selected_year is not None:
            query += f" AND YEAR(e.expense_date) = {selected_year}"
            logger.debug(f"Adding year filter: {selected_year}")

        # Add month filter if specified
        if selected_month is not None:
            try:
                month_numeric = list(calendar.month_name).index(selected_month)
                if month_numeric > 0:
                    query += f" AND MONTH(e.expense_date) = {month_numeric}"
                    logger.debug(f"Adding month filter: {selected_month} ({month_numeric})")
                else:
                    logger.warning(f"Invalid month name provided: {selected_month}")
            except ValueError:
                logger.warning(f"Invalid month name provided: {selected_month}")

        # Add user filter if specified
        if user_id != 'ALL Users' and user_id is not None:
            query += f" AND e.user_id = '{user_id}'"
            logger.debug(f"Adding user filter: {user_id}")

        query += " ORDER BY c.category_name;"
        logger.debug(f"Generated query: {query}")

        conn = self.get_db_connection()
        cursor = conn.cursor()
        cursor.execute(query)
        data = cursor.fetchall()
        conn.close()

        return pd.DataFrame(data, columns=['category_name'])

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
        """Generate SQL query for fetching user expenses dynamically without dropping null values."""
        logger.debug("Generating expense query.")

        query = FETCH_USER_EXPENSES_BASE_QUERY

        # Add year filter if specified
        if selected_year is not None:
            query += f" AND YEAR(e.expense_date) = {selected_year}"
            logger.debug(f"Adding year filter: {selected_year}")

        # Add month filter if specified
        if selected_month is not None:
            try:
                month_numeric = list(calendar.month_name).index(selected_month)
                if month_numeric > 0:
                    query += f" AND MONTH(e.expense_date) = {month_numeric}"
                    logger.debug(f"Adding month filter: {selected_month} ({month_numeric})")
                else:
                    logger.warning(f"Invalid month name provided: {selected_month}")
            except ValueError:
                logger.warning(f"Invalid month name provided: {selected_month}")

        if user_id != 'ALL Users' and user_id is not None:
            query += f" AND e.user_id = {user_id}"
            logger.debug(f"Adding user filter: {user_id}")

        query += " ORDER BY c.category_name, s.subcategory_name, e.amount_paid DESC;"
        logger.debug(f"Generated query: {query}")
        return self.execute_query(query)
    

    def fetch_categories(self, user_id='ALL Users', selected_year=None, selected_month=None):
        """
        Fetch distinct expense categories for a specific user, year, and month.
        """
        query = """
        SELECT DISTINCT c.category_id, c.category_name
        FROM categories c
        JOIN expenses e ON c.category_id = e.category_id
        WHERE 1=1
        """
        
        # Filter by user
        if user_id != 'ALL Users' and user_id is not None:
            query += f" AND e.user_id = '{user_id}'"
        
        # Filter by year
        if selected_year is not None:
            query += f" AND YEAR(e.expense_date) = {selected_year}"
        
        # Filter by month
        if selected_month is not None:
            try:
                month_numeric = list(calendar.month_name).index(selected_month)
                query += f" AND MONTH(e.expense_date) = {month_numeric}"
            except ValueError:
                logger.warning(f"Invalid month name provided: {selected_month}")
        
        query += " ORDER BY c.category_name;"
        logger.debug(f"Generated fetch_categories query: {query}")

        try:
            with self.get_db_connection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute(query)
                    categories = cursor.fetchall()
                    return pd.DataFrame(categories, columns=['category_id', 'category_name'])
        except Exception as e:
            logger.error(f"Error fetching categories: {e}")
            return pd.DataFrame()


    def fetch_subcategories(self, user_id='ALL Users', selected_year=None, selected_month=None, category_id=None):
        """
        Fetch distinct subcategories based on user, year, month, and optionally category_id.
        """
        query = FETCH_SUBCATEGORIES
        
        # Filter by user
        if user_id != 'ALL Users' and user_id is not None:
            query += f" AND e.user_id = '{user_id}'"
        
        # Filter by year
        if selected_year is not None:
            query += f" AND YEAR(e.expense_date) = {selected_year}"
        
        # Filter by month
        if selected_month is not None:
            try:
                month_numeric = list(calendar.month_name).index(selected_month)
                query += f" AND MONTH(e.expense_date) = {month_numeric}"
            except ValueError:
                logger.warning(f"Invalid month name provided: {selected_month}")
        
        # Filter by category
        if category_id is not None:
            query += f" AND s.category_id = {category_id}"
        
        query += " ORDER BY s.subcategory_name;"
        logger.debug(f"Generated fetch_subcategories query: {query}")

        try:
            with self.get_db_connection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute(query)
                    subcategories = cursor.fetchall()
                    return pd.DataFrame(subcategories, columns=['subcategory_id', 'subcategory_name'])
        except Exception as e:
            logger.error(f"Error fetching subcategories: {e}")
            return pd.DataFrame()
        
    def fetch_payment_mode_counts(self, user_id='ALL Users', selected_year=None, selected_month=None, category_id=None):
        """
        Fetch count of payment modes used for selected user, year, month, and category.
        """
        query = FETCH_PAYMENT_MODE_COUNT_QUERY

        # Filter by user
        if user_id != 'ALL Users' and user_id is not None:
            query += f" AND e.user_id = '{user_id}'"

        # Filter by year
        if selected_year is not None:
            query += f" AND YEAR(e.expense_date) = {selected_year}"

        # Filter by month
        if selected_month is not None:
            try:
                month_numeric = list(calendar.month_name).index(selected_month)
                query += f" AND MONTH(e.expense_date) = {month_numeric}"
            except ValueError:
                logger.warning(f"Invalid month name provided: {selected_month}")

        # Filter by category
        if category_id is not None:
            query += f" AND e.category_id = {category_id}"

        #query += " GROUP BY c.category_name,pm.payment_mode_name ORDER BY payment_count DESC;"
        logger.debug(f"Generated fetch_payment_mode_counts query: {query}")


        try:
            with self.get_db_connection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute(query)
                    payment_modes = cursor.fetchall()
                    return pd.DataFrame(payment_modes, columns=['expense_date','category_name','payment_mode_name', 'payment_count'])
        except Exception as e:
            logger.error(f"Error fetching payment mode counts: {e}")
            return pd.DataFrame()