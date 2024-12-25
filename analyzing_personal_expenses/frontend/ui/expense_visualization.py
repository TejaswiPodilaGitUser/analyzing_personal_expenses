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

    def handle_visualization(self, visualization_type, selected_month=None, chart_type="Pie"):
        """Handle visualization based on type and chart preference."""
        if visualization_type == "Monthly":
            self._visualize_monthly(selected_month, chart_type)
        elif visualization_type == "Yearly":
            self._visualize_yearly(chart_type)

    def _visualize_monthly(self, selected_month, chart_type):
        """Visualize monthly expenses."""
        df_month = self.df[self.df['expense_date'].dt.month_name() == selected_month]
        
        if df_month.empty:
            st.warning(f"No data available for the selected month: {selected_month}")
            return

        xlabel = 'Category'
        ylabel = 'Total Amount'
        title = f"Expenses for {selected_month}"

        if chart_type == "Pie":
            plot_pie_chart(df_month.groupby('category_name')['amount_paid'].sum(), title)
        elif chart_type == "Bar":
            plot_bar_chart(df_month.groupby('category_name')['amount_paid'].sum(), xlabel, ylabel, title)

    def _visualize_yearly(self, chart_type):
        """Visualize yearly expenses."""
        df_year = self.df.groupby(['category_name']).agg({'amount_paid': 'sum'}).reset_index()

        if df_year.empty:
            st.warning("No data available for yearly visualization.")
            return

        xlabel = 'Category'
        ylabel = 'Total Amount'
        title = "Yearly Expenses"

        if chart_type == "Pie":
            plot_pie_chart(df_year.set_index('category_name')['amount_paid'], title)
        elif chart_type == "Bar":
            plot_bar_chart(df_year.set_index('category_name')['amount_paid'], xlabel, ylabel, title)
