import pandas as pd
import streamlit as st
from backend.database.db_operations import DatabaseOperations
from frontend.ui.bar_chart import plot_bar_chart
from frontend.ui.pie_chart import plot_pie_chart

class DataVisualization:
    def __init__(self, user_id=None):
        self.user_id = user_id
        self.db_ops = DatabaseOperations()

    def get_user_expenses(self):
        """Fetch user expenses from the database."""
        try:
            df = self.db_ops.fetch_user_expenses(self.user_id)
            if df.empty:
                raise ValueError("No expenses found for the selected user.")
            return df
        except Exception as e:
            print(f"Error fetching expenses: {e}")
            return pd.DataFrame()

    def plot_monthly_expenses(self, df, selected_month="January", chart_type="pie"):
        """Create bar and pie charts for monthly expenses."""
        if df.empty:
            print("No data available to plot monthly expenses.")
            return
        
        df['expense_date'] = pd.to_datetime(df['expense_date'], errors='coerce')
        df['expense_month'] = df['expense_date'].dt.strftime('%B')
        filtered_df = df[df['expense_month'] == selected_month]
        filtered_df['amount_paid'] = pd.to_numeric(filtered_df['amount_paid'], errors='coerce')
        monthly_expenses = filtered_df.groupby('category_name')['amount_paid'].sum()

        if chart_type.lower() == "bar":
            plot_bar_chart(monthly_expenses, "Category", "Amount Paid", f"Top Spending Categories - {selected_month}")
        elif chart_type.lower() == "pie":
            plot_pie_chart(monthly_expenses, f"Top Spending Categories - {selected_month}")

    def plot_yearly_expenses(self, df, chart_type="pie"):
        """Create bar and pie charts for yearly expenses."""
        df['amount_paid'] = pd.to_numeric(df['amount_paid'], errors='coerce')
        yearly_expenses = df.groupby('category_name')['amount_paid'].sum()

        if chart_type.lower() == "bar":
            plot_bar_chart(yearly_expenses, "Category", "Amount Paid", "Yearly Expenses Overview")
        elif chart_type.lower() == "pie":
            plot_pie_chart(yearly_expenses, "Yearly Expenses Breakdown")

    def get_top_spending_categories(self, df):
        """Get the top 10 spending categories."""
        df['amount_paid'] = pd.to_numeric(df['amount_paid'], errors='coerce')
        return df.groupby('category_name')['amount_paid'].sum().nlargest(10).reset_index()

    def get_insights(self, df):
        """Get insights such as max and min spending categories."""
        # Ensure 'amount_paid' exists in the DataFrame
        if 'amount_paid' not in df.columns:
            raise KeyError("The 'amount_paid' column is missing in the data.")
        
        # Group by category and calculate total amount spent per category
        grouped = df.groupby('category_name')['amount_paid'].sum()
        
        # Return insights on max and min spending categories
        return {
            "max_category": grouped.idxmax(),
            "max_amount": grouped.max(),
            "min_category": grouped.idxmin(),
            "min_amount": grouped.min()
        }
