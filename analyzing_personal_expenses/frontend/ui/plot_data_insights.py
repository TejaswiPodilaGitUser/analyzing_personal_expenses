import pandas as pd
import streamlit as st
from frontend.ui.data_insights import get_insights

class PlotDataInsights:
    def __init__(self):
        pass

    def display(self, df):
        """Display expense summary insights."""
        insights = get_insights(df)  # Using the refactored insights method

        st.write("### 📊 Expense Summary: Key Spending Insights")
        if insights['max_category'] == "No data available":
            st.warning("No data available for insights.")
        else:
            st.write(f"▲ **Max Spending:** {insights['max_category']} (${insights['max_amount']:.2f})")
            st.write(f"▼ **Min Spending:** {insights['min_category']} (${insights['min_amount']:.2f})")
