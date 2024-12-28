import streamlit as st
import pandas as pd
import sys
import os

# Add the parent directory to the system path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from frontend.ui.data_visualization import DataVisualization
from frontend.ui.export_data import ExportData
from backend.database.db_operations import DatabaseOperations
from utils.static_expense_data import MONTHS, MESSAGES
import frontend.ui.sidebar as sidebar
from frontend.ui.data_insights import get_insights

def main():
    """Main function to run the Expense Tracker Streamlit App."""
    st.set_page_config(layout="wide")

    # Initialize default variables
    insights = {}
    top_10_df = pd.DataFrame()

    # Initialize DatabaseOperations instance
    db_ops = DatabaseOperations()
    users = db_ops.fetch_users()

    # Sidebar: User and Filter Selections
    user_id, visualization_type, chart_type, selected_month, selected_year, detailed_view_category = sidebar.display_sidebar(users)

    # Fetch User Data for the year
    dv = DataVisualization(user_id=user_id)
    df = dv.get_user_expenses()

    if df.empty:
        st.warning(MESSAGES["no_user_data"])
        return

    df['expense_date'] = pd.to_datetime(df['expense_date'], errors='coerce')
    df['expense_year'] = df['expense_date'].dt.year
    df['expense_month'] = df['expense_date'].dt.strftime('%B')

    # Monthly Visualization
    if visualization_type == "Monthly":
        selected_year = selected_year or st.selectbox("Select Year", sorted(df['expense_year'].unique()), key="year")
        selected_month = selected_month or st.selectbox("Select Month", MONTHS, key="month")
        
        # Ensure filtering with month name (string)
        filtered_df = df[(df['expense_month'] == selected_month) & (df['expense_year'] == int(selected_year))]

        if filtered_df.empty:
            st.warning(MESSAGES["no_month_data"].format(month=selected_month, year=selected_year))
        else:
            st.markdown(f"## 📊 Monthly Expenses Overview for {selected_month} {selected_year}")
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("### 💰 Top 10 Spending Categories")
                # Select only the relevant columns for display and remove date-related columns
                top_10_df = filtered_df[['category_name', 'amount_paid']].nlargest(10, 'amount_paid')
                st.dataframe(top_10_df)
            
            with col2:
                if chart_type in ['Bar', 'Pie']:
                    selected_month_name = selected_month
                    dv.display_monthly_expenses(filtered_df, selected_year, selected_month_name, chart_type)
                else:
                    st.warning("Invalid chart type selected. Please choose Bar, Pie.")
            insights = get_insights(filtered_df, selected_year, selected_month)

    # Yearly Visualization
    elif visualization_type == "Yearly":
        selected_year = selected_year or st.selectbox("Select Year", sorted(df['expense_year'].unique()), key="year")
        filtered_df = df[df['expense_year'] == int(selected_year)]
        
        if filtered_df.empty:
            st.warning(MESSAGES["no_year_data"].format(year=selected_year))
        else:
            st.markdown(f"## 📊 Yearly Expenses Overview for {selected_year}")
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("### 💰 Top 10 Yearly Expenses")
                # Select only the relevant columns for display and remove date-related columns
                top_10_df = filtered_df[['category_name', 'amount_paid']].nlargest(10, 'amount_paid')
                st.dataframe(top_10_df)
            
            with col2:
                dv.display_yearly_expenses(filtered_df, selected_year, chart_type)
            
            insights = get_insights(filtered_df, selected_year)

    # Display Subcategory Breakdown
    if detailed_view_category:
        if visualization_type == "Monthly":
            dv.plot_subcategory.display_subcategory_expenses_user_month(user_id, selected_month, detailed_view_category)
        elif visualization_type == "Yearly":
            dv.plot_subcategory.display_subcategory_expenses_user_yearly(user_id, selected_year, detailed_view_category)

    # Display Insights
    st.markdown("---")
    st.markdown(f"""
        <div style="text-align: center; margin-top: 20px;">
            <h3>{MESSAGES["expense_summary_title"]}</h3>
        </div>
        """, unsafe_allow_html=True)

    if not insights:
        st.warning(MESSAGES["no_insights"])
    else:
        # Ensure max_amount and min_amount are numeric
        max_amount = insights.get('max_amount', 0.0)
        min_amount = insights.get('min_amount', 0.0)

        if pd.isna(max_amount) or max_amount == "No data available":
            max_amount = 0.0
        if pd.isna(min_amount) or min_amount == "No data available":
            min_amount = 0.0

        st.markdown(f"""
            <div style="text-align: center;">
                <p><strong>▲ Max Spending:</strong> {insights.get('max_category', 'N/A')} (${max_amount:.2f})</p>
                <p><strong>▼ Min Spending:</strong> {insights.get('min_category', 'N/A')} (${min_amount:.2f})</p>
    </div>
""", unsafe_allow_html=True)


if __name__ == "__main__":
    main()
