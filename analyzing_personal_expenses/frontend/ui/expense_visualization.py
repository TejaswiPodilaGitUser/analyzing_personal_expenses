import streamlit as st
import pandas as pd
from frontend.ui.bar_chart import plot_bar_chart
from frontend.ui.pie_chart import plot_pie_chart

class ExpenseVisualization:
    def __init__(self, df):
        self.df = df
        # Convert 'expense_date' to datetime if it's not already in datetime format
        if not pd.api.types.is_datetime64_any_dtype(self.df['expense_date']):
            self.df['expense_date'] = pd.to_datetime(self.df['expense_date'])

    def handle_visualization(self, visualization_type, selected_month=None, chart_type="pie"):
        if visualization_type == "Monthly":
            self.visualize_monthly(selected_month, chart_type)
        elif visualization_type == "Yearly":
            self.visualize_yearly(chart_type)

    def visualize_monthly(self, selected_month, chart_type):
        # Filter the data by selected month
        df_month = self.df[self.df['expense_date'].dt.month_name() == selected_month]
        
        if df_month.empty:
            st.warning(f"No data available for the selected month: {selected_month}")
            return

        xlabel = 'Category'
        ylabel = 'Total Amount'
        title = f"Expenses for {selected_month}"

        if chart_type == "Pie":
            # Call the plot_pie_chart function with the required arguments
            plot_pie_chart(df_month, title)
        elif chart_type == "Bar":
            # Pass the required arguments to plot_bar_chart
            plot_bar_chart(df_month, xlabel, ylabel, title)

    def visualize_yearly(self, chart_type):
        # Group data by category for yearly data
        df_year = self.df.groupby(['category_name']).agg({'amount_paid': 'sum'}).reset_index()

        if df_year.empty:
            st.warning("No data available for the selected year.")
            return

        xlabel = 'Category'
        ylabel = 'Total Amount'
        title = "Yearly Expenses"

        if chart_type == "Pie":
            # Call the plot_pie_chart function with the required arguments
            plot_pie_chart(df_year, title)
        elif chart_type == "Bar":
            # Pass the required arguments to plot_bar_chart
            plot_bar_chart(df_year, xlabel, ylabel, title)
