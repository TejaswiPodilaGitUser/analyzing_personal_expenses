import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
from frontend.ui.bar_chart import plot_bar_chart
from frontend.ui.pie_chart import plot_pie_chart
from backend.database.db_operations import DatabaseOperations


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
            return None
        
        df['expense_date'] = pd.to_datetime(df['expense_date'], errors='coerce')
        df['expense_month'] = df['expense_date'].dt.strftime('%B')
        filtered_df = df[df['expense_month'] == selected_month]
        filtered_df['amount_paid'] = pd.to_numeric(filtered_df['amount_paid'], errors='coerce')
        monthly_expenses = filtered_df.groupby('category_name')['amount_paid'].sum()

        if monthly_expenses.empty:
            st.warning(f"No data available for the selected month: {selected_month}")
            return None

        if chart_type.lower() == "bar":
            plot_bar_chart(
                monthly_expenses,
                xlabel="Category",
                ylabel="Amount Paid",
                title=f"Top Spending Categories - {selected_month}"
            )
        elif chart_type.lower() == "pie":
            plot_pie_chart(
                monthly_expenses,
                title=f"Top Spending Categories - {selected_month}"
            )
    
    def plot_yearly_expenses(self, df, chart_type="pie"):
        """Create bar and pie charts for yearly expenses."""
        if df.empty:
            print("No data available to plot yearly expenses.")
            return None

        df['amount_paid'] = pd.to_numeric(df['amount_paid'], errors='coerce')
        yearly_expenses = df.groupby('category_name')['amount_paid'].sum()

        if yearly_expenses.empty:
            st.warning("No data available for yearly expenses.")
            return None

        if chart_type.lower() == "bar":
            plot_bar_chart(
                yearly_expenses,
                xlabel="Category",
                ylabel="Amount Paid",
                title="Yearly Expenses Overview"
            )
        elif chart_type.lower() == "pie":
            plot_pie_chart(
                yearly_expenses,
                title="Yearly Expenses Breakdown"
            )

    def get_top_spending_categories(self, df):
        """Get the top 10 spending categories."""
        if df.empty:
            return pd.DataFrame(columns=['category_name', 'amount_paid'])
        
        df['amount_paid'] = pd.to_numeric(df['amount_paid'], errors='coerce')
        return df.groupby('category_name')['amount_paid'].sum().nlargest(10).reset_index()

    def get_insights(self, df):
        """Get insights such as max and min spending categories."""
        if df.empty:
            return {
                "max_category": "No data available",
                "max_amount": "No data available",
                "min_category": "No data available",
                "min_amount": "No data available"
            }
        
        if 'amount_paid' not in df.columns:
            raise KeyError("The 'amount_paid' column is missing in the data.")
        
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

    def display_expense_summary(self, df):
        """Display expense summary insights."""
        insights = self.get_insights(df)

        st.write("### 📊 Expense Summary: Key Spending Insights")
        if insights['max_category'] == "No data available":
            st.warning("No data available for insights.")
        else:
            st.write(f"▲ **Max Spending:** {insights['max_category']} (${insights['max_amount']:.2f})")
            st.write(f"▼ **Min Spending:** {insights['min_category']} (${insights['min_amount']:.2f})")
