import streamlit as st
from static_expense_data import MONTHS

def display_sidebar(users):
    """
    Display the sidebar with user filters and return selected values.

    Args:
        users (dict): Dictionary of user names and IDs fetched from the database.

    Returns:
        tuple: user_id, visualization_type, chart_type, selected_month
    """
    st.sidebar.title("Choose Filters")

    # User Selection
    user_name = st.sidebar.selectbox(
        "Select User", 
        ["All Users"] + list(users.keys()),  
        index=0
    )
    user_id = None if user_name == "All Users" else users[user_name]

    # Visualization Type (Radio Button)
    visualization_type = st.sidebar.radio(
        "Analysis Period", 
        ["Yearly", "Monthly"], 
        index=0
    )

    # Chart Type
    chart_type = st.sidebar.selectbox(
        "Chart Type", 
        ["Pie", "Bar","Scatter"], 
        index=0
    )

    # Month Selection (if Monthly visualization)
    selected_month = None
    if visualization_type == "Monthly":
        selected_month = st.sidebar.selectbox(
            "Select Month", 
            MONTHS,
            index=0
        )

    # If no month is selected, default to 'January' for monthly visualization
    if visualization_type == "Monthly" and selected_month is None:
        selected_month = "January"

    return user_id, visualization_type, chart_type, selected_month
