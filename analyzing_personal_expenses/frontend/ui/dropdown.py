import streamlit as st

def select_user():
    return st.sidebar.selectbox("Select User", ["All Users", "User 1", "User 2", "Admin"])

def select_chart_type():
    return st.sidebar.selectbox("Select Chart Type", ["Bar", "Pie"])

def select_visualization_type():
    return st.sidebar.selectbox("Special Visualization", ["Monthly", "Yearly"])

def select_month():
    return st.selectbox("Select Month", [
        "January", "February", "March", "April", "May", "June",
        "July", "August", "September", "October", "November", "December"
    ])
