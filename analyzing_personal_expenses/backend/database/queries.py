FETCH_USERS = """
SELECT user_id, user_name FROM users
"""

FETCH_ALL_CATEGORIES = """
SELECT DISTINCT category_name FROM categories
"""

FETCH_USER_CATEGORIES = """
SELECT DISTINCT c.category_name
FROM expenses e
JOIN categories c ON e.category_id = c.category_id
WHERE e.user_id = %s
"""

FETCH_ALL_EXPENSES = """
SELECT e.expense_date, c.category_name, e.amount_paid 
FROM expenses e
JOIN categories c ON e.category_id = c.category_id
"""

FETCH_USER_EXPENSES_YEARLY = """
SELECT e.expense_date, c.category_name, e.amount_paid 
FROM expenses e
JOIN categories c ON e.category_id = c.category_id
WHERE e.user_id = %s AND YEAR(e.expense_date) = %s
"""

FETCH_USER_EXPENSES_MONTHLY = """
SELECT e.expense_date, c.category_name, e.amount_paid 
FROM expenses e
JOIN categories c ON e.category_id = c.category_id
WHERE e.user_id = %s AND DATE_FORMAT(e.expense_date, '%%Y-%%m') = %s
"""

FETCH_ALL_USER_EXPENSES_YEARLY = """
SELECT e.expense_date, c.category_name, e.amount_paid 
FROM expenses e
JOIN categories c ON e.category_id = c.category_id
WHERE YEAR(e.expense_date) = %s
"""

FETCH_ALL_USER_EXPENSES_MONTHLY = """
SELECT e.expense_date, c.category_name, e.amount_paid 
FROM expenses e
JOIN categories c ON e.category_id = c.category_id
WHERE DATE_FORMAT(e.expense_date, '%%Y-%%m') = %s
"""

FETCH_EXPENSES_BY_CATEGORY = """
SELECT COALESCE(s.subcategory_name, 'Uncategorized') AS subcategory_name, SUM(e.amount_paid) AS total_amount
FROM expenses e
LEFT JOIN subcategories s ON e.subcategory_id = s.subcategory_id
LEFT JOIN categories c ON s.category_id = c.category_id
WHERE c.category_name = %s
GROUP BY s.subcategory_name
ORDER BY total_amount DESC
"""

FETCH_ALL_EXPENSES_BY_SUBCATEGORY = """
SELECT COALESCE(s.subcategory_name, 'Uncategorized') AS subcategory_name, SUM(e.amount_paid) AS total_amount
FROM expenses e
LEFT JOIN subcategories s ON e.subcategory_id = s.subcategory_id
GROUP BY s.subcategory_name
ORDER BY total_amount DESC
"""

# Fetch subcategory expenses for a user yearly
FETCH_SUBCATEGORY_EXPENSES_FOR_USER_YEARLY = """
SELECT 
    COALESCE(s.subcategory_name, 'Uncategorized') AS subcategory_name, 
    SUM(e.amount_paid) AS total_amount
FROM expenses e
LEFT JOIN subcategories s ON e.subcategory_id = s.subcategory_id
LEFT JOIN categories c ON s.category_id = c.category_id
WHERE e.user_id = %s AND YEAR(e.expense_date) = %s AND c.category_name = %s
GROUP BY s.subcategory_name
ORDER BY total_amount DESC
"""

# Fetch expenses by category for a user for a specific month
FETCH_EXPENSES_BY_CATEGORY_FOR_MONTH_FOR_USER = """
SELECT 
    COALESCE(s.subcategory_name, 'Uncategorized') AS subcategory_name, 
    SUM(e.amount_paid) AS total_amount
FROM expenses e
LEFT JOIN subcategories s ON e.subcategory_id = s.subcategory_id
LEFT JOIN categories c ON s.category_id = c.category_id
WHERE e.user_id = %s AND DATE_FORMAT(e.expense_date, '%%Y-%%m') = %s AND c.category_name = %s
GROUP BY s.subcategory_name
ORDER BY total_amount DESC
"""

# Fetch subcategory expenses for all users yearly
FETCH_SUBCATEGORY_EXPENSES_FOR_ALL_USERS_YEARLY = """
SELECT 
    COALESCE(s.subcategory_name, 'Uncategorized') AS subcategory_name, 
    SUM(e.amount_paid) AS total_amount
FROM expenses e
LEFT JOIN subcategories s ON e.subcategory_id = s.subcategory_id
LEFT JOIN categories c ON s.category_id = c.category_id
WHERE YEAR(e.expense_date) = %s AND c.category_name = %s
GROUP BY s.subcategory_name
ORDER BY total_amount DESC
"""

# Fetch expenses by category for all users for a specific month
FETCH_EXPENSES_BY_CATEGORY_FOR_MONTH_FOR_ALL_USERS = """
SELECT 
    COALESCE(s.subcategory_name, 'Uncategorized') AS subcategory_name, 
    SUM(e.amount_paid) AS total_amount
FROM expenses e
LEFT JOIN subcategories s ON e.subcategory_id = s.subcategory_id
LEFT JOIN categories c ON s.category_id = c.category_id
WHERE DATE_FORMAT(e.expense_date, '%%Y-%%m') = %s AND c.category_name = %s
GROUP BY s.subcategory_name
ORDER BY total_amount DESC
"""
