import streamlit as st

def display_sidebar():
    # Sidebar Selections with Defaults
    st.sidebar.title("Choose Filters")

    # Default User Selection
    user_id = st.sidebar.selectbox(
        "Select User", 
        ["All Users", "User 1", "User 2", "Admin"], 
        index=0
    )
    user_map = {"All Users": None, "User 1": 1, "User 2": 2, "Admin": 3}

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

    return user_map[user_id], visualization_type, chart_type
