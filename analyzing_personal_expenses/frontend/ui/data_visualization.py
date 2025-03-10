import pandas as pd
import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt
from frontend.ui.plot_monthly_expenses import PlotMonthlyExpenses
from frontend.ui.plot_yearly_expenses import PlotYearlyExpenses
from frontend.ui.plot_subcategory_expenses import PlotSubcategoryExpenses
from frontend.ui.plot_data_insights import PlotDataInsights
from backend.database.db_operations import DatabaseOperations
from backend.data_cleaner import DataCleaner

class DataVisualization:
    def __init__(self, user_id=None, df=None):
        self.user_id = user_id
        self.db_ops = DatabaseOperations()
        self.plot_monthly = PlotMonthlyExpenses()
        self.plot_yearly = PlotYearlyExpenses()
        self.plot_subcategory = PlotSubcategoryExpenses()
        self.plot_insights = PlotDataInsights()
    
        # Data cleaning is handled here only if df is provided
        if df is not None:
            self.data_cleaner = DataCleaner(df)

    def get_user_expenses(self, user_id='ALL Users', selected_year=None, selected_month=None):
        """Fetch user expenses."""
        try:
            df = self.db_ops.generate_expense_query(
                user_id=self.user_id,
                selected_year=selected_year,
                selected_month=selected_month
            )

            if df.empty:
                raise ValueError("No expenses found for the selected user and period.")
            
            # Clean data using DataCleaner if it is initialized
            if hasattr(self, 'data_cleaner'):
                df = self.data_cleaner.clean_data(df)
            return df
        except Exception as e:
            print(f"Error fetching expenses: {e}")
            return pd.DataFrame()

    def display_monthly_expenses(self, df, selected_year=None, selected_month=None, chart_type="pie"):
        """Display monthly expenses chart filtered by year and month."""
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
            return pd.DataFrame(columns=['category_name', 'total_amount'])

        df['total_amount'] = pd.to_numeric(df['total_amount'], errors='coerce').fillna(0)
        if selected_year and selected_month:
            df['expense_date'] = pd.to_datetime(df['expense_date'], errors='coerce')
            df['expense_year'] = df['expense_date'].dt.year
            df['expense_month'] = df['expense_date'].dt.strftime('%B')

            filtered_df = df[
                (df['expense_year'] == int(selected_year)) &
                (df['expense_month'].str.lower() == selected_month.lower())
            ]
        else:
            filtered_df = df

        return filtered_df.groupby('category_name')['total_amount'].sum().nlargest(10).reset_index()
    
    def get_user_expenses_by_subcategory(self, df, user_id=None, selected_year=None, selected_month=None, category=None):
        """
        Fetch subcategory-level expenses, aggregated by 'subcategory_name' with 'total_amount'.
        """
        try:
            if df.empty:
                st.warning("No data available for the selected filters.")
                return pd.DataFrame()

            if 'amount_paid' not in df.columns:
                st.warning("'amount_paid' column is missing from the data.")
                return pd.DataFrame()

            # Normalize the 'total_amount'
            df['total_amount'] = pd.to_numeric(df['amount_paid'], errors='coerce').fillna(0)

            # Filter by year and month if provided
            if selected_year or selected_month:
                if 'expense_date' in df.columns:
                    df['expense_date'] = pd.to_datetime(df['expense_date'], errors='coerce')
                    df['expense_year'] = df['expense_date'].dt.year
                    df['expense_month'] = df['expense_date'].dt.strftime('%B')

            if selected_year and selected_month:
                df = df[
                    (df['expense_year'] == int(selected_year)) &
                    (df['expense_month'].str.lower() == selected_month.lower())
                ]

            # Apply category filter only if a specific category is selected
            if category and category != "All Categories":
                category = category.strip().lower()
                df = df[df['category_name'].str.strip().str.lower() == category]

            # Group by 'subcategory_name' and sum 'total_amount'
            subcategory_df = df.groupby('subcategory_name', as_index=False).agg(
                total_amount=('total_amount', 'sum')
            )
            return subcategory_df

        except Exception as e:
            st.error(f"Error fetching subcategory expenses: {e}")
            return pd.DataFrame()


    def display_subcategory_expenses(self, df, selected_year=None, selected_month=None, category=None):
        """
        Display subcategory expenses as a chart.
        """
        if df.empty:
            st.warning("No data available for subcategory expenses chart.")
            return

        try:
            subcategory_df = df

            if not subcategory_df.empty:
                self.plot_subcategory.fetch_and_plot(
                    subcategory_df,
                    selected_year=selected_year,
                    selected_month=selected_month,
                    category=category
                )
            else:
                st.warning("No valid subcategory data available to display.")
        except Exception as e:
            st.error(f"Error displaying subcategory expenses: {e}")


    def get_payment_mode_count(self, df, selected_year=None, selected_month=None, category=None):
        """Fetch the count of different payment modes."""
        try:
            # Clean the data
            df['payment_mode_name'] = df['payment_mode_name'].str.strip()

            # Filter by selected year and month if provided
            if selected_year or selected_month:
                df['expense_date'] = pd.to_datetime(df['expense_date'], errors='coerce')
                df['expense_year'] = df['expense_date'].dt.year
                df['expense_month'] = df['expense_date'].dt.strftime('%B')

            if selected_year and selected_month:
                df = df[
                    (df['expense_year'] == int(selected_year)) &
                    (df['expense_month'].str.lower() == selected_month.lower())
                ]

            if category and category != "All Categories":
                category = category.strip().lower()
                df = df[df['category_name'].str.strip().str.lower() == category]

            # Group by 'payment_mode' and count occurrences
            payment_mode_count = df['payment_mode_name'].value_counts().reset_index()
            payment_mode_count.columns = ['payment_mode_name', 'count']

            return payment_mode_count
        except Exception as e:
            print(f"Error fetching payment mode count: {e}")
            return pd.DataFrame()
