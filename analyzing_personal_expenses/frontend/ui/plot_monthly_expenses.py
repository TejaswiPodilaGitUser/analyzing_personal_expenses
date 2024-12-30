import pandas as pd
import streamlit as st
from frontend.ui.bar_chart import plot_bar_chart
from frontend.ui.pie_chart import plot_pie_chart
from frontend.ui.line_chart import plot_line_chart
from frontend.ui.scatter_chart import plot_scatter_chart

class PlotMonthlyExpenses:
    def __init__(self):
        pass

    def plot(self, df, selected_year=None, selected_month="January", chart_type="pie", chart_size=(6, 4)):
        """Create bar and pie charts for monthly expenses."""
        if df.empty:
            st.warning("No data available to plot monthly expenses.")
            return None
        
        # Ensure necessary columns are present and valid
        if 'amount_paid' not in df.columns or 'expense_date' not in df.columns:
            st.error("Missing required columns: 'amount_paid' or 'expense_date'.")
            return None

        # Convert 'amount_paid' to numeric, invalid values will become NaN
        # Create a copy after filtering
        df = df.copy()

        # Convert 'amount_paid' to numeric, invalid values will become NaN
        df.loc[:, 'amount_paid'] = pd.to_numeric(df['amount_paid'], errors='coerce')


        # Drop rows with NaN in 'amount_paid' if necessary
        df = df.dropna(subset=['amount_paid'])

        # Convert 'expense_date' to datetime
        df['expense_date'] = pd.to_datetime(df['expense_date'], errors='coerce')
        
        # Extract year and month
        df['expense_year'] = df['expense_date'].dt.year
        df['expense_month'] = df['expense_date'].dt.strftime('%B')

        # Filter data for selected year and selected month
        if selected_year is not None:
            filtered_df = df[
                (df['expense_year'] == int(selected_year)) & 
                (df['expense_month'].str.lower() == selected_month.lower())
            ]
        else:
            filtered_df = df[df['expense_month'].str.lower() == selected_month.lower()]

        if filtered_df.empty:
            st.warning(f"No valid data for the selected year: {selected_year} and month: {selected_month}")
            return None
        
        # Group by category and sum up the expenses
        monthly_expenses = filtered_df.groupby('category_name')['amount_paid'].sum()

        if monthly_expenses.empty:
            st.warning(f"No grouped data available for the selected year: {selected_year} and month: {selected_month}")
            return None

        # Dynamically set the report title
        st.markdown(f"### 📊 Monthly Expenses Overview: {selected_month} {selected_year}")

        # Plot the chart based on selected chart type
        if chart_type.lower() == "bar":
            plot_bar_chart(
                monthly_expenses,
                xlabel="Category",
                ylabel="Amount Paid",
                title=f"Spending Categories - {selected_month} {selected_year}",
                chart_size=chart_size
            )
        elif chart_type.lower() == "pie":
            plot_pie_chart(
                monthly_expenses, 
                title=f"Spending Categories - {selected_month} {selected_year}", 
                chart_size=chart_size
            )
        elif chart_type.lower() == "line":
            plot_line_chart(
                monthly_expenses,
                xlabel="Category",
                ylabel="Amount Paid",
                title=f"Spending Categories - {selected_month} {selected_year}",
                chart_size=chart_size
            )
        elif chart_type.lower() == "scatter":
            plot_scatter_chart(
                monthly_expenses, 
                title=f"Monthly Expenses (Scatter Plot) - {selected_month} {selected_year}", 
                chart_size=(6, 4)
            )
        else:
            st.warning("Invalid chart type selected. Please choose 'Bar' or 'Pie'.")
