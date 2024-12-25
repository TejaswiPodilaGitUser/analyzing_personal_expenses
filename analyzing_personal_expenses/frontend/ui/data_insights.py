import pandas as pd

def get_insights(df):
    """Get insights such as max and min spending categories."""
    if df.empty:
        return {
            "max_category": "No data available",
            "max_amount": "No data available",
            "min_category": "No data available",
            "min_amount": "No data available"
        }
    
    if 'amount_paid' not in df.columns:
        return {
            "max_category": "No data available",
            "max_amount": "No data available",
            "min_category": "No data available",
            "min_amount": "No data available"
        }
    
    grouped = df.groupby('category_name')['amount_paid'].sum()
    
    if grouped.empty:
        return {
            "max_category": "No data available",
            "max_amount": "No data available",
            "min_category": "No data available",
            "min_amount": "No data available"
        }

    return {
        "max_category": grouped.idxmax(),
        "max_amount": grouped.max(),
        "min_category": grouped.idxmin(),
        "min_amount": grouped.min()
    }
