import streamlit as st
import pandas as pd

class ExpenseSummaryInsights:
    def __init__(self, insights):
        self.insights = insights

    def _get_valid_amount(self, amount):
        """Validate and return a numeric amount or default to 0.0."""
        if pd.isna(amount) or amount == "No data available":
            return 0.0
        return amount

    def display(self):
        """Display the expense summary (max/min spending) with centered alignment."""
        st.markdown("---")
        st.markdown(f"""
        <div style="text-align: center; margin-top: 2px;">
            <h3> 💡 Expense Summary Data Insights</h3>
        </div>
        """, unsafe_allow_html=True)

        if not self.insights:
            st.warning("No insights available.")
            return

        max_category = self.insights.get('max_category', 'N/A')
        max_amount = self._get_valid_amount(self.insights.get('max_amount'))
        min_category = self.insights.get('min_category', 'N/A')
        min_amount = self._get_valid_amount(self.insights.get('min_amount'))

        st.markdown(f"""
        <div style="text-align: center;">
            <p><strong>▲ Max Spending:</strong> {max_category} (${max_amount:.2f})</p>
            <p><strong>▼ Min Spending:</strong> {min_category} (${min_amount:.2f})</p>
        </div>
        """, unsafe_allow_html=True)
