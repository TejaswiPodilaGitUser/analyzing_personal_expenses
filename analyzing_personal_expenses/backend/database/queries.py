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

FETCH_ALL_EXPENSES_BY_SUBCATEGORY_BASE_QUERY = """
SELECT 
    c.category_name,
    s.subcategory_name,
    IFNULL(SUM(e.amount_paid), 0) AS total_amount
FROM subcategories s
LEFT JOIN categories c ON s.category_id = c.category_id
LEFT JOIN expenses e ON s.subcategory_id = e.subcategory_id
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
SELECT s.subcategory_name AS subcategory_name, SUM(e.amount_paid) AS total_amount
FROM expenses e
LEFT JOIN subcategories s ON e.subcategory_id = s.subcategory_id
LEFT JOIN categories c ON s.category_id = c.category_id
WHERE c.category_name = %s
GROUP BY s.subcategory_name
ORDER BY total_amount DESC
"""

FETCH_ALL_EXPENSES_BY_SUBCATEGORY = """
SELECT 
    COALESCE(s.subcategory_name, 'Uncategorized') AS subcategory_name, 
    SUM(e.amount_paid) AS total_amount
FROM expenses e
LEFT JOIN subcategories s ON e.subcategory_id = s.subcategory_id
WHERE s.subcategory_name IS NOT NULL AND s.subcategory_name != 'Uncategorized'
GROUP BY s.subcategory_name
ORDER BY total_amount DESC
"""