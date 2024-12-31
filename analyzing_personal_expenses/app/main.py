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
from scripts.static_data import CHART_TYPES

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
    df = dv.get_user_expenses(selected_year=selected_year, selected_month=selected_month)

    if df.empty:
        st.warning(MESSAGES["no_user_data"])
        return

    df['expense_date'] = pd.to_datetime(df['expense_date'], errors='coerce')
    df['expense_year'] = df['expense_date'].dt.year
    df['expense_month'] = df['expense_date'].dt.strftime('%B')

    # Initialize subcategory_df as an empty DataFrame
    subcategory_df = pd.DataFrame()

    # Monthly Visualization
    if visualization_type == "Monthly":
        selected_year = selected_year or st.selectbox("Select Year", sorted(df['expense_year'].unique()), key="year")
        selected_month = selected_month or st.selectbox("Select Month", MONTHS, key="month")
        
        # Ensure filtering with month name (string)
        filtered_df = df[(df['expense_month'] == selected_month) & (df['expense_year'] == int(selected_year))]

        #print("Filtered_df :", filtered_df)

        if filtered_df.empty:
            st.warning(MESSAGES["no_month_data"].format(month=selected_month, year=selected_year))
        else:
            st.markdown(f"## 📊 Monthly Expenses Overview for {selected_month} {selected_year}")
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("### 💰 Top 10 Spending Categories")
                # Select only the relevant columns for display and remove date-related columns
                # Aggregate amount_paid by category
                top_10_df = (filtered_df
                         .groupby('category_name', as_index=False)
                         .agg(total_amount=('amount_paid', 'sum'))
                         .nlargest(10, 'total_amount'))
               # print("Top 10 df: ", top_10_df)
                st.dataframe(top_10_df)
            
            with col2:
                if chart_type in CHART_TYPES:
                    selected_month_name = selected_month
                    dv.display_monthly_expenses(filtered_df, selected_year, selected_month_name, chart_type)
                else:
                   st.warning(f"Invalid chart type selected: {chart_type}")

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
                # Aggregate amount_paid by category
                top_10_df = (filtered_df
                         .groupby('category_name', as_index=False)
                         .agg(total_amount=('amount_paid', 'sum'))
                         .nlargest(10, 'total_amount'))
                st.dataframe(top_10_df)
            
            with col2:
                dv.display_yearly_expenses(filtered_df, selected_year, chart_type)
            
            insights = get_insights(filtered_df, selected_year)

    # Sub Category Bar chart if a category is selected
    # Subcategory Visualization
    # Subcategory Visualization for selected category from dropdown
    if detailed_view_category:
        print("In main.py- detailed_view_category ", detailed_view_category)
        print("In main.py- top_10_df ", top_10_df)

        # Create a dropdown to select a category from all available categories
        available_categories = top_10_df['category_name'].unique().tolist()  # Or fetch from all categories
        
        # If detailed_view_category is not set, default to "All Categories"
        selected_category = detailed_view_category if detailed_view_category else "All Categories"

        print("In main.py- selected_category ", selected_category)
        print("In main.py- available_categories ", available_categories)

        # If category is "All Categories", fetch data for all categories
        # Fetch subcategory data for a specific category and year/month
        # Ensure subcategory_df is fetched with proper filters
        # Fetch updated subcategory data
        subcategory_df = dv.get_user_expenses_by_subcategory(
            user_id=user_id,
            selected_year=selected_year,
            selected_month=selected_month,
            category=selected_category
        )

        # Check structure
        print("Subcategory DataFrame Columns:", subcategory_df.columns)
        print("Subcategory DataFrame Head:", subcategory_df.head())

        # Validate category totals
        if 'category_name' in subcategory_df.columns and 'total_amount' in subcategory_df.columns:
            subcategory_totals = subcategory_df.groupby('category_name')['total_amount'].sum().reset_index()
            top_10_totals = top_10_df.groupby('category_name')['total_amount'].sum().reset_index()
            
            print("Validating Totals Between Subcategory and Top 10 DataFrames")
            print("Subcategory Totals:\n", subcategory_totals)
            print("Top 10 Totals:\n", top_10_totals)
            
            if not subcategory_totals.equals(top_10_totals):
                print("🚨 **Discrepancy Detected! Totals do not match.**")
            else:
                print("✅ **Totals Match Successfully!**")
        else:
            print("⚠️ **Required columns are missing in subcategory_df or top_10_df.**")

        # Display Subcategory Data
        if not subcategory_df.empty:
            st.markdown(f"### 📊 Subcategory Expenses Overview for {selected_category}")
            col1, col2 = st.columns([1, 1])
            with col1:
                dv.display_subcategory_expenses(subcategory_df, selected_year, selected_month, selected_category)
            with col2:
                st.dataframe(subcategory_df)
        else:
            st.warning(MESSAGES["no_subcategory_data"].format(category=selected_category))


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
