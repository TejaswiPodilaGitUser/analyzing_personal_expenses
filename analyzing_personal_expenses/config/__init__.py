import sys
import os

# Base Directory
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Add backend and frontend paths
sys.path.append(os.path.join(BASE_DIR, 'backend'))
sys.path.append(os.path.join(BASE_DIR, 'frontend'))

# Database configurations
DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "password",
    "database": "analyzing_personal_expenses_db"
}
