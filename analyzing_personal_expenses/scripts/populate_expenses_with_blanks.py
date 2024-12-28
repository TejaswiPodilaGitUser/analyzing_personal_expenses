import mysql.connector
import random
from faker import Faker
import os
from dotenv import load_dotenv

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

# Populate Expenses Table with selective NULL values
def populate_expenses_with_blanks(n=50):
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
        # Randomize NULL values for specific fields
        user_id = random.choice(user_ids) if random.random() > 0.3 else None
        subcategory_id = random.choice([None, random.randint(1000, 1010)]) if random.random() > 0.3 else None
        amount_paid = round(random.uniform(10.0, 500.0), 2) if random.random() > 0.3 else None
        
        # Ensure mandatory fields are always populated
        category_id = random.choice(category_ids)
        payment_mode_id = random.choice(payment_mode_ids)
        # Use years fake date range 2020-2026
        expense_date = fake.date_between(start_date='-5y', end_date='now')
        
        try:
            cursor.execute(
                """INSERT INTO expenses 
                (user_id, category_id, subcategory_id, amount_paid, expense_date, payment_mode_id)
                VALUES (%s, %s, %s, %s, %s, %s)""",
                (user_id, category_id, subcategory_id, amount_paid, expense_date, payment_mode_id)
            )
        except mysql.connector.Error as err:
            print(f"❌ Error inserting record {i+1}: {err}")
    
    conn.commit()
    cursor.close()
    conn.close()
    print(f"✅ {n} expenses (with blanks in user_id, subcategory_id, and amount_paid) added successfully!")

if __name__ == "__main__":
    populate_expenses_with_blanks(50)
