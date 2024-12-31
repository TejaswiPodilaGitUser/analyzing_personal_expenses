# To fetch all Users
FETCH_USERS = """
SELECT user_id, user_name FROM users
"""

# To fetch All categories
FETCH_ALL_CATEGORIES = """
SELECT DISTINCT category_name FROM categories
"""

# To fetch all Categories for a user
FETCH_USER_CATEGORIES = """
SELECT DISTINCT c.category_name
FROM expenses e
JOIN categories c ON e.category_id = c.category_id
WHERE e.user_id = %s
"""


