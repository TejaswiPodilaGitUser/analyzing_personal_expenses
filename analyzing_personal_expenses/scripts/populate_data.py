import os
from dotenv import load_dotenv
import mysql.connector
from faker import Faker
from populate_expenses import populate_expenses  # Import the extracted function
from static_data import CATEGORIES, PAYMENT_MODES, CATEGORY_DESCRIPTIONS  # Import static data

# Load environment variables from .env
load_dotenv()

# Database Configuration
db_config = {
    'host': os.getenv('DB_HOST'),
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASSWORD'),
    'database': os.getenv('DB_NAME')
}

fake = Faker()

def get_db_connection():
    return mysql.connector.connect(**db_config)

def populate_users():
    conn = get_db_connection()
    cursor = conn.cursor()

    users = [
        ("admin", "admin@example.com", "admin_password", "admin"),
        ("user1", "user1@example.com", "user_password", "user"),
        ("user2", "user2@example.com", "user_password", "user"),
        ("user3", "user3@example.com", "user_password", "user"),
        ("user4", "user4@example.com", "user_password", "user")
    ]
    
    cursor.executemany(
        """INSERT INTO users (user_name, user_email, password, role)
           VALUES (%s, %s, %s, %s)""",
        users
    )
    
    conn.commit()
    cursor.close()
    conn.close()
    print(f"✅ 5 Users added successfully!")

def populate_categories_and_subcategories():
    conn = get_db_connection()
    cursor = conn.cursor()

    for category in CATEGORIES:
        cursor.execute("SELECT COUNT(*) FROM categories WHERE category_name = %s", (category,))
        if cursor.fetchone()[0] == 0:
            cursor.execute(
                "INSERT INTO categories (category_name) VALUES (%s)",
                (category,)
            )
            category_id = cursor.lastrowid
            
            for subcategory in CATEGORY_DESCRIPTIONS[category]:
                cursor.execute(
                    "INSERT INTO subcategories (category_id, subcategory_name) VALUES (%s, %s)",
                    (category_id, subcategory)
                )
            print(f"✅ Category '{category}' and its subcategories added.")
        else:
            print(f"Category '{category}' already exists, skipping insertion.")
    
    conn.commit()
    cursor.close()
    conn.close()

def populate_payment_modes():
    conn = get_db_connection()
    cursor = conn.cursor()

    for mode in PAYMENT_MODES:
        cursor.execute("SELECT COUNT(*) FROM payment_modes WHERE payment_mode_name = %s", (mode,))
        if cursor.fetchone()[0] == 0:
            cursor.execute(
                "INSERT INTO payment_modes (payment_mode_name) VALUES (%s)",
                (mode,)
            )
            print(f"✅ Payment mode '{mode}' added.")
        else:
            print(f"Payment mode '{mode}' already exists, skipping insertion.")
    
    conn.commit()
    cursor.close()
    conn.close()

def main():
    print("🚀 Starting Database Population...")
    populate_users()
    populate_categories_and_subcategories()
    populate_payment_modes()
    populate_expenses(50)
    print("🎯 All tables populated successfully!")

if __name__ == "__main__":
    main()
