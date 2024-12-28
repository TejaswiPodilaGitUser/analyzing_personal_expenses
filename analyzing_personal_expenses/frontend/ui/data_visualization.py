import pandas as pd
import streamlit as st
from frontend.ui.plot_monthly_expenses import PlotMonthlyExpenses
from frontend.ui.plot_yearly_expenses import PlotYearlyExpenses
from frontend.ui.plot_subcategory_expenses import PlotSubcategoryExpenses
from frontend.ui.plot_data_insights import PlotDataInsights
from backend.database.db_operations import DatabaseOperations
from frontend.ui.horizontal_bar_chart import plot_horizontal_bar_chart

class DataVisualization:
    def __init__(self, user_id=None):
        self.user_id = user_id
        self.db_ops = DatabaseOperations()
        self.plot_monthly = PlotMonthlyExpenses()
        self.plot_yearly = PlotYearlyExpenses()
        self.plot_subcategory = PlotSubcategoryExpenses(user_id=self.user_id)
        self.plot_insights = PlotDataInsights()

    def get_user_expenses(self, selected_year=None, selected_month=None):
        """Fetch user expenses from the database filtered by year and month."""
        try:
            df = self.db_ops.fetch_user_expenses(self.user_id, selected_year, selected_month)

            if df.empty:
                raise ValueError("No expenses found for the selected user and period.")
            return df
        except Exception as e:
            print(f"Error fetching expenses: {e}")
            return pd.DataFrame()
        

    def display_monthly_expenses(self, df, selected_year=None, selected_month=None, chart_type="pie"):
        """Display monthly expenses chart filtered by year and month."""
        # Ensure the month parameter is numeric and properly passed
        self.plot_monthly.plot(df, selected_year=selected_year, selected_month=selected_month, chart_type=chart_type)


    def display_yearly_expenses(self, df, selected_year="2025", chart_type="pie"):
        """Display yearly expenses chart."""
        self.plot_yearly.plot(df, selected_year=selected_year, chart_type=chart_type)

    def display_data_insights(self, df):
        """Display data insights."""
        self.plot_insights.display(df)

    def get_top_spending_categories(self, df, selected_year=None, selected_month=None):
        """Get the top 10 spending categories filtered by year and month."""
        if df.empty:
            return pd.DataFrame(columns=['category_name', 'amount_paid'])

        # Ensure 'amount_paid' is numeric, coercing errors to NaN
        df.loc[:, 'amount_paid'] = pd.to_numeric(df['amount_paid'], errors='coerce')

        # Drop rows where 'amount_paid' is NaN
        df = df.dropna(subset=['amount_paid'])

        # Check if the 'amount_paid' column is numeric
        if df['amount_paid'].dtype not in ['float64', 'int64']:
            st.error("The 'amount_paid' column is not numeric. Please check the data.")
            return pd.DataFrame()

        # If both selected year and month are provided, filter data for that period
        if selected_year and selected_month:
            df['expense_date'] = pd.to_datetime(df['expense_date'], errors='coerce')
            df['expense_year'] = df['expense_date'].dt.year
            df['expense_month'] = df['expense_date'].dt.strftime('%B')

            filtered_df = df[(df['expense_year'] == selected_year) & (df['expense_month'].str.lower() == selected_month.lower())]
        else:
            filtered_df = df

        # Return the top 10 categories by total 'amount_paid'
        return filtered_df.groupby('category_name')['amount_paid'].sum().nlargest(10).reset_index()
