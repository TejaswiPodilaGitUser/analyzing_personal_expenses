import mysql.connector
import random
from faker import Faker
import os
from dotenv import load_dotenv

# Load environment variables from .env to manage database credentials securely
load_dotenv()

# Database Configuration using environment variables
db_config = {
    'host': os.getenv('DB_HOST'),
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASSWORD'),
    'database': os.getenv('DB_NAME')
}

fake = Faker()

# Function to get a connection to the database
def get_db_connection():
    return mysql.connector.connect(**db_config)

# Static Data
CATEGORIES = ['Food', 'Transportation', 'Bills', 'Groceries', 'Subscriptions', 
              'Personal Spending', 'Investments', 'Stationary', 'Fruits & Vegetables', 
              'Home Essentials', 'Sports & Fitness', 'School Fees']

PAYMENT_MODES = ['UPI', 'Netbanking', 'Credit Card', 'Debit Card', 'Online', 'Wallet', 'Cash']

CATEGORY_DESCRIPTIONS = {
    'Food': ['Lunch Bills', 'Dinner', 'Takeaway', 'Snacks', 'Cafe'],
    'Transportation': ['Taxi Fare', 'Bus Ticket', 'Train Ticket', 'Fuel','Tours'],
    'Bills': ['Electricity Bills', 'Water Bills', 'Internet Bills'],
    'Groceries': ['Grocery Shopping', 'Pulses & Grains', 'Milk & Eggs','Dry Fruits','Chocolates & Biscuits'],
    'Subscriptions': ['Amazon Subscription', 'Netflix Subscription', 'Spotify Subscription', 'Magazine Subscription'],
    'Personal Spending': ['Clothing', 'Cosmetics', 'Haircut'],
    'Investments': ['Investment Bonds', 'Fixed Deposits', 'Stocks Purchase'],
    'Stationary': ['Pens & Pencils', 'Notebooks', 'Paper'],
    'Fruits & Vegetables': ['Fruits', 'Vegetables'],
    'Home Essentials': ['Cookware', 'Cleaning Supplies', 'Furniture'],
    'Sports & Fitness': ['Gym Membership', 'Yoga Class', 'Cricket Kit'],
    'School Fees': ['Tuition Fees', 'Books & Stationary','School Fees','Trips']
}

# 1. Populate Users Table (5 users)
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

# 2. Populate Categories and Subcategories (Only new categories)
def populate_categories_and_subcategories():
    conn = get_db_connection()
    cursor = conn.cursor()

    for category in CATEGORIES:
        # Check if category already exists
        cursor.execute("SELECT COUNT(*) FROM categories WHERE category_name = %s", (category,))
        if cursor.fetchone()[0] == 0:
            cursor.execute(
                "INSERT INTO categories (category_name) VALUES (%s)",
                (category,)
            )
            category_id = cursor.lastrowid
            
            # Insert subcategories for this category
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

# 3. Populate Payment Modes (Only new payment modes)
def populate_payment_modes():
    conn = get_db_connection()
    cursor = conn.cursor()

    for mode in PAYMENT_MODES:
        # Check if payment mode already exists
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

# 4. Populate Expenses (50 records)
def populate_expenses(n=50):
    conn = get_db_connection()
    cursor = conn.cursor()

    # Fetch required data
    cursor.execute("SELECT category_id, category_name FROM categories")
    category_data = cursor.fetchall()  # [(1, 'Food'), (2, 'Transportation'), ...]
    category_map = {row[0]: row[1] for row in category_data}  # {1: 'Food', 2: 'Transportation'}
    
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
        
        # Use CATEGORY_DESCRIPTIONS based on category_id
        category_name = category_map[category_id]
        description = random.choice(CATEGORY_DESCRIPTIONS.get(category_name, ["No Description"]))
        
        cursor.execute(
            """INSERT INTO expenses 
               (user_id, category_id, subcategory_id, amount_paid, expense_date, description, payment_mode_id)
               VALUES (%s, %s, %s, %s, %s, %s, %s)""",
            (user_id, category_id, subcategory_id, amount_paid, expense_date, description, payment_mode_id)
        )
    
    conn.commit()
    cursor.close()
    conn.close()
    print(f"✅ {n} expenses added successfully!")

# Main Function
def main():
    print("🚀 Starting Database Population...")
    populate_users()
    populate_categories_and_subcategories()
    populate_payment_modes()
    populate_expenses(50)
    print("🎯 All tables populated successfully!")

if __name__ == "__main__":
    main()
