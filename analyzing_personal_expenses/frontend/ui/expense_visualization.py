import streamlit as st
import pandas as pd
from frontend.ui.bar_chart import plot_bar_chart
from frontend.ui.pie_chart import plot_pie_chart


class ExpenseVisualization:
    """Class to handle visualization of expense data."""

    def __init__(self, df):
        self.df = df.copy()
        if not pd.api.types.is_datetime64_any_dtype(self.df['expense_date']):
            self.df['expense_date'] = pd.to_datetime(self.df['expense_date'])

        # Add 'expense_year' and 'expense_month' columns for filtering later
        self.df['expense_year'] = self.df['expense_date'].dt.year
        self.df['expense_month'] = self.df['expense_date'].dt.month_name()

    def handle_visualization(self, visualization_type, selected_month=None, selected_year=None, chart_type="Pie"):
        """Handle visualization based on type and chart preference."""
        if visualization_type == "Monthly":
            self._visualize_monthly(selected_month, selected_year, chart_type)
        elif visualization_type == "Yearly":
            self._visualize_yearly(selected_year, chart_type)

    def _visualize_monthly(self, selected_month, selected_year, chart_type):
        """Visualize monthly expenses."""
        if not selected_month or not selected_year:
            st.warning("Please select both a month and year.")
            return

        # Filter data for the selected month and year
        df_month = self.df[(self.df['expense_month'] == selected_month) & (self.df['expense_year'] == selected_year)]

        if df_month.empty:
            st.warning(f"No data available for {selected_month} {selected_year}.")
            return

        xlabel = 'Category'
        ylabel = 'Total Amount'
        title = f"Expenses for {selected_month} {selected_year}"

        if chart_type == "Pie":
            plot_pie_chart(df_month.groupby('category_name')['amount_paid'].sum(), title)
        elif chart_type == "Bar":
            plot_bar_chart(df_month.groupby('category_name')['amount_paid'].sum(), xlabel, ylabel, title)

    def _visualize_yearly(self, selected_year, chart_type):
        """Visualize yearly expenses."""
        if not selected_year:
            st.warning("Please select a year.")
            return

        # Filter data for the selected year
        df_year = self.df[self.df['expense_year'] == selected_year].groupby(['category_name']).agg({'amount_paid': 'sum'}).reset_index()

        if df_year.empty:
            st.warning(f"No data available for {selected_year}.")
            return

        xlabel = 'Category'
        ylabel = 'Total Amount'
        title = f"Yearly Expenses for {selected_year}"

        if chart_type == "Pie":
            plot_pie_chart(df_year.set_index('category_name')['amount_paid'], title)
        elif chart_type == "Bar":
            plot_bar_chart(df_year.set_index('category_name')['amount_paid'], xlabel, ylabel, title)
