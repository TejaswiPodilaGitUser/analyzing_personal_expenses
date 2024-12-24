import unittest
from unittest.mock import MagicMock
import re
from backend.database.db_operations import DatabaseOperations  # Replace with your actual import path

# Helper function to normalize SQL queries by trimming spaces
def normalize_sql_query(query):
    # Remove leading/trailing spaces and reduce multiple spaces to a single space
    return re.sub(r'\s+', ' ', query.strip())

class TestDatabaseOperations(unittest.TestCase):

    def setUp(self):
        # Create an instance of the DatabaseOperations class
        self.db_ops = DatabaseOperations()
        
        # Mock the database connection and cursor
        self.db_ops.get_db_connection = MagicMock()
        self.mock_conn = MagicMock()
        self.mock_cursor = MagicMock()
        self.db_ops.get_db_connection.return_value = self.mock_conn
        self.mock_conn.cursor.return_value = self.mock_cursor
    
    def test_fetch_user_expenses_with_user_id(self):
        user_id = 1  # Example user ID
        # Sample SQL query expected and actual values
        expected_query = """
            SELECT e.expense_date, c.category_name, e.amount_paid
            FROM expenses e
            JOIN categories c ON e.category_id = c.category_id
            WHERE e.user_id = %s
        """
        
        # Simulate the database query execution
        self.db_ops.fetch_user_expenses(user_id)
        
        # Get the actual query executed by the mock cursor
        actual_query = self.mock_cursor.execute.call_args[0][0]
        
        # Normalize both the expected and actual queries by trimming spaces
        normalized_expected_query = normalize_sql_query(expected_query)
        normalized_actual_query = normalize_sql_query(actual_query)
        
        # Compare the normalized queries
        self.assertEqual(normalized_expected_query, normalized_actual_query)

    # Add more test methods if needed

if __name__ == '__main__':
    unittest.main()
