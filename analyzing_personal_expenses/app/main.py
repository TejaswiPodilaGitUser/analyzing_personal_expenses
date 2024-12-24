import streamlit as st
import pandas as pd
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from frontend.ui.data_visualization import DataVisualization
from frontend.ui.export_data import save_as_csv, save_as_pdf, capture_screenshot
from backend.database.db_operations import DatabaseOperations
from static_expense_data import MONTHS, MESSAGES  # Import static data

def main():
    # Set up page configuration
    st.set_page_config(layout="wide")

    # Initialize DatabaseOperations instance
    db_ops = DatabaseOperations()

    # Fetch users dynamically from the database
    users = db_ops.fetch_users()

    # Sidebar Selections with Defaults
    st.sidebar.title("Choose Filters")

    # Default User Selection
    user_name = st.sidebar.selectbox(
        "Select User", 
        ["All Users"] + list(users.keys()),  
        index=0
    )

    user_id = None if user_name == "All Users" else users[user_name]

    # Initialize DataVisualization instance with user_id
    dv = DataVisualization(user_id=user_id)

    # Default Visualization Type
    visualization_type = st.sidebar.selectbox(
        "Select Visualization Type", 
        ["Yearly", "Monthly"], 
        index=0
    )

    # Default Chart Type
    chart_type = st.sidebar.selectbox(
        "Select Chart Type", 
        ["Pie", "Bar"], 
        index=0
    )

    # Fetch user expenses
    df = dv.get_user_expenses()

    # Handle case when no data is available
    if df.empty:
        st.warning(MESSAGES["no_user_data"])
        insights = {
            "max_category": MESSAGES["no_insights"],
            "max_amount": MESSAGES["no_insights"],
            "min_category": MESSAGES["no_insights"],
            "min_amount": MESSAGES["no_insights"]
        }
        top_10_df = pd.DataFrame()
    else:
        selected_month = None
        top_10_df = None

        if visualization_type == "Monthly":
            # Month dropdown in sidebar
            selected_month = st.sidebar.selectbox(
                "Select Month", 
                MONTHS,
                index=0
            )
            
            # Ensure expense_date is parsed correctly and filter by month if selected
            df['expense_month'] = pd.to_datetime(df['expense_date']).dt.strftime('%B')
            filtered_df = df[df['expense_month'] == selected_month]
            
            if filtered_df.empty:
                st.warning(MESSAGES["no_month_data"].format(month=selected_month))
                insights = {
                    "max_category": MESSAGES["no_insights"],
                    "max_amount": MESSAGES["no_insights"],
                    "min_category": MESSAGES["no_insights"],
                    "min_amount": MESSAGES["no_insights"]
                }
                top_10_df = pd.DataFrame()
            else:
                col1, col2 = st.columns(2)
                with col1:
                    st.markdown(f"### 💰 Top 10 Spending Categories for {selected_month}")
                with col2:
                    st.markdown(f"### Top Spending Categories For {selected_month}")
                
                col1, col2 = st.columns(2)
                with col1:
                    top_10_df = dv.get_top_spending_categories(filtered_df)
                    st.dataframe(top_10_df)
                
                with col2:
                    dv.plot_monthly_expenses(filtered_df, selected_month, chart_type)
                
                insights = dv.get_insights(filtered_df)

        elif visualization_type == "Yearly":
            col1, col2 = st.columns(2)
            with col1:
                st.markdown(f"### 💰 Top 10 Yearly Expenses for {user_name}")
            with col2:
                st.markdown(f"### Annual Top 10 Spending Categories - {user_name}")
            
            col1, col2 = st.columns(2)
            with col1:
                top_10_df = dv.get_top_spending_categories(df)
                st.dataframe(top_10_df)
            
            with col2:
                dv.plot_yearly_expenses(df, chart_type)
            
            insights = dv.get_insights(df)

    # Centered Data Insights Section
    st.markdown("---")
    st.markdown(
        f"""
        <div style="text-align: center; margin-top: 20px;">
            <h3>{MESSAGES["expense_summary_title"]}</h3>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    if insights['max_category'] == MESSAGES["no_insights"]:
        st.warning(MESSAGES["no_insights"])
    else:
        st.markdown(
            f"""
            <div style="text-align: center;">
                <p><strong>▲ Max Spending:</strong> {insights['max_category']} (${insights['max_amount']:.2f})</p>
                <p><strong>▼ Min Spending:</strong> {insights['min_category']} (${insights['min_amount']:.2f})</p>
            </div>
            """,
            unsafe_allow_html=True
        )

    # Export options only after visualization
    st.sidebar.title("Export Data")
    export_option = st.sidebar.selectbox("Select Export Option", ["CSV", "PDF", "Screenshot"], index=0)
    
    if top_10_df is not None and not top_10_df.empty:
        if export_option == "CSV":
            filename = save_as_csv(top_10_df, user_name=user_name, selected_month=selected_month)
            st.sidebar.download_button("Download CSV", open(filename, "rb").read(), filename)
  
        elif export_option == "PDF":
            filename = save_as_pdf(top_10_df)
            st.sidebar.download_button("Download PDF", open(filename, "rb").read(), filename)
            
        elif export_option == "Screenshot":
            screenshot_path = capture_screenshot(filename="streamlit_screenshot.png")
            st.sidebar.download_button(
                label="Download Screenshot",
                data=open(screenshot_path, "rb").read(),
                file_name="streamlit_screenshot.png"
            )
    else:
        st.warning(MESSAGES["no_export_data"])


if __name__ == "__main__":
    main()
