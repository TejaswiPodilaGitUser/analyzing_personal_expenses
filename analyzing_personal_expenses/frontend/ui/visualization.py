import streamlit as st
import pandas as pd
from frontend.ui.data_visualization import DataVisualization
from utils.static_expense_data import MONTHS, YEARS, MESSAGES

class Visualization:
    def __init__(self, user_id):
        self.dv = DataVisualization(user_id=user_id)

    def get_user_expenses(self):
        return self.dv.get_user_expenses()

    def display_monthly_view(self, df, chart_type):
        """Display monthly view with selected month and chart type."""
        
        # Month dropdown in sidebar using MONTHS from static_expenses.py
        selected_month = st.sidebar.selectbox(
            "Select Month", 
            MONTHS,
            index=0
        )
        
        # Ensure expense_date is parsed correctly and filter by month
        df['expense_month'] = pd.to_datetime(df['expense_date']).dt.strftime('%B')
        filtered_df = df[df['expense_month'] == selected_month]
        
        # Check if filtered data exists
        if filtered_df.empty:
            st.warning(MESSAGES["no_month_data"].format(month=selected_month))
        else:
            # Titles on the same line
            col1, col2 = st.columns(2)
            with col1:
                st.markdown(f"#### 💰 Top 10 Spending Categories for {selected_month}")
            with col2:
                st.markdown(f"### Top Spending Categories For {selected_month}")
            
            # Display data and chart side by side
            col1, col2 = st.columns(2)
            with col1:
                top_10_df = self.dv.get_top_spending_categories(filtered_df)
                st.dataframe(top_10_df)
            
            with col2:
                self.dv.plot_monthly_expenses(filtered_df, selected_month, chart_type)

    def display_yearly_view(self, df, chart_type):
        """Display yearly view with selected year and chart type."""
        
        # Year dropdown in sidebar using YEARS from static_expenses.py
        selected_year = st.sidebar.selectbox(
            "Select Year", 
            YEARS,
            index=0
        )

        # Ensure expense_date is parsed correctly and filter by year
        df['expense_year'] = pd.to_datetime(df['expense_date']).dt.year
        filtered_df = df[df['expense_year'] == int(selected_year)]
        
        # Check if filtered data exists
        if filtered_df.empty:
            st.warning(f"No data available for the selected year: {selected_year}.")
        else:
            # Titles on the same line
            col1, col2 = st.columns(2)
            with col1:
                st.markdown("#### 💰 Top 10 Yearly Expenses")
            with col2:
                st.markdown("#### Annual Top 10 Spending Categories")
            
            # Display data and chart side by side
            col1, col2 = st.columns(2)
            with col1:
                top_10_df = self.dv.get_top_spending_categories(filtered_df)
                st.dataframe(top_10_df)
            
            with col2:
                self.dv.plot_yearly_expenses(filtered_df, chart_type)
