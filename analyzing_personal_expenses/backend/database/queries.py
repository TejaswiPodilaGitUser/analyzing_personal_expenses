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

# To fetch all Categories for a user in a specific year
FETCH_USER_CATEGORIES = """
SELECT DISTINCT c.category_name
FROM expenses e
JOIN categories c ON e.category_id = c.category_id
LEFT JOIN subcategories s ON e.subcategory_id = s.subcategory_id AND s.category_id = c.category_id
WHERE e.amount_paid IS NOT NULL
AND e.category_id IS NOT NULL
AND (e.subcategory_id IS NOT NULL OR s.subcategory_name IS NULL)
AND (s.subcategory_name IS NULL OR s.subcategory_name != 'Uncategorized')
"""

FETCH_USER_EXPENSES_BASE_QUERY = """
SELECT 
e.expense_date,
c.category_name,
s.subcategory_name,
e.amount_paid
FROM expenses e
JOIN categories c ON e.category_id = c.category_id
LEFT JOIN subcategories s ON e.subcategory_id = s.subcategory_id AND s.category_id = c.category_id
WHERE e.amount_paid IS NOT NULL
AND e.category_id IS NOT NULL
AND (e.subcategory_id IS NOT NULL OR s.subcategory_name IS NULL)  -- Allow NULL subcategory_id or exclude NULL values
AND s.subcategory_name != 'Uncategorized'
"""