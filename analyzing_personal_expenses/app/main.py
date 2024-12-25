import streamlit as st
import pandas as pd
import sys
import os

# Add the parent directory to the system path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from frontend.ui.data_visualization import DataVisualization
from frontend.ui.export_data import ExportData
from backend.database.db_operations import DatabaseOperations
from static_expense_data import MONTHS, MESSAGES
import frontend.ui.sidebar as sidebar
from backend.analytics.data_insights import generate_insights


def main():
    """Main function to run the Expense Tracker Streamlit App."""
    # Set up page configuration
    st.set_page_config(layout="wide")

    # Initialize DatabaseOperations instance
    db_ops = DatabaseOperations()
    users = db_ops.fetch_users()

    # Sidebar: User and Filter Selections
    user_id, visualization_type, chart_type, selected_month = sidebar.display_sidebar(users)

    # Fetch User Data
    dv = DataVisualization(user_id=user_id)
    df = dv.get_user_expenses()

    if df.empty:
        st.warning(MESSAGES["no_user_data"])
        insights, top_10_df = {}, pd.DataFrame()
    else:
        # Handle Monthly Visualization
        if visualization_type == "Monthly":
            df['expense_month'] = pd.to_datetime(df['expense_date']).dt.strftime('%B')
            filtered_df = df[df['expense_month'] == selected_month]

            if filtered_df.empty:
                st.warning(MESSAGES["no_month_data"].format(month=selected_month))
                insights, top_10_df = {}, pd.DataFrame()
            else:
                col1, col2 = st.columns(2)
                with col1:
                    st.markdown(f"### 💰 Top 10 Spending Categories for {selected_month}")
                    top_10_df = dv.get_top_spending_categories(filtered_df)
                    st.dataframe(top_10_df)
                with col2:
                    dv.plot_monthly_expenses(filtered_df, selected_month, chart_type)
                insights = generate_insights(filtered_df)

        # Handle Yearly Visualization
        elif visualization_type == "Yearly":
            col1, col2 = st.columns(2)
            with col1:
                st.markdown("### 💰 Top 10 Yearly Expenses")
                top_10_df = dv.get_top_spending_categories(df)
                st.dataframe(top_10_df)
            with col2:
                dv.plot_yearly_expenses(df, chart_type)
            insights = generate_insights(df)

    # Display Insights
    st.markdown("---")
    st.markdown(
        f"""
        <div style="text-align: center; margin-top: 20px;">
            <h3>{MESSAGES["expense_summary_title"]}</h3>
        </div>
        """,
        unsafe_allow_html=True
    )

    if not insights:
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

    user_name = next((name for name, id in users.items() if id == user_id), "All Users")
    # Ensure the user_id and selected_month are passed correctly when initializing ExportData
    export_handler = ExportData(top_10_df, selected_month, user_name)
    export_handler.display()

if __name__ == "__main__":
    main()