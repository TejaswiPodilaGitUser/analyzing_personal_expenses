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

# Fetch All Expenses Base Query
FETCH_ALL_EXPENSES_BASE_QUERY = """
SELECT e.expense_date, c.category_name, e.amount_paid 
FROM expenses e
JOIN categories c ON e.category_id = c.category_id
"""

# Fetch All expenses by Subcategory
FETCH_ALL_EXPENSES_BY_SUBCATEGORY_BASE_QUERY = """
SELECT 
    c.category_name, 
    COALESCE(s.subcategory_name, 'Uncategorized') AS subcategory_name,
    SUM(e.amount_paid) AS total_amount
FROM expenses e
JOIN categories c ON e.category_id = c.category_id
LEFT JOIN subcategories s ON e.subcategory_id = s.subcategory_id AND s.category_id = c.category_id
"""

# Fetch all Expenses for selected Sub category
FETCH_EXPENSES_BY_CATEGORY = """
SELECT s.subcategory_name AS subcategory_name, SUM(e.amount_paid) AS total_amount
FROM expenses e
LEFT JOIN subcategories s ON e.subcategory_id = s.subcategory_id
LEFT JOIN categories c ON s.category_id = c.category_id
WHERE c.category_name = %s
GROUP BY s.subcategory_name
ORDER BY total_amount DESC
"""

# Fetch All Expenses if Categories="ALL categories"
FETCH_ALL_EXPENSES_BY_ALL_CATEGORIES = """
SELECT 
    COALESCE(s.subcategory_name, 'Uncategorized') AS subcategory_name, 
    SUM(e.amount_paid) AS total_amount
FROM expenses e
LEFT JOIN subcategories s ON e.subcategory_id = s.subcategory_id
WHERE s.subcategory_name IS NOT NULL AND s.subcategory_name != 'Uncategorized'
GROUP BY s.subcategory_name
ORDER BY total_amount DESC
"""
