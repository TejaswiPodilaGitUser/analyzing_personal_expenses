import pandas as pd
import streamlit as st
from frontend.ui.horizontal_bar_chart import plot_horizontal_bar_chart
from backend.database.db_operations import DatabaseOperations

class PlotSubcategoryExpenses:
    def __init__(self, user_id=None):
        """Initialize with user_id."""
        self.user_id = user_id
        self.db_ops = DatabaseOperations()

    def fetch_and_plot(self, df, selected_year=None, selected_month=None, category=None):
        """
        Plot the horizontal bar chart for subcategory expenses.

        Args:
            df (pd.DataFrame): Dataframe containing expense data.
            selected_year (str): Selected year.
            selected_month (str): Selected month.
            category (str): Selected category.
        """
        try:
            if df.empty:
                st.warning("No subcategory expenses found for the provided parameters.")
                return
            
            # Ensure 'total_amount' is numeric
            df = df.copy()  # Create a copy to avoid SettingWithCopyWarning
            df.loc[:, 'total_amount'] = pd.to_numeric(df['total_amount'], errors='coerce')
            df = df.dropna(subset=['total_amount'])

            if df.empty:
                st.warning("No valid subcategory data to plot.")
                return

            # Restrict to Top 10 Subcategories by total_amount
            df = df.sort_values(by='total_amount', ascending=True).head(10)

            # Plot Horizontal Bar Chart
            plot_horizontal_bar_chart(df, category)
        
        except Exception as e:
            st.error(f"Error plotting subcategory expenses: {e}")
