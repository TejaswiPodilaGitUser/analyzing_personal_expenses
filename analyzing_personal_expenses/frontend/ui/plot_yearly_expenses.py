import pandas as pd
import streamlit as st
from frontend.ui.bar_chart import plot_bar_chart
from frontend.ui.pie_chart import plot_pie_chart


class PlotYearlyExpenses:
    def __init__(self):
        pass

    def plot(self, df, selected_year="2025", chart_type="pie", chart_size=(8, 5)):
        """Create bar and pie charts for yearly expenses."""
        if df.empty:
            st.warning("No data available to plot yearly expenses.")
            return None

        # Ensure 'expense_date' is in datetime format
        df.loc[:, 'expense_date'] = pd.to_datetime(df['expense_date'], errors='coerce')

        # Check for rows where 'expense_date' is NaT after conversion
        if df['expense_date'].isnull().all():
            st.error("All 'expense_date' values are invalid or missing.")
            return None

        # Filter data for the selected year
        try:
            df = df[df['expense_date'].dt.year == int(selected_year)]
        except AttributeError:
            st.error("The 'expense_date' column is not in the correct datetime format.")
            return None

        if df.empty:
            st.warning(f"No data available for the year {selected_year}.")
            return None

        # Ensure necessary columns are present and valid
        if 'amount_paid' not in df.columns:
            st.error("The 'amount_paid' column is missing from the data.")
            return None
        
        # Convert 'amount_paid' to numeric, invalid values will become NaN
        df.loc[:, 'amount_paid'] = pd.to_numeric(df['amount_paid'], errors='coerce')

        # Drop rows with NaN in 'amount_paid' if necessary
        df = df.dropna(subset=['amount_paid'])

        if df['amount_paid'].isnull().all():
            st.warning("No valid data for yearly expenses.")
            return None

        yearly_expenses = df.groupby('category_name')['amount_paid'].sum()

        if yearly_expenses.empty:
            st.warning("No data available for yearly expenses.")
            return None

        # Dynamically set the report title
        st.markdown(f"### 📅 Yearly Expenses Overview for {selected_year}")

        # Plot the chart based on selected chart type
        if chart_type.lower() == "bar":
            plot_bar_chart(
                yearly_expenses,
                xlabel="Expense Categories",
                ylabel="Amount Paid ($)",
                title=f"Yearly Expenses for {selected_year}",
                chart_size=chart_size
            )
        elif chart_type.lower() == "pie":
            plot_pie_chart(
                yearly_expenses,
                title=f"Yearly Expenses for {selected_year}",
                chart_size=chart_size
            )
        else:
            st.error(f"Unsupported chart type: {chart_type}")