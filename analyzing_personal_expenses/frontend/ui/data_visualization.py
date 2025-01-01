import pandas as pd
import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt
from frontend.ui.plot_monthly_expenses import PlotMonthlyExpenses
from frontend.ui.plot_yearly_expenses import PlotYearlyExpenses
from frontend.ui.plot_subcategory_expenses import PlotSubcategoryExpenses
from frontend.ui.plot_data_insights import PlotDataInsights
from backend.database.db_operations import DatabaseOperations
#from frontend.ui.horizontal_bar_chart import plot_horizontal_bar_chart


class DataVisualization:
    def __init__(self, user_id=None):
        self.user_id = user_id
        self.db_ops = DatabaseOperations()
        self.plot_monthly = PlotMonthlyExpenses()
        self.plot_yearly = PlotYearlyExpenses()
        self.plot_subcategory = PlotSubcategoryExpenses()
        self.plot_insights = PlotDataInsights()

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

        df['total_amount'] = pd.to_numeric(df['total_amount'], errors='coerce')
        df = df.dropna(subset=['total_amount'])

        if df.empty:
            st.warning("No valid data after cleaning.")
            return pd.DataFrame()

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

            # Ensure that 'total_amount' is numeric
            if 'amount_paid' not in df.columns:
                st.warning("'amount_paid' column is missing from the data.")
                return pd.DataFrame()

            df['total_amount'] = pd.to_numeric(df['amount_paid'], errors='coerce')
            df = df.dropna(subset=['total_amount'])  # Drop rows where 'total_amount' is NaN

            if df.empty:
                st.warning("No valid data available after cleaning.")
                return pd.DataFrame()

            # Add year and month columns if needed
            if selected_year or selected_month:
                if 'expense_date' in df.columns:
                    df['expense_date'] = pd.to_datetime(df['expense_date'], errors='coerce')
                    df['expense_year'] = df['expense_date'].dt.year
                    df['expense_month'] = df['expense_date'].dt.strftime('%B')

            # Filter by year and month if specified
            if selected_year and selected_month:
                df = df[
                    (df['expense_year'] == int(selected_year)) &
                    (df['expense_month'].str.lower() == selected_month.lower())
                ]

            # Filter by category if specified
            if category and category != "All Categories":
                df = df[df['category_name'] == category]

            # Aggregate by 'subcategory_name' using 'total_amount'
            subcategory_df = df.groupby('subcategory_name', as_index=False).agg(
                total_amount=('total_amount', 'sum')
            )

            # Check if the aggregation is successful
            if subcategory_df.empty or 'total_amount' not in subcategory_df.columns:
               # st.warning("No valid subcategory data available after aggregation.")
                return pd.DataFrame()

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
            subcategory_df = df;

            if not subcategory_df.empty:
                # Use fetch_and_plot to display the subcategory chart
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
