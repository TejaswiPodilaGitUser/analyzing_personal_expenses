import pandas as pd
import streamlit as st

class PaymentModesInsights:
    def __init__(self, insights):
        self.insights = insights

    def _get_valid_count(self, count):
        """Validate and return a numeric count or default to 0."""
        if pd.isna(count) or count == "No data available":
            return 0
        return count

    def display(self):
        """Display the payment modes summary (max and min usage) with centered alignment."""
        st.markdown(f"""
        <div style="text-align: left; margin-top: 2px;">
            <h3>💳 Payment Modes Insights</h3>
        </div>
        """, unsafe_allow_html=True)

        if not self.insights:
            st.warning("No payment mode insights available.")
            return

        max_payment_mode = self.insights.get('max_payment_mode', 'N/A')
        max_payment_count = self._get_valid_count(self.insights.get('max_payment_count'))
        min_payment_mode = self.insights.get('min_payment_mode', 'N/A')
        min_payment_count = self._get_valid_count(self.insights.get('min_payment_count'))

        st.markdown(f"""
        <div style="text-align: left;">
            <p><strong>💵 Max Payments Done Using:</strong> {max_payment_mode} ({max_payment_count} transactions)</p>
            <p><strong>💸 Min Payments Done Using:</strong> {min_payment_mode} ({min_payment_count} transactions)</p>
        </div>
        """, unsafe_allow_html=True)
