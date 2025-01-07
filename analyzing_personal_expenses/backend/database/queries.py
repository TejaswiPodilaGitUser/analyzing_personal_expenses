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
LEFT JOIN subcategories s ON e.subcategory_id = s.subcategory_id AND s.category_id = c.category_id
"""

# Base query to fetch user expenses with all data (no null value filtering)
FETCH_USER_EXPENSES_BASE_QUERY = """
SELECT 
e.expense_date,
c.category_name,
s.subcategory_name,
e.amount_paid
FROM expenses e
JOIN categories c ON e.category_id = c.category_id
LEFT JOIN subcategories s ON e.subcategory_id = s.subcategory_id AND s.category_id = c.category_id
where 1=1 
"""


FETCH_SUBCATEGORIES="""
SELECT DISTINCT s.subcategory_id, s.subcategory_name
FROM subcategories s
JOIN expenses e ON s.subcategory_id = e.subcategory_id
WHERE 1=1
"""


# Query to fetch count of payment modes for selected user, year, month, and category
FETCH_PAYMENT_MODE_COUNT_QUERY = """
SELECT
    e.expense_date,
    c.category_name,
    pm.payment_mode_name, 
    e.payment_mode_id AS payment_count
FROM 
    expenses e
JOIN 
    payment_modes pm ON e.payment_mode_id = pm.payment_mode_id
JOIN 
    categories c ON e.category_id = c.category_id
WHERE 
    1=1
"""