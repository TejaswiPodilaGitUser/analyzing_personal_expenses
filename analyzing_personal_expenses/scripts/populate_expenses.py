import mysql.connector
import random
from faker import Faker
import os
from dotenv import load_dotenv
from static_data import CATEGORY_DESCRIPTIONS  # Import static data

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
    return mysql.connector.connect(**db_config)

# Populate Expenses Table
def populate_expenses(n=50):
    conn = get_db_connection()
    cursor = conn.cursor()

    # Fetch required data
    cursor.execute("SELECT category_id, category_name FROM categories")
    category_data = cursor.fetchall()  # [(1, 'Food'), (2, 'Transportation')]
    category_map = {row[0]: row[1] for row in category_data}
    
    cursor.execute("SELECT subcategory_id FROM subcategories")
    subcategory_ids = [row[0] for row in cursor.fetchall()]
    
    cursor.execute("SELECT payment_mode_id FROM payment_modes")
    payment_mode_ids = [row[0] for row in cursor.fetchall()]
    
    cursor.execute("SELECT user_id FROM users")
    user_ids = [row[0] for row in cursor.fetchall()]
    
    for _ in range(n):
        user_id = random.choice(user_ids)
        category_id = random.choice(list(category_map.keys()))
        subcategory_id = random.choice(subcategory_ids)
        payment_mode_id = random.choice(payment_mode_ids)
        amount_paid = round(random.uniform(10.0, 500.0), 2)
        expense_date = fake.date_this_year()
        
        # Use CATEGORY_DESCRIPTIONS
        category_name = category_map[category_id]
        description = random.choice(CATEGORY_DESCRIPTIONS.get(category_name, ["No Description"]))
        
        cursor.execute(
            """INSERT INTO expenses 
            (user_id, category_id, subcategory_id, amount_paid, expense_date, payment_mode_id)
            VALUES (%s, %s, %s, %s, %s, %s)""",
            (user_id, category_id, subcategory_id, amount_paid, expense_date, payment_mode_id)
        )
    
    conn.commit()
    cursor.close()
    conn.close()
    print(f"✅ {n} expenses added successfully!")

if __name__ == "__main__":
    populate_expenses(50)
