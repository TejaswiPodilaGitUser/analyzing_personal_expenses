import pandas as pd

def get_payment_mode_insights(df, selected_year=None, selected_month=None):
    """Get insights such as max and min payment modes based on transaction counts."""

    if df.empty:
        return {
            "max_payment_mode": "No data available",
            "max_payment_count": "No data available",
            "min_payment_mode": "No data available",
            "min_payment_count": "No data available"
        }

    if 'payment_mode_name' not in df.columns or 'count' not in df.columns:
        return {
            "max_payment_mode": "No data available",
            "max_payment_count": "No data available",
            "min_payment_mode": "No data available",
            "min_payment_count": "No data available"
        }

    # Create a copy of the DataFrame explicitly
    df = df.copy()

    # Filter data for selected year and month (if provided)
    if selected_year:
        df = df[df['expense_year'] == int(selected_year)]
    if selected_month:
        df = df[df['expense_month'] == selected_month]

    if df.empty:
        return {
            "max_payment_mode": "No data available",
            "max_payment_count": "No data available",
            "min_payment_mode": "No data available",
            "min_payment_count": "No data available"
        }

    # Group by payment mode and get the count of transactions for each mode
    payment_mode_counts = df.groupby('payment_mode_name')['count'].sum()

    if payment_mode_counts.empty:
        return {
            "max_payment_mode": "No data available",
            "max_payment_count": "No data available",
            "min_payment_mode": "No data available",
            "min_payment_count": "No data available"
        }

    # Return max and min payment modes based on count
    return {
        "max_payment_mode": payment_mode_counts.idxmax(),
        "max_payment_count": payment_mode_counts.max(),
        "min_payment_mode": payment_mode_counts.idxmin(),
        "min_payment_count": payment_mode_counts.min()
    }
