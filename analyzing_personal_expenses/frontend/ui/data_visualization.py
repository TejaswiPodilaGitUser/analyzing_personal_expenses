import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import sys
import os

# Add the parent directory to the system path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from frontend.ui.bar_chart import plot_bar_chart
from frontend.ui.pie_chart import plot_pie_chart
from frontend.ui.scatter_chart import plot_scatter_chart
from backend.database.db_operations import DatabaseOperations
from io import StringIO
from frontend.ui.data_insights import get_insights  # Importing the new insights function

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
            st.warning("No data available to plot monthly expenses.")
            return None
        
        # Ensure necessary columns are present and valid
        if 'amount_paid' not in df.columns or 'expense_date' not in df.columns:
            st.error("Missing required columns.")
            return None

        df['expense_date'] = pd.to_datetime(df['expense_date'], errors='coerce')
        df['amount_paid'] = pd.to_numeric(df['amount_paid'], errors='coerce')
        df['expense_month'] = df['expense_date'].dt.strftime('%B')

        # Filter data for selected month
        filtered_df = df[df['expense_month'] == selected_month]

        if filtered_df.empty:
            st.warning(f"No valid data for the selected month: {selected_month}")
            return None
        
        monthly_expenses = filtered_df.groupby('category_name')['amount_paid'].sum()

        if monthly_expenses.empty:
            st.warning(f"No data available for the selected month: {selected_month}")
            return None

        # Dynamically set the report title
        st.markdown(f"### 📅 Monthly Expenses Overview: {selected_month}")

        # Plot the chart
        if chart_type.lower() == "bar":
            plot_bar_chart(
                monthly_expenses,
                xlabel="Category",
                ylabel="Amount Paid",
                title=f"Spending Categories - {selected_month}"
            )
        elif chart_type.lower() == "pie":
            plot_pie_chart(monthly_expenses, title=f"Spending Categories - {selected_month}", chart_size=(6, 4))

        elif chart_type.lower() == "scatter":
            # Use the updated plot_scatter_chart function
            fig = plot_scatter_chart(filtered_df, x='category_name', y='amount_paid', title=f"Expense Scatter Plot - {selected_month}")
            if fig:
                st.pyplot(fig)

        # Enable CSV download
        report_title = f"Top 10 Expenses for {selected_month}"
        self.download_csv(filtered_df, report_title)

    def plot_yearly_expenses(self, df, chart_type="pie"):
        """Create bar and pie charts for yearly expenses."""
        if df.empty:
            st.warning("No data available to plot yearly expenses.")
            return None

        # Ensure necessary columns are present and valid
        if 'amount_paid' not in df.columns:
            st.error("The 'amount_paid' column is missing from the data.")
            return None
        
        df['amount_paid'] = pd.to_numeric(df['amount_paid'], errors='coerce')

        if df['amount_paid'].isnull().all():
            st.warning("No valid data for yearly expenses.")
            return None

        yearly_expenses = df.groupby('category_name')['amount_paid'].sum()

        if yearly_expenses.empty:
            st.warning("No data available for yearly expenses.")
            return None

        # Dynamically set the report title
        st.markdown("### 📅 Yearly Expenses Overview")

        # Plot the chart
        if chart_type.lower() == "bar":
            plot_bar_chart(
                yearly_expenses,
                xlabel="Category",
                ylabel="Amount Paid",
                title="Yearly Expenses Overview"
            )
        elif chart_type.lower() == "pie":
            plot_pie_chart(yearly_expenses, title="Yearly Expenses Overview", chart_size=(6, 4))

        elif chart_type.lower() == "scatter":
            # Use the updated plot_scatter_chart function
            fig = plot_scatter_chart(df, x='category_name', y='amount_paid', title="Yearly Expense Scatter Plot")
            if fig:
                st.pyplot(fig)


        report_title = "Top 10 Annual Expenses"   
        self.download_csv(df, report_title)

    def download_csv(self, df, report_title):
        """Generate and provide a download button for the CSV."""
        if df.empty:
            st.warning("No data available to download as CSV.")
            return

        # Prepare CSV content
        csv_data = df.to_csv(index=False)


    def get_top_spending_categories(self, df):
        """Get the top 10 spending categories."""
        if df.empty:
            return pd.DataFrame(columns=['category_name', 'amount_paid'])
        
        if 'amount_paid' not in df.columns:
            st.error("The 'amount_paid' column is missing from the data.")
            return pd.DataFrame()

        df['amount_paid'] = pd.to_numeric(df['amount_paid'], errors='coerce')
        return df.groupby('category_name')['amount_paid'].sum().nlargest(10).reset_index()

    def display_expense_summary(self, df):
        """Display expense summary insights."""
        insights = get_insights(df)  # Using the refactored insights method

        st.write("### 📊 Expense Summary: Key Spending Insights")
        if insights['max_category'] == "No data available":
            st.warning("No data available for insights.")
        else:
            st.write(f"▲ **Max Spending:** {insights['max_category']} (${insights['max_amount']:.2f})")
            st.write(f"▼ **Min Spending:** {insights['min_category']} (${insights['min_amount']:.2f})")
