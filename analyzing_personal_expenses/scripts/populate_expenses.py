import mysql.connector
import random
from faker import Faker
import os
from dotenv import load_dotenv
import datetime  # Import datetime module

# Load environment variables
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
    """Establish database connection."""
    return mysql.connector.connect(**db_config)

# Populate Expenses Table without NULL values
def populate_expenses(n=50):
    conn = get_db_connection()
    cursor = conn.cursor()

    # Fetch required data
    cursor.execute("SELECT category_id FROM categories")
    category_ids = [row[0] for row in cursor.fetchall()]
    
    cursor.execute("SELECT payment_mode_id FROM payment_modes")
    payment_mode_ids = [row[0] for row in cursor.fetchall()]
    
    cursor.execute("SELECT user_id FROM users")
    user_ids = [row[0] for row in cursor.fetchall()]

    for i in range(n):
        user_id = random.choice(user_ids)
        category_id = random.choice(category_ids)
        payment_mode_id = random.choice(payment_mode_ids)
        
        # Fetch valid subcategory_id for the selected category
        cursor.execute("SELECT subcategory_id FROM subcategories WHERE category_id = %s", (category_id,))
        subcategory_ids = [row[0] for row in cursor.fetchall()]
        subcategory_id = random.choice(subcategory_ids) if subcategory_ids else None
        
        amount_paid = round(random.uniform(10.0, 500.0), 2)
        
        # Create random creation_date between 2020 and 2025
        start_date = datetime.date(2020, 1, 1)  # Start date: January 1, 2020
        end_date = datetime.date(2025, 12, 31)  # End date: December 31, 2025
        creation_date = fake.date_between(start_date=start_date, end_date=end_date)
        
        try:
            cursor.execute(
                """INSERT INTO expenses 
                (user_id, category_id, subcategory_id, amount_paid, expense_date, payment_mode_id, creation_date)
                VALUES (%s, %s, %s, %s, %s, %s, %s)""",
                (user_id, category_id, subcategory_id, amount_paid, creation_date, payment_mode_id, creation_date)
            )
        except mysql.connector.Error as err:
            print(f"❌ Error inserting record {i+1}: {err}")
    
    conn.commit()
    cursor.close()
    conn.close()
    print(f"✅ {n} expenses (all fields populated) added successfully!")

if __name__ == "__main__":
    populate_expenses(50)
