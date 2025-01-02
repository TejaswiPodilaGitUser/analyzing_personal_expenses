import mysql.connector
import sys
import os

# Add the parent directory to the system path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from utils.password_utils import hash_password

def populate_users(get_db_connection):
    """
    Populates the users table with predefined users and hashed passwords.

    Args:
        get_db_connection (function): Function to establish a database connection.
    """
    conn = get_db_connection()
    cursor = conn.cursor()

    # Check if any of the usernames already exist
    existing_usernames = set()
    cursor.execute("SELECT user_name FROM users WHERE user_name IN (%s, %s, %s, %s)", ("user1", "user2", "user3", "user4"))
    for (username,) in cursor.fetchall():
        existing_usernames.add(username)
    
    if existing_usernames:
        print(f"⚠️ The following users already exist: {', '.join(existing_usernames)}. Aborting insertion.")
        cursor.close()
        conn.close()
        return

    users = [
        ("user1", "user1@example.com", "user1_password", "user"),
        ("user2", "user2@example.com", "user2_password", "user"),
        ("user3", "user3@example.com", "user3_password", "user"),
        ("user4", "user4@example.com", "user4_password", "user")
    ]
    
    hashed_users = [
        (username, email, hash_password(password), role) 
        for username, email, password, role in users
    ]

    cursor.executemany(
        """INSERT INTO users (user_name, user_email, password, role)
           VALUES (%s, %s, %s, %s)""",
        hashed_users
    )
    
    conn.commit()
    cursor.close()
    conn.close()
    print(f"✅ 5 Users with encrypted passwords added successfully!")
