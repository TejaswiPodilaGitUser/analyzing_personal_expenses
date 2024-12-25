import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
from frontend.ui.bar_chart import plot_bar_chart
from frontend.ui.pie_chart import plot_pie_chart
from backend.database.db_operations import DatabaseOperations
from io import StringIO

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
        
        df['expense_date'] = pd.to_datetime(df['expense_date'], errors='coerce')
        df['expense_month'] = df['expense_date'].dt.strftime('%B')

        if 'amount_paid' not in df.columns:
            st.error("The 'amount_paid' column is missing from the data.")
            return None
        
        filtered_df = df[df['expense_month'] == selected_month]
        filtered_df['amount_paid'] = pd.to_numeric(filtered_df['amount_paid'], errors='coerce')
        
        if filtered_df['amount_paid'].isnull().all():
            st.warning(f"No valid data for the selected month: {selected_month}")
            return None
        
        monthly_expenses = filtered_df.groupby('category_name')['amount_paid'].sum()

        if monthly_expenses.empty:
            st.warning(f"No data available for the selected month: {selected_month}")
            return None

        # Add heading dynamically based on chart type
        st.markdown(f"### 📅 Monthly Expenses Overview: {selected_month}")

        if chart_type.lower() == "bar":
            plot_bar_chart(
                monthly_expenses,
                xlabel="Category",
                ylabel="Amount Paid",
                title=f"Spending Categories - {selected_month}"
            )
        elif chart_type.lower() == "pie":
            plot_pie_chart(
                monthly_expenses,
                title=f"Spending Categories - {selected_month}"
            )
        
        # Set the title for CSV download
        report_title = f"User {self.user_id} - {selected_month} Top 10 Expenses"
        self.download_csv(filtered_df, report_title)

    def plot_yearly_expenses(self, df, chart_type="pie"):
        """Create bar and pie charts for yearly expenses."""
        if df.empty:
            st.warning("No data available to plot yearly expenses.")
            return None

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

        # Add heading dynamically based on chart type
        st.markdown("### 📅 Yearly Expenses Overview")

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
                title="Yearly Expenses Overview"
            )
        
        # Set the title for CSV download
        report_title = "All Users Top 10 Expenses"
        self.download_csv(df, report_title)

    def download_csv(self, df, report_title):
        """Generate and provide a download button for the CSV."""
        # Prepare CSV content
        csv_data = df.to_csv(index=False)
        
        # Format the file name without underscores
        formatted_report_title = report_title.replace("_", " ")

        # Add CSV download button
        st.download_button(
            label="Download CSV",
            data=csv_data,
            file_name=f"{formatted_report_title}.csv",
            mime="text/csv"
        )

    def get_top_spending_categories(self, df):
        """Get the top 10 spending categories."""
        if df.empty:
            return pd.DataFrame(columns=['category_name', 'amount_paid'])
        
        if 'amount_paid' not in df.columns:
            st.error("The 'amount_paid' column is missing from the data.")
            return pd.DataFrame()

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
            st.error("The 'amount_paid' column is missing from the data.")
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

    def display_expense_summary(self, df):
        """Display expense summary insights."""
        insights = self.get_insights(df)

        st.write("### 📊 Expense Summary: Key Spending Insights")
        if insights['max_category'] == "No data available":
            st.warning("No data available for insights.")
        else:
            st.write(f"▲ **Max Spending:** {insights['max_category']} (${insights['max_amount']:.2f})")
            st.write(f"▼ **Min Spending:** {insights['min_category']} (${insights['min_amount']:.2f})")
