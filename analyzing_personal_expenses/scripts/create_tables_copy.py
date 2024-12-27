import mysql.connector
import os
from dotenv import load_dotenv

# Load environment variables from .env to manage database credentials securely
load_dotenv()

# Database Configuration using environment variables
# These credentials should be stored in your .env file for security purposes
db_config = {
    'host': os.getenv('DB_HOST'),
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASSWORD'),
    'database': os.getenv('DB_NAME')
}

# Establish connection to the MySQL database
# This function returns the database connection object
def get_db_connection():
    return mysql.connector.connect(**db_config)

# SQL script to create tables for the expense tracker application
create_tables_sql = """
-- Drop Existing Tables (if any)
-- These tables are dropped to start fresh in case they already exist
DROP TABLE IF EXISTS expenses;
DROP TABLE IF EXISTS subcategories;
DROP TABLE IF EXISTS categories;
DROP TABLE IF EXISTS payment_modes;
DROP TABLE IF EXISTS users;

CREATE TABLE users (
    user_id INT PRIMARY KEY AUTO_INCREMENT,   -- Unique identifier for each user
    user_name VARCHAR(100) NOT NULL,          -- User's name
    user_email VARCHAR(100) NOT NULL,         -- User's email
    password VARCHAR(255) NOT NULL,           -- User's password (hashed)
    role ENUM('admin', 'user') NOT NULL,      -- User's role (admin or user)
    creation_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP, -- Record creation timestamp
    updation_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP -- Record last update timestamp
);

-- Categories Table: Stores categories for different expense types
CREATE TABLE categories (
    category_id INT AUTO_INCREMENT PRIMARY KEY,         -- Auto-incremented category ID
    category_name VARCHAR(100) NOT NULL UNIQUE,          -- Category name (e.g., 'Food', 'Transport')
    creation_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,   -- Date of creation
    updation_date TIMESTAMP DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP  -- Date of last update
) AUTO_INCREMENT = 100;  -- Starts category IDs from 100

-- Subcategories Table: Stores subcategories for each category
CREATE TABLE subcategories (
    subcategory_id INT AUTO_INCREMENT PRIMARY KEY,       -- Auto-incremented subcategory ID
    category_id INT NOT NULL,                            -- Foreign key referencing category_id
    subcategory_name VARCHAR(100) NOT NULL,              -- Subcategory name
    creation_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,   -- Date of creation
    updation_date TIMESTAMP DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP,  -- Date of last update
    FOREIGN KEY (category_id) REFERENCES categories(category_id) ON DELETE CASCADE ON UPDATE CASCADE  -- Foreign key constraint for category_id
) AUTO_INCREMENT = 1000;  -- Starts subcategory IDs from 1000

-- Payment Modes Table: Stores different payment methods used for expenses
CREATE TABLE payment_modes (
    payment_mode_id INT AUTO_INCREMENT PRIMARY KEY,      -- Auto-incremented payment mode ID
    payment_mode_name VARCHAR(50) NOT NULL UNIQUE,       -- Payment method name (e.g., 'UPI', 'Credit Card')
    creation_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,   -- Date of creation
    updation_date TIMESTAMP DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP  -- Date of last update
);

-- Expenses Table: Stores records of individual expenses made by users
-- Expenses Table: Stores records of individual expenses made by users
CREATE TABLE expenses (
    expense_id INT AUTO_INCREMENT PRIMARY KEY,           -- Auto-incremented expense ID
    user_id INT NULL,                                    -- Foreign key referencing user_id (can be NULL)
    category_id INT NOT NULL,                            -- Foreign key referencing category_id
    subcategory_id INT NOT NULL,                         -- Foreign key referencing subcategory_id
    amount_paid DECIMAL(10,2) NULL,                      -- Amount paid in the expense (can be NULL)
    expense_date DATE NOT NULL,                          -- Date of the expense
    payment_mode_id INT NOT NULL,                        -- Foreign key referencing payment_id
    creation_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,   -- Date of creation
    updation_date TIMESTAMP DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP,  -- Date of last update
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE SET NULL ON UPDATE CASCADE,  -- Foreign key constraint for user_id
    FOREIGN KEY (category_id) REFERENCES categories(category_id) ON DELETE CASCADE ON UPDATE CASCADE,  -- Foreign key constraint for category_id
    FOREIGN KEY (subcategory_id) REFERENCES subcategories(subcategory_id) ON DELETE CASCADE ON UPDATE CASCADE,  -- Foreign key constraint for subcategory_id
    FOREIGN KEY (payment_mode_id) REFERENCES payment_modes(payment_mode_id) ON DELETE CASCADE ON UPDATE CASCADE -- Foreign key constraint for payment_id
) AUTO_INCREMENT = 10000;  -- Starts expense IDs from 10000
"""

# Function to create the tables in the database
# This function will execute the SQL commands to create the necessary tables
def create_tables():
    conn = get_db_connection()  # Get a connection to the database
    cursor = conn.cursor()      # Create a cursor object to execute SQL commands

    try:
        # Execute each SQL command individually to avoid "Commands out of sync" error
        for sql in create_tables_sql.split(';'):  # Split the SQL script by semicolons
            if sql.strip():  # Ensure the SQL command is not empty
                cursor.execute(sql.strip())  # Execute the SQL command
        
        # Commit the changes to the database
        conn.commit()
        print("✅ Tables created successfully!")
    
    except mysql.connector.Error as err:  # Handle any errors that occur during the execution
        print(f"Error: {err}")  # Print the error message
        conn.rollback()  # Rollback the transaction in case of error
    
    finally:
        cursor.close()  # Close the cursor
        conn.close()    # Close the database connection

# Main entry point of the script
# This is where the table creation process is triggered
if __name__ == "__main__":
    create_tables()  # Call the function to create tables
