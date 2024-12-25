import streamlit as st
from static_expense_data import MESSAGES


class ExpenseSummary:
    def __init__(self, insights):
        self.insights = insights

    def display(self):
        """Display the expense summary (max/min spending)."""
        if not self.insights:
            st.warning("No insights available.")
            return

        max_category = self.insights.get('max_category', 'No data available')
        max_amount = self.insights.get('max_amount', 'No data available')
        min_category = self.insights.get('min_category', 'No data available')
        min_amount = self.insights.get('min_amount', 'No data available')

        if max_category == "No data available":
            st.warning("No data available for insights.")
        else:
            st.write(f"▲ **Max Spending:** {max_category} (${max_amount:.2f})")
            st.write(f"▼ **Min Spending:** {min_category} (${min_amount:.2f})")
