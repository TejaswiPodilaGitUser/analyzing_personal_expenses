import pandas as pd


def generate_insights(df):
    """
    Generate insights from the expense data.
    Args:
        df (pd.DataFrame): Filtered DataFrame of expenses.

    Returns:
        dict: Insights dictionary containing max and min spending categories and amounts.
    """
    if df.empty:
        return {
            "max_category": "No insights available",
            "max_amount": 0,
            "min_category": "No insights available",
            "min_amount": 0
        }

    category_totals = df.groupby('category_name')['amount_paid'].sum()
    
    if category_totals.empty:
        return {
            "max_category": "No insights available",
            "max_amount": 0,
            "min_category": "No insights available",
            "min_amount": 0
        }

    max_category = category_totals.idxmax()
    max_amount = category_totals.max()
    min_category = category_totals.idxmin()
    min_amount = category_totals.min()

    return {
        "max_category": max_category,
        "max_amount": max_amount,
        "min_category": min_category,
        "min_amount": min_amount
    }
