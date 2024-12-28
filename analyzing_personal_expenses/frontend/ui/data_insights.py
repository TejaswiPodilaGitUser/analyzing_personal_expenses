import pandas as pd

def get_insights(df, selected_year=None, selected_month=None):
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
    
    # Create a copy of the DataFrame explicitly
    df = df.copy()

    # Ensure 'amount_paid' is numeric and drop NaNs
    df['amount_paid'] = pd.to_numeric(df['amount_paid'], errors='coerce')
    df = df.dropna(subset=['amount_paid'])

    # Filter data for selected year and month (if provided)
    if selected_year:
        df = df[df['expense_year'] == int(selected_year)]
    if selected_month:
        df = df[df['expense_month'] == selected_month]

    if df.empty:
        return {
            "max_category": "No data available",
            "max_amount": "No data available",
            "min_category": "No data available",
            "min_amount": "No data available"
        }

    # Group by category and get the total amount for each category
    grouped = df.groupby('category_name')['amount_paid'].sum()

    if grouped.empty:
        return {
            "max_category": "No data available",
            "max_amount": "No data available",
            "min_category": "No data available",
            "min_amount": "No data available"
        }

    # Return max and min spending categories
    return {
        "max_category": grouped.idxmax(),
        "max_amount": grouped.max(),
        "min_category": grouped.idxmin(),
        "min_amount": grouped.min()
    }
