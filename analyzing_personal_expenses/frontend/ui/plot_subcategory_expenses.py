import pandas as pd
import streamlit as st
from backend.database.db_operations import DatabaseOperations
from frontend.ui.horizontal_bar_chart import plot_horizontal_bar_chart

class PlotSubcategoryExpenses:
    def __init__(self, user_id=None):
        """Initialize with user_id and default figure size."""
        self.user_id = user_id
        self.db_ops = DatabaseOperations()

    def fetch_and_plot(self, fetch_method, *args):
        """Fetch data using the provided method and plot the horizontal bar chart."""
        try:
            df = fetch_method(*args)
            if df.empty:
                st.warning("No subcategory expenses found for the provided parameters.")
                return
            plot_horizontal_bar_chart(df, args[-1], figsize=self.figsize)
        except Exception as e:
            st.error(f"Error fetching subcategory expenses: {e}")

    def display_subcategory_expenses_user_month(self, user_id, selected_month, category_name):
        """Display subcategory expenses chart for selected user, month, and category."""
        self.fetch_and_plot(self.db_ops.fetch_subcategory_user_monthly_expenses, user_id, selected_month, category_name)

    def display_subcategory_expenses_user_yearly(self, user_id, selected_year, category_name):
        """Display subcategory expenses chart for selected user and category for the year."""
        self.fetch_and_plot(self.db_ops.fetch_subcategory_user_expenses_yearly, user_id, selected_year, category_name)

    def display_subcategory_expenses_all_users_month(self, selected_month, category_name):
        """Display subcategory expenses chart for all users, month, and category."""
        self.fetch_and_plot(self.db_ops.fetch_subcategory_expenses_monthly_all_users, selected_month, category_name)

    def display_subcategory_expenses_all_users_yearly(self, selected_year, category_name):
        """Display subcategory expenses chart for all users and category for the year."""
        self.fetch_and_plot(self.db_ops.fetch_subcategory_expenses_yearly_all_users, selected_year, category_name)
   
    def plotbarh(self, df, category_name):
        """Create a horizontal bar chart for subcategory expenses."""
        if df is None or df.empty:
            st.warning("No data available to plot subcategory expenses.")
            return None

        subcategory_expenses = self.db_ops.fetch_expenses_by_category(category_name)
        if subcategory_expenses.empty:
            st.warning(f"No subcategory data available for the selected category: {category_name}")
            return None

        subcategory_expenses['total_amount'] = pd.to_numeric(subcategory_expenses['total_amount'], errors='coerce')
        subcategory_expenses = subcategory_expenses.dropna(subset=['total_amount'])

        if subcategory_expenses.empty:
            st.warning(f"No valid subcategory data to plot for {category_name}.")
            return None

        st.markdown(f"### 📊 Subcategory Expenses Breakdown for {category_name}")
        plot_horizontal_bar_chart(subcategory_expenses, category_name, figsize=self.figsize)
