import streamlit as st
import pandas as pd
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from frontend.ui.export_data import save_as_csv, save_as_pdf, capture_screenshot
from frontend.ui.data_visualization import DataVisualization

st.set_page_config(layout="wide")

# Sidebar Selections with Defaults
st.sidebar.title("Choose Filters")

# Default User Selection
user_id = st.sidebar.selectbox(
    "Select User", 
    ["All Users", "User 1", "User 2", "Admin"], 
    index=0
)
user_map = {"All Users": None, "User 1": 1, "User 2": 2, "Admin": 3}
dv = DataVisualization(user_id=user_map[user_id])

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
    st.warning("No data available for the selected user.")
else:
    if visualization_type == "Monthly":
        # Month dropdown in sidebar
        selected_month = st.sidebar.selectbox(
            "Select Month", 
            ["January", "February", "March", "April", 
             "May", "June", "July", "August", 
             "September", "October", "November", "December"],
            index=0
        )
        
        # Ensure expense_date is parsed correctly and filter by month
        df['expense_month'] = pd.to_datetime(df['expense_date']).dt.strftime('%B')
        filtered_df = df[df['expense_month'] == selected_month]
        
        # Check if filtered data exists
        if filtered_df.empty:
            st.warning(f"No data available for the selected month: {selected_month}.")
        else:
            # Titles on the same line
            col1, col2 = st.columns(2)
            with col1:
                st.markdown(f"### 💰 Top 10 Spending Categories for {selected_month}")
            with col2:
                st.markdown(f"### Top Spending Categories For {selected_month}")
            
            # Display data and chart side by side
            col1, col2 = st.columns(2)
            with col1:
                top_10_df = dv.get_top_spending_categories(filtered_df)
                st.dataframe(top_10_df)
            
            with col2:
                dv.plot_monthly_expenses(filtered_df, selected_month, chart_type)

    elif visualization_type == "Yearly":
        # Titles on the same line
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("### 💰 Top 10 Yearly Expenses")
        with col2:
            st.markdown("### Annual Top 10 Spending Categories")
        
        # Display data and chart side by side
        col1, col2 = st.columns(2)
        with col1:
            top_10_df = dv.get_top_spending_categories(df)
            st.dataframe(top_10_df)
        
        with col2:
            dv.plot_yearly_expenses(df, chart_type)

    # Centered Data Insights Section
    st.markdown("---")  # Add a visual separator
    st.markdown(
        """
        <div style="text-align: center; margin-top: 20px;">
            <h3>📊 Expense Summary: Key Spending Insights</h3>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    insights = dv.get_insights(df)
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
    
    if export_option == "CSV":
        # Export only the top 10 data displayed
        filename = save_as_csv(top_10_df)
        st.sidebar.download_button("Download CSV", open(filename, "rb").read(), filename)
    elif export_option == "PDF":
        # Export only the top 10 data displayed
        filename = save_as_pdf(top_10_df)
        st.sidebar.download_button("Download PDF", open(filename, "rb").read(), filename)
    elif export_option == "Screenshot":
        # Capture the screenshot
        screenshot_path = capture_screenshot(filename="streamlit_screenshot.png")
        st.sidebar.download_button(
            label="Download Screenshot",
            data=open(screenshot_path, "rb").read(),
            file_name="streamlit_screenshot.png",
            mime="image/png"
        )
